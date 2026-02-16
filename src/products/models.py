from decimal import Decimal

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    description = models.TextField(max_length=200, null=True, blank=True)
    slug = models.SlugField(max_length=50, unique=True, null=False, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"


class Tag(BaseModel):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Product(BaseModel):

    category = models.ForeignKey(Category, null=True, on_delete=models.DO_NOTHING)
    description = models.TextField(max_length=250, null=True, blank=True)
    image = models.ImageField(upload_to="imgs/products/", null=True, blank=True)
    name = models.CharField(max_length=80, blank=False, null=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))])

    tags = models.ManyToManyField(Tag, blank=True)

    # NEW helper properties
    @property
    def average_rating(self):
        from django.db.models import Avg

        return self.comments.aggregate(a=Avg("rating"))["a"] or 0

    @property
    def rating_count(self):
        return self.comments.count()

    def __str__(self) -> str:
        return self.name


# NEW model
class Comment(BaseModel):
    product = models.ForeignKey(Product, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    guest_name = models.CharField(max_length=80, blank=True)
    guest_email = models.EmailField(blank=True)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    text = models.TextField(max_length=400, blank=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(condition=models.Q(rating__gte=1, rating__lte=5), name="comment_rating_range"),
            models.UniqueConstraint(
                fields=["product", "user"], name="unique_user_product_comment", condition=models.Q(user__isnull=False)
            ),
        ]
        indexes = [models.Index(fields=["product", "created_at"])]

    def __str__(self):
        who = self.user.username if self.user else (self.guest_name or "Guest")
        return f"{who} - {self.rating}★"

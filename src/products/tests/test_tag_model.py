from django.test import TestCase

from btw_app.utils import log_execution
from products.models import Tag


class TagTestCase(TestCase):

    @classmethod
    def setUpTestData(self):
        self.test_tag_name = "Test Tag"

    def setUp(self):
        Tag.objects.all().delete()

    @log_execution
    def test_successful_tag_creation(self):
        # Test the creation of a tag
        tag = Tag.objects.create(name=self.test_tag_name)
        tag.full_clean()
        self.assertEqual(Tag.objects.count(), 1)
        self.assertEqual(Tag.objects.first().name, self.test_tag_name)
        self.assertIsNotNone(Tag.objects.first().created_at)
        self.assertIsNotNone(Tag.objects.first().updated_at)

    @log_execution
    def test_failure_tag_creation_without_name(self):
        # Test the failure of tag creation without a name
        with self.assertRaises(Exception):
            tag = Tag(name="")
            tag.full_clean()
            tag.save()
        self.assertEqual(Tag.objects.count(), 0)

    @log_execution
    def test_failure_tag_creation_with_duplicate_name(self):
        # Test the failure of tag creation with a duplicate name
        Tag.objects.create(name=self.test_tag_name)
        with self.assertRaises(Exception):
            tag = Tag(name=self.test_tag_name)
            tag.full_clean()
            tag.save()
        self.assertEqual(Tag.objects.count(), 1)

    @log_execution
    def test_failure_tag_creation_with_too_long_name(self):
        # Test the failure of tag creation with a too long name
        field_length = Tag._meta.get_field('name').max_length
        long_name = "a" * (field_length + 1)
        with self.assertRaises(Exception):
            tag = Tag(name=long_name)
            tag.full_clean()
            tag.save()
        self.assertEqual(Tag.objects.count(), 0)

    @log_execution
    def test_tag_string_representation(self):
        # Test the string representation of a tag
        tag = Tag.objects.create(name=self.test_tag_name)
        self.assertEqual(str(tag), self.test_tag_name)

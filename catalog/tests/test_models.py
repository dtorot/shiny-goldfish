from django.test import TestCase

# Create your tests here.
# class YourTestClass(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         print("setUpTestData: Run once to set up non-modified data for all class methods.")
#         pass

#     def setUp(self):
#         print("setUp: Run once for every test method to set up clean data.")
#         pass

#     def test_false_is_false(self):
#         print("Method: test_false_is_false.")
#         self.assertFalse(False)

#     def test_false_is_true(self):
#         print("Method: test_false_is_true.")
#         self.assertTrue(False)

#     def test_one_plus_one_equals_two(self):
#         print("Method: test_one_plus_one_equals_two.")
#         self.assertEqual(1 + 1, 2)

from catalog.models import Guache

class GuacheModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Guache.objects.create(first_name='Alexa', last_name='Xuan', karma=0)

    def test_first_name_label(self):
        guache = Guache.objects.get(id=1)
        field_label = guache._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_last_name_label(self):
        guache = Guache.objects.get(id=1)
        field_label = guache._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')

    def test_date_of_creation_label(self):
        guache = Guache.objects.get(id=1)
        field_label = guache._meta.get_field('date_of_birth').verbose_name
        self.assertEqual(field_label, 'birth')

    def test_first_name_max_length(self):
        guache = Guache.objects.get(id=1)
        max_length = guache._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 100)

    def test_last_name_max_length(self):
        guache = Guache.objects.get(id=1)
        max_length = guache._meta.get_field('last_name').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        guache = Guache.objects.get(id=1)
        expected_object_name = f'{guache.last_name},{guache.first_name}'
        self.assertEqual(str(guache), expected_object_name)

    def test_get_absolute_url(self):
        guache = Guache.objects.get(id=1)
        # This will also fail if the URLConf is not defined.
        self.assertEqual(guache.get_absolute_url(), '/catalog/guaches/1')

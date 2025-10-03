from django.test import TestCase

# Create your tests here.

from django.urls import reverse

from catalog.models import Author

import datetime

from django.utils import timezone

# Get user model from settings
from django.contrib.auth import get_user_model
User = get_user_model()

from catalog.models import Learning, Task, Path, Guache


class GuacheListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 authors for pagination tests
        number_of_guaches = 13

        for guache_id in range(number_of_guaches):
            Guache.objects.create(
                first_name=f'Dominique {guache_id}',
                last_name=f'Surname {guache_id}',
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/catalog/guaches/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('guaches'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('guaches'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/guache_list.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('guaches'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['guache_list']), 10)

    def test_lists_all_guaches(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('guaches')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['guache_list']), 3)


class LearningByUserListViewTest(TestCase):
    def setUp(self):
        # Create two users
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()

        # Create a task
        test_guache = Guache.objects.create(first_name='Dominique', last_name='Rousseau')
        test_path = Path.objects.create(name='Fantasy')
        #test_language = Language.objects.create(name='English')
        test_task = Task.objects.create(
            name='Task Name',
#            summary='My book summary',
#            isbn='ABCDEFG',
            author=test_guache,
#            language=test_language,
        )

        # Create a path as a post-step
        path_objects_for_path = Path.objects.all()
        test_path.creator.set(path_objects_for_path) # Direct assignment of many-to-many types not allowed.
        test_path.save()

        # Create 30 Learning objects
        number_of_learning_instances = 30
        for learning_instance in range(number_of_learning_instances):
            due_back = timezone.localtime() + datetime.timedelta(days=learning_instance%5)
            the_apprentice = test_user1 if learning_instance % 2 else test_user2
            status = 'm'
            Learning.objects.create(
                path=test_task,
                name='Unlikely Learning Task, 2016',
                due_back=due_back,
                apprentice=the_apprentice,
                status=status,
            )
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('my-learnings'))
        self.assertRedirects(response, '/accounts/login/?next=/catalog/mylearnings/')


'''
#to-do 
#We are here >>>> LocalLibrary test: "To verify that the view will redirect to a login page if the user..."
    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('my-borrowed'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'catalog/bookinstance_list_borrowed_user.html')
'''
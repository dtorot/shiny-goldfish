from django.test import TestCase

# Create your tests here.

from django.urls import reverse

from catalog.models import Guache

import datetime

from django.utils import timezone

# Get user model from settings
from django.contrib.auth import get_user_model
User = get_user_model()

from catalog.models import Learning, Task, Path

import uuid

from django.contrib.auth.models import Permission

class GuacheListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 authors for pagination tests
        number_of_guaches = 13

        for guache_id in range(number_of_guaches):
            Guache.objects.create(
                first_name=f'Dominique {guache_id}',
                last_name=f'Surname {guache_id}',
                karma=10,
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
        self.assertTrue(response.context['is_paginated'] == False)
        self.assertEqual(len(response.context['guache_list']), 13)

    def test_lists_all_guaches(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('guaches')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == False)
        self.assertEqual(len(response.context['guache_list']), 13)


class LearningByUserListViewTest(TestCase):
    def setUp(self):
        # Create two users
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()

        # Create a task
        test_guache = Guache.objects.create(first_name='Mr', last_name='Rousseau', karma=10)
        test_guache_apprentice = Guache.objects.create(first_name='Ms', last_name='Dominique', karma=9)
        
        #test_language = Language.objects.create(name='English')
        test_task = Task.objects.create(
            name='Task Name',
#            summary='My book summary',
#            isbn='ABCDEFG',
            creator=test_guache,
#            language=test_language,
        )

        # Create a path that includes the previous tasks as a post-step
        test_path = Path.objects.create(
            name='Fantasy',            
            summary="My powerfull Learning Path",
            refcode="MPLP039"            
        )
        test_path.apprentice.add(test_guache_apprentice)
        test_path.author=test_guache
        test_path.task.add(test_task)

        # Create 30 Learning objects
        number_of_learning_instances = 30
        for learning_instance in range(number_of_learning_instances):
            due_back = timezone.localtime() + datetime.timedelta(days=learning_instance%5)
            the_apprentice = test_user1 if learning_instance % 2 else test_user2
            status = 'm'
            Learning.objects.create(
                path=test_path,
                name='Unlikely Learning Task, 2016',
                due_back=due_back,
                apprentice=the_apprentice,
                status=status,
            )
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('my-learnings'))
        self.assertRedirects(response, '/accounts/login/?next=/catalog/mylearnings/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('my-learnings'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'catalog/learninginstance_list_apprentice_user.html')


class RenewLearningViewTest(TestCase):
    def setUp(self):
        # Create a user
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()

        # Give test_user2 permission to renew books.
        permission = Permission.objects.get(name='Set Learning as changed')
        test_user2.user_permissions.add(permission)
        test_user2.save()

        # Create a task
        test_author = Guache.objects.create(first_name='Dominique', last_name='Rousseau')
        test_task = Task.objects.create(name='Fantasy')
        test_path = Path.objects.create(
            name='Path Title',
            summary='Another Learning Path summary',
            refcode='ABCDEFG',
            author=test_author,
        )

        # Create genre as a post-step
        path_objects_for_task = Path.objects.all()
        test_path.task.set(path_objects_for_task) # Direct assignment of many-to-many types not allowed.
        test_path.save()

        # Create a Learning object for test_user1
        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self.test_learning1 = Learning.objects.create(
            path=test_path,
            serial='Unlikely Imprint, 2016',
            due_back=return_date,
            apprentice=test_user1,
            status='w',
        )

        # Create a BookInstance object for test_user2
        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self.test_learning2 = Learning.objects.create(
            path=test_path,
            serial='Unlikely Imprint, 2016',
            due_back=return_date,
            apprentice=test_user2,
            status='w',
        )

    def test_forbidden_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='test_user1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('renew-learning-master', kwargs={'pk': self.test_learning1.pk}))
        self.assertEqual(response.status_code, 403)
'''
    def test_logged_in_with_permission_borrowed_book(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance2.pk}))

        # Check that it lets us login - this is our book and we have the right permissions.
        self.assertEqual(response.status_code, 200)

    def test_logged_in_with_permission_another_users_borrowed_book(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))

        # Check that it lets us login. We're a librarian, so we can view any users book
        self.assertEqual(response.status_code, 200)

    def test_HTTP404_for_invalid_book_if_logged_in(self):
        # unlikely UID to match our bookinstance!
        test_uid = uuid.uuid4()
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('renew-book-librarian', kwargs={'pk':test_uid}))
        self.assertEqual(response.status_code, 404)

    def test_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'catalog/book_renew_librarian.html')
'''

'''
to-do 
We are here >>>> LocalLibrary test: 
"Add the following tests to the bottom of the test class. These check that only users..."

All the tests are broken, maybe virtualenv configuration
'''
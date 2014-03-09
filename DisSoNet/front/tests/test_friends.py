from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from data.models import Friends, User
from front.views.friends import AreFriends


class UsersAreFriendsViewTest(TestCase):

    def setUp(self):
        password = 'test'
        User.objects.create_user('user1@test.ca', 'Test1', 'Man', password)
        User.objects.create_user('user2@test.ca', 'Test2', 'Man', password)

        self.user1 = User.objects.get(email='user1@test.ca')
        self.user2 = User.objects.get(email='user2@test.ca')

        self.client = Client()

    def test_are_friends_view(self):
        user_id_1 = self.user1.id
        user_id_2 = self.user2.id
        response = self.client.get(reverse('are_friends',
                                           kwargs={'user_id_1': user_id_1,
                                                   'user_id_2': user_id_2}))
        query = response.context['query']
        self.assertTrue(query == 'friends', 'Executed the wrong query')
        friends = response.context['friends']
        are_friends = response.context['are_friends']
        self.assertEqual(are_friends, 'NO',
                         'Should not be friends')
        pass

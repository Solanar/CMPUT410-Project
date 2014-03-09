from django.test import TestCase
from django.test.client import Client

from data.models import User, Friends


class FriendsListTestCase(TestCase):

    def setup(self):
        print("Create dude")
        self.password = 'test'
        User.objects.create_user(email='testUser1@test.ca',
                                 firstName='First',
                                 lastName='Tester',
                                 password=self.password)
        User.objects.create_user(email='testUser2@test.ca',
                                 firstName='Second',
                                 lastName='Tester',
                                 password=self.password)

        self.user1 = User.objects.get(email='testUser1@test.ca')
        self.user2 = User.objects.get(email='testUser2@test.ca')

    def test_add_friends(self):
        friends = Friends.objects.get(user_id_requester=self.user1,
                                      user_id_receiver=self.user2)
        self.assertFalse(friends, "Somehow they're friends already")


# class FriendsListViewTestCase(TestCase):

#     def setup(self):
#         self.client = Client()

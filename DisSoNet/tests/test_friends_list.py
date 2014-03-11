from django.test import TestCase
from django.test.client import Client

from data.models import User, Friends


class FriendsListTestCase(TestCase):
    def setUp(self):
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

        Friends.objects.create(user_id_requester=self.user1,
                               user_id_receiver=self.user2)

    def test_add_friends(self):
        friendReq = Friends.objects.get(user_id_requester=self.user1,
                                        user_id_receiver=self.user2)
        self.assertFalse(friendReq.accepted,
                         "Friend request should not be accepted by default")
        friendReq.accepted = True
        self.assertTrue(friendReq.accepted,
                        "Friend request has been accepted")

    def test_get_empty_friends_list(self):
        pass


# class FriendsListViewTestCase(TestCase):

#     def setup(self):
#         self.client = Client()

from .base import BaseView
from data.models import Friends, User
from django.conf import settings
from django.http import HttpResponseRedirect

from .mixins.friends_list import FriendsListMixin

import json


class FriendRequestView(BaseView):

    login_required = False

    if settings.DEBUG:
        http_method_names = [u'get', u'post']
    else:
        http_method_names = [u'post', u'put']

    template_name = 'test.html'

    def preprocess(self, request, *args, **kwargs):
        super(FriendRequestView, self).preprocess(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        response = request.PUT['friendRequestResponse']
        return self.render_to_response(self.context)

    def post(self, request, *args, **kwargs):

        requester = request.POST['author']
        receiver = request.POST['friend']['author']

        requester = User.objects.get(id=requester.id)
        try:
            receiver = User.objects.get(id=receiver.id)
        except:
            self.context['error'] = 'User does not exist.'
            return HttpResponseRedirect('/')

        Friends.objects.create(user_id_requester=requester,
                               user_id_receiver=receiver)
        return self.render_to_response(self.context)


class FriendsView(FriendsListMixin, BaseView):

    template_name = 'friends.html'

    def preprocess(self, request, *args, **kwargs):
        super(FriendsView, self).preprocess(request, *args, **kwargs)


class AreFriends(BaseView):

    login_required = False
    #TODO: Needs an actual template
    template_name = 'test.html'

    def preprocess(self, request, *args, **kwargs):

        self.context['query'] = 'friends'
        self.context['friends'] = [kwargs['user_id_1'],
                                   kwargs['user_id_2']]
        self.user1 = User.objects.get(id=kwargs['user_id_1'])
        self.user2 = User.objects.get(id=kwargs['user_id_2'])
        super(AreFriends, self).preprocess(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            friend1 = (Friends.objects.get(user_id_requester=self.user1,
                                           user_id_receiver=self.user2) or
                       Friends.objects.get(user_id_requester=self.user2,
                                           user_id_receiver=self.user1))
            if friend1.accepted:
                self.context['are_friends'] = 'YES'
            else:
                self.context['are_friends'] = 'NO'
        except:
            self.context['are_friends'] = 'NO'

        return self.render_to_response(self.context)

    def delete(self, request, *args, **kwargs):
        try:
            friend1 = (Friends.objects.get(user_id_requester=self.user1,
                                           user_id_receiver=self.user2) or
                       Friends.objects.get(user_id_requester=self.user2,
                                           user_id_receiver=self.user1))
        except:
            self.context['error'] = 'These two are not friends'
            return self.render_to_response(self.context)

        try:
            friend1.delete()
        except:
            self.context['error'] = 'Could not delete friendship'

        return self.render_to_response(self.context)

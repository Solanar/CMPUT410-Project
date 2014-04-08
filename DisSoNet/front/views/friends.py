from .base import BaseView
from data.models import Friends, User
from django.conf import settings

from .mixins.friends_list import FriendsListMixin


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
        #TODO: ?
        #response = request.PUT['friendRequestResponse']
        return self.render_to_response(self.context)

    def post(self, request, *args, **kwargs):
        # TODO: JSONify this~
        friends, existed = self._get_friendship(request)
        if existed:
            friends.accepted = True
        friends.save()
        return self.render_to_response(self.context)

    def delete(self, request, *args, **kwargs):
        friends, _ = self._get_friendship(request)
        friends.delete()
        return self.render_to_response(self.context)

    def _get_friendship(self, request):
        # Get the request, in this case the authenticated user
        requesterGUID = request.POST['author[id]']
        requester = User.objects.get(guid=requesterGUID)
        # Get the receiver user object, either locally or remotely
        receiverGUID = request.POST['friend[author][id]']
        receiver = User.objects.get(guid=receiverGUID)

        relationship = self._relationship_exists(requester, receiver)
        if relationship:
            return relationship, True
        else:
            return Friends(user_id_requester=requester,
                           user_id_receiver=receiver), False

    def _relationship_exists(self, user1, user2):
        try:
            return Friends.objects.get(user_id_requester=user1,
                                       user_id_receiver=user2)
        except:
            try:
                return Friends.objects.get(user_id_requester=user2,
                                           user_id_receiver=user1)
            except:
                return False


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
            friends = self._get_friendship(request)
            friends.delete()
            return self.render_to_response(self.context)

    def _get_friendship(self, request):
        receiverGUID = request.POST['author[id]']
        receiver = User.objects.get(guid=receiverGUID)

        requesterGUID = request.POST['friend[author][id]']
        requester = User.objects.get(guid=requesterGUID)

        return Friends.objects.get(user_id_requester=requester,
                                   user_id_receiver=receiver)

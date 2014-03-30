from django.db.models import Q
from data.models import Friends, User


class FriendsListMixin(object):
    '''
    Builds list of friends.
    user in filter MUST be a User object.
    '''

    def preprocess(self, request, *args, **kwargs):
        pending_friends = friends = Friends.objects.none()
        if request.user.is_authenticated():
            user = User.objects.get(email=request.user.email)
            pending_friends = self.get_pending_friends(user)
            friends = self.get_friends_list(user)
            foaf = self.get_foaf_list(friends)
            self.context['foaf_list'] = foaf
            self.context['friend_list'] = friends
            self.context['pending_friend_list'] = pending_friends
        super(FriendsListMixin, self).preprocess(request, *args, **kwargs)

    def get_pending_friends(self, user):
        friends = Friends.objects.filter(Q(user_id_receiver=user) &
                                         Q(accepted=False))
        friend_list = []
        for friend in friends:
            req = User.objects.get(email=friend.user_id_requester)
            friend_list.append(req)
        return friend_list

    def get_friends_list(self, user):
        friends = Friends.objects.filter((Q(user_id_requester=user) |
                                          Q(user_id_receiver=user)) &
                                         Q(accepted=True))
        friend_list = []
        for friend in friends:
            requester = User.objects.get(email=friend.user_id_requester)
            receiver = User.objects.get(email=friend.user_id_receiver)
            if requester == user:
                friend_list.append(receiver)
            elif receiver == user:
                friend_list.append(requester)
        return friend_list

    def get_foaf_list(self, friends):
        foaf_list = []
        for f in friends:
            foaf_list.extend([f for f in self.get_friends_list(f)
                             if f not in foaf_list])
        return foaf_list

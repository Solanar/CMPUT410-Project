from django.db.models import Q
from data.models import Friends, User


class FriendsListMixin(object):
    '''
    Builds list of friends.
    user in filter MUST be a User object.
    '''

    def get_pending_friends(self, user):
        return Friends.objects.filter(Q(user_id_receiver=user) &
                                      Q(accepted=False))

    def get_friends_list(self, user):
        return Friends.objects.filter((Q(user_id_requester=user) |
                                       Q(user_id_receiver=user)) &
                                      Q(accepted=True))

    def preprocess(self, request, *args, **kwargs):
        pending_friends = friends = Friends.objects.none()
        if request.user.is_authenticated():
            user = User.objects.get(email=request.user.email)
            pending_friends = self.get_pending_friends(user)
            friends = self.get_friends_list(user)
        self.context['friend_list'] = friends
        self.context['pending_friend_list'] = pending_friends
        super(FriendsListMixin, self).preprocess(request, *args, **kwargs)

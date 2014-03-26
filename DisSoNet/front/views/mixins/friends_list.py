from django.db.models import Q
from data.models import Friends


class FriendsListMixin(object):
    '''
    Builds list of friends.
    user in filter MUST be a User object.
    '''

    def get_filtered_list(self, filter):
        if 'user' in filter:
            user = filter['user']
            return Friends.objects.filter(Q(user_id_requester=user) |
                                          Q(user_id_receiver=user))

    def preprocess(self, request, *args, **kwargs):
        friends = Friends.objects.all()
        if 'friend_list_filter' in kwargs:
            friends = self.get_filtered_list(kwargs['friend_list_filter'])

        self.context['friend_list'] = friends
        print(friends)
        super(FriendsListMixin, self).preprocess(request, *args, **kwargs)

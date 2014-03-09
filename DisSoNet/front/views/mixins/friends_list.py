from data.models import Friends


class FriendsListMixin():

    def preprocess(self, request, *args, **kwargs):
        friends = None

        super(FriendsListMixin, self).preprocess(request, *args, **kwargs)

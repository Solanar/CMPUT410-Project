from data.models import User


class GetUserMixin():

    def preprocess(self, request, *args, **kwargs):
        user = User.objects.none()
        if request.user.is_authenticated():
            user = User.objects.get(email=request.user.email)
        self.context['user'] = user
        super(GetUserMixin, self).preprocess(request, *args, **kwargs)


class GetAllUsersMixin():

    def preprocess(self, request, *args, **kwargs):
        all_users = User.objects.all()
        if request.user.is_authenticated():
            all_users = all_users.exclude(email=request.user.email)
        self.context['all_users'] = all_users
        super(GetUserMixin, self).preprocess(request, *args, **kwargs)

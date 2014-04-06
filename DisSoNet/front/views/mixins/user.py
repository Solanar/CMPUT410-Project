from data.models import User


class GetUserMixin(object):

    def preprocess(self, request, *args, **kwargs):
        user = User.objects.none()
        if 'user_filter' in kwargs:
            try:
                user = User.objects.get(guid=kwargs['user_filter']['user_id'])
            except:
                pass
        elif request.user.is_authenticated():
            print ("hi2")
            user = User.objects.get(email=request.user.email)
        self.context['user_obj'] = user
        super(GetUserMixin, self).preprocess(request, *args, **kwargs)


class GetAllUsersMixin(object):

    def preprocess(self, request, *args, **kwargs):
        all_users = User.objects.all()
        if request.user.is_authenticated():
            all_users = all_users.exclude(email=request.user.email)
        self.context['all_users'] = all_users
        super(GetAllUsersMixin, self).preprocess(request, *args, **kwargs)

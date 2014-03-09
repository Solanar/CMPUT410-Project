from .base import BaseView
from data.models import Friends, User


class AreFriends(BaseView):

    login_required = False
    #TODO: Needs an actual template
    template_name = 'test.html'

    def preprocess(self, request, *args, **kwargs):

        self.context['query'] = 'friends'
        self.context['friends'] = [kwargs['user_id_1'],
                                   kwargs['user_id_2']]
        super(AreFriends, self).preprocess(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            user1 = User.objects.get(id=kwargs['user_id_1'])
            user2 = User.objects.get(id=kwargs['user_id_2'])
            friend1 = Friends.objects.get(user_id_requester=user1,
                                          user_id_receiver=user2)
            friend2 = Friends.objects.get(user_id_requester=user2,
                                          user_id_receiver=user1)
            if friend1.accepted or friend2.accepted:
                self.context['are_friends'] = 'YES'
            else:
                self.context['are_friends'] = 'NO'
        except:
            self.context['are_friends'] = 'NO'

        return self.render_to_response(self.context)

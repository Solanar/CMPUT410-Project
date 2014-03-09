from django.views.generic import TemplateView
from django.http import HttpResponseRedirect


class BaseView(TemplateView):

    login_required = True

    def __init__(self, *args, **kwargs):
        super(BaseView, self).__init__(*args, **kwargs)
        self.context = dict()

    def get_context_data(self, *args, **kwargs):
        return self.context

    def preprocess(self, request, *args, **kwargs):
        # print("------------Context:\n",self.context)
        # print("------------kwargs:\n",kwargs)
        pass

    def dispatch(self, request, *args, **kwargs):
        if self.login_required and not request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login')
        self.preprocess(request, *args, **kwargs)
        return super(BaseView, self).dispatch(request, *args, **kwargs)

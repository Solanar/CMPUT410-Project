from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from data.forms import UserCreationForm


class BaseView(TemplateView):

    login_required = True
    http_method_names = [u'get', u'post', u'put', u'patch', u'delete',
                         u'head', u'options', u'trace']

    def __init__(self, *args, **kwargs):
        super(BaseView, self).__init__(*args, **kwargs)
        self.context = dict()
        self.context['login_form'] = AuthenticationForm()
        self.context['register_form'] = UserCreationForm()

    def get_context_data(self, *args, **kwargs):
        return self.context

    def preprocess(self, request, *args, **kwargs):
        pass

    def dispatch(self, request, *args, **kwargs):
        if self.login_required and not request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login')
        self.preprocess(request, *args, **kwargs)
        return super(BaseView, self).dispatch(request, *args, **kwargs)

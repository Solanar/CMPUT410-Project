from .base import BaseView
from .author import processRequestFromOtherServer
from data.forms import UserCreationForm, UserChangeForm
from data.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect, Http404

from .mixins.post_list import PostListMixin
from .mixins.user import GetUserMixin


class RegisterView(BaseView):

    login_required = False
    state = 'Enter your information below: '
    template_name = 'registration/register.html'

    def preprocess(self, request, *args, **kwargs):
        self.context['form'] = UserCreationForm()
        self.context['state'] = self.state
        super(RegisterView, self).preprocess(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            # new_user.is_active = false
            # set is_active to false, display msg to user that sys admin
            # has to approve of registration
            new_user = authenticate(email=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1'])
            login(request, new_user)
            return HttpResponseRedirect('/')
        else:
            self.context['state'] = 'Please check the form, ' +\
                'your registration was unsuccessful.'

        self.context['form'] = form
        return self.render_to_response(self.context)


class LoginView(BaseView):

    login_required = False
    template_name = 'registration/login.html'

    def post(self, request, *args, **kwargs):
        email = request.POST.get('username')  # 'email')
        password = request.POST.get('password')
        redirect_next = request.POST.get('next')

        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if redirect_next:
                    return HttpResponseRedirect(redirect_next)
                else:
                    return HttpResponseRedirect('/')
            else:
                state = "Your account is not active, " +\
                        "please contact the site admin."
        else:
            state = "Your email and/or password were incorrect."

        self.context['state'] = state
        self.context['form'] = AuthenticationForm()
        self.context['email'] = email
        self.context['next'] = redirect_next
        return self.render_to_response(self.context)

    def get(self, reuqest, *args, **kwags):
        self.context['state'] = 'Please login below:'
        self.context['form'] = AuthenticationForm()
        return self.render_to_response(self.context)


class LogoutView(BaseView):

    template_name = 'registration/logout.html'

    def preprocess(self, request, *args, **kwargs):
        self.context['state'] = 'You have logged out.'
        logout(request)
        super(LogoutView, self).preprocess(request, *args, **kwargs)


class UserView(BaseView):

    template_name = 'registration/account.html'

    def preprocess(self, request, *args, **kwargs):
        self.context['state'] = 'Edit your account below: '
        self.context['form'] = UserChangeForm(instance=request.user)
        super(UserView, self).preprocess(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            state = 'Account changes were successful.'
        else:
            state = 'Please check the form, account changes were unsuccessful.'

        self.context['state'] = state
        self.context['form'] = form

        return self.render_to_response(self.context)


class UserPostsView(PostListMixin, BaseView):

    login_required = False
    #TODO: Needs a template
    template_name = ''

    def preprocess(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=kwargs['user_id'])
            self.context['state'] = 'All posts for user ' + user
            self.context['post_list_filter'] = {'user': user}
        except:
            self.context['state'] = 'User does not exist, so has no posts'
        super(UserPostsView, self).preprocess(request, *args, **kwargs)


class AuthorProfile(GetUserMixin, BaseView):
    login_required = False
    template_name = "authorProfile.html"

    def preprocess(self, request, *args, **kwargs):
        author_id = kwargs['author_id']
        """
        remote = False
        if request.META.get('HTTP_ACCEPT') == 'application/json':
            remote = True
        """
        kwargs['user_filter'] = {'user_id': author_id}  # , 'remote': remote}
        super(AuthorProfile, self).preprocess(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if request.META.get('HTTP_ACCEPT') == 'application/json':
            if not self.context['user_obj']:
                raise Http404
            return processRequestFromOtherServer(self.context['user_obj'],
                                                 "author")
        else:
            return self.render_to_response(self.context)

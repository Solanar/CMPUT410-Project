from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.views import password_reset, password_reset_confirm, \
    password_reset_done, password_reset_complete
from django.contrib.auth.forms import AuthenticationForm
from data.forms import UserCreationForm, PostCreationForm

from .base import BaseView
from .mixins.friends_list import FriendsListMixin


class HomeView(FriendsListMixin, BaseView):

    login_required = False
    template_name = 'index.html'

    def preprocess(self, request, *args, **kwargs):
        self.context = {'state': 'none'}
        self.context['login_form'] = AuthenticationForm()
        self.context['register_form'] = UserCreationForm()
        self.context['post_form'] = PostCreationForm()
        if request.user.is_authenticated():
            print(request.user.id)
        kwargs['friend_list_filter'] = 'pending'
        super(HomeView, self).preprocess(request, *args, **kwargs)


def test(request):
    context = {'state': 'none'}
    return render(request, 'profile.html', context)


def stream_debug(request):
    context = {'state': 'none'}
    context['login_form'] = AuthenticationForm()
    context['register_form'] = UserCreationForm()
    context['post_form'] = PostCreationForm()
    return render(request, 'authorStream.html', context)


def reset(request, email=None, **kwargs):
    state = 'Please enter your email address below: '
    return password_reset(
        request,
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt',
        post_reset_redirect=reverse('reset_done'),
        extra_context={'state': state, 'email': email, })


def reset_done(request, **kwargs):
    state = "We've emailed you instructions for setting your password. " +\
            "You should be receiving them shortly.\n\n" +\
            "If you don't receive an email, " +\
            "please make sure you've entered the address you " +\
            "registered with, and check your spam folder."
    return password_reset_done(
        request,
        template_name="registration/password_reset_done.html",
        extra_context={'state': state, })


def reset_confirm(request, uidb64=None, token=None, **kwargs):
    return password_reset_confirm(
        request,
        template_name='registration/password_reset_confirm.html',
        uidb64=uidb64, token=token,
        post_reset_redirect=reverse('reset_complete'))


def reset_complete(request, **kwargs):
    state = 'You have completed resetting your password.'
    return password_reset_complete(
        request,
        template_name="registration/password_reset_complete.html",
        extra_context={'state': state, })


def test_rest(request, id=None, *args, **kwargs):
    print ("test_rest", id)
    state = ""

    if request.method == "DELETE":
        print ("DELETE")
        state = "DELETE"
    if request.method == "PUT":
        JSONdata = request.PUT['test_data']
        print("PUT", JSONdata)
        state = "PUT"
    if request.method == "POST":
        JSONdata = request.POST['test_data']
        print("POST", JSONdata)
        state = "POST"
    if request.method == "GET":
        print ("GET")
        state = "GET"

    context = {'state': state}
    return render(request, 'test_rest.html', context)

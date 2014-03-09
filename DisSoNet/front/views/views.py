from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.views import password_reset, password_reset_confirm, \
    password_reset_done, password_reset_complete


def home(request):
    context = {'state':'none'}
    return render(request, 'index.html', context)

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

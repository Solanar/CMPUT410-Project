from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

from front.views.account import LoginView, LogoutView, UserView, RegisterView
from front.views.stream import StreamView
from front.views import views as front_views


if not settings.DEBUG:
    s = {'SSL': settings.ENABLE_SSL}
else:
    s = {}

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DisSoNet.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', front_views.home, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/', LoginView.as_view(), s, name='login'),
    url(r'^accounts/logout/', LogoutView.as_view(), s, name='logout'),
    url(r'^accounts/view/', UserView.as_view(), s, name='user_view'),
    url(r'^accounts/register/', RegisterView.as_view(), s, name='register'),
    url(r'^accounts/reset/$', front_views.reset, s, name='reset'),
    url(r'^accounts/reset/e/(?P<email>.+)/$', front_views.reset,
        s, name='reset'),
    url(r'^accounts/reset/done/$', front_views.reset_done,
        s, name='reset_done'),
    url(r'^accounts/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        front_views.reset_confirm, s, name='reset_confirm'),
    url(r'^accounts/reset/complete/$', front_views.reset_complete,
        name='reset_complete'),
    url(r'^stream/$', StreamView.as_view(), name='reset_complete'),
)

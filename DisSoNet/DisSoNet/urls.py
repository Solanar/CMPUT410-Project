from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

from front.views import *
from front.views import views as front_views

from django.views.decorators.csrf import csrf_exempt


if not settings.DEBUG:
    s = {'SSL': settings.ENABLE_SSL}
else:
    s = {}

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DisSoNet.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', front_views.home, name='home'),
    url(r'^test/', front_views.test, name='test'),
    url(r'^stream_debug/', front_views.stream_debug, name='stream'),
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
    url(r'^posts/?$', PublicPosts.as_view(), name='public_posts'),
    url(r'^posts/(?P<post_id>\w+)/?$', PostResource.as_view(), name='post_resource'),
    url(r'^author/posts/?$', AuthorStream.as_view(), name='author_posts'),
    url(r'^friendrequest/$', csrf_exempt(FriendRequestView.as_view()),
        name='friend_request'),
    url(r'^friends/(?P<user_id_1>\w+)/(?P<user_id_2>\w+)/$',
        AreFriends.as_view(), name='are_friends'),
)

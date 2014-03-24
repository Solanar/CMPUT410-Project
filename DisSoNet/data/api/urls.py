from django.conf.urls import patterns, include, url
from data.api import postApi


urlpatterns = patterns('',
    # urls for posts api
    url(r'^post/(?P<post_id>\w+)/?$', postApi.postResource, name='postResource'),

    # urls for friends api

    # urls for authors api

)

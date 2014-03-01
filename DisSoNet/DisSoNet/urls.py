from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from front import views as front_views


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DisSoNet.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', front_views.home, name='home'), 
    url(r'^admin/', include(admin.site.urls)),
)

from base import BaseView
from data.forms import PostCreationForm
from data.models import Post
from django.db.models import Q
from django.http import HttpResponseRedirect


class PostEdit(BaseView):

    login_required = True
    # TODO Need to create an edit view, lots similiar in 401 proj
    #template_name = '.html'

    def preprocess(self, request, *args, **kwargs):
        super(PostEdit, self).preprocess(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        pass


class PostDelete(BaseView):

    login_required = True

    def preprocess(self, request, *args, **kwargs):
        super(PostDelete, self).preprocess(request, *args, **kwargs)

    def post(self, request, post_id=None, *args, **kwargs):
        pass

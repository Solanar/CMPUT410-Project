from .base import BaseView
from data.forms import PostCreationForm
from data.models import Post
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse


class PostEdit(BaseView):

    # TODO Need to create an edit view, lots similiar in 401 proj
    #template_name = '.html'

    def preprocess(self, request, *args, **kwargs):
        super(PostEdit, self).preprocess(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        pass


class PostDelete(BaseView):

    def preprocess(self, request, *args, **kwargs):
        super(PostDelete, self).preprocess(request, *args, **kwargs)

    def post(self, request, post_id=None, *args, **kwargs):
        pass


class PostCreate(BaseView):
    def post(self, request, *args, **kwags):
        title = request.POST.get("title")
        content_type = request.POST.get("content-type")
        image_url = request.POST.get("image_url")
        content = request.POST.get("content")
        categories = request.POST.get("categories")
        visibility = request.POST.get("visibility")
        try:
            new_post = Post(title=title, source="", origin="", description="", content_type=content_type, content=content, author=request.user, visibility = visibility)
            new_post.save()
        except Exception,e:
            print(e)
        self.context['test'] = 'test'

        try:
            response = HttpResponse(status=201)
            response['Location'] = '/post/' + str(new_post.id) + '/'
            return response
        except Exception,e:
            print(e)

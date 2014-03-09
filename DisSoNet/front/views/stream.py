from base import BaseView
from data.forms import PostCreationForm
from data.models import Post
from django.db.models import Q


class StreamView(BaseView):
    """ View of the 'stream' of all our posts. """

    template_name = 'stream.html'

    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        self.context["posts"] = posts
        form = PostCreationForm()
        self.context["form"] = form
        return self.render_to_response(self.context)

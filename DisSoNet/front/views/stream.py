from .base import BaseView
from data.forms import PostCreationForm
from data.models import Post
from django.db.models import Q
from django.http import HttpResponseRedirect

from .mixins.user import GetUserMixin
from .mixins.post_list import PostListMixin


class StreamView(PostListMixin, GetUserMixin, BaseView):
    """ View of the 'stream' of all our posts. """

    template_name = 'stream.html'

    def preprocess(self, request, *args, **kwargs):
        form = PostCreationForm()
        self.context["form"] = form
        kwargs['post_list_filter'] = 'visible'
        super(StreamView, self).preprocess(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = PostCreationForm(request.POST)
        if form.is_valid():
            post = form.save()
            return HttpResponseRedirect('/stream/')

        # Tyler, im sure there is a way to have the modal with
        # the 'field required' messages. Google isnt behaving for me :(
        self.context['form'] = form
        return self.render_to_response(self.context)

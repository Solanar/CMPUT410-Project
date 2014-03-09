from base import BaseView
from data.forms import PostCreationForm
from data.models import Post
from django.db.models import Q
from django.http import HttpResponseRedirect


class StreamView(BaseView):
    """ View of the 'stream' of all our posts. """

    template_name = 'stream.html'

    def preprocess(self, request, *args, **kwargs):
        posts = Post.objects.all()
        self.context['posts'] = posts
        form = PostCreationForm()
        self.context["form"] = form
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

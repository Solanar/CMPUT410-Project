from data.models import Comment


class CommentListMixin(object):

    def preprocess(self, request, *args, **kwargs):
        post = kwargs['post_object']
        self.context['comments'] = Comment.objects.filter(post=post)
        super(CommentListMixin, self).preprocess(request, *args, **kwargs)

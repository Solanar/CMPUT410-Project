from data.models import Post


class PostListMixin():

    def preprocess(self, request, *args, **kwargs):
        posts = Post.objects.all()
        if 'post_list_filter' in kwargs:
            posts = self.get_filtered_list(posts, kwargs['post_list_filter'])
        self.context['posts'] = posts
        super(PostListMixin, self).preprocess(request, *args, **kwargs)

    def get_filtered_list(self, posts, filter):
        filtered_list = None
        if 'user' in filter:
            filtered_list = posts.filter(author=filter['user'])
        return filtered_list

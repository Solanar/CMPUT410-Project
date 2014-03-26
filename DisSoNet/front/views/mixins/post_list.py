from data.models import Post
from django.db.models import Q


class PostListMixin(object):

    def preprocess(self, request, *args, **kwargs):
        posts = Post.objects.none()
        if 'post_list_filter' in kwargs:
            posts = self.get_filtered_list(kwargs['post_list_filter'])
        self.context['post_list'] = posts
        super(PostListMixin, self).preprocess(request, *args, **kwargs)

    def get_filtered_list(self, filter):
        filtered_list = Post.objects.all()
        if 'visible' in filter:  # /author/posts
            print('Visible posts!')
        elif 'public' in filter:  # /posts
            filtered_list = filtered_list.filter(visibility='PUBLIC')
        elif 'visible_by_author' in filter:  # /author/<author_id>/posts
            print('Posts by author, visible to me!')
        elif 'post_id' in filter:  # /posts/<post_id>
            print('SHOW THE POST!!!!!!')
        return filtered_list

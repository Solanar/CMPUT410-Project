from data.models import Post, User
from django.db.models import Q


class PostListMixin(object):

    def preprocess(self, request, *args, **kwargs):
        posts = Post.objects.none()
        if 'post_list_filter' in kwargs:
            posts = self.get_filtered_list(kwargs['post_list_filter'],
                                           request.user)
        self.context['post_list'] = posts
        super(PostListMixin, self).preprocess(request, *args, **kwargs)

    def get_filtered_list(self, filter, user):
        filtered_list = Post.objects.all()
        user = User.objects.get(email=user.email)
        if 'visible' in filter:  # /author/posts
            filtered_list = self.get_posts_visible_to_current_user(user)
            pass
        elif 'public' in filter:  # /posts
            filtered_list = self.get_all_public_posts()
        elif 'visible_by_author' in filter:  # /author/<author_id>/posts
            author = User.objects.get(id=filter['visible_by_author'])
            filtered_list = self.get_posts_by_author(author, user)
        elif 'post_id' in filter:  # /posts/<post_id>
            filtered_list = Post.objects.get(guid=filter['post_id'])
        return filtered_list

    def get_posts_visible_to_current_user(self, user):
        # post =
        pass

    def get_all_public_posts(self):
        return Post.objects.filter(visibility='PUBLIC')

    def get_posts_by_author(self, author, user):
        posts = self.get_posts_visible_to_current_user(user)
        return posts.filter(author=author)

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
            filtered_list = filtered_list.exclude(Q(visibility='PRIVATE') &
                                                  ~Q(author=user))
            # include posts by current author
            # include posts that are public
            pass
        elif 'public' in filter:  # /posts
            filtered_list = filtered_list.filter(visibility='PUBLIC')
        elif 'visible_by_author' in filter:  # /author/<author_id>/posts
            print('Posts by author, visible to me!')
        elif 'post_id' in filter:  # /posts/<post_id>
            print('SHOW THE POST!!!!!!')
        return filtered_list

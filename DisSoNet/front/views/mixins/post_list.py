from data.models import Comment, Post, User
from django.db.models import Q

from .. import remote_request


class PostListMixin(object):

    def preprocess(self, request, *args, **kwargs):
        posts = Post.objects.none()
        user = None
        if 'post_list_filter' in kwargs:
            if request.user.is_authenticated():
                user = User.objects.get(email=request.user)
            posts = self.get_filtered_list(kwargs['post_list_filter'],
                                           user)

        if isinstance(posts, Post):
            setattr(posts, 'comments',
                    Comment.objects.filter(post=posts).all())
        else:
            for index, post in enumerate(posts):
                setattr(posts[index], 'comments',
                        Comment.objects.filter(post=post).all())

        self.context['post_list'] = posts
        super(PostListMixin, self).preprocess(request, *args, **kwargs)

    def get_filtered_list(self, filter, user):
        filtered_list = Post.objects.all()
        if 'visible' in filter:  # /author/posts
            filtered_list = self.get_posts_visible_to_current_user(user)
        elif 'public' in filter:  # /posts
            filtered_list = self.get_all_public_posts()
        elif 'visible_by_author' in filter:  # /author/<author_id>/posts
            author = User.objects.get(guid=filter['visible_by_author'])
            filtered_list = self.get_posts_by_author(author, user)
        elif 'post_id' in filter:  # /posts/<post_id>
            try:
                filtered_list = Post.objects.get(guid=filter['post_id'])
            except:
                filtered_list = Post.objects.none()
        return filtered_list

    def get_posts_visible_to_current_user(self, user):
        # add all posts by current user
        vis_posts = [p for p in Post.objects.filter(author=user)]
        # add all public posts
        vis_posts.extend([p for p in self.get_all_public_posts()
                         if p not in vis_posts])
        # add all posts by friends, visible to friends
        friend_list = self.context['friend_list']
        for f in friend_list:
            vis_posts.extend([p for p in Post.objects.filter(
                Q(author=f) & Q(visibility='FRIENDS')) if p not in vis_posts])

        # get FOAF posts
        foaf_list = self.context['foaf_list']
        for f in foaf_list:
            vis_posts.extend([p for p in Post.objects.filter(
                Q(author=f) & Q(visibility='FOAF')) if p not in vis_posts])
        return vis_posts

    def get_all_public_posts(self):
        posts = Post.objects.filter(visibility='PUBLIC')
        remote_posts = remote_request.getRemoteObject(None, "posts")
        post_list = list(posts)
        if remote_posts:
            for post in remote_posts:
                post_list.append(post)
        return posts

    def get_posts_by_author(self, author, user):
        posts = self.get_posts_visible_to_current_user(user)
        posts = [p for p in posts if p.author == author]
        return posts

from .base import BaseView
from data.models import Post, Comment, User
from django.http import HttpResponseRedirect, Http404
from .mixins.friends_list import FriendsListMixin
from .mixins.post_list import PostListMixin
from .mixins.comment_list import CommentListMixin
from .author import processRequestFromOtherServer


# http://service/posts (all posts marked as public on the server)
class PublicPosts(PostListMixin, BaseView):

    login_required = False
    template_name = "publicStream.html"

    def preprocess(self, request, *args, **kwargs):
        kwargs['post_list_filter'] = 'public'
        super(PublicPosts, self).preprocess(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if request.META.get('HTTP_ACCEPT') == 'application/json':
            # This a json request from another server
            return processRequestFromOtherServer(self.context['post_list'],
                                                 "posts")
        else:
            # Serve django objects
            sort = self.context['post_list'].order_by('-published_date')
            self.context['post_list'] = sort
            return self.render_to_response(self.context)

    def post(self, request, *args, **kwargs):
        """ . """
        post_data = request.POST.copy()
        post_author = User.objects.get(id=request.user.id)
        post = Post.objects.create(title=post_data["title"],
                                   description=post_data["description"],
                                   content_type=post_data["content_type"],
                                   content=post_data["content"],
                                   author=post_author,
                                   visibility=post_data["visibility"])

        if post_data['image_url']:
            post.image_url = post_data['image_url']

        post.clean()
        post.save()
        return HttpResponseRedirect(request.path + "/" + post.guid)


# http://service/post(s)/{POST_ID} access to a single post with id = {POST_ID}
class PostResource(PostListMixin, BaseView):

    login_required = False
    template_name = "posts/singlePost.html"

    def preprocess(self, request, *args, **kwargs):
        post_id = kwargs['post_id']
        kwargs['post_list_filter'] = {'post_id': post_id}
        super(PostResource, self).preprocess(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        pass

    def get(self, request, *args, **kwargs):
        if request.META.get('HTTP_ACCEPT') == 'application/json':
            # This a json request from another server
            if not self.context['post_list']:
                raise Http404
            return processRequestFromOtherServer((self.context["post_list"],),
                                                 "posts")
        else:
            # Serve django objects
            self.context["post"] = self.context["post_list"]
            return self.render_to_response(self.context)

    def post(self, request, *args, **kwargs):
        #if request.META.get('HTTP_ACCEPT') == 'application/json':
        self.get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        post_to_delete = Post.objects.get(guid=kwargs['post_id'])
        if post_to_delete.author.id == request.user.id:
            post_to_delete.delete()
        return self.render_to_response(self.context)


# http://service/author/posts
# (posts that are visible to the currently authenticated user)
class AuthorStream(FriendsListMixin, PostListMixin, BaseView):

    template_name = "authorStream.html"

    def preprocess(self, request, *args, **kwargs):
        kwargs['post_list_filter'] = 'visible'
        super(AuthorStream, self).preprocess(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if request.META.get('HTTP_ACCEPT') == 'application/json':
            # This a json request from another server
            return processRequestFromOtherServer(self.context['post_list'],
                                                 "posts")
        else:
            # Serve django objects
            return self.render_to_response(self.context)


# http://service/author/{AUTHOR_ID}/posts (all posts made by {AUTHOR_ID}
# visible to the currently authenticated user)
class VisiblePostToUser(FriendsListMixin, PostListMixin, BaseView):

    # todo make a template for this, if it becomes an actual view
    template_name = "visiblePostStream.html"

    def preprocess(self, request, *args, **kwargs):
        author_id = kwargs['author_id']
        kwargs['post_list_filter'] = {'visible_by_author': author_id}
        super(VisiblePostToUser, self).preprocess(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if request.META.get('HTTP_ACCEPT') == 'application/json':
        # This a json request from another server
            if not self.context['post_list']:
                raise Http404
            return processRequestFromOtherServer(self.context['post_list'],
                                                 "posts")
        else:
            return self.render_to_response(self.context)


class PostComments(CommentListMixin, BaseView):

    login_required = False
    template_name = 'test.html'

    def preprocess(self, request, *args, **kwargs):
        post_guid = kwargs['post_id']
        try:
            self.post_obj = Post.objects.get(guid=post_guid)
        except:
            raise Http404

        kwargs['post_object'] = self.post_obj
        super(PostComments, self).preprocess(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        post_content = request.POST['content']

        if request.user.is_authenticated():
            self.user = User.objects.get(email=request.user)

        comment = Comment.objects.create(post=self.post_obj,
                                         user=self.user,
                                         content=post_content)
        comment.clean()
        comment.save()
        return HttpResponseRedirect(request.path)

    def get(self, request, *args, **kwargs):
        if request.META.get('HTTP_ACCEPT') == 'application/json':
            # This a json request from another server
            if not self.context['comments']:
                raise Http404
            return processRequestFromOtherServer(self.context["comments"],
                                                 "comments")
        else:
            return self.render_to_response(self.context)

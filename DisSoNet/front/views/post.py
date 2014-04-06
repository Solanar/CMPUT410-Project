from .base import BaseView
from data.forms import PostCreationForm
from data.models import Post, Comment, User
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from .mixins.friends_list import FriendsListMixin
from .mixins.post_list import PostListMixin
from .mixins.comment_list import CommentListMixin
from .author import processRequestFromOtherServer, getAuthorDict


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
            processRequestFromOtherServer(self.context['post_list'])
        else:
            # Serve django objects
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
        post.clean()

        if post_data['image_url']:
            post.image_url = post_data['image_url']
            post.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


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
            processRequestFromOtherServer(self.context["post_list"], "posts")
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
            processRequestFromOtherServer(self.context['post_list'], "posts")
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
            processRequestFromOtherServer(self.context['post_list'], "posts")
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
            self.context['error'] = "No post exists with that GUID"

        if request.user.is_authenticated():
            self.user = User.objects.get(email=request.user)

        kwargs['post_object'] = self.post_obj
        super(PostComments, self).preprocess(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        post_content = request.POST['content']
        comment = Comment.objects.create(post=self.post_obj,
                                         user=self.user,
                                         content=post_content)
        comment.save()
        return HttpResponseRedirect(request.path)


def getPostDict(post_object):
    """ From all post URLS should return a list of posts like the following.

    Of the form:
    { "posts":[{"title":"string",
                "source":"url",
                "origin":"url",
                "description":"string",
                "content-type":"text/*",
                "content":"string",
                "author":{"id":"sha1",
                          "host":"host",
                          "displayname":"name",
                          "url":"url_to_author"},
                "categories":["cat1", "cat2"],
                "comments":[{"author":{"id":"sha1",
                                       "host":"url",
                                       "displayname":"name"},
                             "comment":"string",
                             "pubDate":"date",
                             "guid":"sha1"}]
                "pubdate":"date",
                "guid":"sha1",
                "visibility":"PUBLIC"}]}

    This function will return the representation of a post to go into this list

    """
    post_dict = {}
    post_dict["title"] = post_object.title
    post_dict["source"] = post_object.source
    post_dict["origin"] = post_object.origin
    post_dict["description"] = post_object.description
    post_dict["content-type"] = post_object.content_type
    post_dict["content"] = post_object.content
    # TODO python datetime is not JSON serializable
    timestring = post_object.published_date.strftime("%a %b %d %h:%m:%s mst %y")
    post_dict["pubdate"] = timestring
    # post_dict["pubdate"] = post_object.published_date
    post_dict["guid"] = post_object.guid
    post_dict["visibility"] = post_object.visibility

    # get the post author, convert to dict and add to post_dict
    author_dict = getAuthorDict(post_object.author, include_url=True)
    post_dict["author"] = author_dict

    # get all comments on this post of return them
    comment_list = Comment.objects.filter(post=post_object)
    comment_dict_list = getCommentDictList(comment_list)
    post_dict["comments"] = comment_dict_list

    return post_dict


def getCommentDictList(comment_list):
    """ Take a list of comment objects, returns list of dict representations.

    Of the form:
    "comments":[{"author":{"id":"sha1",
                           "host":"url",
                           "displayname":"name"},
                 "comment":"string",
                 "pubDate":"date",
                 "guid":"sha1"}]

    :returns: A list of dicts

    """
    comment_dict_list = []
    for comment in comment_list:
        comment_dict = {}
        comment_dict["author"] = getAuthorDict(comment.user)
        comment_dict["comment"] = comment.content
        # TODO python datetime is not JSON serializable
        timestring = comment.published_date.strftime("%a %b %d %h:%m:%s mst %y")
        comment_dict["pubDate"] = timestring
        comment_dict["guid"] = comment.guid
        comment_dict_list.append(comment_dict)

    return comment_dict_list


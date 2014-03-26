from .base import BaseView
from data.forms import PostCreationForm
from data.models import Post
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse

from .mixins.post_list import PostListMixin


import json
from django.http import HttpResponse

from data.models import Post, Comment


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
            post_dict = {}
            post_dict_list = []
            posts = self.context['post_list']
            for post_object in posts:
                post_dict_list.append(getPostDict(post_object))

            post_dict["posts"] = post_dict_list
            json_data = json.dumps(post_dict)
            return HttpResponse(json_data, content_type="application/json")
        else:
            # Serve django objects
            return self.render_to_response(self.context)


# http://service/posts/{POST_ID} access to a single post with id = {POST_ID}
class PostResource(PostListMixin, BaseView):

    login_required = False

    def preprocess(self, request, *args, **kwargs):
        super(PostResource, self).preprocess(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        pass

    def get(self, request, *args, **kwargs):
        post_id = kwargs['post_id']
        post_objects = Post.objects.filter(guid=post_id)
        if request.META.get('HTTP_ACCEPT') == 'application/json':
            # This a json request from another server
            post_dict = {}
            post_dict_list = []
            for post_object in post_objects:
                post_dict_list.append(getPostDict(post_object))

            post_dict["posts"] = post_dict_list
            json_data = json.dumps(post_dict)
            return HttpResponse(json_data, content_type="application/json")
        else:
            # Serve django objects
            # post_objects only returns one post
            self.context['post'] = post_objects[0]
            return self.render_to_response(self.context)

    def post(self, request, *args, **kwargs):
        #if request.META.get('HTTP_ACCEPT') == 'application/json':
        self.get(request, *args, **kwargs)


# http://service/author/posts (posts that are visible to the currently authenticated user)
class AuthorStream(PostListMixin, BaseView):

    template_name = "authorStream.html"

    def preprocess(self, request, *args, **kwargs):
        kwargs['post_list_filter'] = 'visible'
        super(AuthorStream, self).preprocess(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        #if request.META.get('HTTP_ACCEPT') == 'application/json':
        # This a json request from another server
        post_dict = {}
        post_dict_list = []
        posts = self.context['post_list']
        for post_object in posts:
            post_dict_list.append(getPostDict(post_object))

        post_dict["posts"] = post_dict_list
        json_data = json.dumps(post_dict)
        return HttpResponse(json_data, content_type="application/json")
        #else:
        # Serve django objects
        return self.render_to_response(self.context)

# http://service/author/{AUTHOR_ID}/posts (all posts made by {AUTHOR_ID} visible to the currently authenticated user)
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
    # post_dict["pubdate"] = post_object.published_date
    post_dict["guid"] = post_object.guid
    post_dict["visibility"] = post_object.visibility

    # get the post author, convert to dict and add to post_dict
    author_dict = getAuthorDict(post_object.author, include_url=True)
    post_dict["author"] = author_dict

    # get all comments on this post of return them
    comment_list = Comment.objects.filter(post=post_object)
    comment_dict_list = getCommentDictList(comment_list)
    print comment_dict_list
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
        # comment_dict["pubDate"] = comment.published_date
        comment_dict["guid"] = comment.guid
        comment_dict_list.append(comment_dict)

    return comment_dict_list


def getAuthorDict(author_object, include_url=False):
    """ Take a list of author objects, returns it's dict representations.

    "author":
        {
            "id":"sha1",
            "host":"host",
            "displayname":"name",
            "url":"url_to_author"
        },

    :returns: dict representation of an author object

    """
    author_dict = {}
    # TODO change this from email to guid/sha1
    author_dict["id"] = author_object.email
    # TODO decide on what we are using as a user/person's display name
    author_dict["displayname"] = author_object.__str__()
    # TODO add host
    # TODO add url to author (complete with guid) from example json
    # if include_url:
        # author_dict["url"] = author_object.url

    return author_dict

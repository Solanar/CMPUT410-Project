""" postApi.py.

From Requirements in project.org
[ ] implement a restful API for http://service/post/postid
a PUT should insert/update a post
a POST should get the post
a GET should get the post

This file wil supply all the backend/model interface to allow for RESTFUL
calls on the post resource

"""

import json
from django.http import HttpResponse

from data.models import Post, Comment


def postResource(request, post_id):
    """ The post resource for DisSoNet.

    :return: HttpResponse

    """
    if request.method == "PUT":
        #print "PUT"
        pass
    elif request.method in ["GET", "POST"]:
        #print "GET or POST"
        post_dict = {}
        post_dict_list = []
        post_objects = Post.objects.filter(guid=post_id)
        for post_object in post_objects:
            post_dict_list.append(getPostDict(post_object))

        post_dict["posts"] = post_dict_list
        json_data = json.dumps(post_dict)
        return HttpResponse(json_data, content_type="application/json")
    else:
        # Return error code for unsupported http method
        pass


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

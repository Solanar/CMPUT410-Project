from django.http import HttpResponse
import json
import socket

from data.models import Comment


def processRequestFromOtherServer(user_obj, dict_type):
    post_dict = {}
    post_dict_list = []
    if dict_type is "author":
        post_dict_list.append(getAuthorDict(user_obj))
    elif dict_type is "posts":
        post_dict_list.append(getPostDict(user_obj))
    else:
        print ("Unknown type")

    post_dict[dict_type] = post_dict_list
    json_data = json.dumps(post_dict)
    return HttpResponse(json_data, content_type="application/json")


def getAuthorDict(user_obj, include_url=False):
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
    author_dict["id"] = user_obj.guid
    author_dict["displayname"] = user_obj.get_full_name()
    host = socket.gethostname()  # only works if website running on port 80
    ip = "http://10.4.10.2"  # dat hard coding of values
    port = ":8080/"
    author_dict["host"] = ip + port  # host
    # why is this here?
    # if include_url:
        # author_dict["url"] = author_object.url
    author_dict["url"] = ip + port + "author/" + user_obj.guid + "/"
    return author_dict


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
    formatter = "%a %b %d %h:%m:%s mst %y"
    timestring = post_object.published_date.strftime(formatter)
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
        formatter = "%a %b %d %h:%m:%s mst %y"
        timestring = comment.published_date.strftime(formatter)
        comment_dict["pubDate"] = timestring
        comment_dict["guid"] = comment.guid
        comment_dict_list.append(comment_dict)

    return comment_dict_list

import json


def processRequestFromOtherServer(post_objects, dict_type):
    post_dict = {}
    post_dict_list = []
    post_dict_list.append(getAuthorDict(post_objects))

    post_dict[dict_type] = post_dict_list
    json_data = json.dumps(post_dict)
    return HttpResponse(json_data, content_type="application/json")


def getAuthorDict(post_object, include_url=False):
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
    author_object = User.objects.get(guid=post_object.guid)
    author_dict = {}
    # TODO change this from email to guid/sha1
    author_dict["id"] = author_object.email
    # TODO decide on what we are using as a user/person's display name
    author_dict["displayname"] = author_object.get_full_name()
    # TODO add host
    #author_dict["host"] = author_object.host
    author_dict["host"] = ""
    # TODO add url to author (complete with guid) from example json
    # if include_url:
        # author_dict["url"] = author_object.url
    author_dict["url"] = ""

    return author_dict

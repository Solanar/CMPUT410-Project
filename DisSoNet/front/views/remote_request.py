from data.models import Server, User, Post, Comment
import urllib2
import json
from datetime import datetime

"""
#view
    remote = False
    if request.META.get('HTTP_ACCEPT') == 'application/json':
        remote = True
    kwargs['user_filter'] = {'user_id': author_id, 'remote': remote}

#mixin
if not user and kwargs['user_filter'].get('remote'):
        user = self.getRemoteUser(kwargs['user_filter']['user_id'])
"""


def getRemoteObject(guid, obj_type):
    obj_list = []
    for server in Server.objects.all():
        #url = server.url[:-1]  # django adds trailing /
        #url = url + ':' + str(server.port) + '/'
        if server.name == "Local":
            continue
        url = server.url
        url = handleUrlType(url, guid, obj_type)
        print ("url", url)
        obj = serverRequest(url, obj_type)  # 8080
        if not obj:
            url = "http://" + server.ip + "/"
            url = handleUrlType(url, guid, obj_type)
            print ("url1", url)
            obj = serverRequest(url, obj_type)  # 80
        elif obj:
            obj_list.extend(obj)
    return obj_list


def handleUrlType(url, guid, obj_type):
    if obj_type == "posts":
        url = url + "posts/"
    elif obj_type == "author":
        url = url + "author/" + guid + "/"
    return url


def serverRequest(url, obj_type):
    headers = {'Accept': 'application/json'}
    req = urllib2.Request(url, None, headers)
    try:
        data = urllib2.urlopen(req)
        responseType = data.info().gettype()
        #print ("hi0.3", data.read())
        if (responseType != "application/json"):
            print ("Not json!")
            return None
        jsonData = json.load(data)
        return handleObjType(jsonData, obj_type)
    except urllib2.URLError as e:
        msg = ""
        if hasattr(e, 'reason'):
            msg = "Reason: " + str(e.reason)
        if hasattr(e, 'code'):
            msg = msg + " Error code: " + str(e.code)
        #print ("Could not connect to: " + url + " because: " + msg)
        print ("No reply")
        return None


def handleObjType(jsonData, obj_type):
    if obj_type == "posts":
        return getPosts(jsonData)
    elif obj_type == "comments":
        return getComments(jsonData)
    elif obj_type == "author":
        return getAuthor(jsonData)


def getPosts(jsonData):
    posts = jsonData['posts']
    posts_list = []
    for post in posts:
        #print ("hi", post)
        guid = post['guid']
        title = post['title']
        source = post['source']
        origin = post['origin']
        description = post['description']
        content_type = post['content-type']
        content = post['content']
        author_obj = post['author']
        author = getAuthor(author_obj)
        categories = post['categories']
        pubDate = post['pubDate']
        pubDate = getPubDate(pubDate)
        visibility = post['visibility']

        new_post, created = Post.objects.get_or_create(
            title=title, source=source, origin=origin,
            description=description, content_type=content_type,
            content=content, author=author,
            #categories=categories,
            published_date=pubDate, guid=guid,
            visibility=visibility)
        #new_post.save()
        comments_obj = post['comments']
        comments = getComments(comments_obj, new_post)
        #setattr(new_post, 'comments', comments)

        posts_list.append(new_post)
    return posts_list


def getAuthor(jsonData):
    guid = jsonData['id']
    host = jsonData['host']
    displayname = jsonData['displayname']
    url = jsonData['url']
    email = guid + "@remote.ca"
    user, created = User.objects.get_or_create(
        guid=guid,
        firstName=displayname,
        url=url,
        host=host,
        email=email)
    #user.save()
    return user


def getComments(jsonData, post):
    comment_list = []
    for comment in jsonData:
        author_obj = comment['author']
        author = getAuthor(author_obj)
        content = comment['comment']
        pubDate = comment['pubDate']
        pubDate = getPubDate(pubDate)
        guid = comment['guid']
        new_comment, created = Comment.objects.get_or_create(
            post=post, user=author, content=content,
            published_date=pubDate, guid=guid)
        #new_comment.save()
        comment_list.append(new_comment)
        #post.comments.add(new_comment)
    return comment_list


def getPubDate(pubDate):
    formatter = "%a %b %d %h:%m:%s mst %y"
    formatter2 = "%a %b %d %H:%m:%s mst %y"
    try:
        pubDate = datetime.strptime(pubDate, formatter)
    except:
        try:
            pubDate = datetime.strptime(pubDate, formatter2)
        except:
            pubDate = datetime.now()
    return pubDate

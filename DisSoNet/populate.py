#!/usr/bin/env python

#just python things
import os
#import datetime


def populate():
    universal_password = "dissonet"

    # create users
    ua = add_user("test@test.ca", "Test", "Tester", universal_password)
    ub = add_user("test2@test.ca", "Test2", "Tester", universal_password)
    uc = add_user("inactive@test.ca", "Inactive", "Tester", universal_password)
    uc.is_active = False
    uc.save()

    ud = add_user("real@person.ca", "Real", "Person", universal_password)
    ue = add_user("bob@marley.ra", "Bob", "Marley", universal_password)
    uf = add_user("homer@simpson.us", "Homer", "Simpson", universal_password)
    ug = add_user("marge@simpson.us", "Marge", "Simpson", universal_password)
    uh = add_user("bart@simpson.us", "Bart", "Simpson", universal_password)
    ui = add_user("lisa@simpson.us", "Lisa", "Simpson", universal_password)
    uj = add_user("maggie@simpson.us", "Maggie", "Simpson", universal_password)
    uk = add_user("abraham@simpson.us", "Abraham", "Simpson",
                  universal_password)
    ul = add_user("patty@bouvier.us", "Patty", "Bouvier", universal_password)
    um = add_user("selma@bouvier.us", "Selma", "Bouvier", universal_password)
    un = add_user("slh@simpson.us", "Santa's Little Helper", "Simpson",
                  universal_password)
    uo = add_user("milhouse@vanhouten.us", "Milhouse", "Van Houten",
                  universal_password)
    up = add_user("groundskeeper@willie.us", "Groundskeeper", "Willie",
                  universal_password)

    user_list = {ua, ub, uc, ud, ue, uf, ug, uh, ui, uj, uk, ul, um, un, uo}

    uq = add_user("guid@test.ca", "GUID", "Test",
                  universal_password, guid="123abc")
    ur = add_user("guid2@test.ca", "GUID2", "Test",
                  universal_password, guid="abc123")

    # create admin users
    u1 = add_user("eklinger@ualberta.ca", "Eric", "Klinger", "410",
                  is_admin=True)
    u2 = add_user("eric.klinger@gmail.com", "Eric", "Klinger", "410")
    # create normal users
    # ...

    # create categories
    # ...

    # create friends
    add_friend(ua, ub, True)
    add_friend(ua, ud, False)
    add_friend(uf, ue, False)
    add_friend(uf, ug, True)
    add_friend(uf, uh, True)
    add_friend(uf, ui, True)
    add_friend(uf, uj, True)
    add_friend(uf, uk, True)
    add_friend(uf, un, True)
    add_friend(uf, ul, False)
    add_friend(uf, um, False)
    add_friend(ug, uh, True)
    add_friend(ug, ui, True)
    add_friend(ug, uj, True)
    add_friend(ug, uk, True)
    add_friend(ug, ul, True)
    add_friend(ug, um, True)
    add_friend(ug, un, True)
    add_friend(uh, ui, True)
    add_friend(uh, uj, True)
    add_friend(uh, uk, True)
    add_friend(uh, un, True)
    add_friend(uh, uo, True)
    add_friend(ui, un, True)
    add_friend(ui, uo, True)
    add_friend(ul, um, True)
    add_friend(up, un, False)

    # create a post
    #now = datetime.datetime.now()

    for user in user_list:
        add_post("PLAIN PUBLIC", "http://source.ca", "http://origin.ca",
                 "Description",
                 "PLAIN",
                 "Content",
                 user, "PUBLIC")
        add_post("PLAIN PRIVATE", "http://source.ca", "http://origin.ca",
                 "Description",
                 "PLAIN",
                 "Content",
                 user, "PRIVATE")
        add_post("PLAIN FOAF", "http://source.ca", "http://origin.ca",
                 "Description",
                 "PLAIN",
                 "Content",
                 user, "FOAF")
        add_post("PLAIN FRIENDS", "http://source.ca", "http://origin.ca",
                 "Description",
                 "PLAIN",
                 "Content",
                 user, "FRIENDS")
        add_post("PLAIN SERVERONLY", "http://source.ca", "http://origin.ca",
                 "Description",
                 "PLAIN",
                 "Content",
                 user, "SERVERONLY")
        add_post("HTML PUBLIC", "http://source.ca", "http://origin.ca",
                 "Description",
                 "HTML",
                 "Content",
                 user, "PUBLIC")
        add_post("X-MARKDOWN PUBLIC", "http://source.ca", "http://origin.ca",
                 "Description",
                 "X-MARKDOWN",
                 "Content",
                 user, "PUBLIC")

    pa = add_post("Turtles", "http://source.ca", "http://origin.ca",
                  "Description of turtles",
                  "PLAIN",
                  "I like turtles",
                  ua, "PUBLIC")

    pb = add_post("Title", "http://source.ca", "http://origin.ca",
                  "Description2",
                  "HTML",
                  "<div id=\"divid\">I also like turtles</div>",
                  ub, "PUBLIC")

    pc = add_post("D'oh", "http://source.ca", "http://origin.ca",
                  "Description",
                  "PLAIN",
                  "Mmmmmm, posts...",
                  uf, "PUBLIC")

    pd = add_post("Title", "http://source.ca", "http://origin.ca",
                  "Description",
                  "HTML",
                  "<strong>Cowabunga</strong>",
                  uh, "PUBLIC")

    pe = add_post("", "http://source.ca", "http://origin.ca",
                  "",
                  "PLAIN",
                  "",
                  uj, "PUBLIC")

    pf = add_post("Milhouse is not a meme",
                  "http://source.ca", "http://origin.ca",
                  "Milhouse is not a meme",
                  "PLAIN",
                  "Milhouse is not a meme",
                  uo, "PUBLIC")

    pg = add_post("Milhouse is not a meme is a meme though",
                  "http://source.ca", "http://origin.ca",
                  "Milhouse is not a meme is a meme though",
                  "PLAIN",
                  "Milhouse is not a meme is a meme though",
                  ui, "PUBLIC")

    post_list = {pa, pb, pc, pd, pe, pf, pg}

    for post in post_list:
        add_comment(post, un,
                    "BARK BARK BARK!")
        add_comment(post, up,
                    "You'll pay for this! With your children's blood!")

    # servers
    # if using the host (ie cs410-02) it must be done over port 80
    saa = add_server("Local", "10.4.10.2", "http://10.4.10.2:8080/",
                    "8080", "cs410-02")
    sa = add_server("Duplicate", "10.4.10.2", "http://10.4.10.2:8081/",
                    "8081", "cs410-02")
    sab = add_server("Duplicate2", "10.4.10.2", "http://10.4.10.2:3000/",
                     "3000", "cs410-02")
    sb = add_server("Group 1", "10.4.10.1", "http://10.4.10.1:8080/",
                    "8080", "cs410-01")
    sc = add_server("Group 3", "10.4.10.3", "http://10.4.10.3:8080/",
                    "8080", "cs410-03")
    sd = add_server("Group 4", "10.4.10.4", "http://10.4.10.4:8080/",
                    "8080", "cs410-04")
    se = add_server("Group 5", "10.4.10.5", "http://10.4.10.5:8080/",
                    "8080", "cs410-05")
    sf = add_server("Group 6", "10.4.10.6", "http://10.4.10.6:8080/",
                    "8080", "cs410-06")
    sg = add_server("Group 7", "10.4.10.7", "http://10.4.10.7:8080/",
                    "8080", "cs410-07")
    sh = add_server("Group 8", "10.4.10.8", "http://10.4.10.8:8080/",
                    "8080", "cs410-08")
    si = add_server("Group 9", "10.4.10.9", "http://10.4.10.9:8080/",
                    "8080", "cs410-09")

    # print all data for visual confirmation
    printAllUsers()
    printAllCategories()
    printAllFriends()
    printAllPosts()
    printAllComments()
    printAllServers()


def add_user(email, firstName, lastName, password, is_admin=False,
             guid=None):
    user = None
    try:
        user = User.objects.get(email=email)
        return user
    except:
        pass
    if not user:
        if is_admin:
            user = User.objects.create_superuser(email, firstName, lastName,
                                                 password)
        else:
            user = User.objects.create_user(email, firstName, lastName,
                                            password)
        if guid:
            user.guid = guid
        user.clean()
        user.save()
    return user


def add_category():
    pass


def add_friend(requester, receiver, accepted):
    try:
        #requester = User.objects.get(id=requester.id)
        #receiver = User.objects.get(id=receiver.id)
        Friends.objects.create(user_id_requester=requester,
                               user_id_receiver=receiver,
                               accepted=accepted)
    except:
        print "Error creating friend or friend request."


def add_post(title, source, origin, description, content_type, content,
             author, visibility):  # , published_date, guid=None):
    post, created = Post.objects.get_or_create(title=title, source=source,
                                               origin=origin,
                                               description=description,
                                               content_type=content_type,
                                               content=content,
                                               author=author,
                                               #published_date=published_date,
                                               #guid=guid,
                                               visibility=visibility)
    if created:
        #print "created post", title
        post.clean()
        post.save()
        pass
    else:
        print "didn't create post", title
    return post


def add_comment(post, user, content):  # , published_date, guid):
    comment, created = Comment.objects.get_or_create(
        post=post,
        user=user,
        content=content,
        #published_date=published_date,
        #guid=guid
        )
    if created:
        #print "created comment", content
        comment.clean()
        comment.save()
    else:
        print "didn't create comment", content
    return comment


def add_server(name, ip, url, port, host):
    server, created = Server.objects.get_or_create(
        name=name,
        ip=ip,
        url=url,
        port=port,
        host=host,
        )
    if created:
        #print "created server", name
        #server.clean()
        server.save()
    else:
        print "didn't create server", name
    return server


def printAllUsers():
    for user in User.objects.all():
        print user


def printAllCategories():
    for category in Category.objects.all():
        print category


def printAllFriends():
    for friend in Friends.objects.all():
        print friend


def printAllPosts():
    for post in Post.objects.all():
        print post


def printAllComments():
    for comment in Comment.objects.all():
        print comment


def printAllServers():
    for server in Server.objects.all():
        print server


if __name__ == '__main__':
    print("Starting DisSoNet database population script...")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DisSoNet.settings')
    #import DisSoNet things
    from data.models import Post, User, Comment, Friends, Category, Server
    populate()

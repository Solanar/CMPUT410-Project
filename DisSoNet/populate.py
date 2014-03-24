#!/usr/bin/env python

#import just python things
import os


def populate():
    # create users

    # create admin users
    u1 = add_user("eklinger@ualberta.ca", "Eric", "Klinger", "410", is_admin=True)
    # create normal users
    # ...

    # create a post
    # ...

    # print all data for visual confirmation
    printAllUsers()
    printAllPosts()
    printAllComments()

def add_user(email, firstName, lastName, password, is_admin=False):
    user = User.objects.get_or_create(email=email, firstName=firstName,
                                      lastName=lastName, password=password,
                                      is_admin=is_admin)
    return user[0]

def add_post(title, source, origin, description, content_type, author,
             published_date, visibility, guid=None):
    post = Post.objects.get_or_create(title=title, source=source, origin=origin,
                                      description=description,
                                      content_type=content_type, author=author,
                                      published_date=published_date, guid=guid,
                                      visibility=visibility)
    return post[0]

def add_comment(post, user, content, published_date, guid):
    comment = Post.objects.get_or_create(post=post,
                                         user=user,
                                         content=content,
                                         published_date=published_date,
                                         guid=guid)

def printAllUsers():
    for user in User.objects.all():
        print user

def printAllPosts():
    for post in Post.objects.all():
        print post

def printAllComments():
    for comment in Comment.objects.all():
        print comment


if __name__ == '__main__':
    print("Starting DisSoNet database population script...")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DisSoNet.settings')
    #import DisSoNet things
    from data.models import Post, User, Comment
    populate()

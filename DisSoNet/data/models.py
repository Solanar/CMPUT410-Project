from django.db import models
from django import forms


# ANDREW! This is just a placeholder for setting up foreignKeys,
# please swap this out for the django user/auth stuff
class User(models.Model):
    """
    TODO

    Fields:
    id: unique to each author, sha1, or uuid
    host: the URL path to the host/server the user belongs
    display_name: The name the author choses to be displayed

    * Good example for this is in example-article.json
    authors_information: URL to the authors information
    """
    name = models.CharField(max_length=20)


class Category(models.Model):
    """
    TODO

    This model tracks all the categories entered by the users.
    There isn't anything about this section in the spec, however it
    did appear in the example_artivle.json.

    I think if we supply a static list for now, with a multi-select
    functionality for adding categories to your posts will suffice for now.
    We can add dynamic category adding stuff later if needed
    """
    pass


class Friends(models.Model):
    """ Defines the Friends relationship

    Fields:
    user_requester
    user_target
    accepted (false, true)

    With the foreign keys here the reverse relationships should be available
    on the User model.

    """
    pass
    """
    # For the user initiating the friend request
    user_requester = models.ForeignKey(User, related_name='friends')
    # For the receiver of the freind request
    user_target = models.ForeignKey(User, related_name='friend_requests')
    accepted = models.BooleanField()
    """


class Post(models.Model):
    """ Defines a Post Model

    Fields from JSON example_artivle.json
    title: Title of the post
    source: The URL of where we got the post
    origin: The URL of where it actually came from
    description: Brief description of the post, limited by characters of 100
    content-type: choice of [text/html, text/x-markdown, text/plain]
    content: Text field to input the contents of the post
    author: Foreign key referenceing author

    * Need clarification of that implementation of this field
    categories: List, multiple select options for categories this post falls under

    * Special case *
    Comments: Foreign key referencing a comment entry
    For settings up the one-to-many relationship in this case set up a foreign
    key on each comment referencing a post, and django will automatically set
    up the reverse relationship so we can get the comments on a post easily.
    This is accomplished by the 'related_name' argument in the foreignKey of
    each comment. Then we can do 'some_post.comments' and get all the comments
    for that post

    Published date: Date the post was created, not modifiable afterwards
    giud: Still to be implemented. A guid is a 40 digit sha1 thats unique globally between
    all servers.
    visibility: choice of [PUBLIC, FOAF, FRIENDS, PRIVATE, SERVERONLY]
    * From the requirements there is another type. PRIVATE to another author

    """
    # Choices for content_type field
    CONTENT_TYPE_CHOICES = (
        ('HTML', 'text/html'),
        ('X-MARKDOWN', 'text/x-markdown'),
        ('PLAIN', 'text/plain'),
    )

    # Choices for visibility field
    VISIBILITY_CHOICES = (
        ('PUBLIC', 'Public'),
        ('FOAF', 'Friend of a friend'),
        ('FRIENDS', 'Friends'),
        ('PRIVATE', 'Private'),
        ('SERVERONLY', 'Server only'),
    )
    # ID/PK done auto for us
    title = models.CharField("Title", max_length=80)
    source = models.URLField("Source")
    origin = models.URLField("Origin")
    description = models.CharField("Description", max_length=100)
    content_type = models.CharField("Content type", max_length=20,
                                    choices=CONTENT_TYPE_CHOICES)
    content = models.TextField("Content")
    author = models.ForeignKey(User)
    # Commenting out until we get clarification on the implementation of categories
    #categories = models.ForeignKey(Category)
    published_date = models.DateTimeField(auto_now_add=True)
    guid = models.CharField("guid", max_length=40, blank=True)
    visibility = models.CharField("Visibility", max_length=20,
                                  choices=VISIBILITY_CHOICES)


class Comment(models.Model):
    """ Defines a Comment of a post, made by a user

    Fields:
    post: This is a one-to-many field on posts, from the post we can call post.comments
    to get all the comments for that post.
    user: This is a many-to-one field on the comment. A user can author many posts
    content: Text field for inputing the contents of the comment message
    published_date: Date comment was published, unchangable after creation
    giud: Still to be implemented. A guid is a 40 digit sha1 thats unique globally between
    all servers.
    """
    post = models.ForeignKey(Post, related_name='comments')
    user = models.ForeignKey(User)
    content = models.TextField("Content")
    published_date = models.DateTimeField(auto_now_add=True)
    guid = models.CharField("guid", max_length=40, blank=True)

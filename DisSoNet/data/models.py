from django.db import models


class Post(models.Model):
    """ Defines a Post Model

    Fields:
    id
    user_id
    type (markdown html plaintext)
    content
    media_type
    media_content
    privacy (local, friend, friendoffriend, etc)
    timestamp
    """
    # ID/PK done auto for us
    user_id = models.CharField("User ID", max_length=50)
    # TODO set up choies for this field
    # text/html
    # text/x-markdown
    # text/plain
    content_type = models.CharField("Content Type", max_length=50)
    content = models.TextField("Content")
    media_type = models.CharField("Media Type", max_length=50)
    # Media content would be like a link to an image saved on our server
    # Lots of arguments for this field, read the django file management section
    media_content = models.FileField("Media Content")
    # TODO set up choies for this field
    # visibility ["PUBLIC","FOAF","FRIENDS","PRIVATE","SERVERONLY"]
    privacy = models.CharField("Privacy", max_length=20)
    # May consider splitting this into created_time and last_modified
    time_stamp = models.TimeField(auto_now_add=True)

# ANDREW! This is just a placeholder for setting up foreignKeys,
# please swap this out for the django user/auth stuff
class User(model.Models);
    """
    TODO
    """
    pass

class Comment(model.Models);
    """ Defines a Comment of a post, made by a user

    Fields:
    post_id
    user_id
    content
    timestamp
    """
    post_id = models.ForeignKey(Post)
    user_id = models.ForeignKey(User)
    content = TextField("Content")
    time_stamp = models.TimeField(auto_now_add=True)

class Friends(model.Models);
    """ Defines the Friends relationship

    Fields:
    user_id_first
    user_id_second
    accepted (false, true)
    """
    user_id_requester = models.ForeignKey(User)
    user_id_receiver = models.ForeignKey(User)
    accepted = models.BooleanField()

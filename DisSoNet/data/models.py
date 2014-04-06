from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
#from django.forms import CharField, PasswordInput

import hashlib
import urllib2
from datetime import datetime


class UserManager(BaseUserManager):
    def create_user(self, email, firstName, lastName, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=UserManager.normalize_email(email),
                          firstName=firstName,
                          lastName=lastName,
                          )
        user.set_password(password)
        timestring = datetime.now().strftime("%a %b %d %h:%m:%s mst %y")
        stringtohash = timestring + user.email
        user.guid = hashlib.sha1(stringtohash).hexdigest()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, firstName, lastName, password):
        user = self.create_user(email=email,
                                firstName=firstName,
                                lastName=lastName,
                                password=password,
                                )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    class Meta:
        verbose_name_plural = 'Users'
        verbose_name = 'User'

    def clean(self):
        """ clean and validate the models fields. """
        # only set the guid once
        if not self.guid:
            timestring = datetime.now().strftime("%a %b %d %h:%m:%s mst %y")
            stringtohash = timestring + self.email
            self.guid = hashlib.sha1(stringtohash).hexdigest()

    email = models.EmailField("Email", max_length=75, unique=True)
    firstName = models.CharField("First Name", max_length=50)
    lastName = models.CharField("Last Name", max_length=50)

    guid = models.CharField("guid", max_length=40, blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstName', 'lastName']

    def get_full_name(self):
        # The user is identified by full name
        return self.firstName + " " + self.lastName

    def get_short_name(self):
        # The user is identified by their first name
        return self.firstName

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Category(models.Model):
    """
    This model tracks all the categories entered by the users.
    There isn't anything about this section in the spec, however it
    did appear in the example_artivle.json.
    """
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Friends(models.Model):
    """ Defines the Friends relationship

    Fields:
    user_requester
    user_target
    accepted (false, true)

    With the foreign keys here the reverse relationships should be available
    on the User model.

    """
    user_id_requester = models.ForeignKey(User, related_name='requester')
    user_id_receiver = models.ForeignKey(User, related_name='receiver')
    accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user_id_requester", "user_id_receiver")
        verbose_name = "Friends"
        verbose_name_plural = "Friends"

    def __str__(self):
        return self.user_id_requester.email + " -> " \
            + self.user_id_receiver.email + " " + str(self.accepted)


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
    categories: List, multiple select options for categories this post
        falls under

    * Special case *
    Comments: Foreign key referencing a comment entry
    For settings up the one-to-many relationship in this case set up a foreign
    key on each comment referencing a post, and django will automatically set
    up the reverse relationship so we can get the comments on a post easily.
    This is accomplished by the 'related_name' argument in the foreignKey of
    each comment. Then we can do 'some_post.comments' and get all the comments
    for that post

    Published date: Date the post was created, not modifiable afterwards
    giud: Still to be implemented. A guid is a 40 digit sha1 thats unique
        globally between all servers.
    visibility: choice of [PUBLIC, FOAF, FRIENDS, PRIVATE, SERVERONLY]
    * From the requirements there is another type. PRIVATE to another author

    """
    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.title + "-posted by-" + self.author.email

    def clean(self):
        """ clean and validate the models fields.

        Also for posts adds the guid from the present data.

        """
        # only set the guid once
        if not self.guid:
            timestring = datetime.now().strftime("%a %b %d %h:%m:%s mst %y")
            stringtohash = self.title + timestring + self.author.email
            self.guid = hashlib.sha1(stringtohash).hexdigest()

    def save(self, *args, **kwargs):
        if self.image_url:
            image = urllib2.urlopen(self.image_url)
            image_file_path = 'static/images/%s.jpg' % self.guid
            image_file = open(image_file_path, 'wb')
            image_file.write(image.read())
            image_file.close()
            self.image_location = image_file_path

        super(Post, self).save(*args, **kwargs)

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
    # This is for image posts
    image_url = models.URLField("Image URL", blank=True)
    image_location = models.CharField("image_location", max_length=100, blank=True)


class Comment(models.Model):
    """ Defines a Comment of a post, made by a user

    Fields:
    post: This is a one-to-many field on posts, from the post we can call
        post.comments to get all the comments for that post.
    user: This is a many-to-one field on the comment. A user can author many
        posts
    content: Text field for inputing the contents of the comment message
    published_date: Date comment was published, unchangable after creation
    giud: Still to be implemented. A guid is a 40 digit sha1 thats unique
        globally between all servers.
    """
    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return self.post.title + "-commented on by-" + self.user.email

    def clean(self):
        """ clean and validate the models fields. """
        # only set the guid once
        if not self.guid:
            timestring = datetime.now().strftime("%a %b %d %h:%m:%s mst %y")
            stringtohash = self.post.title + timestring + self.user.email
            self.guid = hashlib.sha1(stringtohash).hexdigest()

    post = models.ForeignKey(Post, related_name='comments')
    user = models.ForeignKey(User)
    content = models.TextField("Content")
    published_date = models.DateTimeField(auto_now_add=True)
    guid = models.CharField("guid", max_length=40, blank=True)


class GitHub(models.Model):
    user = models.ForeignKey(User)
    gitUser = models.CharField(max_length=20)
    token = models.CharField(max_length=40)

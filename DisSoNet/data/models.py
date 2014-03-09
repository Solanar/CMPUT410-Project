from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.forms import CharField, PasswordInput


class UserManager(BaseUserManager):
    def create_user(self, email, firstName, lastName, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=UserManager.normalize_email(email),
                          firstName=firstName,
                          lastName=lastName,
                          )
        user.set_password(password)
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

    email = models.EmailField("Email", max_length=75, unique=True)
    firstName = models.CharField("First Name", max_length=50)
    lastName = models.CharField("Last Name", max_length=50)

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
    #user_id = models.CharField("User ID", max_length=50)
    user_id = models.ForeignKey(User)
    # TODO set up choies for this field
    # text/html
    # text/x-markdown
    # text/plain
    content_type = models.CharField("Content Type", max_length=50)
    content = models.TextField("Content")
    media_type = models.CharField("Media Type", max_length=50)
    # Media content would be like a link to an image saved on our server
    # Lots of arguments for this field, read the django file management section
    media_content = models.FileField(upload_to='post/%Y/%m/%d')
    # TODO set up choies for this field
    # visibility ["PUBLIC","FOAF","FRIENDS","PRIVATE","SERVERONLY"]
    privacy = models.CharField("Privacy", max_length=20)
    # May consider splitting this into created_time and last_modified
    time_stamp = models.TimeField(auto_now_add=True)


class Comment(models.Model):
    """ Defines a Comment of a post, made by a user

    Fields:
    post_id
    user_id
    content
    timestamp
    """
    post_id = models.ForeignKey(Post)
    user_id = models.ForeignKey(User)
    content = models.TextField("Content")
    time_stamp = models.TimeField(auto_now_add=True)


class Friends(models.Model):
    """ Defines the Friends relationship

    Fields:
    user_id_first
    user_id_second
    accepted (false, true)
    """
    user_id_requester = models.ForeignKey(User, related_name='requester')
    user_id_receiver = models.ForeignKey(User, related_name='receiver')
    accepted = models.BooleanField()

from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import User, Post, GitHub
class UserCreationForm(forms.ModelForm):  # UserCreationForm):
    errorMessages = {
        'duplicateEmail': _("A user with that email already exists."),
        'passwordMismatch': _("The two password fields didn't match."),
    }

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',
                  'firstName', 'lastName')

    def cleanEmail(self):
        # Since User.email is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data['email']
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(
            self.errorMessages['duplicateEmail'],
            code='duplicateEmail',
        )

    def cleanPassword1(self):  # cleanPassword2 is in UserCreationForm
        password = self.cleaned_data["password1"]
        if len(password) <= 3:
            raise forms.ValidationError('Password too short.')
        return password

    def cleanPassword2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    #password = ReadOnlyPasswordHashField()
    class Meta:
        model = User
        fields = ['email',  # 'password',
                  'firstName', 'lastName', ]

    #def clean_password(self):
            # Regardless of what the user provides, return the initial value.
            # This is done here, rather than on the field, because the
            # field does not have access to the initial value
            #  return self.initial['password']

class PostCreationForm(forms.ModelForm):

    class Meta:
        model = Post
        # origin, source, author, published_date and guid are all handled elsewhere
        fields = ['title', 'description', 'content_type', 'image_url', 'content', 'visibility', ]

class GitHubForm(forms.ModelForm):

    class Meta:
        model = GitHub
        fields = ['gitUser', 'token', ]

    # Choices for Authentication Method field
    AUTH_TYPE_CHOICES = (
        ('pwd', 'Password'),
        ('token', 'Token'),
    )

    authType = forms.MultipleChoiceField(label="Authentication Method", required=True,
     widget=forms.Select, choices=AUTH_TYPE_CHOICES)

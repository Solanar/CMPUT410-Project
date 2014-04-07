from .base import BaseView
from data.models import User
from django.http import HttpResponseRedirect, Http404
import pycurl, json

class GitHubView(BaseView):

    template_name = "base.html"

    def post(self, request, *args, **kwargs):
        errors = []
        if request.method == 'POST':
            if not request.POST.get('gitUser', ''):
                errors.append('Enter your GitHub user name.')
            if not request.POST.get('token', ''):
                errors.append('Enter your GitHub authentication: password or token')
            if not errors:
                gitForm = GitHubForm(request.POST) 
                authType = gitForm.POST.get['authType']
                gitUser = gitForm.POST.get['gitUser']
                secret = gitForm.POST.get['token']
                if authType == "pwd":
                    data = getToken(handle, secret)
                    if data['message'] == "Validation Failed":
                        if data['code'] == "already_exists":
                            errors.append('Token has already been created. Check your GitHub application settings.')
                        else:
                            errors.append('Validation Failed: User name and/or password are incorrect.')
                    else:
                        auth = data['code']
                else:
                    token = secret
                    return HttpResponseRedirect(request.path)

    def getToken(handle, secret):
        print "token"
        github_url = "https://api.github.com/authorizations"
        user_pwd =  handle + ":" + secret
        data = json.dumps({"scopes": ["repo"], "note": "getting-started"})
        connection = pycurl.Curl()
        connection.setopt(pycurl.URL, github_url)
        connection.setopt(pycurl.USERPWD, user_pwd)
        connection.setopt(pycurl.POST, 1)
        connection.setopt(pycurl.POSTFIELDS, data)
        connection.perform()
        print "token2"
        return serializers.serialize('json', connection.getinfo(pycurl.HTTP_CODE), fields=('message','code'))
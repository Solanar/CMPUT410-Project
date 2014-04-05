from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core import serializers
import pycurl, json
from .base import BaseView

class GitHubView(BaseView):


    def initGitHub(request):
        print "init"
        errors = []
        if request.method == 'POST':
            if not request.POST.get('handle', ''):
                errors.append('Enter your GitHub user name.')
            if not request.POST.get('auth', ''):
                errors.append('Enter your GitHub authentication: password or token')
            if not errors:
                gitForm = GitHubForm(request.POST) 
                authType = gitForm.POST.get['authType']
                handle = gitForm.POST.get['handle']
                secret = gitForm.POST.get['auth']
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
                    auth = secret
        print "render"
        return render(request, 'controls/githubForm.html', {'errors': errors})


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
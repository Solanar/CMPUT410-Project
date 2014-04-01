from django.shortcuts import render
from django.http import HttpResponseRedirectfrom django.core import serializers
import pycurl, json

def initGithub(request):
    context = RequestContext(request)
    if request.method == 'POST':
        gitForm = GitHubForm(request.POST) 
        if gitForm.is_valid(): 
            authType = gitForm.cleaned_data['authType']
            handle = gitForm.cleaned_data['handle']
            secret = gitForm.cleaned_data['auth']
            if authType == "pwd":
                data = getToken(handle, secret)
                if data['message'] == "Validation Failed":
                    if data['code'] == "already_exists":
                        auth = "exists"
                    else:
                        auth = "failed"
                else:
                    auth = secret
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        gitForm = GitHubForm()

    return render('controls/githubForm.html', {'gitForm': gitForm}, context)

def getToken(handle, secret):
    github_url = "https://api.github.com/authorizations"
    user_pwd =  handle + ":" + secret
    data = json.dumps({"scopes": ["repo"], "note": "getting-started"})
    connection = pycurl.Curl()
    connection.setopt(pycurl.URL, github_url)
    connection.setopt(pycurl.USERPWD, user_pwd)
    connection.setopt(pycurl.POST, 1)
    connection.setopt(pycurl.POSTFIELDS, data)
    connection.perform()
    return serializers.serialize('json', connection.getinfo(pycurl.HTTP_CODE), fields=('message','code'))
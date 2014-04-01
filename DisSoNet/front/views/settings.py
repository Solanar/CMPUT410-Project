from django.shortcuts import render
from django.http import HttpResponseRedirect
import pycurl, json

def initGithub(request):
    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            github_url = "https://api.github.com/authorizations"
            user_pwd = " : "
            data = json.dumps({"scopes": ["repo"], "note": "getting-started"})
            connection = pycurl.Curl()
            connection.setopt(pycurl.URL, github_url)
            connection.setopt(pycurl.USERPWD, user_pwd)
            connection.setopt(pycurl.POST, 1)
            connection.setopt(pycurl.POSTFIELDS, data)
            connection.perform()
            c.getinfo(pycurl.HTTP_CODE), c.getinfo(pycurl.EFFECTIVE_URL)
    else:
        form = ContactForm() # An unbound form

    return render(request, 'contact.html', {
        'form': form,
    })

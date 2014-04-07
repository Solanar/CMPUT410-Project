from data.models import User  # , Server
#import urllib2
#import json


class GetUserMixin(object):

    def preprocess(self, request, *args, **kwargs):
        user = User.objects.none()
        if 'user_filter' in kwargs:
            try:
                user = User.objects.get(guid=kwargs['user_filter']['user_id'])
            except:
                pass
            """
            if not user and not kwargs['user_filter']['remote']:
                user = self.getRemoteUser(kwargs['user_filter']['user_id'])
            """
        elif request.user.is_authenticated():
            user = User.objects.get(email=request.user.email)
        self.context['user_obj'] = user
        super(GetUserMixin, self).preprocess(request, *args, **kwargs)

    """
    def getRemoteUser(self, guid):
        for server in Server.objects.all():
            url = server.url[:-1]  # django adds trailing /
            url = url + ':' + str(server.port) + '/'
            url = url + "author/" + guid + "/"
            headers = {'Accept': 'application/json'}
            req = urllib2.Request(url, None, headers)
            try:
                data = urllib2.urlopen(req)
                jsonData = json.load(data)
                print ("hi", jsonData)
                jsonguid = jsonData['author'][0]['id']
                jsondisplayName = jsonData['author'][0]['displayname']
                user = User(guid=jsonguid,
                            firstName=jsondisplayName)
                print ("hi1", user)
                return user
            except urllib2.URLError as e:
                msg = ""
                if hasattr(e, 'reason'):
                    msg = "Reason: " + str(e.reason)
                if hasattr(e, 'code'):
                    msg = msg + " Error code: " + str(e.code)
                print ("Could not connect to: " + url + " because: " + msg)
    """


class GetAllUsersMixin(object):

    def preprocess(self, request, *args, **kwargs):
        all_users = User.objects.all()
        if request.user.is_authenticated():
            all_users = all_users.exclude(email=request.user.email)
        self.context['all_users'] = all_users
        super(GetAllUsersMixin, self).preprocess(request, *args, **kwargs)

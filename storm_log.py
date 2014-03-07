import urllib
import urllib2

ACCESS_TOKEN = 'DCYSSgAhrkm2TIgBAKQzZi6jIV8OPBZCSPbmEtstNvzODEk0CBT6RZ9BAkQX6aukJX0Z2IJbu7c='
PROJECT_ID = '04cfd6bca65311e38ea3123139018851'

class StormLog(object):

    def __init__(self, access_token, project_id, input_url=None):
        self.url = input_url or 'https://api.ukhw-4brx.data.splunkstorm.com/1/inputs/http'
        self.project_id = project_id
        self.access_token = access_token

        self.pass_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
        self.pass_manager.add_password(None, self.url, 'x', access_token)
        self.auth_handler = urllib2.HTTPBasicAuthHandler(self.pass_manager)
        self.opener = urllib2.build_opener(self.auth_handler)
        urllib2.install_opener(self.opener)

    def send(self, event_text, sourcetype='syslog', host=None, source=None):
        params = {'project': self.project_id,
                  'sourcetype': sourcetype}
        if host:
            params['host'] = host
        if source:
            params['source'] = source
        url = '%s?%s' % (self.url, urllib.urlencode(params))
        try:
            req = urllib2.Request(url, event_text)
            response = urllib2.urlopen(req)
            return response.read()
        except (IOError, OSError), ex:
            # An error occured during URL opening or reading
            raise


# Example
# Setup the example logger
# Arguments are your access token and the project ID
log = StormLog(ACCESS_TOKEN, PROJECT_ID)
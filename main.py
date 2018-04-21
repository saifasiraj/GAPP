#GAPP
import webapp2
import cgi, os
import cgidb
from google.appengine.ext import ndb


#UID , Name , URL , Description , Deadline , Date , and Tags.
class opportunities(ndb.Model):
    uid = ndb.StringProperty()
    name = ndb.StringProperty()
    url = ndb.StringProperty()
    description = ndb.StringProperty()
    deadline = ndb.StringProperty()
    date = ndb.StringProperty()
    tags = ndb.StringProperty()


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('testing')
        csvfile = self.request.get('file')
        print csvfile




app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)

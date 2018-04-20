#GAPP
import webapp2
from google.appengine.ext import ndb

#UID , Name , URL , Description , Deadline , Date , and Tags.
class opportunities(ndb.Model):
    uid = ndb.IntegerProperty()
    name = ndb.StringProperty()
    url = ndb.StringProperty()
    description = ndb.StringProperty()
    deadline = ndb.DateProperty()
    date = ndb.Dateproperty()
    tags = ndb.StringProperty()

#<input name="csv_file" type="file" id="myFile">

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('testing')

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)

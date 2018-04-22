#GAPP
import webapp2
import jinja2, os
import csv

from google.appengine.ext import ndb

DEFAULT_OPPS = 'OPPLIST_DEF'
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


#UID , Name , URL , Description , Deadline , Date , and Tags.
class Opportunities(ndb.Model):
    uid = ndb.StringProperty()
    name = ndb.StringProperty()
    url = ndb.StringProperty()
    description = ndb.StringProperty()
    deadline = ndb.StringProperty()
    date = ndb.StringProperty()
    tags = ndb.StringProperty()

class Favorites(ndb.Model):
    opp = ndb.StructuredProperty(Opportunities)

    @classmethod
    def favoritesquery(self, userID):
        return self.query(ancestor = userID)



class MainPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render())
    def post(self):
        self.response.headers['Content-Type'] = 'text/plain'
        csvfile = self.request.get('file')
        filelines = csvfile.splitlines()

        headercheck = 0;
        for lines in filelines:
            if(headercheck == 0):
                headercheck+=1
                continue

            reader = csv.reader([lines])
            for mainarr in reader:
                opp = Opportunities(parent=ndb.Key("OppList", DEFAULT_OPPS))
                if(not mainarr[0]):
                    mainarr[0] = mainarr[1].replace(' ', '-')
                opp.uid = mainarr[0]
                opp.name = mainarr[1]
                opp.url = mainarr[2]
                opp.description = mainarr[3]
                opp.deadline = mainarr[4]
                opp.date = mainarr[5]
                opp.tags = mainarr[6]
                opp.favorite = False;
                opp.put()


        self.response.write("DONE")
        self.redirect('/opportunities')

class ListPage(webapp2.RequestHandler):
        def get(self):
            template = JINJA_ENVIRONMENT.get_template('listpage.html')

            a = Opportunities.query(ancestor=ndb.Key("OppList", DEFAULT_OPPS)).fetch()

            self.response.write(template.render(opps = a))

        def post(self):

            userID = self.request.get('userID')
            template = JINJA_ENVIRONMENT.get_template('listpage.html')
            a = Opportunities.query(ancestor=ndb.Key("OppList", DEFAULT_OPPS)).fetch()


            self.response.write(template.render(opps = a, userID = userID))





            #userID = self.request.get('userID')
            #userIDKey = ndb.Key("User", userID)
            #listofFavorites = Favorites.favoritesquery(userIDKey).fetch()
            #self.response.write("DONE2323")



app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/opportunities', ListPage)
], debug=True)

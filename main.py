#GAPP
import webapp2
import jinja2, os
import csv
import json

from google.appengine.ext import ndb

DEFAULT_OPPS = 'OpportunitiesList'
USERID = "NOUSER"
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
        return self.query(ancestor = ndb.Key("Users", userID))



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
            global USERID
            if(self.request.get("Favorite JSON")):
                self.redirect('/favoritedata')
            elif(self.request.get("Favorite List")):
                self.redirect('/favorites')
            elif(self.request.get("Clear ID")):
                USERID = None
            elif(self.request.get("Return")):
                USERID = self.request.get("Return")
            elif(self.request.get("favbtn")):
                tempuid = self.request.get("favbtn")
                self.response.write(tempuid)
                q = Opportunities.query(Opportunities.uid == tempuid).fetch()
                for opps in q:
                    favEntry = Favorites(parent=ndb.Key("Users", USERID))
                    favEntry.opp = opps
                    favEntry.put()
                self.redirect('/favorites')
            else:
                USERID = self.request.get('userID')
            template = JINJA_ENVIRONMENT.get_template('listpage.html')
            a = Opportunities.query(ancestor=ndb.Key("OppList", DEFAULT_OPPS)).fetch()


            self.response.write(template.render(opps = a, userID = USERID))

class FavPage(webapp2.RequestHandler):
        def get(self):
            global USERID

            template = JINJA_ENVIRONMENT.get_template('favorites.html')
            favopps = Favorites.favoritesquery(USERID).fetch()

            self.response.write(template.render(opps = favopps, userID = USERID))

class FavJSON(webapp2.RequestHandler):
    def get(self):
        global USERID
        favopps = Favorites.favoritesquery(USERID).fetch()
        self.response.write(json.dumps([p.to_dict() for p in favopps]))








app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/opportunities', ListPage),
    ('/favorites', FavPage),
    ('/favoritedata', FavJSON)
], debug=True)

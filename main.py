#GAPP
#Saif Siraj


import webapp2
import jinja2, os
import csv
import json

from google.appengine.ext import ndb


#default variables
DEFAULT_OPPS = 'OpportunitiesList'
USERID = "NOUSER"

#intitalize Jinja2 Environment
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


#favorites model with opportunity as param
#query method for ease of use
class Favorites(ndb.Model):
    opp = ndb.StructuredProperty(Opportunities)

    @classmethod
    def favoritesquery(self, userID):
        return self.query(ancestor = ndb.Key("Users", userID))


#the main page
class MainPage(webapp2.RequestHandler):

    #page used to upload the csv file, index.html
    #contains the html code for uploading the file.
    #after upload page moves to the post method.
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render())

    #post method - Parses the CSV file and redirects to the
    #"opportunities" page
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

            #looks at every line after headers and creates
            #opportunity ndb model based on the data (then puts it in datastore)
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

        self.redirect('/opportunities')

#The code behind the opportunities page
#Gives a user id field, clear id option and lists all
#the opportunities in the datastore
#If a user enteres their ID they will also gain access to
#a favorite button for each opportunity as well as an option
#to see the favorites list and a json format of their favorites
class ListPage(webapp2.RequestHandler):
        def get(self):

            #HTML code behind this page for listing
            template = JINJA_ENVIRONMENT.get_template('listpage.html')

            #query set for getting all the opportunities in the datastore
            a = Opportunities.query(ancestor=ndb.Key("OppList", DEFAULT_OPPS)).fetch()

            #renders web page with query as params for the jinja2 template
            self.response.write(template.render(opps = a))

        #this handles any form post
        def post(self):
            global USERID

            #if favorite json button is pressed then it will use webapp2
            #endpoint to redirect to that page.
            if(self.request.get("Favorite JSON")):
                self.redirect('/favoritedata')
            #if favorite list button is pressed it redirects to that page
            elif(self.request.get("Favorite List")):
                self.redirect('/favorites')
            #if clear id button is pressed removes log in
            elif(self.request.get("Clear ID")):
                USERID = None
            #if return is pressed (from favorite list page) saves userid
            elif(self.request.get("Return")):
                USERID = self.request.get("Return")
            #if the favorite button is pressed it gets the value of the UID
            #field the button is pressed for.
            elif(self.request.get("favbtn")):
                tempuid = self.request.get("favbtn")
                self.response.write(tempuid)
                #queries for the opportunity with the uid provided
                q = Opportunities.query(Opportunities.uid == tempuid).fetch()
                for opps in q:
                    favEntry = Favorites(parent=ndb.Key("Users", USERID))
                    favEntry.opp = opps
                    favEntry.put()
                    #redirect to the favorites page after press
                self.redirect('/favorites')
            #assume submit button is pressed on userid field otherwise
            else:
                USERID = self.request.get('userID')

            #generate opportunity list for page
            template = JINJA_ENVIRONMENT.get_template('listpage.html')
            a = Opportunities.query(ancestor=ndb.Key("OppList", DEFAULT_OPPS)).fetch()
            self.response.write(template.render(opps = a, userID = USERID))

class FavPage(webapp2.RequestHandler):
        def get(self):
            global USERID

            #generates template for the html document
            template = JINJA_ENVIRONMENT.get_template('favorites.html')

            #query for a users favorites using userID submitted.
            favopps = Favorites.favoritesquery(USERID).fetch()

            #renders template with the userid and list of favs as params
            self.response.write(template.render(opps = favopps, userID = USERID))

class FavJSON(webapp2.RequestHandler):
    def get(self):
        global USERID

        #gets favorites using userid
        favopps = Favorites.favoritesquery(USERID).fetch()

        #creates JSON data with favorites and writes it to page.
        self.response.write(json.dumps([p.to_dict() for p in favopps]))







#endpoint management

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/opportunities', ListPage),
    ('/favorites', FavPage),
    ('/favoritedata', FavJSON)
], debug=True)

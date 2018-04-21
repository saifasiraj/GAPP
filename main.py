#GAPP
import webapp2
import cgi, os
import cgitb
import jinja2
import csv

from google.appengine.ext import ndb

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
                opp = Opportunities()
                if(not mainarr[0]):
                    mainarr[0] = mainarr[1].replace(' ', '-')
                opp.uid = mainarr[0]
                opp.name = mainarr[1]
                opp.url = mainarr[2]
                opp.description = mainarr[3]
                opp.deadline = mainarr[4]
                opp.date = mainarr[5]
                opp.tags = mainarr[6]
                opp.put()


        self.response.write("DONE")
        self.redirect('/opportunities')

class ListPage(webapp2.RequestHandler):
        def get(self):
            self.response.write("DONE2323")

    #    for lines in filelines:
    #        opp = Opportunities()
    #        if(lines[0] == ','):
    #            noUID = 1
    #        items = lines.split(',')
    #        self.response.write(items)
    #        self.response.write("\n")
    #        self.response.write(lines)
    #        self.response.write("\n")
    #        self.response.write("\n")



app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/opportunities', ListPage)
], debug=True)

import os
import webapp2
from google.appengine.ext.webapp import template


 #FUNCTION
 
def render_template(handler, file_name, template_values):
    path= os.path.join(os.path.dirname(__file__), 'templates/', file_name)

 #HANDLER

def get_template_parameters():
     values={}
     return values

class MainHandler(webapp2.RequestHandler):
     def get(self):
         values= get_template_parameters()
         render_template(self,'mainpage.html', values)

# APP

app = webapp2.WSGIApplication([
    ('/.*', MainHandler)
])
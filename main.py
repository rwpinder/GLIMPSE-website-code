#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import jinja2

#from google.appengine.ext.webapp2 import template
import webapp2
import cgi
import datetime
import urllib
import wsgiref.handlers

from google.appengine.api import users
#from google.appengine.ext import webapp2
#from google.appengine.ext.webapp2 import util



import sys, urllib, string, SOAPpy
from xml.sax import parse, ContentHandler, SAXParseException
from SOAPpy import SOAPProxy
from SOAPpy import *
 
jinja_environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


 # this is  for looking up the IP address of the user and locating the ISP
def checkIP(self):

    SOAPpy.Config.buildWithNamespacePrefix=0
    SOAPpy.Config.debug=0

    server=SOAPProxy("http://v1.fraudlabs.com/ip2locationwebservice.asmx", namespace="http://v1.fraudlabs.com/", noroot=1, soapaction="http://v1.fraudlabs.com/ip2locationwebservice.asmx/IP2Location")

    # Change these values to the address to validate
    license = "02-61QF-BHA4"
    ip = self.request.remote_addr

    myarray = {}

    myarray["IP"]=ip
    myarray["LICENSE"]=license
    
    result = server.IP2Location(inputdata=myarray)

    if (('EPA' in result.ISPNAME) or ('epa' in result.ISPNAME)):
	return True
    else:
	return False

    # if not(result.COUNTRYCODE == 'US'):
    # 	return True

    #    return False



class MainHandler(webapp2.RequestHandler):
    def get(self):
	template = jinja_environment.get_template('test.html')
	template_values = {}
        self.response.out.write(template.render(template_values))


class AboutHandler(webapp2.RequestHandler):
    def get(self):
	template = jinja_environment.get_template('about.html')
	template_values = {}
        self.response.out.write(template.render(template_values))

class RfHandler(webapp2.RequestHandler):
    def get(self):
	template = jinja_environment.get_template('rf.html')
	template_values = {}
        self.response.out.write(template.render(template_values))


class HealthHandler(webapp2.RequestHandler):
    def get(self):
	template = jinja_environment.get_template('health.html')
	template_values = {}
        self.response.out.write(template.render(template_values))

	    
class EcosystemsHandler(webapp2.RequestHandler):
    def get(self):
	template = jinja_environment.get_template('ecosystems.html')
	template_values = {}
        self.response.out.write(template.render(template_values))


class ScenariosHandler(webapp2.RequestHandler):
    def get(self):
	#	template = jinja_environment.get_template('scenarios.html')
	#template_values = {}
        #self.response.out.write(template.render(template_values))
	

	if checkIP(self):
	    template = jinja_environment.get_template('scenarios.html')
	    template_values={}
	    self.response.out.write(template.render(path, template_values))

	else:
	    path = os.path.join(os.path.dirname(__file__), 'scenarios.html')
	    template_values={'redirect':path}
	    template = jinja_environment.get_template('login.html')
	    self.response.out.write(template.render(template_values))



class LoginHandler(webapp2.RequestHandler):
    def get(self):
	template_values={}
	template = jinja_environment.get_template('scenarios.html')
	self.response.out.write(template.render(template_values))

# def main():

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/about', AboutHandler),
    ('/rf', RfHandler),
    ('/health', HealthHandler),
    ('/ecosystems', EcosystemsHandler),
    ('/scenarios',ScenariosHandler),
    ('/login',LoginHandler),    
    ],debug=True)

#    util.run_wsgi_app(application)


#if __name__ == '__main__':
#    main()



    

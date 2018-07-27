#By Oscar.
import os, os.path
import string
import cherrypy
import random
import getInfo
import json
from VMMEditor import VMMEditor

class Table(object):
    @cherrypy.expose
    def index(self):
        with open('form.html', 'r') as content_file:
            contents = content_file.read()
#HTML header.

        head = """
    <head>
        <link href="/static/css/style.css" rel="stylesheet">
        <title>
            DAaaS (VMM) Virual Machine Manager
        </title>
    </head>
        """

#HTML body.
        body = """
        <body>
        <meta name="author" content="Oscar">
        <img src="/static/images/RAL.png" alt="Logo"
        width="261" height="57">

        <h1>DAaaS Virtual Machine Manager</h1>
""" + contents + """

        </body>
            """

#Add all component strings together to make html.

        html = "<html>" + head + body + "</html>"
        return html

    @cherrypy.expose
    def handleForm(self, **params):
        editor = VMMEditor()
        params['parameters']= json.loads(params['parameters'])
        params['tags']= json.loads(params['tags'])
        parameters = json.dumps(params)
        editor.add_new_pool(parameters)
        return "Form: " + parameters
    
    
if __name__ == '__main__':
    conf = {
        '/': {
         'tools.sessions.on': True,
         'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }
    cherrypy.server.socket_host = '0.0.0.0'
    cherrypy.quickstart(Table(), '/', conf)

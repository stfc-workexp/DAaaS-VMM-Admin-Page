import os, os.path
import string
import cherrypy
import random
import getInfo
import cgi
import json
from VMMEditor import VMMEditor


class Table(object):
#HTML header.
    head = """
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="/static/css/style.css" rel="stylesheet">
        <title>
            DAaaS VM Manager
        </title>
    </head>
    """

#HTML Body
    body = """
    <body>
        <div>
            <img src="/static/images/RAL.png" alt="Logo"
            width="261" height="57">
        </div>
        <div class="dropdown">                   
            <button class="dropbtn">Navigation</button>
            <div class="dropdown-content">
                <a href="index">Virtual Machine Manager</a>
                <a href="VMPools">Virtual Machine Pools</a>
            </div>
        </div> 

        <h1>DAaaS Virtual Machine Manager</h1>
        {}

    </body>             
    """

    @cherrypy.expose
    def index(self):
        machines = getInfo.getMachines()
        machineTypes = getInfo.getMachineTypes()

        typeNames = {}
        name = {}
        for machineType in machineTypes:
            typeNames[machineType['id']] = machineType['name']

        
        #Adding if statement so if no data then instead of doing table, it will print an error message.
        if not machines:
            contents = "Error - No Data: We are working hard to fix this issue now"
        else:
            table = "<table>"
            
            table += "<th>" + "Type Of Virtual Machine" + "</th>"
            table += "<th>" + "Hostname " + "</th>"
            table += "<th>" + "VM ID" + "</th>"
            table += "<th>" + "State" + "</th>"
            table += "<th>" + "Last Updated At ..." + "</th>"
            table += "<th>" + "Update ?" + "<th>"

            #Putting all lists into a table.
            for machine in machines:
                table += "<tr>"
                table += "<td>" + typeNames[machine['machine_type_id']] + "</td>"  
                table += "<td>" + machine['hostname'] + "</td>"
                table += "<td>" + str(machine['id']) + "</td>"
                table += "<td>" + machine['state'] + "</td>"
                table += "<td>" + str(machine['acquired_time']) + "</td>"
                table += "<th>" + "<button>UpdateNow</button>" + "</th>"
                
            table += "</table>"
            contents = table

        #Add all component strings together to make html.
        html = "<html>" + self.head +self.body.format(contents) + "</html>"
        return html


    @cherrypy.expose
    def VMPools(self):
        with open('form.html', 'r') as content_file:
            contents = content_file.read()

        #Add all component strings together to make html.
        html = "<html>" + self.head + self.body.format(contents) + "</html>"
        return html
    
    @cherrypy.expose
    def handleForm(self, **params):
        editor = VMMEditor()
        params['parameters']= json.loads(params['parameters'])
        params['tags']= json.loads(params['tags'])
        parameters = json.dumps(params)
        code, response = editor.add_new_pool(parameters)

        if code == 200:
            contents = "New VM Pool created."
        else:
            contents = """
                Response = {1}
            """
        #Add all component strings together to make html.
        html = "<html>" + self.head + self.body.format(contents.format(code,response)) + "</html>"
        return html
    
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

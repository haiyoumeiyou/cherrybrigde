import cherrypy

import instance.ldap_conf as ldap_conf
from application.model.ldaphandler import OnPremADHandler

class Devices:

    @cherrypy.tools.auth(extra_requires=['guest'])
    @cherrypy.tools.template
    def list(self):
        return {'authmenu': cherrypy.session['authmenu']}

    # @cherrypy.tools.auth(extra_requires=['guest'])
    # @cherrypy.tools.template
    # def show(self, id):
    #     return {'authmenu': cherrypy.session['authmenu']}
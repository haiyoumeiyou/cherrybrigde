import cherrypy

class Error:
    @cherrypy.tools.template
    def broken(self):
        return {'authmenu': cherrypy.session['authmenu']}

    @cherrypy.tools.template
    def noauth(self):
        return {'authmenu': cherrypy.session['authmenu']}
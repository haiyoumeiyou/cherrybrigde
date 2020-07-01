import cherrypy


class User:
    @cherrypy.tools.auth(extra_requires=['system'])
    @cherrypy.tools.template
    def profile(self):
        return {'authmenu': cherrypy.session['authmenu'], 'user': cherrypy.session['user']}
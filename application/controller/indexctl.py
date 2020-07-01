
import cherrypy

from application.controller.authctl import Auth
from application.controller.errorctl import Error
from application.controller.userctl import User
from application.controller.newsctl import News
from application.controller.devicectl import Devices

class Index:
    # news = None
    # user = None
    def __init__(self):
        self.auth = Auth()
        self.news = News()
        self.user = User()
        self.devices = Devices()
        self.error = Error()

    _cp_config = {
        'auth.require': []
    }

    @cherrypy.tools.auth()
    @cherrypy.tools.template
    def index(self):
        # if "user" not in cherrypy.session:
        #     raise cherrypy.HTTPRedirect("/login")
        return {'authmenu': cherrypy.session['authmenu']}

    @cherrypy.expose
    def broken(self):
        raise RuntimeError('pretend something has broken')
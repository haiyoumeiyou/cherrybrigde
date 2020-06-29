import datetime
import uuid

import cherrypy

import instance.msal_conf as msal_conf
from application.model.msalhandler import MsalHandler
from application.model.mssqlhandler import HrdbHandler

aad = MsalHandler(msal_conf)
hr_db = HrdbHandler('sql coon string')

class Index:
    # news = None
    # user = None
    def __init__(self):
        self.news = News()
        self.user = User()
        self.error = Error()

    @cherrypy.tools.access()
    @cherrypy.tools.template
    def index(self):
        # if "user" not in cherrypy.session:
        #     raise cherrypy.HTTPRedirect("/login")
        return {'authmenu': cherrypy.session['authmenu']}

    @cherrypy.expose
    def login(self):
        cherrypy.session["state"] = str(uuid.uuid4())
        auth_url = aad._build_auth_url(
            scopes=msal_conf.SCOPE,
            state=cherrypy.session["state"]
        )
        output = """
            Cherry Tree ticket <a href='%s'>Sign In</a>
        """ % auth_url
        return output

    @cherrypy.expose
    def getAToken(self, code=None, state=None, session_state=None, error=None):
        if state and cherrypy.session.get("state") and (state != cherrypy.session["state"]):
            raise cherrypy.HTTPRedict("/index")
        if "error" in cherrypy.request.params:
            output = """
                This is Bye from cherry. <a href="/"> Back </a> <br />
                %s
            """ % str(cherrypy.request.params)
            return output
        if code:
            cache = aad._load_cache(cherrypy.session)
            result = aad._build_msal_app(cache=cache).acquire_token_by_authorization_code(
                code,
                scopes=msal_conf.SCOPE,
                redirect_uri=msal_conf.REDIRECT_PATH
            )
            if "error" in result:
                output = """
                    This is Bye from cherry. <a href="/"> Back </a> <br />
                    %s
                """ % str(cherrypy.request.params)
                return output
            cherrypy.session["user"] = result.get("id_token_claims")
            aad._save_cache(cache, cherrypy.session)
        raise cherrypy.HTTPRedirect("/index")

    @cherrypy.expose
    def logout(self):
        cherrypy.session.pop("user", None)
        raise cherrypy.HTTPRedirect(
            msal_conf.AUTHORITY + "/oauth2/v2.0/logout" +
            "?post_logout_redirect_uri=" + msal_conf.LOGOUT_ENDPOINT
        )

    @cherrypy.expose
    def broken(self):
        raise RuntimeError('pretend something has broken')


class User:
    @cherrypy.tools.access()
    @cherrypy.tools.template
    def profile(self):
        return {'authmenu': cherrypy.session['authmenu'], 'user': cherrypy.session['user']}


class News:
    _list = [
        {'id': 0, 'date': datetime.datetime(2014, 11, 16), 'title': 'Bar', 'text': 'Lorem ipsum'},
        {'id': 1, 'date': datetime.datetime(2014, 11, 17), 'title': 'Foo', 'text': 'Ipsum lorem'}
    ]

    @cherrypy.tools.access()
    @cherrypy.tools.template
    def list(self):
        return {'authmenu': cherrypy.session['authmenu'], 'list': self._list}

    @cherrypy.tools.access()
    @cherrypy.tools.template
    def show(self, id):
        return {'authmenu': cherrypy.session['authmenu'], 'item': self._list[int(id)]}


class Error:
    @cherrypy.tools.template
    def broken(self):
        return {'authmenu': cherrypy.session['authmenu']}

    @cherrypy.tools.template
    def noauth(self):
        return {'authmenu': cherrypy.session['authmenu']}


def errorPage(status, message, **kwargs):
    return cherrypy.tools.template._engine.get_template('page/error.html').render()

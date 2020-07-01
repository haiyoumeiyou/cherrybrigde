import datetime
import uuid

import cherrypy

import instance.msal_conf as msal_conf
from application.model.msalhandler import MsalHandler

aad = MsalHandler(msal_conf)


class Auth:
    @cherrypy.expose
    def login(self):
        cherrypy.session["state"] = str(uuid.uuid4())
        auth_url = aad._build_auth_url(
            scopes=msal_conf.SCOPE,
            state=cherrypy.session["state"]
        )
        # output = """
        #     Cherry Tree ticket <a href='%s'>Sign In</a>
        # """ % auth_url
        # return output
        raise cherrypy.HTTPRedirect(auth_url)

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
import msal
import uuid
# import instance.tolmsalconf as conf

# app_msal_conf = conf

class MsalHandler(object):
    
    def __init__(self, msal_conf):
        self.msal_conf = msal_conf

    def _load_cache(self, session):
        cache = msal.SerializableTokenCache()
        if "token_cache" in session:
            cache.deserialize(session["token_cache"])
        return cache

    def _save_cache(self, cache, session):
        if cache.has_state_changed:
            session["token_cache"] = cache.serialize()

    def _build_msal_app(self, cache=None, authority=None):
        return msal.ConfidentialClientApplication(
            self.msal_conf.CLIENT_ID, authority=authority or self.msal_conf.AUTHORITY,
            client_credential=self.msal_conf.CLIENT_SECRET, token_cache=cache)

    def _build_auth_url(self, authority=None, scopes=None, state=None):
        return self._build_msal_app(authority=authority).get_authorization_request_url(
            scopes or [],
            state=state or str(uuid.uuid4()),
            redirect_uri=self.msal_conf.REDIRECT_PATH)

    def _get_token_from_cache(self, scope=None, session=None):
        cache = self._load_cache(session)  # This web app maintains one cache per session
        cca = self._build_msal_app(cache=cache)
        accounts = cca.get_accounts()
        if accounts:  # So all account(s) belong to the current signed-in user
            result = cca.acquire_token_silent(scope, account=accounts[0])
            self._save_cache(cache, session)
            return result
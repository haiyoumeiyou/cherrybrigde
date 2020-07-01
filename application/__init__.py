import os
import types

import cherrypy
import jinja2

import config

from .model.sqlitehandler import SiteHandler


site_db = SiteHandler()

class TemplateTool(cherrypy.Tool):

    _engine = None
    """jinja environment instance"""

    def __init__(self):
        # print(config.path)
        viewloader = jinja2.FileSystemLoader(os.path.join(config.path, 'application', 'view'))
        self._engine = jinja2.Environment(loader=viewloader)

        cherrypy.Tool.__init__(self, 'before_handler', self.render)

    def __call__(self, *args, **kwargs):
        if args and isinstance(args[0], (types.FunctionType, types.MethodType)):
            # @template
            args[0].exposed = True
            return cherrypy.Tool.__call__(self, **kwargs)(args[0])
        else:
            # @template()
            def wrap(f):
                f.exposed = True
                return cherrypy.Tool.__init__(self, *args, **kwargs)(f)
            return wrap

    def render(self, name=None):
        cherrypy.request.config['template'] = name

        handler = cherrypy.serving.request.handler
        def wrap(*args, **kwargs):
            return self._render(handler, *args, **kwargs)
        cherrypy.serving.request.handler = wrap

    def _render(self, handler, *args, **kwargs):
        template = cherrypy.request.config['template']
        if not template:
            parts = []
            if hasattr(handler.callable, '__self__'):
                parts.append(handler.callable.__self__.__class__.__name__.lower())
            if hasattr(handler.callable, '__name__'):
                parts.append(handler.callable.__name__.lower())
            template = '/'.join(parts)
            # print("no template: ", parts, template)

        data = handler(*args, **kwargs) or {}
        # print("template data: ", data)
        # print("template: ", template)
        renderer = self._engine.get_template('page/{0}.html'.format(template))
        return renderer.render(**data) if template and isinstance(data, dict) else data

class AuthTool(cherrypy.Tool):
    def __init__(self):
        cherrypy.Tool.__init__(
            self,
            'before_handler',
            self.auth_check,
            priority=95
        )

    def auth_check(self, extra_requires=None):
        print('checking auth...')
        requires = cherrypy.request.config.get('auth.require', None)
        if extra_requires is not None:
            add_new = lambda x, y: list(set(x)|set(y))
            requires = add_new(requires, extra_requires)
        if requires is not None:
            user = cherrypy.session.get('user', None)
            if not user:
                raise cherrypy.HTTPRedirect("/auth/login")
            if len(requires) > 0:
                user['groups'] = ['guest']
                check_pass = lambda x, y : True if len(set(x)&set(y)) > 0 else False
                ipass = check_pass(requires, user['groups'])
                if not ipass:
                    raise cherrypy.HTTPRedirect("/error/noauth")
        site_stat, auth_menu = site_db.get_top_menu('system')
        cherrypy.session['authmenu'] = auth_menu



class AccessTool(cherrypy.Tool):
    def __init__(self):
        cherrypy.Tool.__init__(self,
            'before_handler',
            self.check_access,
            priority=95
        )

    def check_access(self):
        if "user" not in cherrypy.session:
            raise cherrypy.HTTPRedirect("/login")
        site_stat, auth_menu = site_db.get_top_menu('system')
        if not site_stat:
            raise cherrypy.HTTPRedirect("/error/noauth")
        auth_href = [h for c, h, g in auth_menu]
        cherrypy.session['authmenu'] = auth_menu
        # print(dir(cherrypy.request), cherrypy.request.path_info)
        if cherrypy.request.path_info not in auth_href:
            raise cherrypy.HTTPRedirect("/error/noauth")


def bootstrap():

    cherrypy.tools.template = TemplateTool()
    # cherrypy.tools.access = AccessTool()
    cherrypy.tools.auth = AuthTool()

    cherrypy.config.update(config.config)

    from .controller.indexctl import Index


    # cherrypy.config.update({'error_page.default': controller.errorPage})
    cherrypy.tree.mount(Index(), '/', config.config)

import os
import cherrypy

path = os.path.abspath(os.path.dirname(__file__))
config = {
    'global': {
        'server.socket_host': '127.0.0.1',
        'server.socket_port': 8080,
        'serverthread_pool': 8,

        'engine.autoreload.on': True,

        'tools.trailing_slash.on': False
    },
    '/resource': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(path, 'public', 'resource')
    },
    '/': {
        'tools.sessions.on': True,
        'tools.sessions.storage_class': cherrypy.lib.sessions.FileSession,
        'tools.sessions.storage_path': os.path.join(path, 'sessions')
    }
}

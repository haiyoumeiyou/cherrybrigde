import datetime
import cherrypy

class News:
    _list = [
        {'id': 0, 'date': datetime.datetime(2014, 11, 16), 'title': 'Bar', 'text': 'Lorem ipsum'},
        {'id': 1, 'date': datetime.datetime(2014, 11, 17), 'title': 'Foo', 'text': 'Ipsum lorem'}
    ]

    @cherrypy.tools.auth(extra_requires=['guest'])
    @cherrypy.tools.template
    def list(self):
        return {'authmenu': cherrypy.session['authmenu'], 'list': self._list}

    @cherrypy.tools.auth(extra_requires=['guest'])
    @cherrypy.tools.template
    def show(self, id):
        return {'authmenu': cherrypy.session['authmenu'], 'item': self._list[int(id)]}

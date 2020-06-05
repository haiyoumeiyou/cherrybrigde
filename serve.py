from application import bootstrap

bootstrap()

if __name__=='__main__':
    import cherrypy
    cherrypy.engine.signals.subscribe()
    cherrypy.engine.start()
    cherrypy.engine.block()
    
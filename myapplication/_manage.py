from myapplication._database import db_session

@app.teardown_appcontext                 #As in the declarative approach, you need to close 
                                         #the session after each request or application context
                                         # shutdown. Put this into your application module:
def shutdown_session(exception=None):
    db_session.remove()


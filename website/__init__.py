#from package import Class
from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

db=SQLAlchemy()

def page_not_found(e):
  return render_template('404.html'), 404

def internal_server_error(e):
  return render_template('500.html'), 500

#create a function that creates a web application
# a web server will run this web application
def create_app():
  
    app=Flask(__name__)  # this is the name of the module/package that is calling this app
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)
    app.debug=True
    app.secret_key='862b1a0d45e29873ab29da77a06728fed0d3c783512a797a'
    #set the app configuration data 
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///mydbname.sqlite'
    #initialise db with flask app
    db.init_app(app)

    bootstrap = Bootstrap5(app)

    # Activate CSRF protection
    CSRFProtect(app)
    
    #initialize the login manager
    login_manager = LoginManager()
    
    #set the name of the login function that lets user login
    # in our case it is auth.login (blueprintname.viewfunction name)
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    #create a user loader function takes userid and returns User
    from .models import User  # importing here to avoid circular references
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    #importing views module here to avoid circular references
    # a common practice.
    from . import views
    app.register_blueprint(views.bp)

    from . import auth
    app.register_blueprint(auth.bp)
    
    return app




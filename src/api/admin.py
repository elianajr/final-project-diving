  
import os
from flask_admin import Admin
from .models import db, Client, Waterdropper, Center, Hotspot, Specie, Sport, Chat, News
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    # admin.add_view(ModelView(Chatassociation, db.session))
    admin.add_view(ModelView(Client, db.session))
    admin.add_view(ModelView(Waterdropper, db.session))
    admin.add_view(ModelView(Center, db.session))
    admin.add_view(ModelView(Hotspot, db.session))
    admin.add_view(ModelView(Specie, db.session))
    admin.add_view(ModelView(Sport, db.session))
    admin.add_view(ModelView(Chat, db.session))
    admin.add_view(ModelView(News, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))
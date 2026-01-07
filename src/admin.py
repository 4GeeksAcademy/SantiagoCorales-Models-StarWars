import os
from flask_admin import Admin
from models import db, User, Character, FavoriteCharacter, FavoritePlanet, FavoriteStarship
from flask_admin.contrib.sqla import ModelView


class UserModelView(ModelView):
    column_auto_select_related = True
    column_list = ['id', 'email', 'password',
                   'is_active', 'favorite_characters',]


class CharacterModelView(ModelView):
    column_auto_select_related = True
    column_list = ['id', 'name', 'height', 'favorited_by']


class FavoriteCharactersModelView(ModelView):
    column_auto_select_related = True
    column_list = ['id', 'user_id', 'user', 'character_id', 'character']


class FavoritePlanetModelView(ModelView):
    column_auto_select_related = True
    column_list = ['id', 'user', 'planet']


class FavoriteStarshipModelView(ModelView):
    column_auto_select_related = True
    column_list = ['id', 'user', 'starship']


def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(CharacterModelView(Character, db.session))
    admin.add_view(FavoriteCharactersModelView(FavoriteCharacter, db.session))
    admin.add_view(FavoritePlanetModelView(FavoritePlanet, db.session))
    admin.add_view(FavoriteStarshipModelView(FavoriteStarship, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))

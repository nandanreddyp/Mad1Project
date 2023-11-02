from flask_restful import Api

api = Api()

from flask import request
from flask_restful import Resource, abort
from functools import wraps
from Musica.database.models import *

api_keys = ['admin@musica.143','fuckyou#420']
def validate_api_key(api_key):
    return api_key in api_keys
def api_key_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('API-Key')  # ! extract the api key from the request headers
        print(api_key)
        if not api_key or not validate_api_key(api_key):
                abort(401, description='Unauthorized - Invalid API Key')
        return f(*args, **kwargs)
    return decorated_function

class UserApi(Resource):
    @api_key_required
    def post(self,id):
        return 'uploaded'
    @api_key_required    
    def put(self,id):
        return 'updated'
    @api_key_required
    def get(self,id):
        return 'info'
    @api_key_required
    def delete(self,id):
        return 'deleted'
    
class SongApi(Resource):
    @api_key_required
    def post(self,id):
        return 'uploaded'
    @api_key_required
    def put(self,id):
        return 'updated'
    @api_key_required
    def get(self,id):
        return 'info'
    @api_key_required
    def delete(self,id):
        return 'deleted'
    
class RatingApi(Resource):
    def post(self,id,value):
        return 'done'
    
class AlbumApi(Resource):
    @api_key_required
    def post(self,id):
        return 'uploaded'
    @api_key_required
    def put(self,id):
        return 'updated'
    @api_key_required
    def get(self,id):
        return 'info'
    @api_key_required
    def delete(self,id):
        return 'deleted'
    
class PlaylistApi(Resource):
    @api_key_required
    def post(self,id):
        return 'uploaded'
    @api_key_required
    def put(self,id):
        return 'updated'
    @api_key_required
    def get(self,id):
        return 'info'
    @api_key_required
    def delete(self,id):
        return 'deleted'

api.add_resource(UserApi, '/api/user/<string:id>')
api.add_resource(SongApi, '/api/song/<int:id>')
api.add_resource(RatingApi, '/api/song/<int:id>/rate/<int:value>')
api.add_resource(AlbumApi, '/api/album/<int:id>')
api.add_resource(PlaylistApi, '/api/playlist/<int:id>')
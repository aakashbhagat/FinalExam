from flask import Response, request
from database.models import Books
from flask_restful import Resource
from flask_jwt_extended.view_decorators import jwt_required
from database.models import User
import datetime
from flask_jwt_extended import create_access_token

class BooksAPI(Resource):

    @jwt_required()
    def get(self):
        book = Books.objects().to_json()
        return Response(book, mimetype="applicaiton/json", status=200)
    
    @jwt_required()
    def post(self):
        body = request.get_json()
        book = Books(**body).save()
        id = book.book_id
        return {'id': str(id)}, 200
    
    
class SingleBookAPI(Resource):
    
    @jwt_required()
    def get(self, id):
        book = Books.objects.get(book_id=id).to_json()
        return Response(book, mimetype="applicaiton/json", status=200)

    @jwt_required()
    def put(self, id):
        body = request.get_json()
        Books.objects.get(book_id=id).update(**body)
        return 'book updated', 200
    
    @jwt_required()
    def delete(self, id):
        Books.objects.get(book_id=id).delete()
        return Response("book Deleted Successfully", mimetype="applicaiton/json", status=200)

class RegisterAPI(Resource):
    
    def post(self):
        body = request.get_json()
        user = User(**body)
        user.hash_password()
        user.save()
        id = user.id
        return {'id': str(id)}, 200
    
class LoginAPI(Resource):
    
    def post(self):
        body = request.get_json()
        user = User.objects.get(email = body.get('email'))
        authorized = user.check_password(body.get('password'))
        if not authorized:
            return {'error': 'Invalid Credentials'}, 401
        expiry = datetime.timedelta(days=1)
        accesss_token = create_access_token(identity=str(user.id), expires_delta=expiry)
        return {'token': accesss_token}, 200
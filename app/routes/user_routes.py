from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from ..config.Config import api
from ..services.user_service import UsersService
from ..models.Api_User import User_fields, login_fields

def user_routes(user_ns):
    @user_ns.route('/register')
    class Register(Resource):
        @api.expect(User_fields)
        def post(self):
            data = api.payload
            email = data['email']

            if UsersService.get_user_by_email(email):
                return {'message': 'User already exists'}, 400

            new_user = UsersService.create_user(data)
            return {'message': 'User created successfully', 'email': new_user.email}, 201

    @user_ns.route('/login')
    class Login(Resource):
        @api.expect(login_fields)
        def post(self):
            data = api.payload
            email = data['email']
            password = data['password']

            user = UsersService.get_user_by_email(email)
            if user and user.password == password:
                access_token = create_access_token(identity=email)
                refresh_token = create_refresh_token(identity=email)
                return {
                    'message': 'Logged in successfully',
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }, 200
            return {'message': 'Invalid credentials'}, 401

    @user_ns.route('/protected')
    class Protected(Resource):
        @jwt_required()
        @api.expect(login_fields)
        @user_ns.doc(security = 'Bearer')  

        def post(self):
            current_user = get_jwt_identity()
            return {'message': f'Hello {current_user}'}

    @user_ns.route('/getaccess')
    class Refresh(Resource):
        @jwt_required(refresh=True)
        @user_ns.doc(security = 'Bearer')  
        def post(self):
            current_user = get_jwt_identity()
            new_access_token = create_access_token(identity=current_user)
            return {'access_token': new_access_token}, 200
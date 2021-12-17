"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from datetime import timedelta

from flask_cors import CORS
from sqlalchemy import exc
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, Account, Waterdropper, Center, Hotspot, Specie, Sport, News
from api.utils import generate_sitemap, APIException
import jwt
import json
import itertools

import cloudinary
import cloudinary.uploader

api = Blueprint('api', __name__)


@api.route('/login', methods=['POST'])
def login():
    
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if email and password:
        account = Account.get_by_email(email)

        if account and check_password_hash(account._password, password) and account._is_active:
            access_token = create_access_token(identity=account.to_dict(), expires_delta=timedelta(minutes=100))
            return {'token': access_token}, 200

        return jsonify({'error':'Not found'}), 200

    return {'error': 'Some parameter is wrong'}, 401

@api.route('/account/<int:id>', methods=[ 'GET'])
def get_account(id):

  account= Account.get_account_by_id(id)

  if account:
      account= account.to_dict()
      return jsonify(account), 200


@api.route('/account', methods=['POST'])
def create_account(): 
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    username = request.json.get("username", None)
    photo = request.json.get("photo", None)
    is_waterdropper = request.json.get("userType", None)
    sports = request.json.get("sports", None)

    if not (email or password or username or is_waterdropper):
        return {'error': 'Missing info'}, 400

    account = Account.get_by_email(email)
    if account and not account._is_active:
        account.reactive_account(username, photo, is_waterdropper, password)
        return jsonify(account.to_dict()), 200
    
    if is_waterdropper == "waterdropper": 
        is_waterdropper = True
    else:
        is_waterdropper = False
        
    new_account = Account(
        email=email, 
        _is_active=True,
        _password=generate_password_hash(password, method='pbkdf2:sha256', salt_length=16),
        username=username, 
        _is_waterdropper=is_waterdropper
    )
    
    try:
        new_account.create(sports) 
        print("aquiii", new_account)
        if is_waterdropper:
            first_name = request.json.get("firstname", None)
            last_name = request.json.get("lastname", None)
            level = request.json.get("level", None)
            location = request.json.get("location", None)
            
            new_waterdropper = Waterdropper(
                account_id=new_account.id,
                first_name=first_name,
                last_name=last_name,
                level=level,
                location=location
            )
            try:
                new_waterdropper.create_waterdropper()
                token = create_access_token(identity=new_account.to_dict(), expires_delta=timedelta(minutes=100))
                return jsonify({'token': token, 'account': new_account.to_dict()}), 201

            except exc.IntegrityError as err:
                print(f"Unexpected {err=}, {type(err)=}")
                return {'error': 'Something went wrong waterdropper'}, 401
        else:
            address = request.json.get("address", None)
            phone = request.json.get("phone", None)
            web = request.json.get("web", None)
            new_center = Center(
                account_id=new_account.id,
                address=address,
                phone=phone,
                web=web
            )
            print(new_center)
            try:
                new_center.create_center()
                token = create_access_token(identity=new_account.to_dict(), expires_delta=timedelta(minutes=100))
                return jsonify({'token': token, 'account': new_account.to_dict()}), 201

            except exc.IntegrityError as err:
                print(f"Unexpected {err=}, {type(err)=}")
                return {'error': 'Something went wrong center'}, 401
    
    except exc.IntegrityError as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return {'error': 'Something went wrong'}, 401


@api.route('/account/<int:id>', methods=["GET"])
@jwt_required()
def get_account_profile(id):
    account = Account.get_account_by_id(id)

    if account and account._is_active:
        return jsonify({'getaccount': account.to_dict()}), 200
    
    return({"error": "Account not found"}), 404


@api.route('/account/<int:id>', methods = ['PUT', 'PATCH'])
@jwt_required()
def update_account_info(id):
    token_id = get_jwt_identity()
    print("token",token_id)

    if token_id.get("id", None) != id:
        return {'error': 'Invalid action'}, 400

    update_info = {
        'email': request.json.get('email', None),
        'password': request.json.get('password', None),
        'username': request.json.get('username', None),
        'photo': request.json.get('photo', None),
        'sports' : request.json.get("sports", None),
        'is_waterdropper': True if request.json.get('userType', None) == "waterdropper" else False
    }

    account = Account.get_account_by_id(id)
    print("aquiii account", account)
    if account:
            updated_account =  account.update_account(**{
                            key:value for key, value in update_info.items() 
                            if value is not None
                        })
            print("aquiii actualizaaaa", updated_account)

            if updated_account._is_waterdropper: 
                update_info_waterdropper = {
                    'first_name': request.json.get('firstname', None),
                    'last_name': request.json.get('lastname', None),
                    'level': request.json.get('level', None),
                    'location': request.json.get('location', None)
                }
        
                waterdropper = Waterdropper.get_waterdropper_by_account_id(id)
                print("aquiii waterdropper", waterdropper)
                if waterdropper:
                        updated_waterdropper =  waterdropper.update_account_waterdropper(**{
                                        key:value for key, value in update_info_waterdropper.items() 
                                        if value is not None
                                    })
                        print("aquiii actualizaaaa", updated_waterdropper)
                        return jsonify(updated_account.to_dict()), 200
                return {'error': 'Waterdropper not found'}, 400

            else:
                update_info_center = {
                    'address': request.json.get('address', None),
                    'phone': request.json.get('phone', None),
                    'web': request.json.get('web', None)
                }
                
                center = Center.get_center_by_account_id(id)
                print("aquiii center", center)
                if center:
                    updated_center =  center.update_account_center(**{
                                    key:value for key, value in update_info_center.items() 
                                    if value is not None
                                })
                    return jsonify(updated_account.to_dict()), 200
                return {'error': 'Center not found'}, 400

    return {'error': 'Account not found'}, 400


@api.route('/account/<int:id>', methods = ['DELETE'])
@jwt_required()
def update_account_status(id):
    user = get_jwt_identity()

    if user.get('id', None) == id:
        account_inactive = Account.get_account_by_id(id)

        if account_inactive:
            account_inactive.soft_delete()
            return jsonify(account_inactive.to_dict()), 200

        return jsonify({'error' : 'Account not found'}), 404



@api.route('/photo/<int:id>', methods=['POST'])
def handle_upload(id):

    # validate that the front-end request was built correctly
    if 'profile_image' in request.files:
        # upload file to uploadcare
        result = cloudinary.uploader.upload(request.files['profile_image'])

        # fetch for the user
        account1 = Account.get_account_by_id(id)
        # update the user with the given cloudinary image URL
        account1.cover_photo = result['secure_url']

        db.session.add(account1)
        db.session.commit()

        return jsonify(account1.to_dict()), 200
    else:
        raise APIException('Missing profile_image on the FormData')







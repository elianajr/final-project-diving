"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from datetime import timedelta
import json

from flask import Flask, request, jsonify, url_for, Blueprint
from flask_cors import CORS
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from sqlalchemy import exc
from werkzeug.security import check_password_hash, generate_password_hash

from api.models import db, Account, Waterdropper, Center, Hotspot, Specie, Sport
from api.utils import generate_sitemap, APIException

import cloudinary
import cloudinary.uploader

api = Blueprint('api', __name__)


@api.route('/account', methods=[ 'GET'])
def get_accounts():

  accounts= Account.get_all()
  all_accounts=[account.to_dict() for account in accounts]
  return jsonify(all_accounts), 200

@api.route('/centers', methods=[ 'GET'])
def get_centers():

  centers= Center.get_all_centers()
  all_centers=[center.to_dict() for center in centers]
  return jsonify(all_centers), 200


@api.route('/account/<int:id>', methods=[ 'GET'])
def get_account(id):

  account= Account.get_account_by_id(id)

  if account:
      account= account.to_dict()
      return jsonify(account), 200
  
@api.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if email and password:
        account = Account.get_by_email(email)
        if account and not account._is_active:
            account.reactive_account(email, password)
            return jsonify(account.to_dict()), 200

        if account and check_password_hash(account._password, password) and account._is_active:
            access_token = create_access_token(identity=account.to_dict(), expires_delta=timedelta(minutes=100))
            return {'token': access_token}, 200

        return jsonify({'error':'Not found'}), 200

    return {'error': 'Some parameter is wrong'}, 401


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
        account.reactive_account(email, is_waterdropper, password)
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
            name = request.json.get("name", None)
            new_center = Center(
                account_id=new_account.id,
                address=address,
                phone=phone,
                web=web,
                name=name
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
        return jsonify(account.to_dict()), 200
    
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
        # TODO obteber URL de almacenaje de foto y dar valor a la propiedad photo con ella
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
                    'web': request.json.get('web', None),
                    'name': request.json.get('name', None)
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


@api.route('/waterdropper/<int:id_waterdropper>/favourite-centers/<int:id_center>', methods=['POST'])
@jwt_required()
def add_favcenter(id_waterdropper,id_center):
    token_id = get_jwt_identity()
    print("token",token_id)

    if token_id.get("id"):
        waterdropper = Waterdropper.get_waterdropper_by_id(id_waterdropper)
        center = Center.get_center_by_id(id_center)
        print("waterdropper",waterdropper)
        print("center",center)

        if waterdropper and center:
            fav_center = waterdropper.add_fav_center(center)
            print(fav_center)
            fav_centers = [center.to_dict() for center in fav_center]
            return jsonify(fav_centers), 200

    return jsonify({'error': 'Favourite center not found'}), 404


@api.route('/waterdropper/<int:id_waterdropper>/favourite-hotspots/<int:id_hotspot>', methods=['POST'])
@jwt_required()
def add_fav_hotspot(id_waterdropper,id_hotspot):
    token_id = get_jwt_identity()
    print("token",token_id)

    if token_id.get("id"):
        waterdropper = Waterdropper.get_waterdropper_by_id(id_waterdropper)
        hotspot = Hotspot.get_hotspot_by_id(id_hotspot)
        print("waterdropper",waterdropper)
        print("hotspot",hotspot)

        if waterdropper and hotspot:
            fav_hotspot = waterdropper.add_fav_hotspot(hotspot)
            print(fav_hotspot)
            fav_hotspots = [hotspot.to_dict() for hotspot in fav_hotspot]
            return jsonify(fav_hotspots), 200

    return jsonify({'error': 'Favourite hotspot not found'}), 404


@api.route('/account/<int:id_account>/favourite-hotspots/<int:id_hotspot>', methods=['POST'])
@jwt_required()
def add_favhotspot(id_account,id_hotspot):
    token_id = get_jwt_identity()
    print("token",token_id)

    if token_id.get("id"):
        center = Center.get_center_by_account_id(id_account)
        hotspot = Hotspot.get_hotspot_by_id(id_hotspot)
        print("center",center)
        print("hotspot",hotspot)

        if center and hotspot:
            center_hotspot = center.add_center_hotspot(hotspot)
            print(center_hotspot)
            center_hotspots = [hotspot.to_dict() for hotspot in center_hotspot]
            return jsonify(center_hotspots), 200

    return jsonify({'error': 'Center hotspot not found'}), 404


@api.route('/accountphoto/<int:id>', methods=['POST'])
def handle_uploadaccount(id):

    # validate that the front-end request was built correctly
    if 'profile_image' in request.files:
        # upload file to uploadcare
        result = cloudinary.uploader.upload(request.files['profile_image'])

        # fetch for the user
        account1 = Account.get_account_by_id(id)
        # update the user with the given cloudinary image URL
        if account1:
             account1.cover_photo = result['secure_url']
             account1.update_photoaccount()
             return jsonify(account1.to_dict()), 200
             
    else:
        raise APIException('Missing profile_image on the FormData')

@api.route('/hotspotphoto/<int:id>', methods=['POST'])
def handle_uploadhotspot(id):

    # validate that the front-end request was built correctly
    if 'media' in request.files:
        # upload file to uploadcare
        result = cloudinary.uploader.upload(request.files['media'])

        # fetch for the user
        hotspot1 = Hotspot.get_hotspot_by_id(id)
        # update the user with the given cloudinary image URL
        hotspot1.photo = result['secure_url']

        hotspot1.update_photohotspot()

        return jsonify(hotspot1.to_dict()), 200
    else:
        raise APIException('Missing profile_image on the FormData')



@api.route('/speciephoto/<int:id>', methods=['POST'])
def handle_uploadspecie(id):

    # validate that the front-end request was built correctly
    if 'profile_image' in request.files:
        # upload file to uploadcare
        result = cloudinary.uploader.upload(request.files['profile_image'])

        # fetch for the user
        specie1 = Specie.get_specie_by_id(id)
        # update the user with the given cloudinary image URL
        specie1.photo = result['secure_url']

        db.session.add(specie1)
        db.session.commit()

        return jsonify(specie1.to_dict()), 200
    else:
        raise APIException('Missing profile_image on the FormData')
    return jsonify({'message':'Hotspot not found'}), 400
  
@api.route('/hotspots/', methods=['GET'])
def get_all_hotpot_by_id():
    hotspot_s = Hotspot.get_all()

    if hotspot_s:
        all_hotspots = [hotspot.to_dict() for hotspot in hotspot_s]
        return jsonify(all_hotspots), 200
      

@api.route('/hotspots', methods=['POST'])
def post_hotspot():
    
    name = request.json.get('name', None)
    photo = request.json.get('photo', None)
    level = request.json.get('level', None)
    description = request.json.get('description', None)
    latitude = request.json.get('latitude', None)
    longitude = request.json.get('longitude', None)
    account_id = request.json.get('account_id', None)
    sport_id = request.json.get('sport_id', None)

    if not latitude or not longitude:
        return jsonify({'error':'Not location'}), 400

    new_hotspot = Hotspot(
        longitude=longitude,
        latitude=latitude,
        name=name,
        level=level,
        description=description,
        account_id=account_id,
        photo=photo,
        sport_id=sport_id
    )
   
    try:
        new_hotspot.create()
        print("back new hotspot",new_hotspot)
    except exc.IntegrityError as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return {'error': 'Something went wrong waterdropper'}, 400
    return jsonify(new_hotspot.to_dict()), 200

@api.route('/search', methods=['POST'])
def get_hotspot_byname():

    name= request.json.get('name',None)
    if name:
        hotspots = Hotspot.query.filter(Hotspot.name.ilike('%' + name + '%'))

        hotspots = hotspots.order_by(Hotspot.name).all()
        hotspots_searched= [hotspot.to_dict() for hotspot in hotspots]
        return jsonify(hotspots_searched)
    else:
        return jsonify({'response':[]})
@api.route('/hotspots/<int:id>', methods=['GET'])
def get_hotpot_id(id):
    hotspot = Hotspot.get_hotspot_by_id(id)

    if hotspot:
        return jsonify(hotspot.to_dict()), 200
    return({"error": "hotspot not found"}), 404

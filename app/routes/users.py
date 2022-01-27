from flask import Blueprint, request, jsonify, make_response, abort
from app import db
import app.validate_requests  as validate
from flask_cors import cross_origin
from datetime import datetime

from app.models.user import User
from app.models.package import Package

from auth.auth import AuthError, requires_auth



users_bp = Blueprint("user", __name__, url_prefix="/users")



@users_bp.errorhandler(AuthError)
def auth_error(error):
    response = jsonify(error.error)
    response.status_code = error.status_code
    return response


@users_bp.route("", methods=["POST"],strict_slashes=False)
@requires_auth("create:user")
def add_user(jwt):
    request_body = request.get_json()
    try:
        new_user= User(
            name=request_body["name"],
            unit=request_body["unit"],
            phone_number=request_body["phone_number"],
            email=request_body["email"]
        )
        db.session.add(new_user)
        db.session.commit()

        return new_user.to_dict(), 201

    except KeyError:
        return make_response(validate.missing_fields(request_body, User), 400)


@users_bp.route("/<id>", methods=["DELETE"])
@requires_auth("delete:user")
def delete_user(id):
    user_id = validate.valid_id(id)
    user = validate.valid_model(user_id, User)

    db.session.delete(user)
    db.session.commit()
    response_body = {"details": f"User {user.id} name: {user.name} unit: {user.unit} successfully deleted"}
    return make_response(response_body), 200

# permission - staff
# 
@users_bp.route("/<id>", methods=["GET"])
@requires_auth("read:users")
def get_user(jwt,id):

    user_id = validate.valid_id(id)
    user = validate.valid_model(user_id, User)

    return user.to_dict()


# ADD PERMISSIONS  -> staff
@users_bp.route("", methods=["GET"])
@requires_auth('read:users')
def get_all_users(jwt):

    users = User.query.all()
    return jsonify([user.to_dict() for user in users])


# ADD PERMISSIONS -> staff and user 
@users_bp.route("/<id>", methods=["PATCH"])
def update_user_info(id):

    user_id = validate.valid_id(id)
    user = validate.valid_model(user_id, User)
    request_body = request.get_json()
    validate_input = validate.check_request_body(request_body, User)
        
    if validate_input !=False:
        return make_response(validate_input,400)

    name = request_body.get('name', None)
    email = request_body.get('email', None)
    unit = request_body.get('unit', None)
    phone_number = request_body.get('phone_number', None)
    
    if name:
        user.name = request_body["name"]
    if email:
        user.email = request_body["email"]
    if unit:
        user.unit = request_body["unit"]
    if phone_number:
        user.phone_number = request_body["phone_number"]
    
    db.session.commit()

    return user.to_dict(), 201



# If package was requested == True else False
# user and manager have access to patch status
@users_bp.route("/<id>/status", methods=["PATCH"])
def update_statuts(id):

    user_id = validate.valid_id(id)
    user = validate.valid_model(user_id, User)
    request_body = request.get_json()

    try:
        user.status = request_body["status"]
        db.session.commit()
        return user.to_dict(), 201

    except KeyError:

        return make_response(validate.missing_fields(request_body, User), 400)


# An user got a package 
# permissions -> staff
@users_bp.route("/<id>/packages", methods=["POST"])
def add_new_package(id):

    user_id = validate.valid_id(id)
    request_body = request.get_json()

    try:
        new_card = Package(
            user_id=user_id,
            description=request_body["description"],
            service_provider=request_body["service_provider"]
        )
        db.session.add(new_card)
        db.session.commit()

        return new_card.to_dict(), 201

    except KeyError:

        return make_response(validate.missing_fields(request_body,Package), 400)

# get all packages related to a user 
@users_bp.route("/<id>/packages", methods=["GET"])
def get_packages_by_user_id(id):

    user_id = validate.valid_id(id)
    validate.valid_model(user_id, User)
    packages = Package.query.filter_by(user_id=user_id).all()

    return jsonify([package.to_dict() for package in packages])


@users_bp.route("/<id>/packages-not-delivered", methods=["GET"])
def get_packages_to_be_delivered(id):

    user_id = validate.valid_id(id)
    validate.valid_model(user_id, User)
    sort_packages = request.args.get("sort")
    
    response_body = []

    if sort_packages == "asc":
        packages = Package.query.order_by(Package.arrived_at.asc())

    elif sort_packages == "desc":
        packages = Package.query.order_by(Package.arrived_at.desc())

    else:
        packages = Package.query.filter_by(user_id=user_id).all()
    
    for package in packages:
        if package.delivery_date == None and package.user_id == user_id:
            response_body.append(package.to_dict())   


    return make_response(jsonify(response_body),200)

# Get all packages and user that required delivery

@users_bp.route("/delivery-requests", methods=["GET"])
def get_requests():

    all_users = User.query.filter_by(status=True).all()
    users= [user.to_dict() for user in all_users]
    result  = []

    for user in users:
        # print(user)
        packages = Package.query.filter_by(delivery_date=None, user_id=user["user_id"] ).all()
        value = {"name": user["name"],
                "id": user["user_id"],
                "unit": user["unit"],
                "packages": [package.to_dict() for package in packages]} 
    
        result.append(value)

    return make_response(jsonify(result),200)



# get all packages delivere -> user and staff
@users_bp.route("/<id>/packages-delivered", methods=["GET"])
def get_all_delivered_packages(id):

    user_id = validate.valid_id(id)
    validate.valid_model(user_id, User)
    packages = Package.query.filter_by(user_id=user_id).all()

    return jsonify([package.to_dict() for package in packages if package.delivery_date])



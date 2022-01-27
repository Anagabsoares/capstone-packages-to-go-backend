from flask import Blueprint, request, jsonify, make_response
from app import db
from datetime import datetime
import app.validate_requests  as validate

from app.models.package import Package
from app.models.user import User

# from auth.auth import AuthError, requires_auth


packages_bp = Blueprint("packages", __name__, url_prefix="/packages")


# get all packages from database 
# staff
@packages_bp.route("", methods=["GET"])
def get_all_packages():

    packages= Package.query.all()
    packages_list = [package.to_dict() for package in packages]
    return make_response(jsonify(packages_list))


@packages_bp.route("/<id>", methods=["GET"])
def get_package(id):

    package_id = validate.valid_id(id)
    package = validate.valid_model(package_id, User)

    return package.to_dict()


# permission -> staff/ Only if was incorrect data !

@packages_bp.route("/<id>", methods=["DELETE"])
def delete_package(id):
    package_id = validate.valid_id(id)
    package = validate.valid_model(package_id, Package)

    db.session.delete(package)
    db.session.commit()
    response_body = {"details": f"User {package.id} provider: {package.service_provider} successfully deleted"}
    return make_response(response_body), 200


# mark a package as delivered
# staff
@packages_bp.route("/<id>/mark-as-delivered", methods=["PATCH"])
def update_package_delivery(id):

    package_id = validate.valid_id(id)
    package = validate.valid_model(package_id, Package)

    if not package.delivery_date:
        package.delivery_date = datetime.utcnow()
    
        db.session.commit()
        response_body = package.to_dict()
        return make_response(response_body,200)
    else:
        return make_response('This package has already been delivered',200)

# staff
@packages_bp.route("/<id>", methods=["PATCH"])
def update_user_info(id):

    package_id = validate.valid_id(id)
    package = validate.valid_model(package_id, Package)
    request_body = request.get_json()
    validate_input = validate.check_request_body(request_body, Package)
        
    if validate_input !=False:
        return make_response(validate_input,400)

    user_id = request_body.get('user_id', None)
    service_provider = request_body.get('service_provider', None)
    description = request_body.get('description', None)
    
    if user_id:
        id_user = validate.valid_id(user_id)
        validate.valid_model(id_user, User)
        package.user_id = request_body["user_id"]
    if service_provider:
        package.service_provider= request_body["service_provider"]
    if description:
        package.unit = request_body["description"]

    db.session.commit()

    return make_response(package.to_dict(),201)
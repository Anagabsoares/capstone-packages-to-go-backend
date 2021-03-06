from flask import Blueprint, request, jsonify, make_response
from app import db
from datetime import datetime
import app.validate_requests  as validate

from app.models.package import Package
from app.models.user import User

from auth.auth import AuthError, requires_auth


packages_bp = Blueprint("packages", __name__, url_prefix="/packages")


@packages_bp.errorhandler(AuthError)
def auth_error(error):
    response = jsonify(error.error)
    response.status_code = error.status_code
    return response

@packages_bp.route("", methods=["GET"])
@requires_auth("read:package")
def get_all_packages(jwt):

    packages= Package.query.all()
    packages_list = [package.to_dict() for package in packages]
    return make_response(jsonify(packages_list)), 200


@packages_bp.route("/<id>", methods=["GET"])
@requires_auth("read:packages")
def get_package(jwt,id):

    package_id = validate.valid_id(id)
    package = validate.valid_model(package_id, Package)

    return make_response(package.to_dict()), 200


@packages_bp.route("/<id>", methods=["DELETE"])
@requires_auth("delete:package")
def delete_package(jwt,id):
    package_id = validate.valid_id(id)
    package = validate.valid_model(package_id, Package)

    db.session.delete(package)
    db.session.commit()
    response_body = {"details": f"User {package.id} provider: {package.service_provider} successfully deleted"}
    return make_response(response_body), 200

@packages_bp.route("/<id>/status", methods=["PATCH"])
@requires_auth('update:request-status')
def update_status(jwt,id):

    package_id = validate.valid_id(id)
    package = validate.valid_model(package_id, Package)
    request_body = request.get_json()

    try:
        package.status = request_body["status"]
        db.session.commit()
        return package.to_dict(), 201

    except KeyError:

        return make_response(validate.missing_fields(request_body, User), 400)


@packages_bp.route("/<id>/mark-as-delivered", methods=["PATCH"])
@requires_auth("update:delivery-status")
def update_package_delivery(jwt,id):

    package_id = validate.valid_id(id)
    package = validate.valid_model(package_id, Package)

    if not package.delivery_date:
        package.delivery_date = datetime.now()

        db.session.commit()
        response_body = package.to_dict()
        return make_response(response_body), 200
    else:
        return make_response('This package has already been delivered'), 200


@packages_bp.route("/<id>", methods=["PATCH"])
@requires_auth("update:packages")
def update_user_info(jwt,id):

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

    return make_response(package.to_dict()),200
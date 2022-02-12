from flask import Blueprint, request, jsonify, make_response, abort
from app import db
import app.validate_requests  as validate
from datetime import datetime

from app.models.notification import Notification

from auth.auth import AuthError, requires_auth


notifications_bp = Blueprint("notification", __name__, url_prefix="/notifications")


@notifications_bp.errorhandler(AuthError)
def auth_error(error):
    response = jsonify(error.error)
    response.status_code = error.status_code
    return response

# admin 
@notifications_bp.route("", methods=["POST"],strict_slashes=False)
@requires_auth("create:notification")
def add_notification(jwt):


    request_body = request.get_json()
    try:
        new_noti= Notification(
            notification_id=request_body["notification_id"],
            entity_type=request_body["entity_type"],
            description=request_body["description"],
            status=request_body["status"]
        )
        db.session.add(new_noti)
        db.session.commit()

        return new_noti.to_dict(), 201

    except KeyError:
        return make_response(validate.missing_fields(request_body, Notification), 400)


@notifications_bp.route("/<id>", methods=["DELETE"])
@requires_auth("delete:notification")
def delete_notification(jwt,id):
    notification_id = validate.valid_id(id)
    notification = validate.valid_model(notification_id, notification)

    db.session.delete(notification)
    db.session.commit()
    response_body = {"details": f"notification {notification.id}  successfully deleted"}
    return make_response(response_body), 200


@notifications_bp.route("/<id>", methods=["GET"])
@requires_auth("read:notification")
def get_notification(jwt,id):

    notification_id = validate.valid_id(id)
    notification = validate.valid_model(notification_id, Notification)

    return notification.to_dict()


@notifications_bp.route("", methods=["GET"])
@requires_auth('read:notifications')
def get_all_notifications(jwt):

    notifications = Notification.query.all()
    return jsonify([notification.to_dict() for notification in notifications])

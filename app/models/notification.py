from app import db
from datetime import datetime, timezone


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship('User', back_populates="notifications", lazy=True)
    entity_type = db.Column(db.Integer,)
    description = db.Column(db.String(100), nullable=True)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.now)
    is_read = db.Column(db.Boolean, default=False)
    status = db.Column(db.Integer, default=False)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "entity_type": self.entity_typeid,
            "description": self.description,
            "created_on": self.created_on,
            "id": self.id,
            "status": self.status,
            "is_read":self.is_read,
        }


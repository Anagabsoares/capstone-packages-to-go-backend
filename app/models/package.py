from app import db
from datetime import datetime, timezone


class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship('User', back_populates="packages", lazy=True)
    description = db.Column(db.String(100), nullable=False)
    service_provider = db.Column(db.String(100), nullable=False)
    arrived_at = db.Column(db.DateTime(timezone=False), nullable=False, default=datetime.utcnow)
    delivery_date = db.Column(db.DateTime(timezone=True), nullable=True)
    status = db.Column(db.Boolean, default=False)
    required_fields = ["user_id", "service_provider", "description"]

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "packages_id": self.id,
            "description": self.description,
            "delivery_date":self.delivery_date if self.delivery_date else "pending",
            "arrived_at":self.arrived_at,
            "service_provider": self.service_provider,
            "status": "requested" if self.status else "false",

        }






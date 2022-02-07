from app import db
from datetime import datetime, timezone


class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship('User', back_populates="packages", lazy=True)
    description = db.Column(db.String(100), nullable=True)
    service_provider = db.Column(db.String(100), nullable=False)
    delivery_date = db.Column(db.DateTime, nullable=True)
    arrived_at = db.Column(db.Date, nullable=False, default=datetime.now)
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
            "status": self.status,
        }






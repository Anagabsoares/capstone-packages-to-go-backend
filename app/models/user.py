from app import db


class  User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    packages = db.relationship("Package", back_populates="user", lazy=True)
    name = db.Column(db.String(50), nullable=False)
    email= db.Column(db.String(64), nullable=True)
    phone_number = db.Column(db.String(100), nullable=True)
    unit = db.Column(db.String(10), nullable=False)
    required_fields = ["name", "unit", "email", "phone_number"]
    
    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "phone_number": self.phone_number,
            "user_id": self.id,
            "unit":self.unit,
            }

            

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

clientfavcenter = db.Table('clientfavcenter',
    db.Column('client_id', db.Integer, db.ForeignKey('client.id'), primary_key=True),
    db.Column('center_id', db.Integer, db.ForeignKey('center.id'), primary_key=True)
)


clientfavspot = db.Table('clientfavspot',
    db.Column('client_id', db.Integer, db.ForeignKey('client.id'), primary_key=True),
    db.Column('hotspot_id', db.Integer, db.ForeignKey('hotspot.id'), primary_key=True)
)


reviewspot = db.Table('reviewspot',
    db.Column('client_id', db.Integer, db.ForeignKey('client.id'), primary_key=True),
    db.Column('hotspot_id', db.Integer, db.ForeignKey('hotspot.id'), primary_key=True)
)


reviewcenter = db.Table('reviewcenter',
    db.Column('client_id', db.Integer, db.ForeignKey('client.id'), primary_key=True),
    db.Column('center_id', db.Integer, db.ForeignKey('center.id'), primary_key=True)
)


clientsport = db.Table('clientsport',
    db.Column('client_id', db.Integer, db.ForeignKey('client.id'), primary_key=True),
    db.Column('sport_id', db.Integer, db.ForeignKey('sport.id'), primary_key=True)
)


centersport = db.Table('centersport',
    db.Column('center_id', db.Integer, db.ForeignKey('center.id'), primary_key=True),
    db.Column('sport_id', db.Integer, db.ForeignKey('sport.id'), primary_key=True)
)



class Client(db.Model):
    __tablename__: "client"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password = db.Column(db.String(120), unique=False, nullable=False)
    clientname = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), unique=False, nullable=False)
    sport_id = db.Column(db.Integer, db.ForeignKey("sport.id"), nullable=False)
    location = db.Column(db.String(120), unique=False, nullable=False)
    chat_id = db.Column(db.Integer, db.ForeignKey("chat.id"), nullable=False)
    photo = db.Column(db.String(120), unique=False, nullable=True)
    _is_active = db.Column(db.Boolean(), unique=False, nullable=False, default=True)
    _is_waterdropper = db.Column(db.Boolean(), unique=False, nullable=False, default=True)
    _is_center = db.Column(db.Boolean(), unique=False, nullable=False, default=True)

    has_waterdropper = db.relationship('Waterdropper')
    has_center = db.relationship('Center')

    have_client_favcenter = db.relationship('Center', secondary=clientfavcenter, back_populates="have_favcenter_client")
    have_client_favspot = db.relationship('Hotspot', secondary=clientfavspot, back_populates="have_favspot_client")
    have_client_revcenter = db.relationship('Center', secondary=reviewcenter, back_populates="have_revcenter_client")
    have_client_revspot = db.relationship('Hotspot', secondary=reviewspot, back_populates="have_revspot_client")
    have_client_sport = db.relationship('Sport', secondary=clientsport, back_populates="have_sport_client")
    
    # has_chat = db.relationship("Chatassociation", back_populates="chat_has")


    def __repr__(self):
        return f'Client {self.email}, id: {self.id}, clientname: {self.clientname}, name: {self.name}, sport_id: {self.sport_id}, level: {self.level}, location: {self.location}, photo: {self.photo}, chat_id: {self.chat_id}' 

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "clientname": self.clientname, 
            "name": self.name, 
            "sport_id": self.sport_id, 
            "level": self.level, 
            "location": self.location, 
            "chat_id": self.chat_id,
            "photo": self.photo,
            "waterdropper": [waterdropper.to_dict() for waterdropper in has_waterdropper],
            "center": [center.to_dict() for center in has_center]
        }

class Waterdropper(db.Model):
    __tablename__: "waterdropper"

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(120), unique=False, nullable=False)
    level = db.Column(db.String(120), unique=False, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"), nullable=False)

    def __repr__(self):
        return f'Waterdropper is role: {self.role}, level: {self.level}' 

    def to_dict(self):
        return {
            "id": self.id,
            "role": self.role,
            "level": self.level
        }


class Center(db.Model):
    __tablename__: "center"

    id = db.Column(db.Integer, primary_key=True)
    levelto = db.Column(db.String(120), unique=False, nullable=True)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"), nullable=False)

    have_favcenter_client = db.relationship('Client', secondary=clientfavcenter, back_populates="have_client_favcenter")
    have_revcenter_client = db.relationship('Client', secondary=reviewcenter, back_populates="have_client_revcenter")
    have_center_sport = db.relationship('Sport', secondary=centersport, back_populates="have_sport_center") 
    
    def __repr__(self):
        return f'Center is level: {self.level}' 

    def to_dict(self):
        return {
            "id": self.id,
            "level": self.level
        }


class Hotspot(db.Model):
    __tablename__: "hotstop"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    photo = db.Column(db.String(120), unique=False, nullable=False)
    location = db.Column(db.String(120), unique=False, nullable=False)
    sport_id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String(120), unique=False, nullable=True)
    specie_id = db.Column(db.Integer, db.ForeignKey("specie.id"), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"), nullable=False)

    have_favspot_client = db.relationship('Client', secondary=clientfavspot, back_populates="have_client_favspot")
    have_revspot_client = db.relationship('Client', secondary=reviewspot, back_populates="have_client_revspot")

    def __repr__(self):
        return f'Hotstop {self.id}, name: {self.name}, sport: {self.sport}, levelto: {self.levelto}, location: {self.location}, photo: {self.photo}' 

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "photo": self.photo, 
            "location": self.location, 
            "sport_id": self.sport_id, 
            "level": self.level, 
            "species_id": self.species_id, 
            "client_id": self.client_id
        }


class Specie(db.Model):
    __tablename__: "specie"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    photo = db.Column(db.String(120), unique=False, nullable=False)
    description = db.Column(db.String(120), unique=False, nullable=False)
    location = db.Column(db.String(120), unique=False, nullable=False)
    is_reported = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return f'Specie {self.id}, name: {self.name}, photo: {self.photo}, description: {self.description}, location: {self.location}, is_reported: {self.is_reported}' 

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "photo": self.photo, 
            "description": self.description, 
            "location": self.location, 
            "is_reported": self.is_reported 
        }


class Sport(db.Model):
    __tablename__: "sport"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)

    have_sport_client = db.relationship('Client', secondary=clientsport, back_populates="have_client_sport")
    have_sport_center = db.relationship('Center', secondary=centersport, back_populates="have_center_sport")

    def __repr__(self):
        return f'Sport {self.id}, name: {self.name}' 

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }


class Chat(db.Model):
    __tablename__: "chat"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)

    # has_client = db.relationship("Chatassociation", back_populates="client_has")
    
    def __repr__(self):
        return f'Chat {self.id}, name: {self.name}' 

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }


# class Chatassociation(db.Model):
#     __tablename__ = "chatassociation"

#     id = db.Column(db.Integer, primary_key=True)
#     client_id = db.Column(db.Integer, db.ForeignKey("client.id"), primary_key=True)
#     chat_id = db.Column(db.Integer, db.ForeignKey("chat.id"), primary_key=True)
#     message = db.Column(db.String(120), unique=False, nullable=False)
#     date = db.Column(db.DateTime(timezone=False))

#     chat_has = db.relationship("Chat", back_populates="has_chat")
#     client_has = db.relationship("Client", back_populates="has_client")

#     def __repr__(self):
#         return f'Chatassociation {self.id}, client_id: {self.client_id}, chat_id: {self.chat_id}, message: {self.message}, date: {self.date}' 

#     def to_dict(self):
#         return {
#             "id": self.id,
#             "client_id": self.client_id,
#             "chat_id": self.chat_id,
#             "message": self.message, 
#             "date": self.date
#         }



class News(db.Model):
    __tablename__: "news"

    id = db.Column(db.Integer, primary_key=True)
    
    def __repr__(self):
        return f'New {self.id}' 

    def to_dict(self):
        return {
            "id": self.id
        }
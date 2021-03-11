from ..utils.sql import db


class Audio(db.Model):
    __tablename__ = 'audio'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), index=True)
    artist = db.Column(db.String(32), index=True)
    img = db.Column(db.String(32), index=True)
    duration = db.Column(db.Integer)


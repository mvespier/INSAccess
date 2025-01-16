from flask_login import UserMixin
from sqlalchemy.sql import func
from . import db
import enum

class User(UserMixin, db.Model):
    """User definition, inherit from UserMixin for authentication"""
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    # user information
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255),nullable=False)
    name = db.Column(db.String(100))
    # admin field
    admin = db.Column(db.Boolean, default=False)
    # incremental user id - used for authentication
    seqid = db.Column(db.Integer, default=0)

    



# class cours (idcours, desc, dateD, dateF, groupeTD, Prof, Salle)

#classe cours/groupeTD (idCours, TD)

# class eleve(cleeUser, depart,annee , groupeTD, langue, ECAOplusieurs?,( filiaire, trucfalcutatif ) ) 

# DEPART&ANNEE&SEMESTRE-NOMCOURS-TD/TP-XX
# DEPART&ANNEE&SEMESTRE-TP/TD-XX
# DEPART&ANNEE&SEMESTRE-TD/TPX-X
# Nom de depart pas forcement correlee a nom request (ex : GC =/ GCU)
# PLUSIEURS NOM POSSIBLE PAR DEPART PERFISP ING PERF

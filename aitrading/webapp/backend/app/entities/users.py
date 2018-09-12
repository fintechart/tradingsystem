# coding=utf-8

import os
import datetime
import jwt
import bcrypt
from marshmallow import Schema, fields
from sqlalchemy import Column, String, Boolean
from .entity import Entity, Base, Session

class User(Entity, Base):
  __tablename__ = "users"

  email = Column(String(255), unique=True, nullable=False)
  password = Column(String(255), nullable=False)
  admin = Column(Boolean, nullable=False, default=False)

  def __init__(self, email, password, admin=False,created_by="register"):
    Entity.__init__(self, created_by)
    self.email = email
    self.password = bcrypt.hashpw(
      password.encode(), bcrypt.gensalt() )
    self.admin = admin

  @staticmethod
  def check_password_hash(userPasswd, inputPasswd):
    return bcrypt.checkpw(inputPasswd.encode(),userPasswd.encode())

  @staticmethod
  def encode_auth_token(user_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
      payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=500),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
        }
      return jwt.encode(
                payload,
                os.getenv('SECRET_KEY','neverguess'),
                algorithm='HS256' )
    except Exception as e:
      return e

  @staticmethod
  def decode_auth_token(auth_token):
    """
    Validates the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
      payload = jwt.decode(auth_token, os.getenv('SECRET_KEY','neverguess'))
      is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
      if is_blacklisted_token:
        return 'Token blacklisted. Please log in again.'
      else:
        return payload['sub']
    except jwt.ExpiredSignatureError:
      return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
      return 'Invalid token. Please log in again.'


class BlacklistToken(Entity,Base):
  """
  Token Model for storing JWT tokens
  """
  __tablename__ = 'blacklist_tokens'

  token = Column(String(500), unique=True, nullable=False)

  def __init__(self, token, created_by="Blocker"):
    Entity.__init__(self, created_by)
    self.token = token

  def __repr__(self):
    return '<id: token: {}'.format(self.token)

  @staticmethod
  def check_blacklist(auth_token):
    # check whether auth token has been blacklisted
    session=Session()
    res = session.query(BlacklistToken).filter_by(token=str(auth_token)).first()
    session.close()
    if res:
      return True
    else:
      return False

class UserSchema(Schema):
    id = fields.Number()
    email = fields.Str()
    password = fields.Str()
    admin = fields.Boolean()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    last_updated_by = fields.Str()


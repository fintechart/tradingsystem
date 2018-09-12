# encoding=utf-8

from flask import request,jsonify
from app import app
from ..entities.entity import Session
from ..entities.users import User,UserSchema,BlacklistToken 

@app.route('/auth/register', methods=['POST'])
def register():
  # get the post data
  pUser = UserSchema(only=('email', 'password')).load(request.get_json())
  u = User(**pUser.data) 
  # check if user already exists
  session = Session()
  user = session.query(User).filter_by(email=u.email).first()
  session.close()
  if not user:
    try:
      # insert the user
      session = Session()
      session.add(u)
      session.commit()
      # generate the auth token
      auth_token = User.encode_auth_token(u.id)
      responseObject = {
        'status': 'success',
        'message': 'Successfully registered.',
        'auth_token': auth_token.decode()
      }
      session.close()
      return jsonify(responseObject), 201
    except Exception as e:
      responseObject = {
        'status': 'fail',
        'message': 'Some error occurred. Please try again.'
      }
      return jsonify(responseObject), 401
  else:
    responseObject = {
      'status': 'fail',
      'message': 'User already exists. Please Log in.',
    }
    return jsonify(responseObject), 202

@app.route('/auth/login', methods=['POST'])
def login():
  # get the post data
  pData = request.get_json()
  em = pData.get('email')
  pw = pData.get('password')
  try:
    # fetch the user data
    session = Session()
    user = session.query(User).filter_by(email=em).first()
    session.close()
    if user and User.check_password_hash(user.password, pw):
      auth_token = User.encode_auth_token(user.id)
      if auth_token:
        responseObject = {
          'status': 'success',
          'message': 'Successfully logged in.',
          'auth_token': auth_token.decode()
        }
        return jsonify(responseObject), 200
    else:
      responseObject = {
        'status': 'fail',
         'message': 'User or password error.'
      }
      return jsonify(responseObject), 404
  except Exception as e:
    responseObject = {
      'status': 'fail',
      'message': 'Try again'
    }
    return jsonify(responseObject), 500


@app.route('/auth/status', methods=['GET'])
def status():
  # get the auth token
  auth_header = request.headers.get('Authorization')
  if auth_header:
    try:
      auth_token = auth_header.split(" ")[1]
    except IndexError:
      responseObject = {
        'status': 'fail',
        'message': 'Bearer token malformed.'
      }
      return jsonify(responseObject), 401
  else:
    auth_token = ''
  if auth_token:
    resp = User.decode_auth_token(auth_token)
    if not isinstance(resp, str):
      session = Session()
      user = session.query(User).filter_by(id=resp).first()
      responseObject = {
        'status': 'success',
        'data': {
           'user_id': user.id,
           'email': user.email,
           'admin': user.admin,
           'created_at': user.created_at
        }
      }
      return jsonify(responseObject), 200
    responseObject = {
      'status': 'fail',
      'message': resp
    }
    return jsonify(responseObject), 401
  else:
    responseObject = {
      'status': 'fail',
      'message': 'Provide a valid auth token.'
    }
    return jsonify(responseObject), 401


@app.route('/auth/logout', methods=['POST','GET'])
def logout():
  # get auth token
  auth_header = request.headers.get('Authorization')
  if auth_header:
    auth_token = auth_header.split(" ")[1]
  else:
    auth_token = ''
  if auth_token:
    resp = User.decode_auth_token(auth_token)
    if not isinstance(resp, str):
      # mark the token as blacklisted
      blacklist_token = BlacklistToken(token=auth_token)
      try:
        # insert the token
        session = Session()
        session.add(blacklist_token)
        session.commit()
        session.close()
        responseObject = {
          'status': 'success',
          'message': 'Successfully logged out.'
        }
        return jsonify(responseObject), 200
      except Exception as e:
        responseObject = {
          'status': 'fail',
          'message': e
        }
        return jsonify(responseObject), 200
    else:
      responseObject = {
        'status': 'fail',
        'message': resp
      }
      return jsonify(responseObject), 401
  else:
    responseObject = {
      'status': 'fail',
      'message': 'Provide a valid auth token.'
    }
    return jsonify(responseObject), 403


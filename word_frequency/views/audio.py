from flask import Blueprint, request, make_response, jsonify, abort, url_for, g
from ..utils.sql import db
from ..model.audio import Audio
from flask_cors import cross_origin
au = Blueprint('au', __name__)



# @au.route('/api/login', methods=['POST'])
# @cross_origin(supports_credentials=True)  # 跨域
# def get_audio():
#     audios = Audio.query
#     return jsonify({'audio': Audio})




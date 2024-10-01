from flask import Blueprint, request, jsonify
from models.music import Music
from routes.auth import token_required

bp = Blueprint('songs', __name__, url_prefix='/songs')

@bp.route('/artist/<int:artist_id>', methods=['GET', 'POST'])
@token_required
def song_list(current_user, artist_id):
    if request.method == 'GET':
        if current_user.role not in ['super_admin', 'artist_manager', 'artist']:
            return jsonify({'message': 'Unauthorized'}), 403
        page = request.args.get('page', 1, type=int)
        songs = Music.get_all_by_artist(artist_id, page=page)
        return jsonify([song.to_dict() for song in songs])
    
    elif request.method == 'POST':
        if current_user.role != 'artist':
            return jsonify({'message': 'Unauthorized'}), 403
        
        data = request.get_json()
        
        if 'title' not in data or not data['title']:
            return jsonify({'message': 'Title is required'}), 400

        Music.create(artist_id, data['title'], data.get('album_name'), data.get('genre'))
        return jsonify({'message': 'Song created successfully'}), 201

@bp.route('/<int:song_id>', methods=['GET', 'PUT', 'DELETE'])
@token_required
def song_operations(current_user, song_id):
    if request.method == 'GET':
        if current_user.role not in ['super_admin', 'artist_manager', 'artist']:
            return jsonify({'message': 'Unauthorized'}), 403
        song = Music.get_by_id(song_id)
        return jsonify(song.to_dict()) if song else jsonify({'message': 'Song not found'}), 404
    
    elif request.method in ['PUT', 'DELETE']:
        if current_user.role != 'artist':
            return jsonify({'message': 'Unauthorized'}), 403
        
        song = Music.get_by_id(song_id)
        if not song:
            return jsonify({'message': 'Song not found'}), 404
        
        if request.method == 'PUT':
            data = request.get_json()
            song.title = data.get('title', song.title)
            song.album_name = data.get('album_name', song.album_name)
            song.genre = data.get('genre', song.genre)
            song.update()
            return jsonify({'message': 'Song updated successfully'})
        
        elif request.method == 'DELETE':
            Music.delete(song_id)
            return jsonify({'message': 'Song deleted successfully'})

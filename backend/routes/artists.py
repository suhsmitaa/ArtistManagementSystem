from flask import Blueprint, request, jsonify, send_file, g
from models.artist import Artist
from models.music import Music
import csv
import io

bp = Blueprint('artists', __name__, url_prefix='/artists')


def get_current_user():
    return g.user if hasattr(g, 'user') else None


@bp.route('/', methods=['GET'])
def artist_list():
    current_user = get_current_user()
    if not current_user or current_user.role not in ['super_admin', 'artist_manager']:
        return jsonify({'message': 'Unauthorized'}), 403

    page = request.args.get('page', 1, type=int)
    artists = Artist.get_all(page=page)
    return jsonify([artist.to_dict() for artist in artists]), 200


@bp.route('/', methods=['POST'])
def create_artist():
    current_user = get_current_user()
    if not current_user or current_user.role != 'artist_manager':
        return jsonify({'message': 'Unauthorized'}), 403

    data = request.get_json()
    required_fields = ['name', 'first_release_year', 'no_of_albums_released']

   
    if not all(field in data for field in required_fields):
        return jsonify({'message': f'Missing required fields: {", ".join(required_fields)}'}), 400

    Artist.create(
        name=data['name'],
        dob=data.get('dob'),
        gender=data.get('gender'),
        address=data.get('address'),
        first_release_year=data['first_release_year'],
        no_of_albums_released=data['no_of_albums_released']
    )
    return jsonify({'message': 'Artist created successfully'}), 201

# Artist operations: Retrieve, Update, Delete
@bp.route('/<int:artist_id>', methods=['GET', 'PUT', 'DELETE'])
def artist_operations(artist_id):
    current_user = get_current_user()
    if not current_user or current_user.role not in ['super_admin', 'artist_manager']:
        return jsonify({'message': 'Unauthorized'}), 403

    artist = Artist.get_by_id(artist_id)

    if request.method == 'GET':
        if not artist:
            return jsonify({'message': 'Artist not found'}), 404
        return jsonify(artist.to_dict()), 200

    elif request.method == 'PUT':
        if current_user.role != 'artist_manager':
            return jsonify({'message': 'Unauthorized'}), 403

        if not artist:
            return jsonify({'message': 'Artist not found'}), 404

        data = request.get_json()
        artist.name = data.get('name', artist.name)
        artist.dob = data.get('dob', artist.dob)
        artist.gender = data.get('gender', artist.gender)
        artist.address = data.get('address', artist.address)
        artist.first_release_year = data.get('first_release_year', artist.first_release_year)
        artist.no_of_albums_released = data.get('no_of_albums_released', artist.no_of_albums_released)

        artist.update()
        return jsonify({'message': 'Artist updated successfully'}), 200

    elif request.method == 'DELETE':
        if current_user.role != 'artist_manager':
            return jsonify({'message': 'Unauthorized'}), 403

        if not artist:
            return jsonify({'message': 'Artist not found'}), 404

        Artist.delete(artist_id)
        return jsonify({'message': 'Artist deleted successfully'}), 200

# Import artists from CSV
@bp.route('/import', methods=['POST'])
def import_artists():
    current_user = get_current_user()
    if not current_user or current_user.role != 'artist_manager':
        return jsonify({'message': 'Unauthorized'}), 403

    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if file and file.filename.endswith('.csv'):
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.reader(stream)
        next(csv_input) 

        for row in csv_input:
            try:
                Artist.create(
                    name=row[0],
                    dob=row[1] if row[1] else None,
                    gender=row[2] if row[2] else None,
                    address=row[3] if row[3] else None,
                    first_release_year=int(row[4]) if row[4] else None,
                    no_of_albums_released=int(row[5]) if row[5] else None
                )
            except Exception as e:
                return jsonify({'message': f'Error importing artist: {str(e)}'}), 400

        return jsonify({'message': 'Artists imported successfully'}), 201

    return jsonify({'message': 'Invalid file format'}), 400

# Export artists to CSV
@bp.route('/export', methods=['GET'])
def export_artists():
    current_user = get_current_user()
    if not current_user or current_user.role != 'artist_manager':
        return jsonify({'message': 'Unauthorized'}), 403

    artists = Artist.get_all()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(['Name', 'DOB', 'Gender', 'Address', 'First Release Year', 'No. of Albums Released'])
    for artist in artists:
        writer.writerow([
            artist.name,
            artist.dob.isoformat() if artist.dob else '',
            artist.gender,
            artist.address,
            artist.first_release_year,
            artist.no_of_albums_released
        ])

    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name='artists.csv'
    )




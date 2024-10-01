from utils.db import execute_query
from datetime import datetime

class Music:
    def __init__(self, id=None, artistId=None, title=None, album_name=None, genre=None, 
                 created_at=None, updated_at=None):
        self.id = id
        self.artistId = artistId
        self.title = title
        self.album_name = album_name
        self.genre = genre
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def create(artistId, title, album_name=None, genre=None):
        query = """
        INSERT INTO music (artistId, title, album_name, genre)
        VALUES (%s, %s, %s, %s)
        """
        params = (artistId, title, album_name, genre)
        return execute_query(query, params)

    @staticmethod
    def get_by_id(song_id):
        query = "SELECT * FROM music WHERE id = %s"
        params = (song_id,)
        result = execute_query(query, params, fetch_one=True)
        if result:
            return Song(*result)
        return None

    @staticmethod
    def get_all_by_artist(artist_id, page=1, per_page=10):
        offset = (page - 1) * per_page
        query = "SELECT * FROM music WHERE artistId = %s LIMIT %s OFFSET %s"
        params = (artist_id, per_page, offset)
        results = execute_query(query, params, fetch_all=True)
        return [Song(*result) for result in results]

    def update(self):
        query = """
        UPDATE music 
        SET artistId = %s, title = %s, album_name = %s, genre = %s
        WHERE id = %s
        """
        params = (self.artistId, self.title, self.album_name, self.genre, self.id)
        return execute_query(query, params)

    @staticmethod
    def delete(song_id):
        query = "DELETE FROM music WHERE id = %s"
        params = (song_id,)
        return execute_query(query, params)

    def to_dict(self):
        return {
            'id': self.id,
            'artistId': self.artistId,
            'title': self.title,
            'album_name': self.album_name,
            'genre': self.genre,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
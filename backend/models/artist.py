from utils.db import execute_query
from datetime import datetime

class Artist:
    def __init__(self, id=None, name=None, dob=None, gender=None, address=None,
                 first_release_year=None, no_of_albums_released=None,
                 created_at=None, updated_at=None):
        self.id = id
        self.name = name
        self.dob = dob
        self.gender = gender
        self.address = address
        self.first_release_year = first_release_year
        self.no_of_albums_released = no_of_albums_released
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def create(name, dob=None, gender=None, address=None, first_release_year=None, no_of_albums_released=None):
        query = """ INSERT INTO artist (name, dob, gender, address, first_release_year, no_of_albums_released)
                VALUES (%s, %s, %s, %s, %s, %s)"""
        params = (name, dob, gender, address, first_release_year, no_of_albums_released)
        result = execute_query(query, params, fetch_one=True) 
        if result:
            return result 
        return None


    @staticmethod
    def get_by_id(artist_id):
        query = "SELECT * FROM artist WHERE id = %s"
        params = (artist_id,)
        result = execute_query(query, params, fetch_one=True)
        print(f"Result from get_by_id({artist_id}): {result}")
        if result:
            return Artist(**result)
        return None

    @staticmethod
    def get_all(page=1, per_page=10):
        offset = (page - 1) * per_page
        query = "SELECT * FROM artist LIMIT %s OFFSET %s"
        params = (per_page, offset)
        results = execute_query(query, params, fetch_all=True)
        return [Artist(**row) for row in results]

    def update(self):
        query = """
        UPDATE artist 
        SET name = %s, dob = %s, gender = %s, address = %s, 
            first_release_year = %s, no_of_albums_released = %s
        WHERE id = %s
        """
        params = (self.name, self.dob, self.gender, self.address,
                  self.first_release_year, self.no_of_albums_released, self.id)
        result = execute_query(query, params)
        return result > 0

    @staticmethod
    def delete(artist_id):
        query = "DELETE FROM artist WHERE id = %s"
        params = (artist_id,)
        result = execute_query(query, params)
        if result: 
            return True
        return False

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'dob': self.dob.isoformat() if self.dob else None,
            'gender': self.gender,
            'address': self.address,
            'first_release_year': self.first_release_year,
            'no_of_albums_released': self.no_of_albums_released,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
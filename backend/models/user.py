# models/user.py
from utils.db import execute_query
from datetime import datetime

class User:
    def __init__(self, id=None, first_name=None, last_name=None, email=None, password=None, 
                 phone=None, dob=None, gender=None, address=None, role=None, 
                 createdAt=None, updatedAt=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.phone = phone
        self.dob = dob
        self.gender = gender
        self.address = address
        self.role = role
        self.createdAt = createdAt
        self.updatedAt = updatedAt

    @staticmethod
    def create(first_name, last_name, email, password, role, phone=None, dob=None, gender=None, address=None):
        query = """
        INSERT INTO user (first_name, last_name, email, password, role, phone, dob, gender, address)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (first_name, last_name, email, password, role, phone, dob, gender, address)
        return execute_query(query, params)

    @staticmethod
    def get_by_id(user_id):
        query = "SELECT * FROM user WHERE id = %s"
        params = (user_id,)
        result = execute_query(query, params, fetch_one=True)
        return User(*result) if result else None

    @classmethod
    def get_by_username(cls,first_name):
        query = "SELECT * FROM user WHERE first_name = %s"
        params = (first_name,)
        result = execute_query(query, params, fetch_one=True)  
        # return User(*result)
        if result:
            return cls(**result) 
        else:
            None

    @classmethod
    def get_by_first_name_and_email(cls, first_name, email):
        query = "SELECT * FROM user WHERE first_name = %s AND email = %s"
        params = (first_name, email)
        result = execute_query(query, params, fetch_one=True)  
        if result:
            return cls(**result)  
        return None  


    @staticmethod
    def get_all(page=1, per_page=10):
        offset = (page - 1) * per_page
        query = "SELECT * FROM user LIMIT %s OFFSET %s"
        params = (per_page, offset)
    
        results = execute_query(query, params, fetch_all=True)
        if results is None:
            return []

        return [User(**result) for result in results] 


    def update(self):
        query = """
        UPDATE user 
        SET first_name = %s, last_name = %s, email = %s, password = %s, 
            phone = %s, dob = %s, gender = %s, address = %s, role = %s
        WHERE id = %s
        """
        params = (self.first_name, self.last_name, self.email, self.password,
                  self.phone, self.dob, self.gender, self.address, self.role, self.id)
        return execute_query(query, params)

    @staticmethod
    def delete(user_id):
        query = "DELETE FROM user WHERE id = %s"
        params = (user_id,)
        return execute_query(query, params)

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'dob': self.dob.isoformat() if self.dob else None,
            'gender': self.gender,
            'address': self.address,
            'role': self.role,
            'createdAt': self.createdAt.isoformat() if self.createdAt else None,
            'updatedAt': self.updatedAt.isoformat() if self.updatedAt else None
        }

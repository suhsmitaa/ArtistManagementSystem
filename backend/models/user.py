from utils.db import execute_query

class User:
 
    def __init__(self,id,firstname,lastname,email,password,phone=None,dob=None,gender=None,address=None):
        self.id=id
        self.firstname=firstname
        self.lastname=lastname
        self.email=email
        self.password=password
        self.phone=phone
        self.dob=dob
        self.gender=gender
        self.address=address

    @classmethod
    def create(cls,user):
        query = """Insert into user (firstname,lastname,email,password,phone,dob,gender,address) 
                Values(%s,%s,%s,%s,%s,%s,%s,%s)"""
        params =(user.firstname,user.lastname,user.email,user.password,user.phone,user.dob,user.gender,user.address)
        return execute_query(query,params)
    
    @staticmethod
    def get_by_id(user_id):
        query ="Select * from user where id = %s"
        params = (user_id,)
        result = execute_query(query,params)

        if result:
            return User(*result[0]) if result else None
        else:
            return None
       
    @staticmethod
    def get_by_username(username):
        query ="Select * from user where firstname = %s"
        params = (username,)
        result = execute_query(query,params)

        if result:
            return User(*result[0]) if result else None
        else:
            return None
        
    @classmethod
    def get_by_all(cls,page, per_page):
        offset = (page - 1) * per_page
        query ="Select * from user LIMIT %s OFFSET %s"
        params = (page,offset)
        result= execute_query(query,params)

        if result :
            return [cls(*row) for row in result]
        else:
            return []
        
        
    @classmethod
    def update(cls,user_id,firstname=None,lastname=None,email=None,password=None,phone=None,dob=None,gender=None,address=None):
        query= "Update user SET"
        field =[]
        params=[]

        if firstname:
            field.append("firstname = %s")
            params.append(firstname)
        if lastname:
            field.append("lastname = %s")
            params.append(lastname)
        if email:
            field.append("email = %s")
            params.append(email)
        if phone:
            field.append("phone = %s")
            params.append(phone)
        if dob:
            field.append("dob = %s")
            params.append(dob)
        if gender:
            field.append("gender = %s")
            params.append(gender)
        if address:
            field.append("address = %s")
            params.append(address)
        
        if not field:
            return None
        

        query += ", ".join(field) + " where id = %s"
        params.append(user_id)

        result = execute_query(query,params)

        if result :
            return True
        else:
            return False

        
    @classmethod
    def delete(cls,user_id):
        query = "Delete from user where id =  %s"
        params = (user_id,)
        
        result =execute_query(query,params)

        if result:
             return True
        else:
            return False
        
    
    
    


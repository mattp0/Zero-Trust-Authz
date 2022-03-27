from typing import List
class User():
    def __init__(self, init) -> None:
        self.id = init['_id']
        self.email: str = init['email']
        self.name: str = init['name']
        self.hd: str = init['hd']
        self.permissions: str = init['permissions']

    def get_user_id(self):
        return self.id

    def get_permissions(self):
        return self.permissions

    def get_email(self):
        return self.email
    
    def get_name(self):
        return self.name

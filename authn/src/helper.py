import requests
def build_user(user):
    return user

def add_user(user, url):
    full = url+"/create"
    
    x = requests.post(full, data=user)
    if x.status_code == 200:
        return True
    else:
        return False  
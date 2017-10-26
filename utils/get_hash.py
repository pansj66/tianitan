# 取散列值,给密码加密
from hashlib import sha1

def get_hash(password):
    '''取一个字符串的hash值'''
    sh = sha1()
    sh.update(password.encode('utf8'))
    return sh.hexdigest()
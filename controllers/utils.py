import bcrypt

def encrypt(password):
    passwd = bytes(password, encoding='utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(passwd, salt)
    return hashed

def decrypt(hashed, password):
    return bcrypt.checkpw(bytes(password, encoding='utf-8'), hashed)
    


if __name__ == '__main__':
    hashpw = encrypt('helloworld')
    print(decrypt(hashpw, 'helloworld'))
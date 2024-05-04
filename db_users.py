from hashlib import sha256
from random import randint
import secrets


class DbUsers:
    file_name = 'users.txt' 
        
    @staticmethod 
    def gen_token(zero_t = False):
        return secrets.token_hex(16) if not zero_t else '0'*32

    @staticmethod
    def search(data, by='login'):        
        file = open(DbUsers.file_name)
        pattr = ''
        offset = 0
        if by == 'login':
            pattr = data + ' '  
        elif by == 'token':
            pattr = ' ' + data + "\n"
            offset = float('inf')
        while file:
            line = file.readline()        
            if line == "":
                break
            out = line.find(pattr)
            if out > offset or out == -1:
                continue
            offset = file.tell()
            file.close()
            data = line.split(' ')
            return {
                'login': data[0],
                'pwd_hash': data[1],
                'token': data[2].strip(),
                'offset': offset,
                'line_len': len(line)
            }            
        file.close()
        
    @staticmethod
    def reg(login, pwd):
        file = open(DbUsers.file_name, 'a')
        if DbUsers.search(login):
            print('this login already exists')
            return None
        file.write(login + ' ' + (sha256(pwd.encode()).hexdigest()) + ' ' + DbUsers.gen_token(zero_t=True) + '\n')
        print('user added')        
        file.close()
        return DbUsers.auth(login, pwd)
    
    @staticmethod
    def auth(login, pwd):    
        user_data = DbUsers.search(login)
        if not user_data:
            return None
        if sha256(pwd.encode()).hexdigest() != user_data['pwd_hash']:
            return None    
        token = DbUsers.gen_token()
        f = open('users.txt', 'r+b')
        f.seek(user_data['offset'] - 34)
        f.write(token.encode())
        f.close()       
        return token
    
    @staticmethod
    def verify_token(token):
        user_data = DbUsers.search(token, 'token')
        if not user_data:
            return None
        return user_data['login']
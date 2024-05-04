import uuid


class DbChat:
    chats_file = 'chats.txt'
    user_chats_file = 'u_chats.txt'
    history_file = 'history.txt'
    delim = '<delim>'

    @staticmethod
    def get_chat_info(id):
        f = open(DbChat.chats_file)
        while f:
            line = f.readline()
            if line == '':
                break
            if line.find(str(id) + DbChat.delim) != 0:
                continue
            data = line.strip().split(DbChat.delim)
            f.close()
            return {
                'id': data[0],
                'name': data[1],
                'type': data[2]
            }
        f.close()
        return None

    @staticmethod
    def create_chat(id=None, name='', type='group'):
        if id is None:
            id = uuid.uuid4()

        # проверка на дублирование id чата
        if DbChat.get_chat_info(id):
            return None

        f = open('chats.txt', 'a+')
        f.write(str(id) + DbChat.delim + name + DbChat.delim + type)
        return {
            'id': id,
            'name': name,
            'type': type
        }


out = DbChat.create_chat(name='test chat', type='group')
print(out)

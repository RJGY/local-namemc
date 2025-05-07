import requests
import sys

minecraft_api_host = 'https://api.mojang.com/users/profiles/minecraft/'
minecraft_api_uuid_host = 'https://sessionserver.mojang.com/session/minecraft/profile/'

class Player:
    def __init__(self, uuid: str, names: list[str], reason: str) -> None:
        self.uuid = uuid
        self.names = names
        self.reason = reason

    def get_current_name(self) -> str:
        return self.names[-1]
    
    def to_file_str(self) -> str:
        return self.uuid + '|' + ','.join(self.names) + '|' + (self.reason or '')
    
    def __str__(self) -> str:
        return f'Current Name: {self.get_current_name()}, Previous Names: {self.names[:-1]}, UUID: {self.uuid}, Reason: {self.reason}'
    
    def __eq__(self, other):
        if isinstance(other, Player):
            return (self.uuid == other.uuid)
        return False
    
players: list[Player] = []

def convert_username_to_uuid(username: str):
    uuid_obj = requests.get(minecraft_api_host + username)
    if uuid_obj.status_code != 200:
        return
    return uuid_obj.json()['id']


def convert_uuid_to_username(uuid: str):
    username_obj = requests.get(minecraft_api_uuid_host + uuid)
    if username_obj.status_code != 200:
        return
    return username_obj.json()['name']


def populate_player_list():
    f = open('player_list.txt', 'r')
    player_str_list = [line.rstrip('\n') for line in f.readlines()]
    players.clear()
    for player_str in player_str_list:
        uuid, names, reason = player_str.split('|', 2)
        reason = reason if reason else None
        players.append(Player(uuid, names.split(','), reason))


def save_to_file() -> None:
    str_arr = []
    for player in players:
        str_arr.append(player.to_file_str())
    f = open('player_list.txt', 'w')
    text = '\n'.join(str_arr)
    f.write(text)


def add_player(name: str, reason: str=None) -> None:
    uuid = convert_username_to_uuid(name)
    player = Player(uuid, [name], reason)
    if player in players:
        print(f'{name} is already on the list')
        return
    players.append(player)
    save_to_file()


def get_player_by_uuid(uuid: str) -> Player:
    for player in players:
        if player.uuid == uuid:
            return player
        

def get_player_by_name(name: str) -> Player:
    for player in players:
        if player.get_current_name() == name:
            return player
        

def change_reason(name_or_uuid: str, reason: str) -> None:
    if len(name_or_uuid) != 32:
        player = get_player_by_name(name_or_uuid)
        if not player:
            print(f'{name_or_uuid} is not in the list.')
            return
        
        player.reason = reason
    else:
        player = get_player_by_uuid(name_or_uuid)
        if not player:
            print(f'UUID {name_or_uuid} is not in the list.')
            return
        
        player.reason = reason
    save_to_file()


def bulk_add_players(file_path: str) -> None:
    f = open(file_path, 'r')
    player_str_list = [line.rstrip('\n') for line in f.readlines()]
    for player_str in player_str_list:
        if '|' in player_str:
            names, reason = player_str.split('|', 1)
        else:
            names = player_str
            reason = None
        names = names.split(',')
        uuid = convert_username_to_uuid(names[-1])
        player = Player(uuid, names, reason)
        if player in players:
            print(f'{names[-1]} is already on the list')
            continue
        players.append(player)
    save_to_file()


def remove_player(name: str) -> None:
    player = get_player_by_name(name)
    if not player:
        print(f'Could not find {name}')
        return
    players.remove(player)
    save_to_file()


def list_all_players() -> None:
    print(f'Number of players on list: {len(players)}')
    for player in players:
        name = convert_uuid_to_username(player.uuid)
        if name != player.get_current_name():
            player.names.append(name)
        
    for player in players:
        print(player)


def e2e_test():
    populate_player_list()
    add_player('RJGY', 'baller')
    bulk_add_players('add.txt')
    remove_player('RJGY')
    list_all_players()


def print_help():
    print('Commands:')
    print('add <username> <reason> - Adds a user to the list. Reason is an optional argument.')
    print('remove <username> - Remove a user from the list.')
    print('reason <username/uuid> <reason> - Add/Change a reaon for a user on the list (user must already be on the list). Either uuid or username can be passed into the ')
    print('bulk <file_path> - Add multiple users to the list. Check example.txt for an example of how to format your file.')
    print('list - List all users on the list. This also updates the list if their name has changed since the last update.')


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print_help()
    else:
        populate_player_list()
        match sys.argv[1]:
            case 'add':
                if len(sys.argv) == 2:
                    print('Add command requires username.')
                elif len(sys.argv) == 3:
                    add_player(sys.argv[2])
                else:
                    add_player(sys.argv[2], sys.argv[3])
            case 'remove':
                if not sys.argv[2]:
                    print('Remove command requires username.')
                else:
                    remove_player(sys.argv[2])
            case 'reason':
                if not sys.argv[2] or not sys.argv[3]:
                    print('Reason command requires username and reason.')
                else:
                    change_reason(sys.argv[2], sys.argv[3])
            case 'bulk':
                if not sys.argv[2]:
                    print('Bulk command requires a file path. This includes the file extension.')
                else:
                    bulk_add_players(sys.argv[2])
            case 'list':
                list_all_players()
            case _:
                print_help()

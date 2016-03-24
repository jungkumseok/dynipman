import requests, socket, json
import conf

CLIENT_NAME = conf.CLIENT['name']

# SERVER_URL = 'http://www.jungkumseok.com:7883'
SERVER_URL = conf.SERVER['url']

def device_info():
    info = {
            'host': socket.gethostname(),
            'name': CLIENT_NAME,
            'nonce': 'abcdefg',
            }
    print("Client host: "+info['host'])
    print("Client name: "+info['name'])
    print("Client secret: "+info['nonce'])
    return info
    
def report_ip():
    update = requests.post(SERVER_URL+'update/?code='+conf.SHARED_SECRET, data=json.dumps(device_info())).json()
    print(update)
    return update

def show_menu():
    print('\n-Menu---------------------------')
    print('\n1. Show Device Info')
    print('2. Report IP Address to Server')
    print('\n--------------------------------')
    return {
            '1': device_info,
            '2': report_ip,
            }

def run():
    KEEP_ALIVE = True
    print('=HELLO==================')
    print(' starting jksdns client ')
    print('========================')
    while KEEP_ALIVE:
        menu = show_menu()
        uin = input(' >> ')
        if uin in menu:
            menu[uin]()
        KEEP_ALIVE = not (uin == 'exit')
    print('========================')
    print(' quitting jksdns client ')
    print('====================BYE=')
    return

if __name__ == "__main__":
    run()
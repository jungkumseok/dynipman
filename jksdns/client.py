import requests, socket

CLIENT_NAME = 'jks-xeon-home'

def device_info():
    ip = socket.gethostname()
    info = {
            'name': CLIENT_NAME,
            'ip': socket.gethostbyname(socket.gethostname())
            }
    
    print("Client name: "+info['name'])
    print("Client secret: ")
    print("IP: "+str(info['ip']))
    print("Hostname: ")
    return info
    
def report_ip():
    print("Say IP")
    print("Requesting Server")
    print("Server Response: ")
    response = requests.get('http://192.168.0.73:8010/').content
    print(response)
    update = requests.post('http://192.168.0.73:8010/update/', data = { 'myname': 'Client 1',
                                                                        'myip': 'My IP 1',
                                                                        'yourip': '192.168.0.73:8010' }).json()
    print(update)

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
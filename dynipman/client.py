import socket, requests, json, datetime, time
from dynipman import conf

CLIENT_NAME = conf.CLIENT['name']
UPDATE_INTERVAL = conf.CLIENT['update_interval']
SERVER_URL = conf.SERVER['url']

def device_info():
    info = {
            'host': socket.gethostname(),
            'name': CLIENT_NAME
            }
    return info
    
def report_ip():
    update = requests.post(SERVER_URL+'update/?code='+conf.SHARED_SECRET, data=json.dumps(device_info())).json()
    print(datetime.datetime.now())
    print(update)
    return update

def run():
    while True:
        report_ip()
        time.sleep(UPDATE_INTERVAL)
    
if __name__ == "__main__":
    run()
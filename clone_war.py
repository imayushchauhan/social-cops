import os
import json
import time
import uuid
import shutil
import paho.mqtt.client as mqtt
from watchdog.observers import Observer 
from watchdog.events import FileSystemEventHandler

# create unique client_id for mqtt
client_id = uuid.uuid4().hex[:6].upper()

# create path of the directory to monitor
# path = "C:\\Users\\Ayush\\Desktop\\test"
path = "/usr/src/app/clonewar"

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        data = {"client_id": client_id, "event_type": event.event_type, "src_path": event.src_path, "is_directory": event.is_directory}	
        json_data = json.dumps(data)
        client.publish("clonewar", json_data, 1)

    def on_modified(self, event):
        data = {"client_id": client_id, "event_type": event.event_type, "src_path": event.src_path, "is_directory": event.is_directory}
        if event.is_directory == False:
            fo = open(event.src_path,"r")
            file_data = fo.read()
            fo.close()
            data['data'] = file_data

        json_data = json.dumps(data)
        client.publish("clonewar", json_data, 1)

    def on_deleted(self, event):
        data = {"client_id": client_id, "event_type": event.event_type, "src_path": event.src_path, "is_directory": event.is_directory}	
        json_data = json.dumps(data)
        client.publish("clonewar", json_data, 1)

    def on_moved(self, event):
        data = {"client_id": client_id, "event_type": event.event_type, "src_path": event.src_path, "dest_path": event.dest_path, "is_directory": event.is_directory}	
        json_data = json.dumps(data)
        client.publish("clonewar", json_data, 1)

        json_data = json.dumps(data)
        client.publish("clonewar", json_data, 1)
      
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+ str(rc))
    client.subscribe("clonewar")    

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    data = json.loads(msg.payload)
    if(data['client_id'] == client_id):
        print("stop")
        return

    print(data)
    event_type = data['event_type']
    src_path = data['src_path']
    dest_path = data['dest_path']
    is_directory = data['is_directory']
    file_data = data['data']

    if(event_type == 'created'):
        if(is_directory == True):
            os.mkdir(src_path)
        else:
            file = open(src_path, "w") 
            file.write(file_data) 
            file.close() 

    if(event_type == 'modified'):
        if(is_directory == False):
            print(src_path)
            fw = open(src_path, "w") 
            fw.write(file_data) 
            fw.close()    

    if(event_type == 'deleted'):
        if(is_directory == True):
            shutil.rmtree(src_path)
        else:
            os.remove(src_path)

    if(event_type == 'moved'):
        os.rename(src_path, dest_path)               


if __name__ == "__main__":
    print("start")
    # create mqtt client
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("broker.hivemq.com")
    client.loop_start()
    
    # create a handler to monitor the directory
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
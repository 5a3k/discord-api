import json
import time
import threading
from api import Client

def main():
    data = json.load(open("config.json"))
    token = data["token"]

    client = Client(token)
    print(f"Running as @{client.user['username']}!")
    
    target = input("target user id:")
    msg = ""
    
    rename = input("rename? (0/1):")
    if rename == "1":
        rename = True
        msg = input("msg:")
    
    delete = input("delete? (0/1):")
    if delete == "1":
        delete = True
    
    count = int(input("count:"))
    
    def process_iteration(group_id):
        gc = client.create_groupchat(group_id)
        if rename:
            gc.rename(msg)
        if delete:
            gc.delete()

    threads = []
    for i in range(count):
        thread = threading.Thread(target=process_iteration, args=(target,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()

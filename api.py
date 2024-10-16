import requests

class Client:
    def __init__(self, token):
        self.token = token
        self.session = requests.Session()
        self.session.headers = {"Authorization": token}
        self.base = "https://discord.com/api"
        self.user = self.session.get(f"{self.base}/v6/users/@me").json()

    class Reaction:
        def __init__(self, session, channel_id, message_id, reaction):
            self.session = session
            self.channel_id = channel_id
            self.message_id = message_id
            self.reaction = reaction
            self.base = "https://discord.com/api"

        def unreact(self):
            return self.session.delete(
                f"{self.base}/v9/channels/{self.channel_id}/messages/{self.message_id}/reactions/{self.reaction}/@me"
            )
    
    def find_reaction(self, channel_id, message_id, reaction):
        return Reaction(self.session, channel_id, message_id, reaction)
    
    class Thread:
        def __init__(self, session, thread_id):
            self.session = session
            self.thread_id = thread_id
            self.base = "https://discord.com/api"

        def delete(self):
            return self.session.delete(
                url=f"{{self.base}}/v9/channels/{self.thread_id}"
            ).json()
        
        def edit_thread(self, thread_name):
            return self.session.patch(
                url=f"{self.base}/v9/channels/{self.thread_id}",
                data={
                    "name": thread_name
                }
            ).json()
        
        def lock_thread(self):
            return self.session.patch(
                url=f"{self.base}/v9/channels/{self.thread_id}",
                data={
                    "locked": True
                }
            ).json()
        
        def unlock_thread(self):
            return self.session.patch(
                url=f"{self.base}/v9/channels/{self.thread_id}",
                data={
                    "locked": False
                }
            ).json()
        
        def close_thread(self):
            return self.session.patch(
                url=f"{self.base}/v9/channels/{self.thread_id}",
                data={
                    "archived": True
                }
            ).json()
    
    def create_thread(self, channel_id, message_id, thread_name):
        response = self.session.post(
            url=f"{self.base}/v9/channels/{channel_id}/messages/{message_id}/threads",
            data={
                "name": thread_name
            }
        ).json()
        return Client.Thread(self.session, response["id"])
    
    def find_thread(self, thread_id):
        return Client.Thread(self.session, thread_id)
    
    class Message:
        def __init__(self, session, channel_id, message_id):
            self.session = session
            self.channel_id = channel_id
            self.message_id = message_id
            self.base = "https://discord.com/api"

        def delete(self):
            return self.session.delete(
                url=f"{self.base}/v9/channels/{self.channel_id}/messages/{self.message_id}"
            )

        def edit(self, content):
            return self.session.patch(
                url=f"{self.base}/v9/channels/{self.channel_id}/messages/{self.message_id}",
                data={
                    "content": content
                }
            ).json()

        def react(self, reaction):
            response = self.session.put(
                f"{self.base}/v9/channels/{self.channel_id}/messages/{self.message_id}/reactions/{reaction}/@me"
            )
            return Client.Reaction(self.session, self.channel_id, self.message_id, reaction)

        def unreact(self, reaction):
            return self.session.delete(
                f"{self.base}/v9/channels/{self.channel_id}/messages/{self.message_id}/reactions/{reaction}/@me"
            )
        
        def pin_message(self):
            return self.session.put(
                url=f"{self.base}/v9/channels/{self.channel_id}/pins/{self.message_id}"
            )
        
        def unpin_message(self):
            return self.session.delete(
                url=f"{self.base}/v9/channels/{self.channel_id}/pins/{self.message_id}"
            )
        
        def thread(self, thread_name):
            response = self.session.post(
                url=f"{self.base}/v9/channels/{self.channel_id}/messages/{self.message_id}/threads",
                data={
                    "name": thread_name
                }
            ).json()
            return Client.Thread(self.session, response["id"])
    
    def send_message(self, channel_id, content):
        response = self.session.post(
            url=f"{self.base}/v9/channels/{channel_id}/messages",
            data={
                "content": content
            }
        ).json()
        return Client.Message(self.session, response["channel_id"], response["id"])
    
    def find_message(self, channel_id, message_id):
        return Client.Message(self.session, channel_id, message_id)
    
    class Channel:
        def __init__(self, session, channel_id):
            self.session = session
            self.channel_id = channel_id
            self.base = "https://discord.com/api"
        
        def rename(self, name = "example"):
            return self.session.patch(
                f"{self.base}/v9/channels/{self.channel_id}", json={"name": name}
            ).json()
        
        def delete(self):
            return self.session.delete(
                f"{self.base}/v9/channels/{self.channel_id}?silent=true"
            )
    
    def find_channel(self, channel_id):
        return Client.Channel(self.session, channel_id)
    
    # [=====TYPES=====]
    # 0- TEXT CHANNEL
    # 1- ???
    # 2- VOICE CHANNEL
    # 3- ???
    # 4- CATEGORY
    # [===============]
    def create_channel(self, guild_id, name = "example", type = 0, permissions = []):
        r = self.session.post(
            f"{self.base}/v9/guilds/{guild_id}/channels", json={"name": name, "permission_overwrites": permissions, "type": type}
        ).json()
        return Client.Channel(self.session, r["id"])
    
    def create_groupchat(self, target_id, recipients = []):
        if recipients == []:
            recipients = [f"{self.user['id']}", f"{target_id}"]
        
        r = self.session.post(
            f"{self.base}/v10/users/@me/channels", json={"recipients": recipients}
        ).json()
        return Client.Channel(self.session, r["id"])
    
    def scrape_channel(self, channel_id, limit):
        return self.session.get(
            f"https://discord.com/api/v9/channels/{channel_id}/messages?limit={limit}"
        ).json()

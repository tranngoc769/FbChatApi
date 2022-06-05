import atexit
from excel.crawl import load_data
import json
import getpass
import fbchat
import random
def load_cookies(filename):
    try:
        # Load cookies from file
        with open(filename) as f:
            return json.load(f)
    except FileNotFoundError:
        return  # No cookies yet
def save_cookies(filename, cookies):
    with open(filename, "w") as f:
        json.dump(cookies, f)
def load_session(cookies):
    if not cookies:
        return
    try:
        return fbchat.Session.from_cookies(cookies)
    except fbchat.FacebookError as err:
        print(err)
        return  # Failed loading from cookies
cookies = load_cookies("session.json")
session = load_session(cookies)
client = fbchat.Client(session=session)
if not session:
    session = fbchat.Session.login("<email>", getpass.getpass())
atexit.register(lambda: save_cookies("session.json", session.get_cookies()))
print("Own id: {}".format(session.user.id))
SENDABLE_REACTIONS = ["❤", "😍", "😆", "😮", "😢", "😠", "👍", "👎"]
DICTIONARY = {}
KEYS = []
ANS_STATUS = {

}
CURRENT_QUESTION = {

}
LIST_USERS = {

}
from threading import Thread
import threading
import time
def thread_excel(numbers):
    listener = fbchat.Listener(session=session, chat_on=False, foreground=False)
    for event in listener.listen():
        if isinstance(event, fbchat.MessageEvent):
            # print(f"{event.message.text} from {event.author.id} in {event.thread.id}")
            sender_id = event.author.id
            user_name = ""
            try:
                username = LIST_USERS[sender_id]
            except:
                user = client._fetch_info(sender_id)
                user_name = user[sender_id]["name"]
            msg = event.message.text
try:
	t1 = threading.Thread(target=thread_excel, args=(1,))
	t1.start()
	t1.join()
except:
	print ("error")
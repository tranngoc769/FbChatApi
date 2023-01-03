import atexit
import json
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
    exit()
atexit.register(lambda: save_cookies("session.json", session.get_cookies()))
print("Own id: {}".format(session.user.id))
USER_ID = session.user.id
SENDABLE_REACTIONS = ["❤", "😍", "😆", "😮", "😢", "😠", "👍", "👎"]
OFFLINE_MESSAGE = "Trần Ngọc đang offline, vui lòng để lại lời nhắn sau tiếng bíp!"
IS_ENABLE = False
SENDED_USERS = {}
from threading import Thread
import threading
import time
def thread_main(numbers):
    global IS_ENABLE, SENDABLE_REACTIONS, USER_ID,SENDED_USERS
    listener = fbchat.Listener(session=session, chat_on=False, foreground=False)
    for event in listener.listen():
        if isinstance(event, fbchat.MessageEvent):
            print(f"{event.message.text} from {event.author.id} in {event.thread.id}")
            sender_id = event.author.id
            msg = event.message.text
            print(event.message)
            return
            if (USER_ID == sender_id and msg == "open"):
                IS_ENABLE = True
                event.thread.send_text("Đã bật trợ lý ảo")
                SENDED_USERS = {}
                return
            if (USER_ID == sender_id and msg == "close"):
                IS_ENABLE = True
                event.thread.send_text("Đã tắt trợ lý ảo")
                SENDED_USERS = {}
                return
            event.message.react(random.choice(SENDABLE_REACTIONS))
            if msg == None:
                continue
            event.thread.send_text("Câu hỏi của "+str(user_name)+"\n❤ "+question)
            # print(f"{event.message.text} from {event.author.id} in {event.thread.id}")
try:
	t1 = threading.Thread(target=thread_main, args=(1,))
	t1.start()
	t1.join()
except:
	print ("error")
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
KEY_CODE = "EX"
HELP_CODE = "HELP"
ANS = ["A","B","C","D"]
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
    global DICTIONARY,KEYS,ANS_STATUS,CURRENT_QUESTION,LIST_USERS
    DICTIONARY = load_data('excel/data.json')
    for key in DICTIONARY.keys():
        KEYS.append(key)
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
            if msg == None:
                continue
            else:
                msg = msg.upper()
            if msg  == HELP_CODE:
                help_msg = "HDSD Phần mềm ôn thi MS Excel 2010:\n\t-Cú pháp tạo câu hỏi mới: ex\n\t-Cú pháp trả lời: A,B,C,D,a,b,c,d\n\t-Lưu ý: trả lời đúng câu hỏi hiện tại để có thể tiếp tục câu hỏi tiếp theo\nGood luck to youuu"
                event.thread.send_text(help_msg)
                event.message.react("😍")
            if (msg == KEY_CODE or msg in ANS):
                # 
                if (msg == KEY_CODE):
                    try:
                        if (ANS_STATUS[event.author.id]['is_answer'] != True):
                          event.thread.send_text("Chưa trả lời đúng câu hỏi trước đó!")
                        else:
                            raise Exception("continue")
                    except:
                        question_id = random.choice(KEYS)
                        ANS_STATUS[event.author.id] = {
                            "question" : question_id,
                            "is_answer": False
                        }
                        question = DICTIONARY[question_id]['question']
                        event.thread.send_text("Câu hỏi của "+str(user_name)+"\n❤ "+question)
                else:
                    try:
                        if (ANS_STATUS[event.author.id]['is_answer'] == True):
                            raise Exception("continue")
                        else:
                            question_id = ANS_STATUS[event.author.id]["question"]
                            ans = DICTIONARY[question_id]["answer"]
                            if (msg != ans):
                                ANS_STATUS[event.author.id]['is_answer'] = False
                                event.thread.send_text(msg+ " không là đáp án đúng")
                                event.message.react("😠")
                            else:
                                event.thread.send_text(msg+ " là đáp án đúng. Chúc mừngggg")
                                event.message.react("❤")
                                ANS_STATUS[event.author.id]['is_answer'] = True
                    except:
                        event.thread.send_text("Chưa chọn câu hỏi!")
            # print(f"{event.message.text} from {event.author.id} in {event.thread.id}")
            # event.message.react(random.choice(SENDABLE_REACTIONS))
try:
	t1 = threading.Thread(target=thread_excel, args=(1,))
	t1.start()
	t1.join()
except:
	print ("error")
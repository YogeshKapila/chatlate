#!/usr/bin/env python3
"""
Script for Tkinter GUI chat client
"""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import hashlib

from server import MSG_SPLIT_PATTERN, LANG_SPLIT_PATTERN, AVAILABLE_LANGS

TRANSLATION_DB = dict()
CLIENT_DETAILS = {"lang": "ja"}
special_msg = ["{quit}", "{listlangs}"]

def receive():
    """
    Handles receiving of messages
    """
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            print("RECEIVED MSG: ", msg)
            if not MSG_SPLIT_PATTERN in msg:
                msg_list.insert(tkinter.END, msg)
            else:
                translated, original = msg.split(MSG_SPLIT_PATTERN)
                TRANSLATION_DB[hashlib.md5(translated.encode('utf-8')).hexdigest()] = original
                msg_list.insert(tkinter.END, translated)

        except OSError:
            break


def send(event=None):  # event is passed by binders.
    """
    Handles sending of messages
    """
    msg = my_msg.get()
    size = msg_list.size()
    my_msg.set("")  # Clears input field.
    print("MSG:", msg)
    if size!=1 and msg not in special_msg:
        print("Trying to send... {}".format(msg))
        msg = msg + LANG_SPLIT_PATTERN + CLIENT_DETAILS["lang"]
    print("SENDING: ", msg)
    if msg == special_msg[1]:
        msg_list.insert(tkinter.END, AVAILABLE_LANGS)
        return
    client_socket.send(bytes(msg, "utf8"))
    if msg == special_msg[0]:
        client_socket.close()
        top.quit()




def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()

def clear_default_text(event):
    entry_field.delete(0, "end")
    return None

def double_click_callback(event):
    print("Double Clicked!!")
    print(msg_list.get(tkinter.ACTIVE))
    index = msg_list.curselection()[0]
    curr_item = msg_list.get(index)
    hashed_item = hashlib.md5(curr_item.encode('utf-8')).hexdigest()
    print(TRANSLATION_DB)
    print(hashed_item, type(hashed_item))
    if hashed_item in TRANSLATION_DB:
        print("Yes!")
        msg_list.delete(index)
        msg_list.insert(index, TRANSLATION_DB[hashed_item])
        msg_list.insert(index, curr_item + " >>")
    




top = tkinter.Tk()
top.title("Chatlate")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("Type your messages here.")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.bind("<Double-Button-1>" , double_click_callback)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)


msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.bind("<Button-1>", clear_default_text)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

#----Now comes the sockets part----
HOST = input('Enter host(Leave empty to use default, default is `localhost`: ')
PORT = input('Enter port(Leave empty to use default): ')
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

if not HOST:
    HOST = 'localhost'

BUFSIZ = 2048
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.

    
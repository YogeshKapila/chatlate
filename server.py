#!/usr/bin/env python3

"""
Server for multithreaded (asynchronous) chat application
"""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

import translate

clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

MSG_SPLIT_PATTERN = "Q!@#ERF"
LANG_SPLIT_PATTERN = "t%$Hs0)"
AVAILABLE_LANGS = ["ja", "en", "es"]

def accept_incoming_connections():
    """
    Sets up handling for incoming clients
    """
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Greetings from the Chatlate! Now type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """
    Handles a single client connection
    """

    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            print("REcvd msg type: ", type(msg))
            enc_lang_pattern = LANG_SPLIT_PATTERN.encode("utf-8")
            lang = None
            if enc_lang_pattern in msg:
                print("lang found")
                msg, lang = msg.split(enc_lang_pattern)
                print(lang)
                lang = lang.decode("utf-8")
            translated = translate.translate_str(msg, lang=lang)
            print(translated)
            translated = translated.encode("utf-8")
            # broadcast(msg, name+": ")
            final_msg = translated + MSG_SPLIT_PATTERN.encode("utf-8") + msg
            broadcast(final_msg, name+": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """
    Broadcasts a message to all the clients
    """

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

if __name__ == "__main__":
    SERVER = socket(AF_INET, SOCK_STREAM)
    SERVER.bind(ADDR)
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
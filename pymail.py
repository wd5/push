#!/usr/bin/env python3

import imaplib, sys, email

import argparse

class MailParser(object):
    pass

class Pymail(object):

    def __init__(self):
        self.IMAP_SERVER='imap.gmail.com'
        self.IMAP_PORT=993
        self.M = None
        self.response = None
        self.all_mail = "[Gmail]/All Mail"

    def __str__(self):
        print "Python mail client"
 
    def login(self, username, password):
        self.M = imaplib.IMAP4_SSL(self.IMAP_SERVER, self.IMAP_PORT)
        resp, self.response = self.M.login(username, password)
        return resp

    def list_folders(self):
        resp, data = self.M.list()
        return map((lambda x : x.split(" ")[2:]), data)

    def fetch(self, uid): pass

    def search(self, query): pass

    def select(self, mailbox): pass

    def message_headers(self, uid):
        resp, data = self.M.fetch(uid, '(BODY[HEADER])')
        parser = email.HeaderParser()
        msg = parser.parsestr(data[0][1])
        return msg

    def message_body(self, uid):
        """ Extract the body text from an email message """
        resp, data = self.M.fetch(uid, '(BODY.PEEK[TEXT])')
        for response_part in data:
            if isinstance(response_part, tuple):
                return response_part[1]

    def messages_from(self, person):
        """ Gets all messages from a given person """
        resp, data = self.M.search(None, 'FROM', person) 
        return data

    def select_folder(self, folder="inbox"):
        resp, data = self.M.select(folder)
        return resp

    def get_message(self, uid):
        """ Get a single email message by uid """
        resp, data = self.M.fetch(uid, '(RFC822)')
        return resp

    def logout(self):
        self.M.logout()

def main(mail):
    print("What would you like to do?")
    print("1: View all folders")
    print("2: Read a message")
    try:
        while True:
            cmd = raw_input('Enter command: ')
            if cmd == "1":
                print(mail.list_folders())
            else: main(mail)
    except KeyboardInterrupt:
        sys.exit(0)
    except: 
        sys.exit(1)
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-u", "--username", help="User name")
    parser.add_argument("-p", "--password", help="Password")

    args = parser.parse_args()
   
    mail = Pymail()
    mail.login(args.username, args.password)
    main(mail)


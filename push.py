#!/usr/bin/env python

import imaplib, sys, email

import argparse

class MailParser(object):
    pass

class Push(object):

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

    def search(self, *args):
        """ Gets all messages from a given person """
        resp, data = self.M.search(None, *args) 
        return data

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
        return data

    def unread_email(self):
        """ Returns the number of unopened email messages """
        return len(self.list_unread_email())

    def list_unread_email(self):
        messages = self.search('UnSeen')
        return messages[0].split()

    def logout(self):
        self.M.logout()

def mail_menu(mail):
    print("\nHello. You have %d unread email messages\n" % mail.unread_email())
    print("What would you like to do?")
    print("1: List unread email")
    print("2: Read a message")
    print("3: List folders")
    print("\n--------------------\nType 'q' or 'quit' to exit\n")

def main(mail):
    try:
        while True:
            mail_menu(mail)
            cmd = raw_input('Enter command: ').strip()
            if cmd == "1":
                print(mail.list_unread_email())
            elif cmd == "2": 
                message_id = raw_input("Please enter message id: ")
                print(mail.get_message(message_id))
            elif cmd == "3":
                print(mail.list_folders())
            elif (cmd == "q") or (cmd == "quit"):
                print("\nBye...")
                break
                sys.exit(0)
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
   
    mail = Push()

    mail.login(args.username, args.password)
    mail.select_folder() # select the inbox folder
    main(mail)


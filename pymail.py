#!/usr/bin/env python3

import imaplib, sys

user="you@gmail.com"
password="password"
all_mail = "[Gmail]/All Mail"

class MailParser(object):
    pass

class Pymail(object):

    def __init__(self):
        self.IMAP_SERVER='imap.gmail.com'
        self.IMAP_PORT=993
        self.M = None
        self.response = None

    def __str__(self):
        print "Python mail client"
 
    def login(self, username=user, password=pwd):
        self.M = imaplib.IMAP4_SSL(self.IMAP_SERVER, self.IMAP_PORT)
        status, self.response = self.M.login(username, password)
        return status

    def list_folders(self):
        response, folders = self.M.list()
        return map((lambda x : x.split(" ")[2:]), folders)

    def fetch(self, uid): pass

    def search(self, query): pass

    def select(self, mailbox): pass

    def messages_from(self, person):
        """ Gets all messages from a given person """
        response, message_ids = self.M.search(None, 'FROM', person) 
        return message_ids

    def select_folder(self, folder="inbox"):
        status, response = self.M.select(folder)
        return status

    def get_message(self, uid):
        """ Get a single email message by uid """
        status, response = self.M.fetch(uid, '(RFC822)')
        return response

    def list_mailboxes(self):
        self.select_mailbox()
        status, response = self.M.search(None, 'ALL')
        return response
        
    def logout(self):
        self.M.logout()

if __name__ == '__main__':

    main()

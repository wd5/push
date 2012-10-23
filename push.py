#!/usr/bin/env python

#################################
#
#  Push.py
#
#  A simple command line client for interacting with Gmail
# 
#  Example
#  
#  python push.py -u yourname@gmail.com -p password
#
##################################

import imaplib, sys, email, datetime

import argparse, itertools

def color_string(text):
    blue = '\033[36m'
    end  = '\033[0m'
    return blue + text + end

def autologin():
    """ 
        Utility function used for testing that enables
        a one line quick login

    """
    p = Push()
    p.login("", "")
    p.select_folder()
    return p

class MessageParser(object):

    @staticmethod
    def parse(message_string):
        """ Parse an email message """
        return email.message_from_string(message_string)

    @staticmethod
    def headers(email_message):
        return email_message.items()

    @staticmethod
    def msg_from(email_message_instance):
        return email_message_instance['From']

    @staticmethod
    def msg_to(email_message_instance):
        return email_message_instance['To']

    @staticmethod
    def msg_body(email_message_instance):
        """ Gets the message body """
        maintype = email_message_instance.get_content_maintype()
        if maintype == 'multipart':
            for part in email_message_instance.get_payload():
                if part.get_content_maintype() == 'text':
                    return part.get_payload()
        elif maintype == 'text':
            return email_message_instance.get_payload()


class PushClient(object):

    ALL_MAIL = "[Gmail]/All Mail"

    def __init__(self):
        self.IMAP_SERVER='imap.gmail.com'
        self.IMAP_PORT=993
        self.M = None
        self.response = None

    def __str__(self):
        print "Python mail client"
 
    def login(self, username, password):
        self.M = imaplib.IMAP4_SSL(self.IMAP_SERVER, self.IMAP_PORT)
        try:
            response, self.response = self.M.login(username, password)
            return response
        except imaplib.IMAP4.error, err:
            print(err)
            sys.exit(1)

    def list_folders(self):
        resp, data = self.M.list()
        return map((lambda x : x.split(" ")[2:]), data)

    def fetch(self, uid): pass

    def search(self, *args):
        """ Gets all messages from a given person """
        resp, data = self.M.search(None, *args) 
        return data

    def search_today(self):
        """ Find all messages sent/recieved today """
        date = (datetime.date.today() - datetime.timedelta(1)).strftime("%d-%b-%Y")
        resp, data = self.M.uid('search', None, '(SENTSINCE {date})'.format(date=date))
        return self.as_list(data)

    def count_emails_for_today(self):
        """ Get the number of emails for today """
        return len(self.search_today())

    def as_list(self, data):
        """ Returns message data as a list """
        return data[0].split()

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
        return self.as_list(data)

    def select_folder(self, folder="inbox"):
        resp, data = self.M.select(folder)
        return resp

    def get_message(self, message_id):
        """ Get a single email message by normal id """
        resp, data = self.M.fetch(message_id, '(RFC822)')
        return data[0][1] # Returns the actual message string

    def get_message_by_uid(self, uid):
        """ Get a single email message by uid """
        resp, data = self.M.uid('FETCH', str(uid), '(RFC822)')
        return self.as_list(data)

    # Unread email

    def unread_email(self):
        """ Returns the number of unopened email messages """
        return len(self.list_unread_email())

    def list_unread_email(self):
        messages = self.search('UnSeen')
        return self.as_list(messages)

    # Inbox

    def all_uids(self):
        """" Returns unique ids from the inbox """
        resp, data = self.M.uid('search', None, "ALL") 
        return data[0]

    def last_message(self):
        """ Returns the last email message id from the inbox """
        resp, data = self.M.search(None, "ALL")
        return data[0].split()[-1]
  
    def all_uids(self, folder="inbox"):
        """ Returns all uids from a folder """
        self.select_folder(folder)
        resp, data = self.M.uid('search', 'ALL')
        return self.as_list(data)

    def since(self, date_string):
        """ Returns all messages recieved after a given date 
            e.g self.since('01-Jan-2012') 
        """
        resp, data = self.M.uid('search', '(SINCE %s)' % date_string)
        return self.as_list(data)

    def inbox(self, limit=10):
        """ Get messages info from inbox """
        self.select_folder("inbox")
        messages = self.all_uids()
        rev  = itertools.islice(reversed(messages), 0, limit)
        data = self.M.uid('FETCH', ','.join(map(str,rev)) , '(BODY.PEEK[HEADER.FIELDS (From Subject)] RFC822.SIZE)')
        return data

    def logout(self):
        self.M.logout()


# Methods for printing out data to the console 


def mail_menu(mail):
    print(color_string("\nHello. You have %d unread email messages\n" % mail.unread_email()))
    print("What would you like to do?")
    print("1: List unread email")
    print("2: Read a message")
    print("3: List folders")
    print("4: Show inbox")
    print("\n--------------------\nType 'q' or 'quit' to exit\n")

def render_message(message_id):
    message = mail.get_message(message_id)
    parsed = MessageParser.parse(message)
    print("\n------------------------\n")
    print("To : %s" % (MessageParser.msg_to(parsed)))
    print("From : %s" % (MessageParser.msg_from(parsed)))
    print("\n")
    print(MessageParser.msg_body(parsed))
    print("\n------------------------\n")            


def main(mail):
    try:
        while True:
            mail_menu(mail)
            cmd = raw_input('Enter command: ').strip()
            if cmd == "1":
                print(mail.list_unread_email())
            # Print out the email message in the terminal
            elif cmd == "2": 
                message_id = raw_input("Please enter message id: ")
                render_message(message_id)
            elif cmd == "3":
                print(mail.list_folders())
            elif cmd == "4":
                print("Inbox")
            elif (cmd == "q") or (cmd == "quit"):
                print("\nBye...\n")
                break
                sys.exit(0)
            else: main(mail)
    except KeyboardInterrupt:
        mail.logout()
        sys.exit(0)
    except: 
        mail.logout()
        sys.exit(1)
      
  
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username", help="User name")
    parser.add_argument("-p", "--password", help="Password")

    args = parser.parse_args()
   
    mail = PushClient()

    mail.login(args.username, args.password)
    mail.select_folder() # select the inbox folder
    main(mail)


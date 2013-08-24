import imaplib, re
import quopri
import os
import time
import socket
import email
import urllib2
import json
from email.header import decode_header

#Fillup the REST params in a dic
#Encode JSON, add API KEY header
#Make request

def postToPT(subj, content):
    dict_content = {'description':content,'name':subj}
    json_content = json.dumps(dict_content, encoding='iso-8859-1')
    encoded_content = json_content.encode('iso-8859-1')
    headers = {"Content-Type":"application/json", "X-TrackerToken":"__TOKENID__"}
    request = urllib2.Request("https://www.pivotaltracker.com/services/v5/projects/__PROJECTID__/stories", encoded_content, headers)
    try: 
        urllib2.urlopen(request)
    except urllib2.HTTPError, e:
        print e.code
    except urllib2.URLError, e:
        print e.args
    print 'Posted'


#imap connection to mail server
#generate application specific password in case of gmail
#2factor auth needs to be enabled to generate application specific password
def checkMail():
    imap_host = 'imap.gmail.com'
    mail = imaplib.IMAP4_SSL(imap_host)
    mail.login("__email__", "__app-specific-password__")
    mail.select("inbox") # connect to inbox.
    result, data = mail.uid('search', None, 'UNSEEN')
    for num in data[0].split():
        typ, data = mail.fetch(num, '(RFC822)')
        msg = email.message_from_string(data[0][1])
        sender = msg['from']
        subj, encoding = email.Header.decode_header(msg['subject'])[0]
        if len(re.findall(r'\[([^]]*)\]',subj)) != 2:
            continue
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get_content_subtype() != 'plain':
                continue
            content = part.get_payload()
            ncontent = quopri.decodestring(content)
            print 'Posting to PT'
            print subj, ncontent
            postToPT(subj, ncontent)
    print 'Exitting'


checkMail()

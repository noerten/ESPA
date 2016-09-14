
def download_attach_gain():
    from datetime import datetime
    import email, imaplib, os, re
    import shelve
    import keyring
    from PyQt4 import QtGui
    from PyQt4.QtGui import QMessageBox
    __version__ = "0.5"
    try:
        #check_list=dict.fromkeys(['download_d','show_d','download_g',
        #'show_g','download_p','show_p'])
        s=shelve.open('config.db', flag="r")
        mail_dict=s['mails']
        check_dict=s['checkboxes']
        if check_dict[0]==False and check_dict[2]==False and check_dict[4]==False:
            sys.exit()
        user=mail_dict['mail1']
        pwd=keyring.get_password('ESPA_email', user)
        s.close()
        showlog=list() #what we show to user
        loglist=list()
        # connecting to the gmail imap server
      #  testcount=0
        fold=0
        folde=0
        date_month = ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
        gainpath=os.path.join('Statements','Gain')
        dormanpath=os.path.join('Statements','Dorman')
        list_path=(gainpath, dormanpath)
        for onepath in list_path:
            if onepath==gainpath and check_dict[2]==False:
                continue
            if onepath==dormanpath and check_dict[0]==False:
                continue
        #look for files:
            try:
                for pdffile in os.listdir(onepath):
                    if pdffile.endswith(".PDF") or pdffile.endswith(".pdf"):
                        loglist.append(pdffile)
                ld=loglist[len(loglist)-1]
                ld=ld[0:10]
                last_d=ld.split('-')
                x=int(last_d[1])
                mon=date_month[x-1]
                last_date=last_d[2]+'-'+mon+'-'+last_d[0]
                print mon
                print 'last date', last_date      
            except:
                last_date='20-Aug-2000'
                loglist=list()
                print 'nothing before'
            try:
                m = imaplib.IMAP4_SSL("imap.gmail.com")
                m.login(user,pwd)
            #    sys.exit()
                #The SENTSINCE date format is DD-Jun-YYYY. In python, that would be strftime('%d-%b-%Y').
                #date = (datetime.date.today() - datetime.timedelta(1)).strftime("%d-%b-%Y")
                #result, data = mail.uid('search', None, '(SENTSINCE {date})'.format(date=date))
                #print m.list()  use to get all the mailboxes
                m.select() # here you a can choose a mail box like INBOX instead
                if onepath == gainpath:
                    resp, items = m.search(None, '(FROM "gfstatements@gaincapital.com")','(SUBJECT "DAILY CLIENT STATEMENT")',\
                                           '(SENTSINCE {date})'.format(date=last_date)) # IMAP rules here (check http://www.example-code.com/csharp/imap-search-critera.asp)
                elif onepath == dormanpath:
                    resp, items = m.search(None, '(FROM "DORMANLLC@ameritech.net")','(SUBJECT "Attached Daily Statement")',\
                                           '(SENTSINCE {date})'.format(date=last_date)) # IMAP rules here (check http://www.example-code.com/csharp/imap-search-critera.asp)
                items = items[0].split() # getting the mails id
            except:
                print 'fail'
                err_connect = QMessageBox.warning(None, ("ESPA"),
                                       ("Cannot connect to email"))
            for emailid in items:
                resp, data = m.fetch(emailid, "(RFC822)") # fetching the mail, "`(RFC822)`" means "get the whole stuff", but you can ask for headers only, etc
                email_body = data[0][1] # getting the mail content
                mail = email.message_from_string(email_body) # parsing the mail content to get a mail object 
            #        else: continue
            #    Check if any attachments at all
                if mail.get_content_maintype() != 'multipart':
                    continue
            # we use walk to create a generator so we can iterate on the parts and forget about the recursive headach
                for part in mail.walk():
                    #multipart are just containers, so we skip them
                    if part.get_content_maintype() == 'multipart':
                        continue
                    if onepath == gainpath:
                        if part.get_content_type() == "text/plain": # ignore attachments/html
                            body = part.get_payload(decode=True)
                            dat=re.findall('as of ([0-9]+)', body)
                            for num in dat:
                                date=int(num)
                        # is this part an attachment ?
                        if part.get('Content-Disposition') is None:
                            continue
                        filename = part.get_filename()
                        if filename=='PrivacyNotice.pdf': continue
                        newfn=str(date)+'_'+filename
                        newfn=newfn[0:4]+'-'+newfn[4:6]+'-'+newfn[6:]
                        att_path = os.path.join(onepath, newfn)
                    if onepath == dormanpath:
                        if part.get_content_type() == "text/plain": # ignore attachments/html
                            body = part.get_payload(decode=True)
                            dat=re.findall('for (.+[0-9]+)', body)
                            cur_month = dat[0]
                            x=datetime.strptime(cur_month, '%b %d, %Y')
                            date = x.strftime('%Y%m%d')
                        # is this part an attachment ?
                        if part.get('Content-Disposition') is None:
                            continue
                        filename = part.get_filename()
                        if filename=='PrivacyNotice.pdf': continue
                        newfn=date+'_'+filename
                        newfn=newfn[0:4]+'-'+newfn[4:6]+'-'+newfn[6:]
                        att_path = os.path.join(onepath, newfn)
            #check if file is already downloaded

                    if fold<1:
                        fold=fold+1
                        print 'Checking existence of folder with statements' 
                    if not os.path.isdir(onepath):
                        print 'Creating folder with statements' 
                        os.makedirs(onepath)
                        folde=folde+1
                    if os.path.isdir(onepath) and folde<1:
                        folde=folde+1
                        print '''Folder with statements exists '''
                    #Check if its already there
                    if os.path.isfile(att_path) :
                        print date,'statement exists'
                    if not os.path.isfile(att_path) :
                        # finally write the stuff
                        fp = open(att_path, 'wb')
                        fp.write(part.get_payload(decode=True))
                        print 'Saved',newfn,'Statement'
                        showlog.append(newfn)
                        fp.close()
                        
                    loglist.append(newfn)
          #          testcount=testcount+1
          #      print testcount
          #      if testcount>2: break
            #create or check existance of log
            print showlog
            showmelog='\n'.join(showlog)    

        m.close()
        m.logout()
        msgBox = QMessageBox()
        msgBox.setWindowTitle('ESPA')
        if len(showmelog)==0:
            msgBox.setText('Nothing was downloaded')
        else:
            msgBox.setText('Following statements were downloaded:\n'+showmelog)
        msgBox.exec_()
        #    QMessageBox.information("ListWidget", "You clicked: "+showmelog)
                    
    except:
        err_shelve = QMessageBox.warning(None, ("ESPA"),
                                   ('''Nothing was set to download, go to "Settings"'''))
        
if __name__ == '__main__':
    
    download_attach_gain()
    

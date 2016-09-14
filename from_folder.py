#!/usr/bin/env python
def states_from_folder():
    import os
    import sys
    import shelve
    import re
    from datetime import datetime
    import shutil
    from StringIO import StringIO
    from pdfminer.pdfparser import PDFParser
    from pdfminer.pdfdocument import PDFDocument
    from pdfminer.pdfpage import PDFPage
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.pdfdevice import PDFDevice
    from pdfminer.layout import LAParams
    from pdfminer.converter import  TextConverter # , XMLConverter, HTMLConverter
    from PyQt4 import QtGui
    from PyQt4.QtGui import QMessageBox
    __version__ = "0.2.0"
    try:
        s=shelve.open('config.db','r')
        source_path=s['select_folder']
        get_from_subfolder_item=s['get_from_subfolder']

        showmelog=[]
        gainpath=os.path.join('Statements','Gain')
        dormanpath=os.path.join('Statements','Dorman')
        phillippath=os.path.join('Statements','Phillip')
        #admispath=os.path.join('Statements','Admis')
        list_path=(gainpath, dormanpath, phillippath)
        #for onepath in list_path:
        for root, dirs, files in os.walk(source_path):
            for pdffile in files:
                if pdffile.endswith(".PDF") or pdffile.endswith(".pdf"):
                    filepath = os.path.join(root, pdffile)
                    fp = open(filepath, 'rb')
                    parser = PDFParser(fp)
                    document = PDFDocument(parser)
                    if not document.is_extractable:
                        raise PDFTextExtractionNotAllowed
                    rsrcmgr = PDFResourceManager()
                    retstr = StringIO()
                    laparams = LAParams()
                    codec = 'utf-8'
                    device = TextConverter(rsrcmgr, retstr, codec = codec, laparams = laparams)
                    interpreter = PDFPageInterpreter(rsrcmgr, device)
                    count_page=0
                    for page in PDFPage.create_pages(document):
                        count_page=count_page+1
                        if count_page>1:
                            break
                        interpreter.process_page(page)
                        data =  retstr.getvalue()
                        
                    brokers=['DORMAN TRADING','GAIN CAPITAL', 'Daily Activity Statement']#, 3rd for phillip
                            # 'Daily Customer Account Status']#the last one is for admis
                    for broker in brokers:
                        match=re.search(broker, data)
                        if match:
                            if broker == 'DORMAN TRADING':
                                get_date = re.findall('STATEMENT DATE: (.+[0-9])', data)
                                get_date = get_date[0].replace(',','')
                                date_object = datetime.strptime(get_date, '%b %d %Y')
                                pdf_name = date_object.strftime('%Y-%m-%d')
                                pdf_name = pdf_name+pdffile[len(pdffile)-4:]
                                dorman_f_path=os.path.join('Statements','Dorman',pdf_name)
                                if not os.path.exists(dormanpath):
                                    os.makedirs(dormanpath)
                                if os.path.exists(dorman_f_path):
                                    continue
                                else:
                                    showmelog.append(pdf_name)
                                    shutil.copy(filepath, dorman_f_path)
                                
                            elif broker == 'GAIN CAPITAL':
                                get_date = re.findall('Account Summary as of (.+[0-9])', data)
                                date_object = datetime.strptime(get_date[0], '%d-%b-%y')
                                pdf_name = date_object.strftime('%Y-%m-%d')
                                pdf_name = pdf_name+pdffile[len(pdffile)-4:]
                                
                                gain_f_path=os.path.join('Statements','Gain',pdf_name)
                                if not os.path.exists(gainpath):
                                    os.makedirs(gainpath)
                                if os.path.exists(gain_f_path):
                                    continue
                                else:
                                    showmelog.append(pdf_name)
                                    shutil.copy(filepath, gain_f_path)
                                    
                            elif broker == 'Daily Activity Statement':
                                get_date = re.findall('Date (.*[0-9])', data)
                                get_date = get_date[0]
                                get_date = re.findall('\s(.*[0-9])', get_date)
                                date_object = datetime.strptime(get_date[0], '%m/%d/%Y')
                                date_for_pdf_name = date_object.strftime('%Y-%m-%d')
                                get_acc = re.findall('Account (.*[0-9])', data)
                                get_acc = get_acc[0]
                                acc = re.findall('\s(.*[0-9])', get_acc)
                                acc=acc[0]
                                pdf_name = date_for_pdf_name+'_'+acc+'.pdf'
                                print pdf_name
                                phillip_f_path=os.path.join('Statements','Phillip',pdf_name)
                                print phillip_f_path
                                if not os.path.exists(phillippath):
                                    os.makedirs(phillippath)
                                if os.path.exists(phillip_f_path):
                                    continue
                                else:
                                    showmelog.append(pdf_name)
                                    shutil.copy(filepath, phillip_f_path)

#                            elif broker == 'Daily Customer Account Status':
#                                get_date = re.findall('Business Date = (.+[0-9])', data)
#                                date_object = datetime.strptime(get_date[0], '%Y-%m-%d')
#                                print date_object
#                                date_for_pdf_name = date_object.strftime('%Y-%m-%d')
#                                11111
#                                get_acc = re.findall('Report For - (.+[0-9])', data)
#                                acc = get_acc[0]
#                                pdf_name = date_for_pdf_name+'-'+acc+'.pdf'
#                                print pdf_name
#                                admis_f_path=os.path.join('Statements','Admis',pdf_name)
#                                if not os.path.exists(admispath):
#                                    os.makedirs(admispath)
#                                if os.path.exists(admis_f_path):
#                                    continue
#                                else:
#                                    showmelog.append(pdf_name)
 #                                   shutil.copy(filepath, admis_f_path)
                            break
            if get_from_subfolder_item==True:
                pass
            
            else:
                break

        if len(showmelog)==0:
            err_shelve = QMessageBox.warning(None, ("ESPA"),
                                         ('Nothing was copied'))
        else:
            msgBox = QMessageBox()
            msgBox.setWindowTitle('ESPA')
            showmelog.sort()
            showlog='\n'.join(showmelog)
            msgBox.setText('Following statements were copied:\n'+showlog)
            msgBox.exec_()
    except:
        #print 'olala'
        err_shelve = QMessageBox.warning(None, ("ESPA"),
                                         ("You didn't select the folder to copy from."))

if __name__ == '__main__':
    states_from_folder()

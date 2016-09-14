def import_stats():
    from pdfminer.pdfparser import PDFParser
    from pdfminer.pdfdocument import PDFDocument
    from pdfminer.pdfpage import PDFPage
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.pdfdevice import PDFDevice
    from pdfminer.layout import LAParams
    from pdfminer.converter import  TextConverter # , XMLConverter, HTMLConverter
    import urllib2
    import re
    import os
    import sys
    import logging
    from StringIO import StringIO
    import sqlite3
    from PyQt4 import QtGui
    from PyQt4.QtGui import QMessageBox
    __version__ = "0.6.0"
    #with by row imprt
    showlog=list() #what we show to user
    column_count=0

    pdflist=list()
    
    deposit_list=[]
    dorman_pdf=[]
    dorman_pdf_mistake=[]
    gain_pdf=[]
    gain_pdf_mistake=[]
    phillip_pdf=[]
    phillip_pdf_mistake=[]
    
    if not os.path.exists('logs'):
        os.makedirs('logs')
    log_file = os.path.join('logs','logging.txt')
    logging.basicConfig(filename=log_file,level=logging.DEBUG,
                    format='\n\n%(asctime)s %(levelname)s %(name)s %(message)s')

    gainpath=os.path.join('Statements','Gain')
    dormanpath=os.path.join('Statements','Dorman')
    phillippath=os.path.join('Statements','Phillip')
    
    if not os.path.exists(dormanpath):
        os.makedirs(dormanpath)
    if not os.path.exists(gainpath):
        os.makedirs(gainpath)
    if not os.path.exists(phillippath):
        os.makedirs(phillippath)
        
    list_path=(gainpath, dormanpath, phillippath)
    for onepath in list_path:
        
        datalist=list()
        ##########################
        #dev
        if onepath==gainpath: continue
        if onepath==dormanpath: continue
        ##########################
        try:
            conn= sqlite3.connect('stat.sqlite3')
            cur=conn.cursor()
            if onepath==gainpath:
                cur.execute('SELECT Date FROM acc_stats_gain')
            elif onepath==dormanpath:
                cur.execute('SELECT Date FROM acc_stats_dorman')
            elif onepath==phillippath:
                cur.execute('SELECT Date FROM acc_stats_phillip')
            for row in cur:
                row=str(row[0])
                datalist.append(row)
            conn.close()
        except:
            try:
                conn.close()
            except:
                pass
            pass
     #   count_big=0
        conn = sqlite3.connect('stat.sqlite3', detect_types=sqlite3.PARSE_DECLTYPES)
        cur=conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS acc_stats_gain\
                    (Date DATE, Payments_Receipts REAL,\
                    Account_Cash_Balance REAL,\
                    Realized_Profit_Loss REAL, Premiums REAL,\
                    Commissions_and_Fees REAL, Clearing REAL,\
                    NFA REAL, Fees REAL, Commission REAL,\
                    New_Cash_Balance REAL,\
                    Open_Trade_Equity REAL, Total_Equity REAL,\
                    Option_Market_Value REAL,\
                    Long_Option_Value REAL,\
                    Short_Option_Value REAL,\
                    Net_Liquidating_Value REAL,\
                    Initial_Margin REAL, Maintenance_Margin REAL,\
                    Risk_Maintenance REAL, Risk_Initial REAL,\
                    Collateral_Used REAL,\
                    Margin_Default_Excess REAL,\
                    Total_Fees REAL, Total_Broker_Comm REAL,\
                    Cash_in_out TEXT)')
        
        cur.execute('CREATE TABLE IF NOT EXISTS acc_stats_dorman (Date DATE,\
                    Beginning_Balance REAL, Commission REAL, Clearing_Fees REAL,\
                    Exchange_Fees REAL,NFA_Fees REAL, Total_Fees REAL,\
                    Net_Profit_Loss_From_Trades REAL, Cash_Amounts REAL,\
                    Ending_Balance REAL, Open_Trade_Equity REAL, Total_Equity REAL,\
                    Net_Market_Value_Of_Options REAL, Account_Value_At_Market REAL,\
                    Initial_Margin_Requirment REAL, Maintenance_Margin_Requirement REAL,\
                    Excess_Equity REAL, Commissions_and_Fees REAL, Cash_in_out TEXT)')
        
        cur.execute('CREATE TABLE IF NOT EXISTS acc_stats_phillip (Date DATE,\
                    Beginning_Balance REAL, Adjustments REAL, Commission REAL,\
                    Clearing_Fee REAL, Globex_Fee REAL, NFA_Fee REAL, Platform REAL,\
                    Transaction_Fee REAL, US4_Swap_Val REAL, Realised_PL REAL,\
                    Option_Premium REAL, Ending_Balance REAL, Forward Value REAL,\
                    Open_Trade_Equity REAL, Open US4_Swap_Val REAL, Equity_Balance REAL,\
                    Long_Option_Value REAL, Short_Option_Value REAL,\
                    Net_Option_Value REAL, Net_Liquid_Value REAL, Collateral REAL,\
                    Equity_Collateral REAL, Initial_Margin REAL, Maint_Margin REAL,\
                    Margin_Ex_Def REAL, Commissions_and_Fees REAL, Cash_in_out TEXT)')
        

        for f in os.listdir(onepath):
            if f.endswith(".pdf") or f.endswith(".PDF"):
                fwopdf=f[:10]
                                
                if fwopdf in datalist:
                    print 'cont',fwopdf
                    continue
                else:
                    fdate=fwopdf
                print '\n\n',fdate,'\n\n'
                filepath=os.path.join(onepath, f)
                one_row=[fdate]
                fp = open(filepath, 'rb')
                # Create a PDF parser object associated with the file object.
                parser = PDFParser(fp)
                # Create a PDF document object that stores the document structure.
                document = PDFDocument(parser)
                # Check if the document allows text extraction. If not, abort.
                if not document.is_extractable:
                    raise PDFTextExtractionNotAllowed
                # Create a PDF resource manager object that stores shared resources.
                # Define parameters to the PDF device objet 
                rsrcmgr = PDFResourceManager()
                retstr = StringIO()
                laparams = LAParams()
                codec = 'utf-8'
                # Create a PDF device object
                device = TextConverter(rsrcmgr, retstr, codec = codec, laparams = laparams)
                # Create a PDF interpreter object
                interpreter = PDFPageInterpreter(rsrcmgr, device)

                # Process each page contained in the document
                for page in PDFPage.create_pages(document):
                    interpreter.process_page(page)
                    data =  retstr.getvalue()
                    
                #list w all items
                if onepath==gainpath:
                    data_rows=('PAYMENTS/RECEIPTS','ACCOUNT CASH BALANCE',
                               'REALIZED PROFIT/LOSS','PREMIUMS',
                               'COMMISSIONS & FEES','CLEARING','NFA','FEES',
                               'COMMISSION','NEW CASH BALANCE',
                               'OPEN TRADE EQUITY','TOTAL EQUITY',
                               'OPTION MARKET VALUE','LONG OPTION VALUE',
                               'SHORT OPTION VALUE', 'NET LIQUIDATING VALUE',
                               'INITIAL MARGIN','MAINTENANCE MARGIN',
                               'RISK MAINTENANCE','RISK INITIAL',
                               'COLLATERAL USED','MARGIN DEFAULT/EXCESS')
                elif onepath==dormanpath:
                    data_rows=('BEGINNING BALANCE', 'COMMISSION',
                               'CLEARING FEES', 'EXCHANGE FEES','NFA FEES',
                               'TOTAL FEES', 'NET PROFIT/LOSS FROM TRADES',
                               'CASH AMOUNTS', 'ENDING BALANCE',
                               'OPEN TRADE EQUITY', 'TOTAL EQUITY',
                               'NET MARKET VALUE OF OPTIONS',
                               'ACCOUNT VALUE AT MARKET',
                               'INITIAL MARGIN REQUIREMENT',
                               'MAINTENANCE MARGIN REQUIREMENT','EXCESS EQUITY')
                elif onepath == phillippath:
                    data_rows=('Beginning Balance', 'Adjustments',
                               'Commission', 'Clearing Fee','Globex Fee',
                               'NFA Fee', 'Platform', 'Transaction Fee',
                               'US4/Swap Val', 'Realised P/L', 'Option Premium',
                               'Ending Balance', 'Forward Value',
                               'Open Trade Equity', 'Open US4/Swap Val',
                               'Equity Balance', 'Long Option Value',
                               'Short Option Value', 'Net Option Value',
                               'Net Liquid. Value', 'Collateral',
                               'Equity Collateral', 'Initial Margin',
                               'Maint. Margin', 'Margin Ex/Def')
                           
                commiss=('COMMISSION', 'CLEARING FEES', 'EXCHANGE FEES',
                         'NFA FEES')
                margin_list=['INITIAL MARGIN','MAINTENANCE MARGIN',
                             'RISK MAINTENANCE','RISK INITIAL']
                for item in data_rows:
                    if onepath==gainpath:
                        reg=item+'.+R'
                        matches = re.findall(reg, data)
                        if not matches:
                            matches = 'VALU 0.00 CR 0.00 CR'
                    elif onepath==dormanpath:
                        reg=item+'.+'
                        matches = re.findall(reg, data)
                        if not matches:
                            matches = ['0.00']
                    elif onepath==phillippath:
                        reg=item+'.+'
                        matches = re.findall(reg, data)
                        if item == 'US4/Swap Val':
                            matches = [matches[-1]]
                        if item == 'Collateral':
                            matches = [matches[0]]

                    strmatches=''.join(matches)               
                    if onepath==gainpath:
                        strmatches=strmatches.replace(' ','')
                        numb = re.findall('.+?([0-9.]+).R$', strmatches)
                        cr_or_dr=re.findall('.+?[0-9.]+(.R)$', strmatches)
                        try:
                            item_numb=float(numb[0])
                            if cr_or_dr[0]=='DR':
                                if item in margin_list:
                                    item_numb=item_numb
                                else:
                                    item_numb=-item_numb
                            one_row.append(item_numb)                           
              #              column_count=column_count+1
            #                if column_count<
                        except:
                            continue
                    if onepath==dormanpath:
                        strmatches=''.join(matches)
                        strmatches=strmatches.split(' ')
                        strmatches = filter(bool, strmatches)
                        omgomg='.*?([0-9]*)[\,]{0,1}([0-9.]+)'
                        numb = re.findall(omgomg, strmatches[-1])
                        cr_or_dr=re.findall('.*?[0-9.]+(DR)$', strmatches[-1])
                        try:
                            if item in commiss:
                                wwwww=''.join(numb[len(numb)-1])
                                item_numb=float(wwwww)
                            else:
                                wwwww=''.join(numb[0])
                                item_numb=float(wwwww)
                            if len(cr_or_dr)>0 and cr_or_dr[0]=='DR':
                                item_numb=-item_numb
                            one_row.append(item_numb)
                        except:
                            print 'didnt manage to get a number'
                            logging.error('didnt manage to get a numb from dorman %s' % fdate, exc_info=True)
                            continue
                        
                    if onepath==phillippath:
                        strmatches=''.join(matches)
                        strmatches=strmatches.split(' ')
                        strmatches = filter(bool, strmatches)
                        omgomg='.*?(-*[0-9]*)[\,]{0,1}([0-9.]+)'
                        numb = re.findall(omgomg, strmatches[-1])
                        try:
                            wwwww=''.join(numb[0])
                            item_numb=float(wwwww)
                            one_row.append(item_numb)
                        except:
                            print 'didnt manage to get a number'
                            logging.error('didnt manage to get a numb from dorman %s' % fdate, exc_info=True)
                            continue
                if onepath==dormanpath:
                    if 'WIRE TRANSFER RECEIVED' in data:
                        one_row.append('deposit')
                    elif 'WIRE TRANSFER SENT' in data:
                        one_row.append('cashout')
                    else:
                        one_row.append('nothing')
                if onepath==gainpath:
                    if 'Transfer from holding account' in data:
                        one_row.append('deposit')
                    elif 'Transfer to holding account' in data:
                        one_row.append('cashout')
                    else:
                        one_row.append('nothing')
                if onepath == phillippath:
                    #
                    ##
                    ###
                    #add transfers for phillip
                    one_row.append('nothing')
                print one_row    
                print '\n'
#                print 'column count', column_count
#                column_count=column_count+1
#                if column_count>2:
#                    print 'olola'
#                    break

                if onepath==gainpath:
                    try:

                        cur.execute('INSERT INTO acc_stats_gain (Date, Payments_Receipts,\
                                    Account_Cash_Balance, Realized_Profit_Loss, Premiums,\
                                    Commissions_and_Fees, Clearing, NFA, Fees, Commission,\
                                    New_Cash_Balance, Open_Trade_Equity, Total_Equity,\
                                    Option_Market_Value, Long_Option_Value, Short_Option_Value,\
                                    Net_Liquidating_Value, Initial_Margin, Maintenance_Margin,\
                                    Risk_Maintenance, Risk_Initial, Collateral_Used, Margin_Default_Excess, Cash_in_out)\
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', one_row)
                        cur.execute('UPDATE acc_stats_gain SET Total_Broker_Comm=Fees+Commission, Total_Fees=Clearing+NFA')
                        conn.commit()
                        gain_pdf.append(f)
                        print 'added gain', f

                    except:
                        gain_pdf_mistake.append(f)
                        print 'didnt add gain (mistake)', f
                        logging.error('didnt add gain (mistake)', exc_info=True)

                elif onepath==dormanpath:
                        #gain total comis and fees=dorman comiss+totalfees
                        #dorman commiss=gain_fees+commiss
                        #dorman exch+clearing=gain clearing
                    try:
                        
                        cur.execute('INSERT INTO acc_stats_dorman (Date, Beginning_Balance,\
                                    Commission, Clearing_Fees, Exchange_Fees,\
                                    NFA_Fees, Total_Fees, Net_Profit_Loss_From_Trades, Cash_Amounts,\
                                    Ending_Balance, Open_Trade_Equity, Total_Equity,\
                                    Net_Market_Value_Of_Options, Account_Value_At_Market,\
                                    Initial_Margin_Requirment, Maintenance_Margin_Requirement,\
                                    Excess_Equity, Cash_in_out) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', one_row)
                        cur.execute('UPDATE acc_stats_dorman SET Commissions_and_Fees=Total_Fees+Commission')
                        conn.commit()
                        print 'added dorman', f
                        dorman_pdf.append(f)
                    except:
                        print 'didnt add dorman (mistake)', f
                        dorman_pdf_mistake.append(f)
                        logging.error('didnt add dorman (mistake)', exc_info=True)
#####################################
                elif onepath==phillippath:
                    try:
                        cur.execute('INSERT INTO acc_stats_phillip (Date) VALUE (?)', one_row[0])
                        print '000'
                        cur.execute('INSERT INTO acc_stats_phillip (Date,\
                                    Beginning_Balance, Adjustments, Commission,\
                                    Clearing_Fee, Globex_Fee, NFA_Fee, Platform,\
                                    Transaction_Fee, US4_Swap_Val, Realised_PL,\
                                    Option_Premium, Ending_Balance, Forward Value,\
                                    Open_Trade_Equity, Open US4_Swap_Val, Equity_Balance,\
                                    Long_Option_Value, Short_Option_Value,\
                                    Net_Option_Value, Net_Liquid_Value, Collateral,\
                                    Equity_Collateral, Initial_Margin, Maint_Margin,\
                                    Margin_Ex_Def, Cash_in_out) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', one_row)
                        print '1111'
                        cur.execute('UPDATE acc_stats_phillip SET\
                                    Commissions_and_Fees=Commission+Clearing_Fee+NFA_Fee+Platform+\
                                    Globex_Fee+Transaction_Fee')
                        conn.commit()
                        print 'added phillip', f
                        phillip_pdf.append(f)
                    except:
                        print 'didnt add phillip (mistake)', f
                        phillip_pdf_mistake.append(f)
                        logging.error('didnt add phillip (mistake)', exc_info=True)

    conn.close()
    mistakes_list=gain_pdf_mistake+dorman_pdf_mistake+phillip_pdf_mistake
    show_mistakes='\n'.join(mistakes_list)
    statements_list=gain_pdf+dorman_pdf+phillip_pdf
    show_statements='\n'.join(statements_list)
    msgBox = QMessageBox()
    msgBox.setWindowTitle('ESPA')
    if len(mistakes_list)==0 and len(statements_list)==0:
        msgBox.setText('Nothing was found to import')
        print 'len=0'
    else:
        if len(mistakes_list)!=0 and len(statements_list)==0:
            msgBox.setText('Statistics from following statements were NOT imported\n(nothing was imported because of mistakes):\n'+show_mistakes)
        elif len(mistakes_list)==0 and len(statements_list)!=0:
            msgBox.setText('Statistics from following statements were imported:\n'+show_statements)
        elif len(mistakes_list)!=0 and len(statements_list)!=0:
            msgBox.setText('Statistics from following statements were NOT imported:\n(nothing was imported because of mistakes)'
                           +show_mistakes+'\nStatistics from following statements were imported:\n'+show_statements)
    msgBox.exec_()    
if __name__ == '__main__':
    import_stats()



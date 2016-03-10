import sqlite3
import matplotlib
import pandas as pd
import numpy as np
import matplotlib.mlab as mlab
from datetime import datetime
from collections import Counter
import shelve
from PyQt4 import QtGui
from PyQt4.QtGui import QMessageBox
import os
import logging
def res_distr():
    if not os.path.exists('logs'):
        os.makedirs('logs')
    log_file = os.path.join('logs','logging.txt')
    logging.basicConfig(filename=log_file,level=logging.DEBUG,
                    format='\n\n%(asctime)s %(levelname)s %(name)s %(message)s')

    try:
        s=shelve.open('config.db', flag="r")
        check_dict=s['checkboxes']
    except:
        err_shelve = QMessageBox.warning(None, ("ESPA"),
                                       ('''Nothing was set to show, go to "Settings"'''))
    try:
        delta=0
        prev=1
        delta_list=list()
        delta_list2=list()
        conn=sqlite3.connect('stat.sqlite3')
        cur=conn.cursor()
        #check_list=dict.fromkeys(['download_d','download_g','show_d','show_g'])
        if check_dict[3]==True:
            cur.execute('SELECT Net_Liquidating_Value FROM acc_stats_gain')
            g=[]
            for row in cur:
                g.append(row)
        else:
            g=[]

        if check_dict[2]==True:
            cur.execute('SELECT Account_Value_At_Market FROM acc_stats_dorman')
            d=[]
            for row in cur:
                d.append(row)
        else:
            d=[]
        conn.close()
        merged_list=d+g
        for row in merged_list:
            delta_list.append(row)
        count=0
        for row in delta_list:
            count=count+1
            num=row[0]
            if prev==0:
                continue
            else:
                delta=(num-prev)/prev
            prev=num
            if delta>0.8 or delta<-0.8:
                continue
            else:
                delta_list2.append(delta)
        delta_list2[0]=0.0
        numb_of_bins=np.ceil((abs(min(delta_list2))+abs(max(delta_list2)))*100)
        axisx=sorted(delta_list2)
        axisx=np.array(axisx)
        mu=sum(delta_list2)/(len(delta_list2))
        std_dev=np.std(delta_list2, ddof=1)
        distr = mlab.normpdf(axisx, mu, std_dev)
    except:
        axisx=[]
        distr=[]
        delta_list=[]
        numb_of_bins=[]
        print 'problem in res_distr'
        logging.error('problem in res_distr', exc_info=True)
    return axisx, distr, delta_list2, numb_of_bins
#res_distr()

def get_date_value(value):
    
    if value=='equity' or value=='equity w/o transfers':
        request=['Account_Value_At_Market','Net_Liquidating_Value']
    if value=='balance':
        request=['Ending_Balance','New_Cash_Balance']
    if value=='realized_pl':
        request=['Net_Profit_Loss_From_Trades','Realized_Profit_Loss']
    if value=='cum_realized_pl':
        request=['Net_Profit_Loss_From_Trades','Realized_Profit_Loss']
    if value=='init_margin':
        request=['Initial_Margin_Requirment','Initial_Margin']
    if value=='cum_comm_fees':
        request=['Commissions_and_Fees','Commissions_and_Fees']
    try:
        s=shelve.open('config.db', flag="r")
        check_dict=s['checkboxes']
    except:
        err_shelve = QMessageBox.warning(None, ("ESPA"),
                                   ("Nothing was set to show"))
    try:
#check_list=dict.fromkeys(['download_d','download_g','show_d','show_g'])
        conn=sqlite3.connect('stat.sqlite3',detect_types=sqlite3.PARSE_DECLTYPES)
        cur=conn.cursor()
        if check_dict[2]==True:
            cur.execute('SELECT Date, %s FROM acc_stats_dorman ORDER BY Date'
                        % (request[0]))
            d=cur.fetchall()
            d=dict(d)
        else:
            d={}
        if check_dict[3]==True:
            cur.execute('SELECT Date, %s FROM acc_stats_gain ORDER BY Date'
                        % (request[1]))
            g=cur.fetchall()
            g=dict(g)
        else:
            g={}
        if value=='equity w/o transfers' or value=='cum_comm_fees':
            if value=='equity w/o transfers':
                if check_dict[2]==True:
                    cur.execute('''SELECT Date, Cash_Amounts FROM acc_stats_dorman\
                                WHERE Cash_in_out IS NOT 'nothing' ORDER BY Date''')
                    d_cash=cur.fetchall()
                    d_cash=dict(d_cash)
                else:
                    d_cash={}
                if check_dict[3]==True:
                    cur.execute('''SELECT Date, Payments_Receipts\
                                FROM acc_stats_gain\
                                WHERE Cash_in_out IS NOT 'nothing' ORDER BY Date''')
                    g_cash=cur.fetchall()
                    g_cash=dict(g_cash)
                else:
                    g_cash={}
            if value=='cum_comm_fees':
                if check_dict[2]==True:
                    cur.execute('''SELECT Date, Cash_Amounts FROM acc_stats_dorman\
                                WHERE Cash_in_out IS 'nothing' ORDER BY Date''')
                    d_cash=cur.fetchall()
                    d_cash=dict(d_cash)
                else:
                    d_cash={}
                if check_dict[3]==True:
                    cur.execute('''SELECT Date, Payments_Receipts FROM acc_stats_gain\
                                WHERE Cash_in_out IS 'nothing' ORDER BY Date''')
                    g_cash=cur.fetchall()
                    g_cash=dict(g_cash)
                else:
                    g_cash={}
    #####################
            temp_cash_d_list_value=[]
            cash_d_list_value=[]
            cash_d_list_key=[]
            temp_cash_dd={k:d_cash.get(k,0) for k in set(d)}
            temp_cash_gg={k:g_cash.get(k,0) for k in set(g)}
            temp_cash_d={k:temp_cash_dd.get(k,0)+temp_cash_gg.get(k,0)
                         for k in set(temp_cash_dd) | set(temp_cash_gg)}
            for k in reversed(sorted(temp_cash_d)):
                temp_cash_d_list_value.append(temp_cash_d[k])
                cash_d_list_key.append(k)
            temp_pos=0
            if value=='equity w/o transfers':
                for i in temp_cash_d_list_value:
                    k=sum(temp_cash_d_list_value[temp_pos:])
                    cash_d_list_value.append(k)
                    temp_pos=temp_pos+1
            else: cash_d_list_value=temp_cash_d_list_value
            cash_d_list_value=list(reversed(cash_d_list_value))
            cash_d_list_key=list(reversed(cash_d_list_key))
            dict_cash=dict(zip(cash_d_list_key,cash_d_list_value))
            lissst_date=[]
            lissst_value=[]
        conn.close()

        list_date=[]
        list_value=[]
        if value=='equity w/o transfers':
            full_dict={k:d.get(k,0)+g.get(k,0)-dict_cash.get(k,0)
                       for k in set(d) | set(g)}
        elif value=='cum_comm_fees':
            full_dict={k:d.get(k,0)+g.get(k,0)+dict_cash.get(k,0)
                       for k in set(d) | set(g)}        
        else:
            full_dict= {k: d.get(k, 0) + g.get(k, 0) for k in set(d) | set(g)}    
        for	k in sorted(full_dict):
            list_date.append(k)
            list_value.append(full_dict[k])
        if value=='cum_realized_pl' or value=='cum_comm_fees':
            arr=np.array(list_value)
            arr=np.cumsum(arr)
            list_value=list(arr)
        else:
            pass
    except:
        list_date=[]
        list_value=[]
        print 'problem in get_date_value'
        logging.error('problem in get_date_value', exc_info=True)

    return list_date, list_value
#get_date_value('equity w/o transfers')

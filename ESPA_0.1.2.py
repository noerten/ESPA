#!/usr/bin/env python

import numpy as np
import os
import sys
import random
import shelve
import sqlite3

import keyring
import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.dates import date2num
from matplotlib.figure import Figure
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')
import pandas as pd
from PyQt4 import QtCore
from PyQt4.QtCore import QCoreApplication, Qt
from PyQt4 import QtGui
from PyQt4.QtGui import QListWidget, QListWidgetItem, QApplication, QMessageBox
from PyQt4 import QtSql

import requests
from requests import *
from from_folder import states_from_folder
from dnld_attach import download_attach_gain
from pdfparser import import_stats
__version__ = "0.2.0"

class Myplot(QtGui.QTabWidget):
    def __init__(self, parent=None):
        super(Myplot, self).__init__(parent)
        self.setTabPosition(QtGui.QTabWidget.West)
        self.tab1 = QtGui.QWidget()	
        self.tab2 = QtGui.QWidget()
        self.tab3 = QtGui.QTabWidget()
        self.tab3_1 = QtGui.QWidget()
        self.tab3_2 = QtGui.QWidget()
        self.tab3_3 = QtGui.QWidget()
        
        self.addTab(self.tab1,"Charts")
        self.addTab(self.tab2,"Analysis")
        self.addTab(self.tab3,"Database")
        self.tab3.addTab(self.tab3_1,"Dorman")
        self.tab3.addTab(self.tab3_2,"Gain")
        self.tab3.addTab(self.tab3_3,"Phillip")
        self.setCurrentIndex(2)
        self.figure = plt.figure(frameon=True, tight_layout=False)
        self.list_w_series()
        self.currentChanged.connect(self.clicked)
        self.add_checks()
        try:
            settings_path=os.path.join('logs','logging.txt')
            if not os.path.exists(dormanpath):
                pass
            else:
                self.clicked()
        except:
            pass
        try:
            self.add_table_dorman()
        except:
            pass
        try:
            self.add_table_gain()
        except:
            pass
        try:
            self.add_table_phillip()
        except:
            pass
 #   def test_print(self):
 #       print self.dwmqy_btngroup.checkedId()
    def list_w_series(self):
       # self.rb1=QtGui.QRadioButton('D')
      #  self.rb2=QtGui.QRadioButton('W')
        #self.rb3=QtGui.QRadioButton('M')
        #self.rb4=QtGui.QRadioButton('Q')
        #self.rb5=QtGui.QRadioButton('Y')
      #  self.dwmqy_btngroup=QtGui.QButtonGroup()
       # self.dwmqy_btngroup.addButton(self.rb1,1)
        #self.dwmqy_btngroup.addButton(self.rb2,2)
        #self.dwmqy_btngroup.addButton(self.rb3,3)
        #self.dwmqy_btngroup.addButton(self.rb4,4)
        #self.dwmqy_btngroup.addButton(self.rb5,5)

      #  self.dwmqy_btngroup.buttonClicked.connect(self.test_print)
       # print self.dwmqy_btngroup.checkedButton
        #create model with future checable items
        self.series_list_model = QtGui.QStandardItemModel()
        #using view we will display it
        self.series_list_view = QtGui.QListView()
     #   self.series_list_view.setFlow(QtGui.QListView.LeftToRight)
        self.series_list_view.setFixedWidth(180)
        self.series_list_view.setModel(self.series_list_model)
        self.series_list_view.setEditTriggers(QtGui.QAbstractItemView.
                                              NoEditTriggers)
        self.series_list_view.setSelectionMode(QtGui.QAbstractItemView.
                                              NoSelection)
        self.series_list_view.setFocusPolicy(QtCore.Qt.NoFocus)
        self.series_list_model.itemChanged.connect(self.show_plot)
        
    def add_checks(self):
        self.canvas = FigureCanvas(self.figure)
      #  tab1_RB_layout=QtGui.QHBoxLayout()
      #  tab1_RB_layout.addWidget(self.rb1)
      #  tab1_RB_layout.addWidget(self.rb2)
      #  tab1_RB_layout.addWidget(self.rb3)
      #  tab1_RB_layout.addWidget(self.rb4)
      #  tab1_RB_layout.addWidget(self.rb5)
        

        tab1_RB_list_layout=QtGui.QVBoxLayout()
       # tab1_RB_list_layout.addLayout(tab1_RB_layout)
        
        tab1_RB_list_layout.addWidget(self.series_list_view)
        tab1_layout=QtGui.QHBoxLayout()
        tab1_layout.addLayout(tab1_RB_list_layout)
        tab1_layout.addWidget(self.canvas)
        self.tab1.setLayout(tab1_layout)
        self.figure2 = plt.figure(frameon=True, tight_layout=False)
        self.canvas2 = FigureCanvas(self.figure2)
        tab2_layout=QtGui.QHBoxLayout()
        tab2_layout.addWidget(self.canvas2)
        self.tab2.setLayout(tab2_layout)
        #self.refresh_btn = QtGui.QPushButton('Save', self)
       # self.refresh.clicked.connect(self.model_d.select())

    def add_table_dorman(self):
        tab3_1_view = QtGui.QTableView()
       # tab3_1_refr_btn = QtGui.QPushButton('Refresh')
        db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("stat.sqlite3")
        db.open()
        tab3_1_model = QtSql.QSqlTableModel()
        tab3_1_model.setTable('acc_stats_dorman') 
        tab3_1_model.select()
        tab3_1_view.setModel(tab3_1_model)
        tab3_1_view.setAlternatingRowColors(True)
        tab3_1_view.resizeColumnsToContents()
        tab3_1_view.resizeRowsToContents()
        tab3_1_view.setSortingEnabled(True)
        tab3_1_view.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        tab3_1_layout=QtGui.QVBoxLayout()
     #   tab3_1_layout.addWidget(tab3_1_refr_btn)
        tab3_1_layout.addWidget(tab3_1_view)
        self.tab3_1.setLayout(tab3_1_layout)##########################
        
    def add_table_gain(self):
        tab3_2_view = QtGui.QTableView()
       # tab3_2_refr_btn = QtGui.QPushButton('Refresh')
        db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("stat.sqlite3")
        db.open()
        tab3_2_model = QtSql.QSqlTableModel()
        tab3_2_model.setTable('acc_stats_gain') 
        tab3_2_model.select()
        tab3_2_view.setModel(tab3_2_model)
        tab3_2_view.setAlternatingRowColors(True)
        tab3_2_view.resizeColumnsToContents()
        tab3_2_view.resizeRowsToContents()
        tab3_2_view.setSortingEnabled(True)
        tab3_2_view.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

        tab3_2_layout=QtGui.QVBoxLayout()
     #   tab3_2_layout.addWidget(tab3_2_refr_btn)
        tab3_2_layout.addWidget(tab3_2_view)
        self.tab3_2.setLayout(tab3_2_layout)##########################

    def add_table_phillip(self):
        tab3_3_view = QtGui.QTableView()
       # tab3_2_refr_btn = QtGui.QPushButton('Refresh')
        db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("stat.sqlite3")
        db.open()
        tab3_3_model = QtSql.QSqlTableModel()
        tab3_3_model.setTable('acc_stats_phillip') 
        tab3_3_model.select()
        tab3_3_view.setModel(tab3_3_model)
        tab3_3_view.setAlternatingRowColors(True)
        tab3_3_view.resizeColumnsToContents()
        tab3_3_view.resizeRowsToContents()
        tab3_3_view.setSortingEnabled(True)
        tab3_3_view.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

        tab3_3_layout=QtGui.QVBoxLayout()
     #   tab3_2_layout.addWidget(tab3_2_refr_btn)
        tab3_3_layout.addWidget(tab3_3_view)
        self.tab3_3.setLayout(tab3_3_layout)##########################

        #if i write db.close() there is nosorting
      #  db.close()
      #  del db
      #  QtSql.QSqlDatabase.removeDatabase("stat.sqlite3")

        
    def fill_series_list(self, names):
        self.series_list_model.clear()
        for name in names:
            item = QtGui.QStandardItem(name)
            if name=='Equity w/o transfers':
                item.setCheckState(Qt.Checked)
            else: item.setCheckState(Qt.Unchecked)
            item.setCheckable(True)
            self.series_list_model.appendRow(item)
        
    def show_plot(self):
        xxx=self.plot_list
        
        self.ax = self.figure.add_subplot(111)
     #   self.ax2 = self.figure.add_subplot(211)
     #   self.ax2.get_yaxis().set_visible(False)
     #   self.ax2.get_xaxis().set_visible(False)

        self.ax.clear()
     #   self.ax2.clear()
        self.ax.hold(True)
        tableau=self.chart_param()
        count=0
        for row in range(self.series_list_model.rowCount()):
            model_index = self.series_list_model.index(row, 0)
            checked = self.series_list_model.data(model_index,
                Qt.CheckStateRole) == QtCore.QVariant(Qt.Checked)
            name = str(self.series_list_model.data(model_index).toString())
            axi_x=(xxx[count])[0]
       ##     axis_x=range(len(axi_x))
       ##     axis_x_date = [(one_date).strftime("%Y-%m-%d") for one_date in axi_x]
       ##     print axis_x
            axis_y=(xxx[count])[1]
            if checked:
                if name in self.bar_list_name:
                    self.ax.bar(axi_x,axis_y, color=tableau[row],
                                label=name)
                else:
                    self.ax.plot(axi_x,axis_y,
                                 color=tableau[row], linewidth=3, label=name)
                try:
                    ann_max=self.ax.annotate(max(axis_y), xy=(axi_x[axis_y.index(max(axis_y))], max(axis_y)),
                                 xytext=(0, 5), textcoords='offset points')
                    ann_min=self.ax.annotate(min(axis_y), xy=(axi_x[axis_y.index(min(axis_y))], min(axis_y)),
                                 xytext=(0, -12), textcoords='offset points')
                    if axi_x[-1]==axi_x[axis_y.index(min(axis_y))] or axi_x[-1]==axi_x[axis_y.index(max(axis_y))]:
                        pass
                    else:
                        ann_last=self.ax.annotate(axis_y[-1], xy=(axi_x[-1], axis_y[-1]),
                                 xytext=(2, 0), textcoords='offset points')
                except:
                    pass

              #      self.ax.imshow(axi_x,axis_y, interpolation='none')
              #      mpldatacursor.datacursor(bbox=dict(fc='white'),
              #                               arrowprops=dict(arrowstyle='simple',
               #                                              fc='white', alpha=0.5))
               #     mpldatacursor.datacursor(hover=True, bbox=dict(alpha=1, fc='w'))
#
         #           self.ax.set_xticks(axis_x)
          #          self.ax.set_xticklabels(axis_x_date)
      #              locator = matplotlib.ticker.MaxNLocator()
      #              self.ax.xaxis.set_major_locator(locator)

                   #self.ax.locator_params(nbins=4)

                    # Set the xtick labels to correspond to just the dates you entered.

                    
    #                self.ax.set_xticklabels(rotation=30, 'right')
            count=count+1
            #(0., 1.02, 1., .102
            #When bbox_to_anchor and loc are used together, the loc argument
            #will inform matplotlib which part of the bounding box of the
            #legend should be placed at the arguments of bbox_to_anchor
      #  self.box = self.ax.get_position()
        self.ax.set_position([0.05, 0.15, 0.9, 0.8])

        # Put a legend below current axis
        self.ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=5,
          fancybox=True, shadow=True)

     #   self.ax.legend(bbox_to_anchor=(0., 0.0, 0, -0.05), loc=2, 
     #                  mode=None, borderaxespad=0)
   #     lgd = self.ax.legend(loc='upper center', bbox_to_anchor=(0.5,-0.1))
   #     self.figure.savefig('samplefigure', bbox_extra_artists=(lgd,),
    #                        bbox_inches='tight')

        self.canvas.draw()
        
    def res_distr(self, axisx, distr, delta_list2, numb_of_bins):
        self.ax = self.figure2.add_subplot(111)
        self.ax.clear()
        self.ax.hold(True)
        self.ax.plot(axisx, distr)
        self.ax.hist(delta_list2, bins=numb_of_bins)
        vals = self.ax.get_xticks()
        self.ax.set_xticklabels(['{:3.0f}%'.format(xx*100) for xx in vals])
        self.ax.set_title('A distribution of daily equity changes')
        self.ax.set_xlabel('Daily equity changes')
        self.ax.set_ylabel('Number of daily equity changes')

        # refresh canvas
        self.canvas2.draw()
    def get_data_for_0_tab(self):
        x=requests.get_date_value('equity')
        eq_wo_tr=requests.get_date_value('equity w/o transfers')
        y=requests.get_date_value('balance')
        z=requests.get_date_value('init_margin')
        real_pl=requests.get_date_value('realized_pl')
        cum_real_pl=requests.get_date_value('cum_realized_pl')
        cum_comm_fees=requests.get_date_value('cum_comm_fees')
        x_name='Equity'
        eq_wo_tr_name='Equity w/o transfers'
        y_name='Balance'
        z_name='Initial Margin'
        real_pl_name='Realized P/L'
        cum_real_pl_name='Cumulative Realized P/L'
        cum_comm_fees_name='Cumulative Comm. & Fees'
        self.names_list=(x_name,eq_wo_tr_name,y_name, z_name, real_pl_name,
                    cum_real_pl_name, cum_comm_fees_name)
        self.fill_series_list(self.names_list)
        self.plot_list=(x,eq_wo_tr,y,z,real_pl,cum_real_pl,cum_comm_fees)
        self.bar_list_name=(z_name, real_pl_name)    
        self.show_plot()
    def clicked(self):
        index=self.currentIndex()
        if index == 0:
            self.get_data_for_0_tab()
#            self.get_data(plot_list)
        if index == 1:
            a, b, c, d = requests.res_distr()
            self.res_distr(a, b, c, d)

    def chart_param (self):
        #change places 3 and 4
        tableau20 = [(31, 119, 180), (174, 199, 232), (255, 187, 120),
                          (255, 127, 14), (44, 160, 44), (152, 223, 138),
                          (214, 39, 40), (255, 152, 150), (148, 103, 189),
                          (197, 176, 213), (140, 86, 75), (196, 156, 148),
                          (227, 119, 194), (247, 182, 210), (127, 127, 127),
                          (199, 199, 199), (188, 189, 34), (219, 219, 141),
                          (23, 190, 207), (158, 218, 229)]    
        for i in range(len(tableau20)):    
            r, g, b = tableau20[i]    
            tableau20[i] = (r / 255., g / 255., b / 255.)
        return tableau20

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        exitAction = QtGui.QAction(QtGui.QIcon('Stuff/exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)
        dnldAction= QtGui.QAction(QtGui.QIcon('Stuff/download.png'), '&Statements from Gmail', self)
        dnldAction.setShortcut('Ctrl+D')
        dnldAction.setStatusTip('Download  data from email')
        dnldAction.triggered.connect(download_attach_gain)
        importAction= QtGui.QAction(QtGui.QIcon('Stuff/import.png'), '&Import to Database', self)
        importAction.setShortcut('Ctrl+I')
        importAction.setStatusTip('Import data to database')
        importAction.triggered.connect(self.import_to_db)
        settingsAction= QtGui.QAction(QtGui.QIcon('Stuff/settings.png'), '&Settings', self)
        settingsAction.setStatusTip('Settings')
        settingsAction.setShortcut('Ctrl+O')
        settingsAction.triggered.connect(self.my_settings)
       # helpAction= QtGui.QAction(QtGui.QIcon('Stuff/help.png'), '&How to use', self)
       # helpAction.setStatusTip('How to use the application')
       # helpAction.triggered.connect(self.my_help)
        #aboutAction= QtGui.QAction(QtGui.QIcon('Stuff/about.png'), '&About', self)
        #aboutAction.setStatusTip('About the application')
        getfolderAction= QtGui.QAction(QtGui.QIcon('Stuff/folder.png'), '&Statements from Folder', self)
        getfolderAction.setStatusTip('Copy your statements from folder and/or subfolders')
        getfolderAction.triggered.connect(states_from_folder)
       # aboutAction.triggered.connect(self.my_about)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(getfolderAction)
        fileMenu.addAction(dnldAction)
        fileMenu.addAction(importAction)
        fileMenu.addAction(settingsAction)
        fileMenu.addAction(exitAction)
        #helpMenu = menubar.addMenu('&Help')
        #helpMenu.addAction(helpAction)
        #helpMenu.addAction(aboutAction)

        self.statusBar().showMessage('Ready')
        self.showMaximized()
        self.setMinimumSize(600, 400)
        self.setWindowTitle('ESPA')
        self.setWindowIcon(QtGui.QIcon('Stuff/icon.png.'))

        copy_import_action= QtGui.QAction(QtGui.QIcon('Stuff/copy_import.png'), 'Copy and import', self)
        copy_import_action.setStatusTip('Copy your statements from folder and/or subfolders and import data to database')
        copy_import_action.triggered.connect(self.copy_import)
        download_import_action= QtGui.QAction(QtGui.QIcon('Stuff/download_import.png'), 'Download and import', self)
        download_import_action.setStatusTip('Download your statements from Gmail and import data to database')
        download_import_action.triggered.connect(self.download_import)

        self.toolbar = self.addToolBar('')
        self.toolbar.addAction(copy_import_action)
        self.toolbar.addAction(download_import_action)
        #setup window widgets
        self.main_widget= QtGui.QWidget(self)
        #lines up widgets horizontally
        self.layout = QtGui.QHBoxLayout(self.main_widget)
        mp=Myplot(self.main_widget)
        self.layout.addWidget(mp)
        self.main_widget.setFocus()
            
        self.setCentralWidget(self.main_widget)
        if not os.path.exists('config.db'):
            self.my_settings()

    def copy_import(self):
        states_from_folder()
        self.import_to_db()

    def download_import(self):
        download_attach_gain()
        self.import_to_db()
        
    def import_to_db(self):
        import_stats()
       #Myplot().add_table_gain()
       # Myplot().add_table_dorman()
        
    def my_settings(self):
        s = MySettings()
        s.exec_()
        
    def my_help(self):
  #      help_window=QtGui.QDialog()
        self.help_text = QtGui.QLabel('''For now you can copy statements \
from specified folder/subfolders or download statements from gmail \
accounts. For latter if you have simple verification, you should use \
your password to connect to gmail account.If you have 2-step verification, \
you should create app password. You can find the information about it here \
https://support.google.com/accounts/answer/185833?hl=en''')
        self.help_text.setOpenExternalLinks(True)
        self.help_text.setWindowTitle('ESPA')
        self.help_text.setWindowIcon(QtGui.QIcon('Stuff/icon.png.'))
        self.help_text.setWordWrap(True)
        self.help_text.show()

class MySettings(QtGui.QDialog):
    def __init__(self):
        
        super(MySettings , self).__init__()
        self.setWindowIcon(QtGui.QIcon('Stuff/settings.png'))

        self.setWindowTitle('Settings')
        self.mail_pwd = QtGui.QLabel("Enter your:")
        self.enter_mail = QtGui.QLabel("Gmail address")
        self.enter_pwd = QtGui.QLabel("Application password")
        self.acc_mail =QtGui.QLineEdit("")
        
        #self.acc_mail.setText
        self.acc_pwd =QtGui.QLineEdit("")
        self.acc_pwd.setEchoMode(QtGui.QLineEdit.Password)
        self.save_btn = QtGui.QPushButton('Save', self)
        self.save_btn.setCheckable(True)
        self.save_btn.clicked.connect(self.save_login_pwd)
    #get and save settings
        self.okbtn = QtGui.QPushButton('OK', self)
        self.okbtn.clicked.connect(self.ok_settings)
        self.cancelbtn=QtGui.QPushButton('Cancel', self)
        self.cancelbtn.clicked.connect(self.close)

        self.save_layout = QtGui.QVBoxLayout()
        self.save_layout.addWidget(self.mail_pwd)
        self.save_layout.addWidget(self.save_btn)

        self.mail_layout = QtGui.QVBoxLayout()
        self.mail_layout.addWidget(self.enter_mail)
        self.mail_layout.addWidget(self.acc_mail)
        
        self.pwd_layout = QtGui.QVBoxLayout()
        self.pwd_layout.addWidget(self.enter_pwd)
        self.pwd_layout.addWidget(self.acc_pwd)
        self.download_fcm = QtGui.QLabel("Download statements for:")
        self.download_d = QtGui.QCheckBox('Dorman Trading', self)
        self.download_g = QtGui.QCheckBox('Gain Capital', self)
        self.download_p = QtGui.QCheckBox('PhillipCapital', self)
        
        self.show_fcm = QtGui.QLabel("Show charts for:")
        self.show_d = QtGui.QCheckBox('Dorman Trading', self)
        self.show_g = QtGui.QCheckBox('Gain Capital', self)        
        self.show_p = QtGui.QCheckBox('PhillipCapital', self)
###################################3
        self.select_f_label = QtGui.QLabel("Select a folder to copy\nstatements from:")
        self.select_f_text = QtGui.QLineEdit()
        self.select_f_button=QtGui.QPushButton('', self)
        self.select_f_button.clicked.connect(self.select_folder)
        self.select_f_button.setIcon(QtGui.QIcon('Stuff/folder.png'))
        self.select_f_button.setFixedSize(20, 20)
        self.get_from_subfolder = QtGui.QCheckBox('Copy from subfolders', self)
        self.reminder = QtGui.QLabel('''Click on another tab to apply changes''')
###########################

        self.mail_password_layout = QtGui.QHBoxLayout()
        self.mail_password_layout.addLayout(self.save_layout)
        self.mail_password_layout.addLayout(self.mail_layout)
        self.mail_password_layout.addLayout(self.pwd_layout)
        
        gridLayout = QtGui.QGridLayout()
        
        gridLayout.addWidget(self.download_fcm, 0, 0)
        gridLayout.addWidget(self.download_d, 0, 1)
        gridLayout.addWidget(self.download_g, 0, 2)
        gridLayout.addWidget(self.download_p, 0, 3)
        
        gridLayout.addWidget(self.show_fcm, 1, 0)
        gridLayout.addWidget(self.show_d, 1, 1)
        gridLayout.addWidget(self.show_g, 1, 2)
        gridLayout.addWidget(self.show_p, 1, 3)

        folder_layout = QtGui.QHBoxLayout()
        folder_layout.addWidget(self.select_f_label)
        folder_layout.addWidget(self.select_f_text)
        folder_layout.addWidget(self.select_f_button)
        folder_layout.addWidget(self.get_from_subfolder)
        
        btn_layout = QtGui.QHBoxLayout()
        btn_layout.addStretch(1)

        btn_layout.addWidget(self.okbtn)
        btn_layout.addWidget(self.cancelbtn)

        total_layout=QtGui.QVBoxLayout()
        total_layout.addLayout(folder_layout)
        total_layout.addLayout(self.mail_password_layout)
        total_layout.addLayout(gridLayout)
        total_layout.addWidget(self.reminder)
        total_layout.addLayout(btn_layout)

        self.setLayout(total_layout)
        self.setFixedSize(500, 200)
        self.check_group = QtGui.QButtonGroup()
        self.check_group.addButton(self.download_d,0)
        self.check_group.addButton(self.download_g,1)
        self.check_group.addButton(self.download_p,2)
        self.check_group.addButton(self.show_d,3)
        self.check_group.addButton(self.show_g,4)
        self.check_group.addButton(self.show_p,5)
        self.check_group.setExclusive(False)

#check_list=dict.fromkeys(['download_d','show_d','download_g',
        #'show_g','download_p','show_p'])

        try:
            s=shelve.open('config.db', flag="r")
            print 'opened'
            try:
                self.check_dict=s['checkboxes']
                
                if self.check_dict[0]==True:
                    print '0 download_d'
                    self.download_d.setCheckState(Qt.Checked)
                else:
                    self.download_d.setCheckState(Qt.Unchecked)
                    
                if self.check_dict[1]==True:
                    print '1 show_d'
                    self.show_d.setCheckState(Qt.Checked)
                else:
                    self.show_d.setCheckState(Qt.Unchecked)
                    
                if self.check_dict[2]==True:
                    print '2 download_g'
                    self.download_g.setCheckState(Qt.Checked)
                else:
                    self.download_g.setCheckState(Qt.Unchecked)
                    
                if self.check_dict[3]==True:
                    print '3 show_g'
                    self.show_g.setCheckState(Qt.Checked)
                else:
                    self.show_g.setCheckState(Qt.Unchecked)
                    
                if self.check_dict[4]==True:
                    print '4 download_p'
                    self.download_p.setCheckState(Qt.Checked)
                else:
                    self.download_p.setCheckState(Qt.Unchecked)
                    
                if self.check_dict[5]==True:
                    print '5 show_p'
                    self.show_p.setCheckState(Qt.Checked)
                else:
                    self.show_p.setCheckState(Qt.Unchecked)
                    
            except:
                print 'no dict'
                self.check_dict=dict.fromkeys([0,1,2,3,4,5], False)
            try:
                
                self.mail_dict=s['mails']
                self.acc_mail.setText(self.mail_dict['mail1'])
                self.acc_pwd.setText(keyring.get_password('ESPA_email',
                                                          self.mail_dict['mail1']))
            except:
                self.mail_dict=dict.fromkeys(['mail1'])
            try:
                self.select_f_text.setText(s['select_folder'])
            except:
                pass
            try:
                self.get_from_subfolder_item=s['get_from_subfolder']
                if self.get_from_subfolder_item==True:
                    print '0'
                    self.get_from_subfolder.setCheckState(Qt.Checked)
                else:
                    self.get_from_subfolder.setCheckState(Qt.Unchecked)
            except:
                pass

            s.close()
        except:
            print 'nothing'
            self.check_dict=dict.fromkeys([0,1,2,3,4,5], False)
            self.mail_dict=dict.fromkeys(['mail1'])
            self.get_from_subfolder_dict={'get_from_subfolder', True}

        #######
        self.check_group.buttonClicked[QtGui.QAbstractButton].connect(self.settings_dict)

    def settings_dict(self, button):
        self.check_dict[self.check_group.id((button))]=button.isChecked()

    def save_login_pwd(self):
        #access the QlineEdit and use text() to access its text
        self.mail1 =str(self.acc_mail.text())
        self.pwd1 =str(self.acc_pwd.text())
        keyring.set_password('ESPA_email', self.mail1, self.pwd1)

    def ok_settings(self):
        s=shelve.open('config.db')
        s['checkboxes']=self.check_dict
        try:
            self.mail_dict['mail1']=self.mail1
            s['mails']=self.mail_dict
        except:
            pass
        try:
            s['select_folder']=self.folder_text
        except:
            pass
        try:
            if self.get_from_subfolder.isChecked():
                s['get_from_subfolder']=True
            else:
                s['get_from_subfolder']=False
        except:
            pass
        s.close()
        self.close()
     #   xx=Myplot()
        #xx.setCurrentIndex(2)
     #   xx.get_data_for_0_tab()

        
        

    def select_folder(self):
        fname = QtGui.QFileDialog.getExistingDirectory(self, "Select Directory")
        self.folder_text = str(fname)
        if len(self.folder_text) >0:
            self.select_f_text.setText(self.folder_text)
        else:
            pass
            
def main():
    app = QtGui.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()    

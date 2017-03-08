# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow

from Ui_main import Ui_MainWindow
from shadowsocks import local
from multiprocessing import Process
import sys
import os
import json
import logging

def read_json(title):
    save_path = os.path.join(sys.path[0], title)
    if title in [x for x in os.listdir('.')]:
        with open(save_path, "r") as f:
            j = json.load(f)
    else:
        j = {}
    return j    

def savejson(title, json_dict):
    save_path = os.path.join(sys.path[0], title)
    with open(save_path , mode = 'w') as f : 
        json.dump(json_dict,f, ensure_ascii = False ,indent=2)   


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
    
    @pyqtSlot()
    def on_b_yes_clicked(self):
        """
        Slot documentation goes here.
        """
        logging.info("close ss-local...")
        self.sslocal_process.terminate()
        self.sslocal_process.join()
        logging.info("restart ss-local")
        sslocal_process = Process(target=local.main, daemon = True)
        sslocal_process.start()
        self.sslocal_process = sslocal_process
        # TODO: not implemented yet

    @pyqtSlot()
    def on_b_exit_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet

    @pyqtSlot()
    def on_add_config_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        
        raise NotImplementedError


if __name__ == "__main__":
    logging.getLogger('').handlers = []
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    app = QtWidgets.QApplication(sys.argv)
    mySW = MainWindow()
    sslocal_process = Process(target=local.main, daemon = True)
    sslocal_process.start()
    mySW.sslocal_process = sslocal_process
    user_json = read_json("user.json")
    configlist = mySW.configlist
    for k,v in user_json.items():
        configlist.addItem(k)
    mySW.show()
    sys.exit(app.exec_())
    


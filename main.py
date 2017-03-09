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
import time
import collections

def read_json(title):
    save_path = os.path.join(sys.path[0], title)
    if title in [x for x in os.listdir('.')]:
        with open(save_path, "r") as f:
            j = json.load(f, object_pairs_hook=collections.OrderedDict)
    else:
        j = {}
    return j    

def save_json(title, json_dict):
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

    def save_config(self):
        new_config = collections.OrderedDict()
        gui_config = self.gui_config
        new_config["server"] = self.serverAddrEdit.text()
        new_config["server_port"] = self.serverPortSpinBox.value()
        new_config["password"] = self.pwdEdit.text()
        new_config["method"] = self.encryptComboBox.currentText()
        new_config["timeout"] = self.timeoutSpinBox.value()
        new_config["one_time_auth"] = self.otaCheckBox.isChecked()
        save_json("config.json", new_config)
        new_config["remarks"] = self.remarksEdit.text()
        index = self.configlist.currentRow()
        if index < len(gui_config["configs"]):
            gui_config["configs"][index] = new_config
        else:    
            gui_config["configs"].append(new_config)
        save_json("gui-config.json", gui_config)
        if new_config.get("remarks","") == "":
            item_text = "%s:%s" %(new_config["server"], new_config["server_port"])
        else:
            item_text = "%s (%s:%s)" %(new_config["remarks"], new_config["server"], new_config["server_port"])      
        self.configlist.currentItem().setText(item_text)

    @pyqtSlot()
    def on_b_yes_clicked(self):
        """
        Slot documentation goes here.
        """
        logging.info("close ss-local...")
        self.sslocal_process.terminate()
        self.sslocal_process.join()
        self.save_config()
        logging.info("restart ss-local")
        sslocal_process = Process(target=local.main, daemon = True)
        sslocal_process.start()
        self.sslocal_process = sslocal_process
        # TODO: not implemented yet

    @pyqtSlot()
    def on_b_exit_clicked(self):
        self.sslocal_process.terminate()
        self.sslocal_process.join()

    @pyqtSlot()
    def on_del_config_clicked(self):
        index = self.configlist.currentRow()
        self.configlist.takeItem(index)
        if index < len(self.gui_config["configs"]):
            self.gui_config["configs"].pop(index)
        self.update()    

    @pyqtSlot()
    def on_add_config_clicked(self):
        new_config = collections.OrderedDict()
        count = self.configlist.count()
        self.configlist.addItem("127.0.0.1")
        new_config["server"] = "127.0.0.1"
        new_config["server_port"] = 1080
        new_config["password"] = "password"
        new_config["method"] = "aes-256-cfb"
        new_config["timeout"] = 600
        new_config["one_time_auth"] = False
        new_config["remarks"] = ""
        self.gui_config["configs"].append(new_config)
        self.configlist.setCurrentRow(count)
        self.update()

    def update(self):
        user_json = self.gui_config
        index = self.configlist.currentRow()
        select_config = user_json["configs"][index]
        remarks = select_config.get("remarks","")
        server_addr = select_config["server"]
        server_port = select_config["server_port"]
        password = select_config["password"]
        method = select_config["method"]
        timeout = select_config["timeout"]
        one_time_auth = select_config["one_time_auth"]
        self.serverAddrEdit.setText(server_addr)
        self.serverPortSpinBox.setValue(int(server_port))
        self.pwdEdit.setText(password)
        self.encryptComboBox.setCurrentText(method)
        self.timeoutSpinBox.setValue(timeout)
        self.otaCheckBox.setChecked(one_time_auth)
        self.remarksEdit.setText(remarks)



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
    mySW.gui_config = read_json("gui-config.json")
    configlist = mySW.configlist
    for x in mySW.gui_config.get("configs",{}):
        if x.get("remarks","") == "":
            item_text = "%s:%s" %(x["server"], x["server_port"])
        else:
            item_text = "%s (%s:%s)" %(x["remarks"],x["server"], x["server_port"])    
        configlist.addItem(item_text)
    index = mySW.gui_config.get("index", 0)
    configlist.setCurrentRow(index)
    mySW.update()
    mySW.show()
    sys.exit(app.exec_())
    


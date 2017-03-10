# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
from __future__ import absolute_import, division, print_function, \
    with_statement

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QSystemTrayIcon
from PyQt5.QtGui import QIcon

from Ui_main import Ui_MainWindow
from shadowsocks import local as ss_local
import sys
import os
import json
import logging
import time
import collections

# Module multiprocessing is organized differently in Python 3.4+
try:
    # Python 3.4+
    if sys.platform.startswith('win'):
        import multiprocessing.popen_spawn_win32 as forking
    else:
        import multiprocessing.popen_fork as forking
except ImportError:
    import multiprocessing.forking as forking

if sys.platform.startswith('win'):
    # First define a modified version of Popen.
    class _Popen(forking.Popen):
        def __init__(self, *args, **kw):
            if hasattr(sys, 'frozen'):
                # We have to set original _MEIPASS2 value from sys._MEIPASS
                # to get --onefile mode working.
                os.putenv('_MEIPASS2', sys._MEIPASS)
            try:
                super(_Popen, self).__init__(*args, **kw)
            finally:
                if hasattr(sys, 'frozen'):
                    # On some platforms (e.g. AIX) 'os.unsetenv()' is not
                    # available. In those cases we cannot delete the variable
                    # but only set it to the empty string. The bootloader
                    # can handle this case.
                    if hasattr(os, 'unsetenv'):
                        os.unsetenv('_MEIPASS2')
                    else:
                        os.putenv('_MEIPASS2', '')

    # Second override 'Popen' class with our modified version.
    forking.Popen = _Popen


# Example for testing multiprocessing.

import multiprocessing

class SendeventProcess(multiprocessing.Process):
    def __init__(self, *args, **kwrg):
        multiprocessing.Process.__init__(self, *args, **kwrg)


def read_json(config_path):
    with open(config_path, "rb") as f:
        ff = f.read().decode("utf-8")
        j = json.loads(ff, object_hook=collections.OrderedDict)
    return j

def save_json(config_path, json_dict):
    with open(config_path , mode = 'w', encoding="utf-8") as f : 
        json.dump(json_dict,f, ensure_ascii = False ,indent=2)

def find_config(config_name):
    config_path = config_name
    if os.path.exists(config_path):
        return config_path
    config_path = os.path.join(os.path.dirname(__file__), '../', config_name)
    if os.path.exists(config_path):
        return config_path
    return None

def to_bytes(s):
    if bytes != str:
        if type(s) == str:
            return s.encode('utf-8')
    return s


def to_str(s):
    if bytes != str:
        if type(s) == bytes:
            return s.decode('utf-8')
    return s


def check_config(config):
    config['password'] = to_str(config.get('password', ''))
    config['method'] = to_str(config.get('method', 'aes-256-cfb'))
    config['port_password'] = config.get('port_password', None)
    config['timeout'] = int(config.get('timeout', 300))
    config['fast_open'] = config.get('fast_open', False)
    config['one_time_auth'] = config.get('one_time_auth', False)
    config['server_port'] = config.get('server_port', 8388)
    return config


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
        config_path = find_config("config.json")
        if config_path == None:
            logging.error("config_path is None")
        save_json(config_path,  new_config)
        new_config["remarks"] = self.remarksEdit.text()
        index = self.configlist.currentRow()
        if index < len(gui_config["configs"]):
            gui_config["configs"][index] = new_config
            gui_config["index"] = index
        else:
            gui_config["configs"].append(new_config)
        
        config_path = find_config("gui-config.json")
        if config_path == None:
            logging.error("config_path is None")
        save_json(config_path, gui_config)
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
        sslocal_process = SendeventProcess(target=ss_local.main, daemon = True)
        sslocal_process.start()
        self.sslocal_process = sslocal_process
        self.showMessage("配置已生效！")
        self.destroy()

    @pyqtSlot()
    def on_b_exit_clicked(self):
        self.destroy()

    def app_quit(self):
        self.sslocal_process.terminate()
        self.sslocal_process.join()
        sys.exit()

    def closeEvent(self, event):
        self.destroy()
        event.ignore()

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

    def Tray_init(self):
        self.tray = QSystemTrayIcon()
        self.icon = QIcon('Shadowsocks_logo.png')
        self.tray.setIcon(self.icon)
        self.tray.activated[QSystemTrayIcon.ActivationReason].connect(self.TrayEvent)
        self.tray_menu = QtWidgets.QMenu(QtWidgets.QApplication.desktop())
        self.ShowAction = QtWidgets.QAction(u'还原 ', self, triggered=self.re_build)
        self.QuitAction = QtWidgets.QAction(u'退出 ', self, triggered=self.app_quit)
        self.tray_menu.addAction(self.ShowAction)
        self.tray_menu.addAction(self.QuitAction)
        self.tray.setContextMenu(self.tray_menu) #设置系统托盘菜单
        self.tray.show()
        self.showMessage("shadowsocks-pyqt 已经启动！")

    def re_build(self):
        self.hide()
        self.update()
        self.show()
        self.activateWindow()
    
    def TrayEvent(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:  
            if self.isHidden() or self.destroyed:
                self.re_build()
            else:  
                self.hide()

    def showMessage(self, text):
        icon = self.tray.MessageIcon()
        self.tray.showMessage(u'提示', text, icon,1000)


if __name__ == "__main__":
    try:
        logging.getLogger('').handlers = []
        logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
        multiprocessing.freeze_support()
        app = QtWidgets.QApplication(sys.argv)
        My_App = MainWindow()
        sslocal_process = SendeventProcess(target=ss_local.main, daemon = True)
        sslocal_process.start()
        My_App.sslocal_process = sslocal_process
        config_path = find_config("gui-config.json")
        if config_path == None:
            logging.error("config_path is None")
            raise
        My_App.gui_config = read_json(config_path)
        configlist = My_App.configlist
        for x in My_App.gui_config.get("configs",{}):
            x = check_config(x)
            if x.get("remarks","") == "":
                item_text = "%s:%s" %(x["server"], x["server_port"])
            else:
                item_text = "%s (%s:%s)" %(x["remarks"],x["server"], x["server_port"])    
            configlist.addItem(item_text)
        index = My_App.gui_config.get("index", 0)
        configlist.setCurrentRow(index)
        My_App.Tray_init()
        # My_App.update()
        # My_App.show()
        sys.exit(app.exec_())
    except Exception as e:
        logging.info(e)
        raise
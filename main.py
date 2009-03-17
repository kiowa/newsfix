#!/usr/bin/env python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
import sys
from ui.login import Ui_LoginDialog
from ui.main import Ui_MainWindow
import GoogleReader.reader
from GoogleReader.const import CONST


class Main:
    def main(self):
        self.reader = GoogleReader.reader.GoogleReader()
        self.setupGui()
        self.setupSignals()
        self.showGui()
        sys.exit(self.app.exec_())

    def setupGui(self):
        self.app = QApplication(sys.argv)
        self.loginWindow = QDialog()

        self.window = QMainWindow()
        self.mainWindow = Ui_MainWindow()
        self.mainWindow.setupUi(self.window)

        self.loginDialog = Ui_LoginDialog()
        self.loginDialog.setupUi(self.loginWindow)    
        self.setupPrinters()
        #self.loginWindow.setParent(self.window)

    def setupPrinters(self):
        printers = QPrinterInfo.availablePrinters()
        self.printerModel = QStandardItemModel()
        count = 0
        for p in printers:
            item = QStandardItem(p.printerName())
            item._printer = p
            self.printerModel.appendRow(item)
            if (p.isDefault()):
                defaultIndex = count
        self.mainWindow.printerList.setModel(self.printerModel)
        self.mainWindow.printerList.setCurrentIndex(defaultIndex)
        
    def getSelectedPrinter(self):
        index = self.mainWindow.printerList.currentIndex()
        item = self.printerModel.item(index)
        printerInfo = item._printer
        printer = QPrinter(printerInfo)
        return printer
        
    def showGui(self):
        self.window.show()
        self.loginWindow.exec_()
        

    def slotLogin(self):
        username = self.loginDialog.emailAddress.text()
        password = self.loginDialog.password.text()
        self.reader.identify(username, password)
        if (self.reader.login()):
            self.loginWindow.accept()
            #self.getTags()
            self.getSubscriptions()
        else:
            self.loginDialog.errorLabel.setText("Login failed")

    def setupSignals(self):
        QObject.connect(self.loginDialog.loginButton, SIGNAL("clicked()"), self.slotLogin)
        QObject.connect(self.mainWindow.previewButton, SIGNAL("clicked()"), self.slotPreview)
        QObject.connect(self.mainWindow.printButton, SIGNAL("clicked()"), self.slotPrint)
    
    def slotPrint(self):
        self.createHtml()
        self.createPreview()
        self.webFrame.print_(self.getSelectedPrinter())
        
    
    def slotPreview(self):
        self.createHtml()
        self.createPreview()
        self.showPreview()


    def getEntries(self):
        content = []
        sub_ids = self.getCheckedSubscriptions()
        maxArts = self.mainWindow.maxArticles.value()
        for i in sub_ids:
            feed = self.reader.get_feed(feed = i, exclude_target=CONST.ATOM_STATE_READ, count = maxArts)
            entries = feed.get_entries()
            while True:
                try:
                    entry = entries.next()
                    content.append(entry)
                except StopIteration:
                    break
        return content


    def createHtml(self):
        html = u"<html><head></head><body>"
        for entry in self.getEntries():
            html = html + u"<h1>%s</h1>" % entry["title"]
            html = html + u"<i>%s %s</i><br />" % (entry["author"], entry["link"])
            html = html + entry["content"]
        html = html + u"</body></html>"
        self.html = html


        
    def createPreview(self):
        self.webFrame = QWebView()
        self.webFrame.setHtml(self.html)
    
    def showPreview(self):        
        self.webFrame.show()

        
    def getSubscriptions(self):
        self.subModel = QStandardItemModel()
        subs = self.reader.get_subscription_list()['subscriptions']
        for s in subs:
            label = s['title']
            sub_id = s['id']
            item = QStandardItem(label)
            item.sub_id = sub_id
            item.setCheckable(True)
            self.subModel.appendRow(item)
        self.mainWindow.labelList.setModel(self.subModel)

    def getCheckedSubscriptions(self):
        subs = []
        for i in range(self.subModel.rowCount()):
            item = self.subModel.item(i)
            if (item.checkState() == Qt.Checked):
                subs.append(item.sub_id)
        return subs


if __name__ == "__main__":
    print "Starting..."
    Main().main()

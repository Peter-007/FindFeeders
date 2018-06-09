#!/usr/bin/env python

import re, time
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QFileDialog, QGridLayout,QLabel, QLineEdit,
                             QPushButton,QTreeWidget,QTreeWidgetItem,QTreeWidgetItemIterator,
                             QStyledItemDelegate,QTabWidget,
                             QCheckBox, QTableWidget, QTableWidgetItem,QVBoxLayout, QWidget)
import Feeders #,Find_Tx

class FindFeeder(QWidget):
    def __init__(self, parent = None):
        super(FindFeeder, self).__init__(parent)

        tabWidget = QTabWidget()
        tabWidget.addTab(InTab(), "入库")
        tabWidget.addTab(OutTab(), "出库")

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(tabWidget)
        self.setLayout(mainLayout)
        self.setWindowTitle("Find FEEDER")

class InTab(QWidget):
    def __init__(self, parent=None):
        super(InTab, self).__init__(parent)
        self.feeders = Feeders.Feeders()
        
        lableRfID = QLabel("标签ID:")
        self.editRfID = QLineEdit()
        self.editRfID.setMaxLength(4)
        self.buttonSave = QPushButton("入库")

        lableSapID = QLabel("物料ID:")
        self.editSapID = QLineEdit()

        lableList = QLabel("库存列表:")
        self.tableList = QTableWidget(0,2)
        self.tableList.setHorizontalHeaderLabels(['标签ID', '物料ID'])

        self.buttonSave.clicked.connect(self.save)

        mainLayout = QGridLayout()
        mainLayout.addWidget(lableRfID, 0, 0)
        mainLayout.addWidget(self.editRfID, 0, 1)
        mainLayout.addWidget(self.buttonSave, 0, 2)
        mainLayout.addWidget(lableSapID, 1, 0)
        mainLayout.addWidget(self.editSapID, 1, 1)
        mainLayout.addWidget(lableList, 2, 0, Qt.AlignTop)
        mainLayout.addWidget(self.tableList, 2, 1)

        self.setLayout(mainLayout)
        self.update()
        
    def update(self):
        d = self.feeders.dict_Feeders
        self.tableList.setRowCount(0)
        for k in sorted(d.keys()):
            self.tableList.insertRow(0)
            self.tableList.setItem(0, 0, QTableWidgetItem(k))
            self.tableList.setItem(0, 1, QTableWidgetItem(d[k]))
            
        self.tableList.resizeColumnsToContents()
        
    def save(self):
        strRfID = self.editRfID.text()
        strSapID = self.editSapID.text()
        if (strSapID.strip() == "") or (strSapID == ""): return
        self.feeders.insert(strRfID, strSapID)

        self.editRfID.setText("")
        self.editSapID.setText("")
        self.update()


class OutTab(QWidget):
    def __init__(self, parent=None):
        super(OutTab, self).__init__(parent)


        lableFilePath = QLabel("物料文件：")
        self.editFilePath = QLineEdit()
        self.buttonImport = QPushButton("导入")
        self.buttonLocate = QPushButton("定位")
        self.buttonOut = QPushButton("出库")

        lableSapIDList = QLabel("物料ID列表:")
        self.tree = QTreeWidget()
        self.tree.setColumnCount(3)
        self.tree.setHeaderLabels(['物料ID','标签ID','状态'])

        self.buttonImport.clicked.connect(self.importSapIDs)
        self.buttonLocate.clicked.connect(self.Locate)
        self.buttonOut.clicked.connect(self.removeID)

        mainLayout = QGridLayout()
        mainLayout.addWidget(lableFilePath, 0, 0)
        mainLayout.addWidget(self.editFilePath, 0, 1)
        mainLayout.addWidget(self.buttonImport, 0, 2)
        mainLayout.addWidget(lableSapIDList, 1, 0, Qt.AlignTop)
        mainLayout.addWidget(self.buttonLocate, 1, 2, Qt.AlignTop)
        mainLayout.addWidget(self.buttonOut, 2, 2, Qt.AlignTop)
        mainLayout.addWidget(self.tree, 1, 1, 9, 1 )

        self.setLayout(mainLayout)


    def GetSapIDs(self,strFilePath):
        listID = []
        with open(strFilePath, 'r') as f:
            strAll = f.read()

        listTemp = strAll.split('\n')[3:-2]
        for x in listTemp:
            strID = re.split(r'\s+', x)[2]
            # strID = "".join(list(filter(str.isdigit, strID)))
            listID.append(strID)
        return listID

    def importSapIDs(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,
            "QFileDialog.getOpenFileName()", self.editFilePath.text(),
            "Text Files (*.txt)", options=options)
        if not fileName: return

        self.editFilePath.setText(fileName)
        listID = self.GetSapIDs(fileName)
        iLength = len(listID)
        self.feeders = Feeders.Feeders()

        self.root = QTreeWidgetItem(self.tree)
        self.root.setText(0, 'SAP ID')
        for i in range(iLength):
            SapID = listID[i]
            RfID = self.feeders.findFeeder(SapID)
            id = QTreeWidgetItem(self.root)
            id.setText(0, SapID)
            id.setText(1, RfID)
            id.setText(2, 'N/A')
            id.setCheckState(0, 0)

        self.tree.expandAll()
        self.tree.resizeColumnToContents(0)
        self.root.sortChildren(1, 0)

    def Locate(self):
        for i in range(self.root.childCount()):
            child = self.root.child(i)
            if child.checkState(0):
                if child.text(1) == 'N/A':
                    child.setText(2, '无法定位')
                else:
                    child.setText(2, '已定位')
                    # strRfID = self.editRfID.text()
                    # tx = Find_Tx.Tx()
                    # tx.FindID(strRfID)
                    # del tx

    def removeID(self):
        flag = True
        while flag == True:
            flag = False
            for i in range(self.root.childCount()):
                child = self.root.child(i)
                if child.checkState(0):
                    self.root.removeChild(child)
                    self.feeders.remove(child.text(1))
                    flag = True
                    break

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    mainUI = FindFeeder()
    mainUI.show()
    sys.exit(app.exec_())

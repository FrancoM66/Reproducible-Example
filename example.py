import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QItemDelegate, QWidget, QTableWidget, QTableWidgetItem, QPushButton, QHeaderView, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import Qt
import pandas as pd


class ComboBoxDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super(ComboBoxDelegate, self).__init__(parent)
        self.items = []

    def setItems(self, items):
        self.items = items

    def createEditor(self, widget, option, index):
        editor = QtWidgets.QComboBox(widget)
        editor.addItems(self.items)
        return editor

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.ItemDataRole.EditRole)
        if value:
            editor.setCurrentText(str(value))
            print("Data Changed")

    def setModelData(self, editor, model, index):
        model.setData(index, editor.currentIndex(), Qt.ItemDataRole.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.window_width, self.window_height = 700, 500
        self.resize(self.window_width, self.window_height)
        self.setWindowTitle('Load Excel (or CSV) data to QTableWidget')

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.button = QPushButton('&Load Data')
        self.button.clicked.connect(lambda _, xl_path=excel_file_path,: self.loadExcelData(xl_path))
        layout.addWidget(self.button)

    def loadExcelData(self, excel_file_dir):
        df = pd.read_csv(excel_file_dir)
        if df.size == 0:
            return

        df.fillna('', inplace=True)
        self.table.setRowCount(df.shape[0])
        self.table.setColumnCount(df.shape[1])
        self.table.setHorizontalHeaderLabels(df.columns)

        # returns pandas array object
        for row in df.iterrows():
            values = row[1]
            for col_index, value in enumerate(values):
                if isinstance(value, (float, int)):
                    value = '{0:0,.0f}'.format(value)
                tableItem = QTableWidgetItem(str(value))
                self.table.setItem(row[0], col_index, tableItem)
        self.create_delegate(self.table)
        self.table.setColumnWidth(2, 300)
    
    def create_delegate(self, table):
        test_del = ComboBoxDelegate()
        test_list = ["Gravity Main", "Manhole", "Lateral"]
        test_del.setItems(test_list)
        table.setItemDelegateForColumn(0, test_del)


if __name__ == '__main__':
    # don't auto scale when drag app to a different monitor.
    # QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    
    excel_file_path = "O:\Field Services Division\Field Support Center\Project Acceptance\99999 - Test Folder This is a Test\Excel\CIP Gravity.csv"

    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 17px;
        }
    ''')
    
    myApp = MyApp()
    myApp.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing Window...')
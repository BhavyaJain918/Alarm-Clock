import datetime
import mysql.connector
from PyQt6.QtWidgets import QLineEdit , QGridLayout , QApplication , QWidget , QPushButton , QLabel , QComboBox
from PyQt6.QtCore import Qt , QTimer
from PyQt6.QtGui import QIcon
from Init_Alarm import create_database
import sys
year = []
days = []
month = []
hours = []
minute = []


class Window(QWidget):
    def __init__(self):
        global layout
        super().__init__()
        self.setWindowIcon(QIcon("C:\\Users\\Bhavya Jain\\Downloads\\Alarm.png"))
        self.setWindowTitle("Alarm Clock")
        self.setContentsMargins(10 , 10 , 20 , 20)

        layout = QGridLayout()
        self.setLayout(layout)

        self.label1 = QLabel("Set Date: ")
        layout.addWidget(self.label1 , 0 , 0)
        self.input1 = QComboBox()
        status = years()
        self.input1.addItems(year)
        self.input1.currentTextChanged.connect(self.month1)
        self.input1.currentTextChanged.connect(self.days1)
        self.input1.currentTextChanged.connect(self.hours_day)
        self.input1.currentTextChanged.connect(self.minute_day)
        layout.addWidget(self.input1 , 0 , 1)

        self.input_2 = QComboBox()
        self.month1()
        self.input_2.setMaximumWidth(40)
        self.input_2.currentTextChanged.connect(self.days1)
        self.input_2.currentTextChanged.connect(self.hours_day)
        self.input_2.currentTextChanged.connect(self.minute_day)
        layout.addWidget(self.input_2 , 0 , 2)
        
        self.input_3 = QComboBox()
        self.days1()
        self.input_3.setMaximumWidth(40)
        self.input_3.currentTextChanged.connect(self.hours_day)
        self.input_3.currentTextChanged.connect(self.minute_day)
        layout.addWidget(self.input_3 , 0 , 2 , Qt.AlignmentFlag.AlignRight)

        self.label2 = QLabel("Set Time: ")
        layout.addWidget(self.label2 , 1 , 0)
        self.input2 = QComboBox()
        self.hours_day()
        self.input2.currentTextChanged.connect(self.minute_day)
        layout.addWidget(self.input2 , 1 , 1)
        
        self.input_4 = QComboBox()
        self.minute_day()
        self.input_4.setMinimumWidth(80)
        layout.addWidget(self.input_4 , 1 , 2)

        self.label3 = QLabel("Alarm Message: ")
        layout.addWidget(self.label3 , 2 , 0)
        self.input3 = QLineEdit()
        self.input3.setPlaceholderText("Custom Message")
        self.label3.setContentsMargins(0 , 0 , 0 , 10)
        self.input3.setContentsMargins(0 , 0 , 0 , 10)
        self.input3.setMinimumWidth(100)
        layout.addWidget(self.input3 , 2 , 1 , 1 , 2)

        self.button1 = QPushButton("Set Alarm")
        self.button1.setFixedWidth(116)
        layout.addWidget(self.button1 , 3 , 1 , Qt.AlignmentFlag.AlignVCenter)
        self.button1.clicked.connect(self.setalarm)
        self.close()

    def setalarm(self):
        date1 = self.input_3.currentText() + '-' + self.input_2.currentText() + '-' + self.input1.currentText()
        time1 = self.input2.currentText() + ':' + self.input_4.currentText()
        mes = self.input3.text()
        if mes == '':
            mes = "Wake Up"
        try:
            myc.execute("INSERT INTO Alarm VALUES (%s , %s , %s)" , (time1 , date1 , mes))
            mydb.commit()
        except mysql.connector.errors.DatabaseError:
            sys.exit()
        self.label5 = QLabel("Alarm set successfully")
        layout.addWidget(self.label5 , 4  , 1 , Qt.AlignmentFlag.AlignVCenter)
        QTimer.singleShot(2000 , lambda: self.label5.setText(""))
    
    def days1(self):
        days_31 = ["01" , "03" , "05"  , "07" , "08" , "10" , "12"]
        days_30 = ["04" , "06" , "09" , "11"]
        yer = self.input1.currentText()
        mon = self.input_2.currentText()
        global days
        days.clear()
        if mon == '':
            mon = datetime.datetime.today().strftime("%m")
        if int(yer) == int(datetime.datetime.today().strftime("%Y")):
            if int(mon) == int(datetime.datetime.today().strftime("%m")):
                start = int(datetime.datetime.today().strftime("%d"))
            else:
                start = 1
        else:
            start = 1
        for i in range(start  , 29):
            if i < 10:
                days.append('0' + str(i))
            else:
                days.append(str(i)) 
        self.input_3.clear()
        self.input_3.addItems(days)
        if (mon in days_31):
            self.input_3.insertItem(28 , "29")
            self.input_3.insertItem(29 , "30")
            self.input_3.insertItem(30 , "31")
        elif (mon in days_30):
            self.input_3.insertItem(28 , "29")
            self.input_3.insertItem(29 , "30")
        elif(mon == "02" and (int(yer) % 4) == 0):
            self.input_3.insertItem(28 , "29")

    def month1(self):
        global month
        month.clear()
        year_ = self.input1.currentText()
        if int(year_) == int(datetime.datetime.today().strftime("%Y")):
            start0 = int(datetime.datetime.today().strftime("%m")) 
        else:
            start0 = 1
        for i in range(start0 , 13):
            if i < 10:
                month.append('0' + str(i))
            else:
                month.append(str(i))
        self.input_2.clear()
        self.input_2.addItems(month)

    def hours_day(self):
        global hours
        hours.clear()
        year_now = self.input1.currentText()
        mon_now = self.input_2.currentText()
        day_now = self.input_3.currentText()
        if mon_now == '':
            mon_now = datetime.datetime.today().strftime("%m")
        if day_now == '':
            day_now = datetime.datetime.today().strftime("%d")
        if int(year_now) == int(datetime.datetime.today().strftime("%Y")):
            if int(mon_now) == int(datetime.datetime.today().strftime("%m")):
                if int(day_now) == int(datetime.datetime.today().strftime("%d")):
                    start1 = int(datetime.datetime.today().strftime("%H"))
                else:
                    start1= 0
            else:
                start1 = 0
        else:
            start1 = 0
        for i in range(start1 , 24):
            if i < 10:
                hours.append('0' + str(i))
            else:
                hours.append(str(i))
        self.input2.clear()
        self.input2.addItems(hours)
    
    def minute_day(self):
        global minute
        minute.clear()
        year_now = self.input1.currentText()
        mon_now = self.input_2.currentText()
        day_now = self.input_3.currentText()
        hr_now = self.input2.currentText()
        if mon_now == '':
            mon_now = datetime.datetime.today().strftime("%m")
        if day_now == '':
            day_now = datetime.datetime.today().strftime("%d")
        if hr_now == '':
            hr_now = datetime.datetime.today().strftime("%H")
        if int(year_now) == int(datetime.datetime.today().strftime("%Y")):
            if int(mon_now) == int(datetime.datetime.today().strftime("%m")):
                if int(day_now) == int(datetime.datetime.today().strftime("%d")):
                    if int(hr_now) ==  int(datetime.datetime.today().strftime("%H")):
                        start2 = int(datetime.datetime.today().strftime("%M"))
                    else:
                        start2 = 0
                else:
                    start2= 0
            else:
                start2 = 0
        else:
            start2 = 0
        for i in range(start2 , 60):
            if i < 10:
                minute.append('0' + str(i))
            else:
                minute.append(str(i))
        self.input_4.clear()
        self.input_4.addItems(minute)

def years():
    cur = datetime.datetime.today().strftime("%Y")
    fut = int(cur) + 8
    for i in range(int(cur) , fut):
        year.append(str(i))
    return 0

usern = input("Enter Username: ")
password = input("Enter Password: ")
stat = create_database(usern , password)
if stat == 0 or stat == 1007:
    try:
        mydb = mysql.connector.connect(host = "localhost" , user = usern , passwd = password , database = "Clock")
        myc = mydb.cursor()
    except mysql.connector.errors.DatabaseError as de:
        sys.exit()
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
else:
    print(stat)
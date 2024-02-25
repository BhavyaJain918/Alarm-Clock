import threading
import tkinter
import datetime
import winsound
import mysql.connector
import time
import sys

try:
    # Replace the empty quotes with your MySQL username and password
    mydb = mysql.connector.connect(host = "localhost" , user = "" , passwd = "" , database = "Clock")   
    myc = mydb.cursor(buffered = True) 
except mysql.connector.errors.DatabaseError:
     sys.exit()

snd = "C:\\Users\\Bhavya Jain\\Music\\Alarm.wav"

def check_alarm():
        alarm_set = set()
        while True:
            global cur_date
            cur_date = datetime.date.today().strftime("%d-%m-%Y")
            myc.execute("SELECT Time FROM Alarm WHERE Date = %s" , (cur_date , ))
            alarm = myc.fetchall()
            for a in alarm:
                for x in a:
                    alarm_set.add(str(x))
            while alarm_set != set():
                global alarm1
                for alarm1 in alarm_set:
                    if alarm1 == datetime.datetime.now().strftime("%H:%M"):
                        myc.execute("SELECT Message FROM Alarm WHERE Time = %s" , (alarm1 , ))
                        mess = myc.fetchone()
                        if mess != None:
                            myc.execute("DELETE FROM Alarm WHERE Time = %s" , (str(alarm1) , ))
                            mydb.commit()
                            global m
                            for m in mess:
                                 return m
                    else:
                        continue
                return False
def print1(msg):
        global root
        root = tkinter.Tk()
        root.geometry("250x100")
        root.title("Alarm Clock")
        photo = tkinter.PhotoImage(file = "C:\\Users\\Bhavya Jain\\Downloads\\Alarm.png")
        root.iconphoto(False , photo)
        txt = f"Alarm: {str(msg)}"
        lbl = tkinter.Label(root , text = txt)
        lbl.place(relx = 0.5 , rely = 0.2 , anchor = "center")
        btn = tkinter.Button(root , text = "Stop" , command = stop)
        btn.place(relx = 0.35 , rely = 0.6 , anchor = "center")
        btn1 = tkinter.Button(root , text = "Snooze" , command = snooze)
        btn1.place(relx = 0.6 , rely = 0.6 , anchor = "center")
        return 0

def play():
    try:
        winsound.PlaySound(snd , winsound.SND_ASYNC | winsound.SND_FILENAME | winsound.SND_LOOP)
    except RuntimeError:
         sys.exit()

def stop():
    winsound.PlaySound(None , winsound.SND_PURGE)

def snooze():
    try:
        winsound.PlaySound(None , winsound.SND_PURGE)
        alarm2 = datetime.datetime.strptime(alarm1 , "%H:%M")
        alarm2 += datetime.timedelta(minutes = 10)
        alarm3 = alarm2.strftime("%H:%M")
        myc.execute("INSERT INTO Alarm VALUES (%s , %s , %s)" , (alarm3 , cur_date , str(m)))
        mydb.commit()
        lbl2 = tkinter.Label(root , text = "Snoozed for 10 minutes")
        lbl2.place(relx = 0.5 , rely = 0.8 , anchor = "center")
    except RuntimeError:
         sys.exit()
    except mysql.connector.errors.DatabaseError:
         sys.exit()

while True:
    time.sleep(6)
    msg = check_alarm()
    if msg != False:
        ans = print1(msg)
        if ans == 0:
            th = threading.Thread(target = play)
            th.start()
            root.mainloop()
            winsound.PlaySound(None , winsound.SND_PURGE)
    else:
         continue
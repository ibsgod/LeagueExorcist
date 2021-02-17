import subprocess
from tkinter import *
from tkinter import font
import os
import smtplib
from email.mime.text import MIMEText
currProc = "LeagueClient.exe"
procText = None
warnText = None
popup = None
def get_processes_running():
    tasks = subprocess.check_output(['tasklist']).decode('cp866', 'ignore').split("\r\n")
    p = []
    for task in tasks:
        m = re.match("(.+?) +(\d+) (.+?) +(\d+) +(\d+.* K).*",task)
        if m is not None and ".exe" in m.group(1):
            p.append({"image":m.group(1),
                        "pid":m.group(2),
                        "session_name":m.group(3),
                        "session_num":m.group(4),
                        "mem_usage":m.group(5)
                        })
    p.sort(reverse=True, key=lambda x: int(x["mem_usage"].split()[0].replace("," , "")))
    return p
def send(to):
    smtp_ssl_host = 'smtp.gmail.com'
    smtp_ssl_port = 465
    username = 'EMAIL_HERE'
    password = 'PASSWORD_HERE'

    from_addr = username
    to_addrs = [to]
    message = MIMEText("I just closed League Exorcist! Cringe!")
    message['subject'] = 'Bruh'
    message['from'] = from_addr
    message['to'] = ', '.join(to_addrs)
    server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
    server.login(username, password)
    server.sendmail(from_addr, to_addrs, message.as_string())
    print("Sent email", "to:", to)
    server.quit()

def huntProcess(name):
    global currProc
    global procText
    if name is None:
        return
    currProc = name
    procText = "Currently hunting: " + (currProc if currProc is not None else "None")
    warnText.configure(text="Make sure you're sure before hunting!")
    chooseText.configure(text=procText)

def hunting():
    global processes
    global listt
    global currProc
    global popup
    global warnText
    processes = get_processes_running()
    listt.delete(0, listt.size())
    for i in range(len(processes)):
        listt.insert(i + 1, processes[i]["image"])
        if currProc is not None and currProc == processes[i]["image"]:
            os.system("taskkill /f /im " + currProc)
            warnText.configure(text=currProc + " has been hunted!")
    root.after(5000, hunting)


root = Tk()
root.geometry("500x500")
title = Label(root, text="League Exorcist", pady=0, font=font.Font(size=30, family="Microsoft Yahei UI Light"))
title.pack()
listt = Listbox(root, height=16, width=40)
processes = get_processes_running()
for i in range(len(processes)):
    listt.insert(i+1, processes[i]["image"])
procText = "Currently hunting: " + (currProc if currProc is not None else "None")
chooseText = Label(root, text=procText, pady=5, font=font.Font(size=15, family="Microsoft Yahei UI Light"))
chooseText.pack()
listt.pack()
warnText = Label(root, wraplength=400, text="Make sure you're sure before hunting! Processes update every 5 sec", pady=10, font=font.Font(size=14, family="Microsoft Yahei UI Light"))
warnText.pack()
killButt = Button(root, text="Hunt!", padx=20, pady=0, font=font.Font(size=15, family="Microsoft Yahei UI Light"), command=lambda: huntProcess(processes[listt.curselection()[0]]["image"] if len(listt.curselection()) > 0 else None))
killButt.pack()
root.after(5000, hunting)
def on_closing():
    send("FRIEND'S EMAIL HERE")
    sys.exit()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
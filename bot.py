from datetime import datetime
import schedule
import re
import time as tm
import sqlite3
from os import path
import pyautogui
import attendee_bot

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Put the google login credential.
username = ""
password = ""

def waiting(xpath, driver):
    im_in = None
    wait_for = 1
    while True:
        try:
            im_in = driver.find_element_by_xpath(xpath)
            print("I'm in the lecture")
            return im_in
        except:
            if wait_for <= 15:
                print("Not Yet Joined")
                tm.sleep(60)
                wait_for += 1
            else:
                return im_in

def val_day(given_day):
    days = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
    return True if given_day.lower() in days else False

def val_time(time):
    return False if not re.match("([01]?[0-9]|2[0-3]):[0-5][0-9]", time) else True

def createDB():
    conn = sqlite3.connect('timetable.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE timetable(class_name text, start_time text, end_time text, day text, class_link text)''')
    conn.commit()
    conn.close()
    print("Timetable DB Created")

def modify_timetable():
    if not(path.exists("timetable.db")):
        createDB()
    ch = int(input("1.Add class\n2.Done\nEntert Choice:"))
    while(ch == 1):
        class_name = input("Enter Class Name:")
        start_time = input("Enter Starting Time of Class In HH:MM Format:")
        while not(val_time(start_time)):
            print("Invalid Input, Try Again")
            start_time = input("Enter Starting Time of Class In HH:MM Format:")

        end_time = input("Enter Ending Time of Class In HH:MM Format:")
        while not(val_time(start_time)):
            print("Invalid Input, Try Again")
            end_time = input("Enter Ending Time of Class In HH:MM Format:")

        day = input("Enter Day(Note: specify full word):")
        while not(val_day(day)):
            print("Invalid Input, Try Again")
            day = input("Enter Day(Note: specify full word):")

        class_link = input("Enter Class Link(Specific for meet Only):")

        conn = sqlite3.connect('timetable.db')
        c = conn.cursor()

        c.execute("INSERT INTO timetable VALUES ('%s', '%s', '%s', '%s', '%s')"%(class_name,start_time,end_time,day,class_link))
        conn.commit()
        conn.close()
        print("Class Added to Database\n")
        ch = int(input("1.Add class\n2.Done\nEntert Choice:"))

def view_timetable():
    if not(path.exists('timetable.db')):
        print("DB is not created")
        return
    else:
        conn = sqlite3.connect('timetable.db')
        c = conn.cursor()
        for row in c.execute('SELECT * FROM timetable'):
            print(row)
        conn.close()

def join_class(class_name, start_time, end_time, class_link):
    opt = Options()
    opt.add_argument("--disable-infobars")
    opt.add_argument("start-maximized")
    opt.add_argument("--disable-extensions")
    opt.add_argument("--start-maximized")
    opt.add_experimental_option("prefs", { \
        "profile.default_content_setting_values.media_stream_mic": 1, 
        "profile.default_content_setting_values.media_stream_camera": 1,
        "profile.default_content_setting_values.geolocation": 1, 
        "profile.default_content_setting_values.notifications": 1 
    })
    driver=webdriver.Chrome(executable_path='chromedriver.exe',options=opt)

    driver.get('https://stackoverflow.com/users/signup?ssrc=head&returnurl=%2fusers%2fstory%2fcurrent%27')
    tm.sleep(3)
    driver.find_element_by_xpath('//*[@id="openid-buttons"]/button[1]').click()
    driver.find_element_by_xpath('//input[@type="email"]').send_keys(username)
    driver.find_element_by_xpath('//*[@id="identifierNext"]').click()
    tm.sleep(3)
    driver.find_element_by_xpath('//input[@type="password"]').send_keys(password)
    driver.find_element_by_xpath('//*[@id="passwordNext"]').click()
    tm.sleep(2)
    driver.get(class_link)
    tm.sleep(5)

    """try:
        mic_btn = driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[5]/div[3]/div/div/div[2]/div/div[1]/div[1]/div/div[4]/div[1]/div/div/div')
        cam_btn = driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[5]/div[3]/div/div/div[2]/div/div[1]/div[1]/div/div[4]/div[2]/div/div')
        entr_btn =driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[5]/div[3]/div/div/div[2]/div/div[1]/div[2]/div/div[2]/div/div[1]/div/span')
        exit_xpath = '//*[@id="ow3"]/div[1]/div/div[5]/div[3]/div[9]/div[2]/div[2]/div'
    except:
        mic_btn = driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[6]/div[3]/div/div/div[2]/div/div[1]/div[1]/div/div[4]/div[1]/div/div/div')
        cam_btn = driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[6]/div[3]/div/div/div[2]/div/div[1]/div[1]/div/div[4]/div[2]/div/div')
        entr_btn =driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[6]/div[3]/div/div/div[2]/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/span')    
        exit_xpath = '//*[@id="ow3"]/div[1]/div/div[6]/div[3]/div[9]/div[2]/div[2]/div'
    """

    try:
        if driver.find_element_by_xpath('//*[@data-tooltip="Turn off microphone (CTRL + D)"]'):
            driver.find_element_by_xpath('//*[@data-tooltip="Turn off microphone (CTRL + D)"]').click()
    except:
        print("Microphone was off already")
        
    try:
        if driver.find_element_by_xpath('//*[@data-tooltip="Turn off camera (CTRL + E)"]'):
            driver.find_element_by_xpath('//*[@data-tooltip="Turn off camera (CTRL + E)"]').click()
    except:
        print("Camera was off already")


    driver.find_element_by_xpath('//*[@class="uArJ5e UQuaGc Y5sE8d uyXBBb xKiqt"]').click()
    im_in = waiting('//*[@id="ow3"]', driver)
    if im_in == None:
        print("there is no lect")
        attendee_bot.send_msg(class_name = class_name, status="noclass", start_time = start_time, end_time = end_time)
    else:
        attendee_bot.send_msg(class_name = class_name, status="joined", start_time = start_time, end_time = end_time)
        tm.sleep(10)

        tmp = "%H:%M"
        class_running_time = datetime.strptime(end_time,tmp) - datetime.strptime(start_time,tmp)
        tm.sleep(class_running_time.seconds)
        pyautogui.press('enter')    
        driver.find_element_by_xpath('//*[@data-tooltip="Leave call"]').click()
        print("Lecture is Over")
        attendee_bot.send_msg(class_name = class_name, status="left", start_time = start_time, end_time = end_time)
        driver.close()
    
def scheduling():
    if not(path.exists('timetable.db')):
        print("Timetable is not present!, make timetable first")
        return
    else:
        conn = sqlite3.connect('timetable.db')
        c = conn.cursor()
        for row in c.execute('SELECT * FROM timetable'):
            class_name = row[0]
            start_time = row[1]
            end_time = row[2]
            day = row[3]
            class_link = row[4]

            if day.lower() == "monday":
                schedule.every().monday.at(start_time).do(join_class, class_name, start_time, end_time, class_link)
                print("Scheduled Class '%s' on %s at %s"%(class_name,day,start_time))
            if day.lower() == "tuesday":
                schedule.every().tuesday.at(start_time).do(join_class, class_name, start_time, end_time, class_link)
                print("Scheduled Class '%s' on %s at %s"%(class_name,day,start_time))
            if day.lower() == "wednesday":
                schedule.every().wednesday.at(start_time).do(join_class, class_name, start_time, end_time, class_link)
                print("Scheduled Class '%s' on %s at %s"%(class_name,day,start_time))
            if day.lower() == "thursday":
                schedule.every().thursday.at(start_time).do(join_class, class_name, start_time, end_time, class_link)
                print("Scheduled Class '%s' on %s at %s"%(class_name,day,start_time))
            if day.lower() == "friday":
                schedule.every().friday.at(start_time).do(join_class, class_name, start_time, end_time, class_link)
                print("Scheduled Class '%s' on %s at %s"%(class_name,day,start_time))
            if day.lower() == "saturday":
                schedule.every().saturday.at(start_time).do(join_class, class_name, start_time, end_time, class_link)
                print("Scheduled Class '%s' on %s at %s"%(class_name,day,start_time))
            if day.lower() == "sunday":
                schedule.every().sunday.at(start_time).do(join_class, class_name, start_time, end_time, class_link)
                print("Scheduled Class '%s' on %s at %s"%(class_name,day,start_time))
    while True:
        schedule.run_pending()
        tm.sleep(1)
              

if __name__ == "__main__":
    ch = int(input("1.Modify Timetable\n2.View Timetable\n3.Start Bot\nEnter a Choice:"))
    if ch == 1:
        modify_timetable()
    elif ch == 2:
        view_timetable()
    elif ch == 3:
        scheduling()


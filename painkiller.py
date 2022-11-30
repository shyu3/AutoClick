import pyautogui
import tkinter as tk
import tkinter.ttk
import os
import datetime # 현재 시간 출력용
import time     # sleep 함수 사용
import threading
import keyboard
# 윈도우에선 1로바꾸셈
TITLE = "LSauto v1.0.2"
RESOLUTION_OFFSET = 1
Button_X=575+430
BOX_X=475+440
Stop_bit=False
run_key="F5"
stop_key="F4"
def tk_window_config():
    window = tk.Tk()
    window.title('LSauto')
    window.geometry('680x960')
    eStatus, maxcnt=count_image_list()
    
    #count image view
    label1 =tk.Label(window, text ="num of inmage:",width=10)
    label1.grid(row=0, column=0)
    
    entry1=tk.Entry(window)
    entry1.grid(row=0, column=1)
    if eStatus == "OK":
        entry1.insert("end",maxcnt)

    btn1 = tk.Button(window,text="Refresh",command =refresh_button,repeatdelay=1000, repeatinterval=100)
    btn1.grid(row=0, column=2)
    
    #run button view
    label2 =tk.Label(window, text ="Auto Click:",width=10)
    label2.grid(row=1, column=0)
    btn2 = tk.Button(window,text="Run",command =run_button,repeatdelay=1000, repeatinterval=100)
    btn2.grid(row=1, column=1)
    
    
    return window

def count_image_list():
    dir_path = "./asset_list/"
    global file_path
    cnt=0
    for (root, directories, files) in os.walk(dir_path):
        for file in files:
            if '.png' in file:
                file_path = os.path.join(root, file)
                cnt+=1
                print(cnt)
                print(file_path)
    file_path= file_path.split("/")
    file_path= file_path[2].split("asset")
    file_path= file_path[1].split(".png")
    
    if int(file_path[0]) == cnt:
        return "OK",cnt
    else :
        pyautogui.alert("image num & image cnt not equal")
        return "NOK",cnt
def browsing_image_onece(max) :
    # list=[]
    for i in range(1,max+1):
        path_str = "./asset_list/asset"+ str(i) +".png"
        for i in range(0,12):
            print(i)
            list = pyautogui.locateOnScreen(path_str, confidence=0.9, grayscale=True)
            move_cursor_and_click_onece(list)

def move_cursor_and_click_onece(list) :   
    global Stop_bit

    if Stop_bit ==True :
        Stop_bit=False
        return
    
    x = list.left/RESOLUTION_OFFSET
    y = list.top/RESOLUTION_OFFSET
    dx = list.width/(2*RESOLUTION_OFFSET)
    dy = list.height/(2*RESOLUTION_OFFSET)
    
    # 이걸로 테스트하고 잘되면 밑에꺼 참조 푸셈
    pyautogui.moveTo(x+dx, y+dy)

    if Click_ON.get() == True:
        time.sleep(0.01)
        pyautogui.click(x+dx,y+dy)



def browsing_image_list(max) :
    # list=[]
    global Stop_bit
    Stop_bit_status = False
    for i in range(1,max+1):
        if Stop_bit_status == True :
            Stop_bit=False
            break;
        else:
            path_str = "./asset_list/asset"+ str(i) +".png"
            list = pyautogui.locateAllOnScreen(path_str, confidence=0.9, grayscale=True)
            Stop_bit_status= move_cursor_and_click(list)

def move_cursor_and_click(list) :
    global Stop_bit
    for i in list:
        if Stop_bit ==True :
            break;
        # if keyboard.is_pressed("e") :
        #     Stop_bit=True
        #     break;
        x = i.left/RESOLUTION_OFFSET
        y = i.top/RESOLUTION_OFFSET
        dx = i.width/(2*RESOLUTION_OFFSET)
        dy = i.height/(2*RESOLUTION_OFFSET)
        
        # 이걸로 테스트하고 잘되면 밑에꺼 참조 푸셈
        pyautogui.moveTo(x+dx, y+dy)

        if Click_ON.get() == True:
            time.sleep(0.01)
            pyautogui.click(x+dx,y+dy)
    
    return Stop_bit
def refresh_button():
    reStatus, maxcnt=count_image_list()
    entry0.delete(0,10)
    entry0.insert("end",maxcnt)
    
def run_button():
    global run_key
    global stop_key
    # stopping=threading.Thread(target=stop_thread,args=(stop_key,))
    # stopping.daemon = True
    # stopping.start()
    
    running= threading.Thread(target=run_thread)
    running.daemon = True
    running.start()
    
def stop_thread(key):
    global Stop_bit
    while True:
        time.sleep(0.02)
        if keyboard.is_pressed(key) :
            Stop_bit=True
            break
    
def run_thread():
    imagecnt=entry0.get()
    if Click_ON_casting_method.get() == True:
       browsing_image_list(int(imagecnt))
    else:
        browsing_image_onece(int(imagecnt))
    pyautogui.alert("Finished!")
    return

def stop_button():
    global Stop_bit
    Stop_bit=True
    return
    
def auto_run_keyPressHandler(e):
    run_button()
    print("Pressed1: ",e.keycode)
    
def apply_auto_run_key():
    global window
    global run_key
    run_key=str(entry2.get())
    # window.bind("<"+str(entry2.get())+">",auto_run_keyPressHandler)
    # window.bind("<F5>",auto_run_keyPressHandler)
    return

def stop_keyPressHandler(e):
    stop_button()
    print("Pressed2: ",e.keycode)
    
def apply_stop_key():
    global window
    global stop_key
    stop_key=str(entry3.get())
    # key1=window.bind("<"+str(entry3.get())+">",stop_keyPressHandler)
    # window.bind("<F4>",stop_keyPressHandler)
    return

def key_thread(keyS,keyR):
    global Stop_bit
    global stop_key, run_key
    while True:
        time.sleep(0.02)
        if keyboard.is_pressed(stop_key) :
            Stop_bit=True
            time.sleep(0.05)
            # break
        elif keyboard.is_pressed(run_key) :
            run_button()
            time.sleep(0.05)
            # break
        
#############################  main  #####################################

# window=tk_window_config()
window = tk.Tk()
window.title(TITLE)
window.geometry('720x960+200+200')
window.resizable(True, True)
Status, maxcnt=count_image_list()

#count image view
label0 =tk.Label(window, text ="image num:",width=20)
label0.grid(row=0, column=0)

entry0=tk.Entry(window,width=10)
entry0.grid(row=0, column=1)
if Status == "OK":
    entry0.insert("end",maxcnt)

btn0 = tk.Button(window,text="Refresh",command =refresh_button,repeatdelay=1000, repeatinterval=100)
btn0.grid(row=0, column=5)

#run button view
label1 =tk.Label(window, text ="Auto Click:",width=20)
label1.grid(row=1, column=0)

btn1 = tk.Button(window,text="Run",command =run_button,repeatdelay=1000, repeatinterval=100)
btn1.grid(row=1, column=5)

Click_ON=tk.BooleanVar()
checkbutton1=tk.Checkbutton(window , variable=Click_ON,text="On/Off",width=10)#
checkbutton1.grid(row=1, column=1)
checkbutton1.select()

#run Command key
label2 =tk.Label(window, text ="Auto run Command:",width=20)
label2.grid(row=2, column=0)

entry2=tk.Entry(window,width=10)
entry2.grid(row=2, column=1)
entry2.insert("end","F5")


btn2 = tk.Button(window,text="Apply",command =apply_auto_run_key,repeatdelay=1000, repeatinterval=100)
btn2.grid(row=2, column=5)
apply_auto_run_key()

#stop Command key
label3 =tk.Label(window, text ="Stop Command:",width=20)
label3.grid(row=3, column=0)

entry3=tk.Entry(window,width=10)#,state="readonly"
entry3.grid(row=3, column=1)
entry3.insert("end","F4")


btn3 = tk.Button(window,text="Apply",command =apply_stop_key,repeatdelay=1000, repeatinterval=100)
btn3.grid(row=3, column=5)
apply_stop_key()


Click_ON_casting_method=tk.BooleanVar()
checkbutton4=tk.Checkbutton(window , variable=Click_ON_casting_method,text="All/OnebyOne",width=12)#
checkbutton4.grid(row=5, column=1)
checkbutton4.select()

if __name__== "__main__":
    # global run_key
    # global stop_key
    keyboarding=threading.Thread(target=key_thread,args=(stop_key,run_key))
    keyboarding.daemon = True
    keyboarding.start()
    
    window.mainloop()
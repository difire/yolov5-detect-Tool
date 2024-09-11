import cv2
from UI.TkUI import mytkinter
from tkinter import filedialog
from PIL import Image,ImageTk
import threading
import time

from DetectApi import DETECT_API        #yolov5使用模型检测接口

class MyTk(mytkinter):
    tab_id=0
    cap=None
    video_switch=False#控制视频开始或者结束
    pause_switch=False#控制视频播放或者暂停
    check_switck=False#控制视频检测
    def __init__(self):
        super().__init__()
        self.setupUi()
        # 初始化模型
        try:
            with open("configure.txt", "r") as f:
                conf_data = f.read().split(" ")
                print(conf_data)
            weight = conf_data[0]
            self.label1['text']=weight
            # print(weight)
            imgsz = int(conf_data[1])  # 输入图片的大小 默认640(pixels)
            self.var2.set(conf_data[1])
            conf_thres = float(conf_data[2])  # object置信度阈值 默认0.25  用在nms中
            self.var3.set(conf_data[2])
            iou_thres = float(conf_data[3])  # 做nms的iou阈值 默认0.45   用在nms中
            self.var4.set(conf_data[3])
            max_det = int(conf_data[4])  # 每张图片最多的目标数量  用在nms中
            self.var5.set(conf_data[4])
            device = conf_data[5]
            self.var6.set(conf_data[5])
            self.DETECT = DETECT_API(weight, imgsz, conf_thres, iou_thres, max_det, device)
        except Exception as e:
            print("模型初始化失败：", e)
            # return 0

        self.btn1.config(command=self.open_pt_file)
        self.btn2.config(command=self.save_config)

        self.myplace()
        # 监听窗口大小改变
        self.bind('<Configure>', self.window_resize)
        self.cv.bind("<Button-1>", self.Begin)
        self.bind("<Key>",self.KEY_EVENTS)

    def Begin(self,event):
        self.tab_main.place(relx=0, rely=0, relwidth=1, relheight=1)
    def open_pt_file(self):
        file=filedialog.askopenfilename(title='选择权重文件',filetypes=[("权重文件",".pt")])
        print(file)
        self.label1.config(text=file)

    def open_pic(self):
        file = filedialog.askopenfilename(title='选择图片', filetypes=[("图片1", ".jpg"),("图片2", ".png")])
        print(file)
        self.current_img=cv2.imread(file)
        self.show_origin_pic(self.current_img*1,self.VLabel1)

    def open_video(self):
        if self.video_switch:return None
        file = filedialog.askopenfilename(title='选择视频', filetypes=[("1", ".MP4"), ("2", ".avi")])
        print(file)
        if not file:return None
        self.cap=cv2.VideoCapture()
        self.cap.open(file)
        self.video_switch=True
        self.check_switck=True
        self.mythread(self.show_video)

    def open_cam(self):
        if self.video_switch:return None
        self.cap = cv2.VideoCapture(0)
        if self.cap.isOpened():
            self.video_switch=True
            self.check_switck = True
            # self.mythread(self.show_video)
            self.show_video()

    def VideoSwitch(self):
        self.video_switch=not self.video_switch

    def PauseSwitch(self):
        self.pause_switch= not self.pause_switch

    def CheckSwitch(self):
        self.check_switck = not self.check_switck
    def mythread(self,cmd):
        t=threading.Thread(target=cmd)
        t.start()

    def show_video(self):
        # t1=time.time()
        while self.video_switch:
            # time.sleep(20)
            if self.pause_switch:
                # time.sleep(50)
                continue
            else:
                ret, frame = self.cap.read()
                if ret:
                    if self.tab_id==1:
                        vlabelin=self.VLabel3
                        vlabelout=self.VLabel4
                    elif self.tab_id==2:
                        vlabelin=self.VLabel5
                        vlabelout=self.VLabel6
                    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    self.show_origin_pic(frame,vlabelin)
                    if self.check_switck:self.show_result(frame,vlabelout)
                else:
                    self.video_switch=False
                    break
        self.cap.release()
        


    def show_result(self,img,label):
        detections = self.DETECT.detect(img)
        for i in detections:
            # print(i)
            x, y, w, h = i['position']
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
            img = cv2.putText(img, "{} {}".format(i['class'],round(i['conf'], 3)), (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),
                              1,
                              cv2.LINE_AA)
        frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        p_w = frame.shape[1]
        p_h = frame.shape[0]
        L_w = label.winfo_width()
        L_h = label.winfo_height()
        i = p_w / p_h
        j = L_w / L_h
        if (i > j):
            p_w = int(L_w)
            p_h = int(p_w / i)
        else:
            p_h = int(L_h)
            p_w = int(p_h * i)
        img_=Image.fromarray(frame)
        img_=img_.resize((p_w,p_h))
        self.result_img_tk=ImageTk.PhotoImage(img_)
        label.config(image=self.result_img_tk)

    def KEY_EVENTS(self,event):
        print("char:{} ASCII:{} 按键名:{} 代码:{}".format(event.char,event.keycode,event.keysym,event.keysym_num))
        # print(self.tab_main.select())
        if event.char=='1':
            self.tab_id=0
            self.tab_main.select(self.tab_id)
        elif event.char=='2':
            self.tab_id = 1
            self.tab_main.select(self.tab_id)
        elif event.char=='3':
            self.tab_id = 2
            self.tab_main.select(self.tab_id)
        elif event.char=='4':
            # print("设置")
            self.tab_id = 3
            self.tab_main.select(self.tab_id)
        elif event.char=='o':
            if self.tab_id==0:
                self.open_pic()
            elif self.tab_id==1:
                self.open_video()
            elif self.tab_id==2:
                self.open_cam()
        elif event.char=='c':
            if self.tab_id==0:
                self.show_result(self.current_img,self.VLabel2)
            elif self.tab_id==1 or self.tab_id==2:
                self.CheckSwitch()
        elif event.char=='p':
            self.PauseSwitch()
        elif event.char=='q':
            self.VideoSwitch()


    def myplace(self):#place布局，self.cv作为父控件，其尺寸改变，其子控件大小相应刷新
        self.cv.place(x=0,y=0,width=self.width,height=self.height)

    def mybutton(self, canvas, x, y, w, h, text):
        canvas.create_rectangle(int(x - w / 2), int(y - h / 2), int(x + w / 2), int(y + h / 2), fill="white",
                                outline="grey", width=0, tags=("BOTTON", "border",))
        t = canvas.create_text(x, y, text=text, font=('黑体', 15, 'bold'), fill='black', tags=("BOTTON", "btn_text",))
        canvas.tag_bind("btn_text", "<Enter>", lambda event: canvas.itemconfig("current", fill='#bbbeee'))
        canvas.tag_bind("btn_text", "<Leave>", lambda event: canvas.itemconfig("current", fill='black'))
        return t


    def save_config(self):
        weight = self.label1['text']
        # print(weight)
        imgsz = int(self.var2.get())  # 输入图片的大小 默认640(pixels)
        conf_thres = float(self.var3.get())  # object置信度阈值 默认0.25  用在nms中
        iou_thres = float(self.var4.get())  # 做nms的iou阈值 默认0.45   用在nms中
        max_det = int(self.var5.get())  # 每张图片最多的目标数量  用在nms中
        device = self.var6.get()
        config_txt = "{} {} {} {} {} {}".format(weight, imgsz, conf_thres, iou_thres, max_det, device)
        with open("configure.txt", "w") as f:
            f.write(config_txt)
        self.DETECT = DETECT_API(weight, imgsz, conf_thres, iou_thres, max_det, device)
        print("已保存设置", weight, imgsz, conf_thres, iou_thres, max_det, device, sep='\t')
        self.tab_main.select(self.tab_id)

    def show_origin_pic(self,cv2_img,vlabel):#图像预处理，用于显示图像
        #将cv2格式文件转二进制格式
        rgb_img=cv2.cvtColor(cv2_img,cv2.COLOR_BGR2RGB)
        p_w = rgb_img.shape[1]
        p_h = rgb_img.shape[0]
        L_w = vlabel.winfo_width()
        L_h = vlabel.winfo_height()
        i = p_w / p_h
        j = L_w / L_h
        if (i > j):
            p_w = int(L_w)
            p_h = int(p_w / i)
        else:
            p_h = int(L_h)
            p_w = int(p_h * i)
        img=Image.fromarray(rgb_img)
        img=img.resize((p_w,p_h))
        # print(img.size)
        self.tk_img=ImageTk.PhotoImage(img)
        vlabel.config(image=self.tk_img)



    def window_resize(self,event=None):
        if event:
            # print(event)
            if self.winfo_width()==self.width and self.winfo_height()==self.height:
                return
            if self.first_load:
                self.first_load=False
                return
            self.width=self.winfo_width()
            self.height=self.winfo_height()
            self.myplace()
            # print(self.place_slaves(),self.place_slaves()[0].place_info())




if __name__=='__main__':
    top=MyTk()
    top.mainloop()

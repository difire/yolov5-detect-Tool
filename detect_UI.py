import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QCursor,QIcon,QKeySequence
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication,QMainWindow,QFileDialog,QMenu,QAction,QShortcut
from UI.WinUI import Ui_YOLOWindow
import cv2

from DetectApi import DETECT_API        #yolov5使用模型检测接口

class Begin(QMainWindow,Ui_YOLOWindow):
    def __init__(self):
        super(Begin, self).__init__()
        self.setupUi(self)
        # 设置图标
        self.setWindowIcon(QtGui.QIcon(QtGui.QPixmap("UI/bg1.jpg")))

        #初始化模型
        try:
            with open("configure.txt", "r") as f:
                conf_data=f.read().split(" ")
                print(conf_data)
            weight = conf_data[0]
            self.label.setText(weight)
            # print(weight)
            imgsz = int(conf_data[1])  # 输入图片的大小 默认640(pixels)
            self.lineEdit.setText(conf_data[1])
            conf_thres = float(conf_data[2])  # object置信度阈值 默认0.25  用在nms中
            self.lineEdit_2.setText(conf_data[2])
            iou_thres = float(conf_data[3])  # 做nms的iou阈值 默认0.45   用在nms中
            self.lineEdit_3.setText(conf_data[3])
            max_det = int(conf_data[4])  # 每张图片最多的目标数量  用在nms中
            self.lineEdit_4.setText(conf_data[4])
            device = conf_data[5]
            self.lineEdit_5.setText(conf_data[5])
            self.DETECT = DETECT_API(weight, imgsz, conf_thres, iou_thres, max_det, device)
        except Exception as e:
            print("模型初始化失败：",e)
            # return 0


        #声明在self.tab中创建右键菜单
        self.tab.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tab.customContextMenuRequested.connect(self.create_rightmenu)#连接菜单显示函数

        self.tab_2.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tab_2.customContextMenuRequested.connect(self.create_rightmenu2)  # 连接菜单显示函数

        self.tab_3.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tab_3.customContextMenuRequested.connect(self.create_rightmenu3)  # 连接菜单显示函数

        self.connect_btn()

        self.cam_switch=0
        self.tab_index=0

        #设置快捷键
        #tab
        QShortcut(QKeySequence("O"), self.tab,self.open_pic)
        QShortcut(QKeySequence("C"), self.tab, self.check_pic)
        # tab2
        QShortcut(QKeySequence("O"), self.tab_2, self.open_video)
        QShortcut(QKeySequence("P"), self.tab_2, self.VideoSwitch)  #暂停开关
        QShortcut(QKeySequence("C"), self.tab_2, self.VideoCheckSwitch)#检测开关
        QShortcut(QKeySequence("Q"), self.tab_2, self.CloseVideo)
        # tab3
        QShortcut(QKeySequence("O"), self.tab_3, self.open_cam)
        QShortcut(QKeySequence("C"), self.tab_3, self.VideoCheckSwitch)
        QShortcut(QKeySequence("Q"), self.tab_3, self.close_cam)




    def connect_btn(self):
        self.pushButton.clicked.connect(self.open_pt_file)
        self.pushButton_3.clicked.connect(self.save_config)


    def create_rightmenu(self):
        #菜单对象1
        self.tab_menu=QMenu(self.tab)

        self.actionA=QAction(QIcon('UI/bg1.jpg'), u'选择图片', self.tab)
        self.actionA.setShortcut('O')      #设置快捷键，实际这里设置的快捷键无效，但能在选项后面显示快捷键，故还是加上了
        self.tab_menu.addAction(self.actionA)#将动作A加入菜单

        self.actionB = QAction(QIcon('UI/bg1.jpg'), u'检测', self.tab)
        self.actionB.setShortcut('C')  # 设置快捷键，实际这里设置的快捷键无效，但能在选项后面显示快捷键，故还是加上了

        self.tab_menu.addAction(self.actionB)  # 将动作B加入菜单

        self.actionC = QAction(QIcon('UI/bg1.jpg'), u'保存图片', self.tab)
        self.actionC.setShortcut('S')  # 设置快捷键，实际这里设置的快捷键无效，但能在选项后面显示快捷键，故还是加上了
        self.tab_menu.addAction(self.actionC)  # 将动作C加入菜单

        self.actionA.triggered.connect(self.open_pic)
        self.actionB.triggered.connect(self.check_pic)

        self.tab_menu.popup(QCursor.pos())#声明当前鼠标在tab控件上右击时，在鼠标位置显示菜单

    def create_rightmenu2(self):
        #菜单对象1
        self.tab_menu2=QMenu(self.tab_2)

        self.actionA2=QAction(QIcon('UI/bg1.jpg'), u'选择视频', self.tab_2)
        self.actionA2.setShortcut('O')  # 设置快捷键，实际这里设置的快捷键无效，但能在选项后面显示快捷键，故还是加上了
        self.tab_menu2.addAction(self.actionA2)#将动作A加入菜单

        self.actionB2 = QAction(QIcon('UI/bg1.jpg'), u'检测', self.tab_2)
        self.actionB2.setShortcut('C')  # 设置快捷键，实际这里设置的快捷键无效，但能在选项后面显示快捷键，故还是加上了
        self.tab_menu2.addAction(self.actionB2)  # 将动作B加入菜单

        self.actionC2 = QAction(QIcon('UI/bg1.jpg'), u'暂停开关', self.tab_2)
        self.actionC2.setShortcut('P')  # 设置快捷键，实际这里设置的快捷键无效，但能在选项后面显示快捷键，故还是加上了
        self.tab_menu2.addAction(self.actionC2)  # 将动作C加入菜单

        self.actionD2 = QAction(QIcon('UI/bg1.jpg'), u'关闭视频', self.tab_2)
        self.actionD2.setShortcut('Q')  # 设置快捷键，实际这里设置的快捷键无效，但能在选项后面显示快捷键，故还是加上了
        self.tab_menu2.addAction(self.actionD2)  # 将动作C加入菜单

        self.actionA2.triggered.connect(self.open_video)
        self.actionB2.triggered.connect(self.VideoCheckSwitch)
        self.actionC2.triggered.connect(self.VideoSwitch)
        self.actionD2.triggered.connect(self.CloseVideo)

        self.tab_menu2.popup(QCursor.pos())#声明当前鼠标在tab控件上右击时，在鼠标位置显示菜单


    def create_rightmenu3(self):
        #菜单对象1
        self.tab_menu3=QMenu(self.tab_3)

        self.actionA3=QAction(QIcon('UI/bg1.jpg'), u'打开摄像头', self.tab_3)
        self.actionA3.setShortcut('O')      #设置快捷键，实际这里设置的快捷键无效，但能在选项后面显示快捷键，故还是加上了
        self.tab_menu3.addAction(self.actionA3)#将动作A加入菜单

        self.actionB3 = QAction(QIcon('UI/bg1.jpg'), u'检测', self.tab_3)
        self.actionB3.setShortcut('C')  # 设置快捷键，实际这里设置的快捷键无效，但能在选项后面显示快捷键，故还是加上了
        self.tab_menu3.addAction(self.actionB3)  # 将动作B加入菜单

        self.actionC3 = QAction(QIcon('UI/bg1.jpg'), u'关闭摄像头', self.tab_3)
        self.actionC3.setShortcut('Q')  # 设置快捷键，实际这里设置的快捷键无效，但能在选项后面显示快捷键，故还是加上了
        self.tab_menu3.addAction(self.actionC3)  # 将动作C加入菜单

        self.actionA3.triggered.connect(self.open_cam)
        self.actionB3.triggered.connect(self.VideoCheckSwitch)
        self.actionC3.triggered.connect(self.close_cam)

        self.tab_menu3.popup(QCursor.pos())#声明当前鼠标在tab控件上右击时，在鼠标位置显示菜单

    def open_pt_file(self):
        print("选择权重")
        pt_file = QFileDialog.getOpenFileName(self, "选择权重文件", r".", "*.pt")
        if (pt_file[0] == ""): return 0
        print("pt_file: ", pt_file)
        self.label.setText(pt_file[0])

    def save_config(self):
        weight=self.label.text()
        # print(weight)
        imgsz = int(self.lineEdit.text())  # 输入图片的大小 默认640(pixels)
        conf_thres = float(self.lineEdit_2.text())  # object置信度阈值 默认0.25  用在nms中
        iou_thres = float(self.lineEdit_3.text())  # 做nms的iou阈值 默认0.45   用在nms中
        max_det = int(self.lineEdit_4.text()) # 每张图片最多的目标数量  用在nms中
        device = self.lineEdit_5.text()
        config_txt="{} {} {} {} {} {}".format(weight,imgsz,conf_thres,iou_thres,max_det,device)
        with open("configure.txt","w")as f:
            f.write(config_txt)
        self.DETECT=DETECT_API(weight,imgsz,conf_thres,iou_thres,max_det,device)
        print("已保存设置",weight,imgsz,conf_thres,iou_thres,max_det,device,sep='\t')
        self.tabWidget.setCurrentIndex(0)
    def open_pic(self):
        self.label_8.setText('输入')
        self.label_9.setText('输出')
        print("打开图片")
        # pic_file = QFileDialog.getOpenFileName(self, "选择图片", r".", "*.jpg;;*.png;;ALL Files(*)")
        pic_file = QFileDialog.getOpenFileName(self, "选择图片", r"", "*.jpg;;*.png;;ALL Files(*)")
        if (pic_file[0] == ""): return 0
        print("pic_file: ", pic_file)
        try:
            frame = cv2.imread(pic_file[0])
            self.check_img=frame*1      #相当于深层复制
        except:
            print("读取图片失败，请确保图片路径没有中文字符")
            return 0
        self.tab_index=0
        frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        p_w = frame.shape[1]
        p_h = frame.shape[0]
        L_w = self.label_8.width()
        L_h = self.label_8.height()
        i = p_w / p_h
        j = L_w / L_h
        if (i > j):
            p_w = int(L_w)
            p_h = int(p_w / i)
        else:
            p_h = int(L_h)
            p_w = int(p_h * i)
        pixmap = QtGui.QImage(frame, frame.shape[1], frame.shape[0], frame.shape[1] * 3, QtGui.QImage.Format_RGB888)
        # pixmap = QtGui.QPixmap.fromImage(pixmap)
        pixmap = QtGui.QPixmap(pixmap).scaled(p_w,p_h)
        self.label_8.setPixmap(pixmap)

    def check_pic(self):
        if self.label_8.pixmap():
            img=self.check_img*1
            self.show_result(img,self.label_9)


    def open_video(self):
        self.label_10.setText('输入')
        self.label_11.setText('输出')
        print("打开视频")
        # self.video_file = QFileDialog.getOpenFileName(self, "选择视频", ".", "*.mp4;;*.avi;;ALL Files(*)")
        self.video_file = QFileDialog.getOpenFileName(self, "选择视频", "", "*.mp4;;*.avi;;ALL Files(*)")
        if (self.video_file[0] == ""): return 0
        self.label_10.setText(self.video_file[0])
        self.tab_index=1
        print("video_file:", self.video_file)
        self.cap = cv2.VideoCapture()
        self.cap.open(self.video_file[0])
        if self.cap.isOpened():
            self.cam_switch=1
        else:
            self.cam_switch=0
            return 0
        #显示第一张画面
        self.video_switch = True #True表示视频播放
        self.timer1 = QtCore.QTimer()
        self.timer1.start(int(1000 / self.cap.get(5)))
        self.timer1.timeout.connect(self.show_video)
        # self.timer1.blockSignals(True)#暂停定时器
        self.video_check_switch=True
        self.video_switch = True #设置视频暂停开关，False表示视频暂停
    def open_cam(self):
        self.cap = cv2.VideoCapture(0)
        if self.cap.isOpened():
            self.cam_switch=1
        else:
            self.cam_switch=0
            return 0
        self.tab_index=2
        # 创建定时器
        self.timer1 = QtCore.QTimer()
        self.timer1.start(int(1000 / self.cap.get(5)))
        self.timer1.timeout.connect(self.show_video)
        self.video_check_switch=True
        self.video_switch=True

    def close_cam(self):
        self.cam_switch=0

    def CloseVideo(self):
        self.cam_switch = 0

    def VideoCheckSwitch(self):
        self.video_check_switch=not self.video_check_switch
    def VideoSwitch(self):
        self.video_switch= not self.video_switch

    def show_video(self):
        if not self.video_switch: return None
        ret, frame = self.cap.read()
        if ret:
            if self.tab_index==1:
                label_in=self.label_10
                label_out = self.label_11
            elif self.tab_index==2:
                label_in=self.label_12
                label_out = self.label_13
                # 水平翻转图片
                frame = cv2.flip(frame, 1)
            if self.video_check_switch :self.show_result(frame*1, label_out)
            frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

            p_h, p_w = frame.shape[:2]
            L_w = label_in.width()
            L_h = label_in.height()
            pixmap = QtGui.QImage(frame, p_w, p_h, QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(pixmap)
            # 最大等比例显示图片在label中
            ratio = max(p_w / L_w, p_h / L_h)
            pixmap.setDevicePixelRatio(ratio)
            label_in.setPixmap(pixmap)



            if (self.cam_switch==0):
                self.timer1.stop()
                self.cap.release()
                label_in.setText("输入")
    def show_result(self,img,label):
        t1 = time.time()
        detections = self.DETECT.detect(img)
        for i in detections:
            # print(i)
            x, y, w, h = i['position']
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
            img = cv2.putText(img, "{} {}".format(i['class'],round(i['conf'], 3)), (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 0, 255),
                              2,
                              cv2.LINE_AA)
        T = (time.time() - t1)
        img = cv2.putText(img, "{} FPS - {}s".format(round(1 / T, 2),round(T,3)), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        p_w = frame.shape[1]
        p_h = frame.shape[0]
        L_w = label.width()
        L_h = label.height()
        i = p_w / p_h
        j = L_w / L_h
        if (i > j):
            p_w = int(L_w)
            p_h = int(p_w / i)
        else:
            p_h = int(L_h)
            p_w = int(p_h * i)
        pixmap = QtGui.QImage(frame, frame.shape[1], frame.shape[0], frame.shape[1] * 3, QtGui.QImage.Format_RGB888)
        # pixmap = QtGui.QPixmap.fromImage(pixmap)
        pixmap = QtGui.QPixmap(pixmap).scaled(p_w, p_h)
        label.setPixmap(pixmap)

if __name__=='__main__':
    import sys
    app = QApplication(sys.argv)
    begin_win = Begin()
    begin_win.show()
    sys.exit(app.exec_())
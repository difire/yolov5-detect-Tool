from TkUI import mytkinter


class MyTk(mytkinter):
    
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.tab_main.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.myplace()
        # 监听窗口大小改变
        self.bind('<Configure>', self.window_resize)

    def myplace(self):#place布局，self.cv作为父控件，其尺寸改变，其子控件大小相应刷新
        self.cv.place(x=0,y=0,width=self.width,height=self.height)

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

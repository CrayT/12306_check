#! /usr/bin/env python3
#encoding:utf-8
from docopt import docopt
from TrainCollection import TrainCollection
import requests
import re
from wx import *
import wx.grid 
# from wx import adv
import wx.adv 
def cli(from_station, to_station, date):
    url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8955'
    r = requests.get(url, verify=False)
    stations = re.findall(r'([\u4e00-\u9fa5]+)\|([A-Z]+)', r.text)
    station = dict(stations)

    from_station = station.get(from_station)
    to_station = station.get(to_station)
    date = date
    print(to_station)
    url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(
        date, from_station, to_station
    )

    r = requests.get(url, verify=False)
    rows = r.json()['data']['result']
    mapp=r.json()['data']['map']
    l=[]

    for row in rows:

        listt=[]
        listt=row.split('|')

        if "列车停运" in listt:
            pass
        else:
            url_price='https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice?train_no={}&from_station_no={}&to_station_no={}&seat_types={}&train_date={}'.format(
            listt[2],listt[16],listt[17],listt[35],date
            )
            # rr = requests.get(url_price, verify=False)

            # rrr = rr.json()['data']
            rw={}

            # if 'A9' in rrr.keys():
            #     rw['sw']=rrr['A9']
            # else:
            #     rw['sw']=''
            # if 'M' in rrr.keys():
            #     rw['yd']=rrr['M']
            # else:
            #     rw['yd']=''
            # if 'WZ' in rrr.keys():    
            #     rw['ed']=rrr['WZ']
            # else:
            #     rw['ed']=''
            # if 'A4' in rrr.keys():
            #     rw['rw']=rrr['A4']
            # else:
            #     rw['rw']=''
            # if 'A3' in rrr.keys():
            #     rw['yw']=rrr['A3']
            # else:
            #     rw['yw']=''
            # if 'A2' in rrr.keys():
            #     rw['rz']=rrr['A2']
            # else:
            #     rw['rz']=''
            # if 'A1' in rrr.keys():
            #     rw['yz']=rrr['A1']
            #     rw['wz']=rrr['A1']
            # else:
            #     rw['yz']=''
            #     rw['wz']=''
            # print(rrr)        
            
            rw['station_train_code']=listt[3]

            rw['from_station_name']=mapp[listt[6]]
            rw['to_station_name']=mapp[listt[7]]

            rw['start_time']=listt[8]
            rw['arrive_time']=listt[9]

            rw['time']=listt[10]

            rw['sw_num']=listt[32]
            rw['ydz_num']=listt[31]
            rw['edz_num']=listt[30]
            rw['yz_num']=listt[29]
            rw['yw_num']=listt[28]
            rw['wz_num']=listt[26]
            rw['rz_num']=listt[24]
            rw['rw_num']=listt[23]
            
            
            l.append(rw)

    return l

def getItem(lis):
        listt=[]
        key=['station_train_code','from_station_name','to_station_name','start_time','arrive_time','time','sw_num','ydz_num','edz_num','rw_num','yw_num','rz_num','yz_num','wz_num']
        key_price=['sw','yd','ed','rw','yw','rz','yz','wz']
        for i in range(len(key)):
            if i <=5:
                listt.append(lis[key[i]])
            else:
                if key_price[i-6] in lis.keys():
                    listt.append(lis[key[i]]+'/'+lis[key_price[i-6]])
                else:
                    listt.append(lis[key[i]])
        return listt
class MyFrame(Frame):
    def __init__(self):
        Frame.__init__(self,None,-1,title="火车票查询",pos=(100,100),size=(1000,600))
        panel=Panel(self,-1)

        self.grid = wx.grid.Grid(panel, -1,pos=(20,70),size=(780,600),style=WANTS_CHARS)
        
        self.grid.AutoSizeColumns()
        self.row=0
        self.col=0
        self.button1=Button(panel,-1,"登陆",pos=(410,20),size=(100,20))
        self.button2=Button(panel,-1,"查询",pos=(850,380),size=(100,20))

        StaticText(panel,-1,"用户名:",pos=(20,20))
        text_input1=TextCtrl(panel,-1,pos=(70,20),size=(120,20))
        self.__TextBox1=text_input1

        StaticText(panel,-1,"密码:",pos=(200,20))
        text_input2=TextCtrl(panel,-1,pos=(240,20),size=(120,20))
        self.__TextBox2=text_input2

        StaticText(panel,-1,"出发:",pos=(830,80))
        text_input3=TextCtrl(panel,-1,pos=(870,80),size=(100,20))
        self.__TextBox3=text_input3
        
        StaticText(panel,-1,"到达:",pos=(830,120))
        text_input4=TextCtrl(panel,-1,pos=(870,120),size=(100,20))
        self.__TextBox4=text_input4
        
        StaticText(panel,-1,"日期:",pos=(830,160))
        self.datepick = wx.adv.CalendarCtrl(panel,-1,pos=(800,180))

        StaticText(panel,-1,"出发时间:",pos=(810,330))
        text_input6=TextCtrl(panel,-1,pos=(870,330),size=(100,20))
        self.__TextBox6=text_input6

        self.button2.Bind(EVT_BUTTON,self.run_file)

        StaticText(panel,-1,"Version: 1.0",pos=(900,530))
        StaticText(panel,-1,"By: Xu.T",pos=(900,550))
        self.InitUI() 

    def run_file(self,event): 
        date=str(self.datepick.PyGetDate())[:10]  #拿到日历的日期
        dic=cli(self.__TextBox3.GetValue(), self.__TextBox4.GetValue(), date)    #调用识别文件函数
        
        dic_tmp=[]
        for j in range(len(dic)):
            if self.__TextBox6.GetValue() and ( int(dic[j]['start_time'].split(':')[0]) >= int(self.__TextBox6.GetValue()) ) : 
                dic_tmp.append(dic[j])
            else:
                pass

        if len(dic_tmp) != 0:
            dic=dic_tmp
        else:
            dic=dic

        if self.row ==0 : #grid尚未被创建
            self.grid.CreateGrid(len(dic), 14)
        else: #grid已经创建，需要删除row或增加row
            if self.row >= len(dic):
                self.grid.DeleteRows(pos=len(dic), numRows=self.row-len(dic)) #删除多余的row
            else:
                self.grid.InsertRows(pos=self.row, numRows=len(dic)-self.row)

        self.grid.SetRowLabelSize(23)  #列表签宽度

        ll=['车次', '出发站','到达站', '出发时','到达时', '历时', '商务', '一等座', '二等座',  '软卧',  '硬卧', '软座', '硬座', '无座']
        for i in range(len(ll)):
            if i ==0:
                self.grid.SetColSize(i, 60)
            elif i > 2:
                self.grid.SetColSize(i, 47)
            self.grid.SetColLabelValue(i,ll[i])
            self.grid.SetCellAlignment(0, i, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        self.grid.EnableDragColSize(enable=True) #可以拖动列宽
        
        for j in range(len(dic)):
            list1 = getItem(dic[j])
            for i in range(len(list1)):
                self.grid.SetCellValue(j, i, list1[i])
                self.grid.SetCellAlignment(j, i, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
                if j%2 == 0:
                    self.grid.SetCellBackgroundColour(j, i, "light blue")
                else:
                    pass
                
        self.col=self.grid.GetNumberCols()
        self.row=self.grid.GetNumberRows()

    def InitUI(self):    #自定义的函数,完成菜单的设置  
        menubar = MenuBar()        #生成菜单栏  
        filemenu = Menu()        #生成一个菜单  
        qmi1 = MenuItem(filemenu,1, "help")     #生成一个help菜单项  
        qmi2 = MenuItem(filemenu,2, "Quit")  #quit项，id设为2，在bind中调用
        filemenu.AppendItem(qmi1)            #把菜单项加入到菜单中  
        filemenu.AppendItem(qmi2)  

        menubar.Append(filemenu, "&File")        #把菜单加入到菜单栏中  
        self.SetMenuBar(menubar)            #把菜单栏加入到Frame框架中  
        self.Bind(EVT_MENU, self.OnQuit, id=2)    #给菜单项加入事件处理，id=2  
        self.Bind(EVT_MENU, self.help_window, id=1)  #help窗口
        self.Show(True)        #显示框架  

    def OnQuit(self, e):    #自定义函数　响应菜单项　　  
        self.Close()

    def help_window(self,event): #定义help窗口
        dial=MessageDialog(None,"None",pos=(10,10)) #测试用
        dial.ShowModal()


if __name__ == "__main__":

    app = App()    #创建应用的对象
    myframe = MyFrame()    #创建一个自定义出来的窗口
    myframe.Show()    #这两句一定要在MainLoop开始之前就执行    
    app.MainLoop()

'''
商务 P
一等座 M
二等座   WZ
软卧  A4
硬卧  A3
软座 A2
硬座  A1
无座 A1
'''
#! /usr/bin/env python3
#encoding:utf-8

"""Train tickets query via command-line.

Usage:
    tickets [-gdtkz] <from> <to> <date>

Options:
    -h,--help   显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达

Example:
    tickets beijing shanghai 2016-08-25
"""
from docopt import docopt
from TrainCollection import TrainCollection
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
import requests
import re
from wx import *
import wx.grid 
import wx.adv 
from json import loads
import json
from configparser import ConfigParser
from reSizePic import pic_con
disable_warnings(InsecureRequestWarning) 
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
    mapp = r.json()['data']['map']
    l = []
    for row in rows:
        listt = []
        listt = row.split('|')
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

session = requests.Session()            #定义session，保持一个会话，验证码post和用户post保持同一个会话，之后的下单跨域保持登录
session.verify=False 
locate = {
    "1":"44,44,",
    '2':'114,44,',
    '3':'185,44,',
    '4':'254,44,',
    '5':'44,124,',
    '6':'114,124,',
    '7':'185,124,',
    '8':'254,124,'
    }
head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36', 
    'Referer': 'https://kyfw.12306.cn/otn/login/init'
    }

def login_getPic():
    resp1 = session.get('https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&',headers=head)
    with open('./pic/code.png','wb') as f:
        f.write(resp1.content)
    pic_con(path='./pic')

def login_to(code):
    cfg = ConfigParser()
    cfg.read('config.conf') #读取配置文件
    username = cfg['user']['username']
    passwd = cfg['user']['passwd']

    print(code)
    code = str(code).split(',')
    codes = ''
    for i in code:
        codes += locate[i]
    data = {
    'answer': codes,
    'login_site': 'E',
    'rand': 'sjrand'
    }
    resp = session.post('https://kyfw.12306.cn/passport/captcha/captcha-check',headers = head,data = data)
    print("resp \n",resp.content.decode('utf-8'))
    html = loads(resp.content.decode('utf-8'))

    if html['result_code'] == '4':
        print('验证码校验成功！')

        login_url = 'https://kyfw.12306.cn/passport/web/login'
        user = {
            'username': username,
            'password': passwd,
            'appid': 'otn'
        }
        resp2 = session.post(login_url,headers=head,data=user)
        html = loads(resp2.content.decode('utf-8'))
        print(resp2.text)
        if html['result_code'] == 0:
            print('登陆成功！')
            yzdata={
                'appid':'otn'
            }
            tk_url='https://kyfw.12306.cn/passport/web/auth/uamtk'
            resp3=session.post(tk_url,data=yzdata,headers=head)
            print('第一次验证:')
            print(resp3.text)
            login_message=resp3.json()['newapptk']
            print('loginMessage=',login_message)
            yz2data={
                'tk':login_message
            }
            client_url='https://kyfw.12306.cn/otn/uamauthclient'
            resp4=session.post(client_url,data=yz2data,headers=head)
            print('第二次验证:')
            print(json.loads(resp4.text))
            mes_json=json.loads(resp4.text)
            username=mes_json['username']
            mes='用户: '+username+',登陆成功！'
            return mes
        else:
            print('登陆失败！')
            return '登陆失败！'
    else:
        print('验证码校验失败，正在重新请求页面...')
        return "验证码校验失败"

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

# 重置Image对象尺寸的函数
def resizeBitmap(image, width=200, height=200):
    bmp = image.Scale(width, height).ConvertToBitmap()
    return bmp

class MyFrame(Frame):
    
    def __init__(self):
        Frame.__init__(self,None,-1,title="火车票查询",pos=(100,100),size=(1050,700))
        self.panel=Panel(self,-1)
 
        login_getPic() #拿到验证图片

        self.grid = wx.grid.Grid(self.panel, -1,pos=(20,70),size=(780,600),style=WANTS_CHARS)
        
        self.grid.AutoSizeColumns()
        self.row = 0
        self.col = 0

        self.button1 = Button(self.panel,-1,"登陆",pos=(720,60),size=(100,20))
        self.button2 = Button(self.panel,-1,"查询",pos=(850,380),size=(100,20))
        self.button3 = Button(self.panel,-1,"刷新验证码",pos=(20,10),size=(100,20))

        StaticText(self.panel,-1,"验证码:",pos=(720,5))
        text_input0 = TextCtrl(self.panel,-1,pos=(720,30),size=(120,20))
        self.__TextBox0 = text_input0 

        StaticText(self.panel,-1,"出发:",pos=(830,80))
        text_input3 = TextCtrl(self.panel,-1,pos=(870,80),size=(100,20))
        self.__TextBox3 = text_input3
        
        StaticText(self.panel,-1,"到达:",pos=(830,120))
        text_input4 = TextCtrl(self.panel,-1,pos=(870,120),size=(100,20))
        self.__TextBox4 = text_input4
        
        StaticText(self.panel,-1,"日期:",pos=(830,160))
        self.datepick = wx.adv.CalendarCtrl(self.panel,-1,pos=(800,180))

        StaticText(self.panel,-1,"出发时间:",pos=(810,330))
        text_input6 = TextCtrl(self.panel,-1,pos=(870,330),size=(100,20))
        self.__TextBox6 = text_input6
        
        self.button1.Bind(EVT_BUTTON,self.login)

        self.button2.Bind(EVT_BUTTON,self.run_file)

        self.button3.Bind(EVT_BUTTON,self.fresh_pic) #刷新验证码

        StaticText(self.panel,-1,"Version: 2.0",pos=(900,630))
        StaticText(self.panel,-1,"By: Xu.T",pos=(900,650))

        img_big = wx.Image("./pic/new.jpg", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        staticBmp = wx.StaticBitmap(self.panel, -1, img_big, pos=(130, 0))

        #显示目标图片名称
        img_big = wx.Image("./pic/3.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        staticBmp = wx.StaticBitmap(self.panel, -1, img_big, pos=(20, 35))

        
        self.InitUI() 

    def login(self,event):
        mess = login_to(self.__TextBox0.GetValue())
        dial = MessageDialog(None,mess)
        dial.ShowModal()
        #self.fresh_pic

    def fresh_pic(self,event):
        self.Refresh()  #刷新验证码需要刷新窗口来显示新图片。
        login_getPic() #重新得到验证图片。
        img_big = wx.Image("./pic/new.jpg", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        staticBmp = wx.StaticBitmap(self.panel, -1, img_big, pos=(130, 0))
        # img_big = wx.Image("./pic/new.jpg", wx.BITMAP_TYPE_ANY) #显示验证图片
        # staticBmp.SetBitmap(resizeBitmap(img_big, 200, 100))
        img_big = wx.Image("./pic/3.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        staticBmp = wx.StaticBitmap(self.panel, -1, img_big, pos=(20, 35))


    def run_file(self,event): 
        date = str(self.datepick.PyGetDate())[:10]  #拿到日历的日期
        dic = cli(self.__TextBox3.GetValue(), self.__TextBox4.GetValue(), date)    #调用识别文件函数
        dic_tmp = []
        for j in range(len(dic)):
            if self.__TextBox6.GetValue() and ( int(dic[j]['start_time'].split(':')[0]) >= int(self.__TextBox6.GetValue()) ) : 
                dic_tmp.append(dic[j])
            else:
                pass
        if len(dic_tmp) != 0:
            dic = dic_tmp
        else:
            dic = dic
        if self.row == 0 : #grid尚未被创建
            self.grid.CreateGrid(len(dic), 14)
        else: #grid已经创建，需要删除row或增加row
            if self.row >= len(dic):
                self.grid.DeleteRows(pos=len(dic), numRows=self.row-len(dic)) #删除多余的row
            else:
                self.grid.InsertRows(pos=self.row, numRows=len(dic)-self.row)
        self.grid.SetRowLabelSize(23)  #列表签宽度
        ll = ['车次', '出发站','到达站', '出发时','到达时', '历时', '商务', '一等座', '二等座',  '软卧',  '硬卧', '软座', '硬座', '无座']
        for i in range(len(ll)):
            if i == 0:
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
        self.col = self.grid.GetNumberCols()
        self.row = self.grid.GetNumberRows()

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
        dial = MessageDialog(None,"None",pos=(10,10)) #测试用
        dial.ShowModal()

if __name__ == "__main__":
    app = App()    #创建应用的对象
    myframe = MyFrame()    #创建一个自定义出来的窗口
    myframe.Show()    #这两句一定要在MainLoop开始之前就执行    
    app.MainLoop()
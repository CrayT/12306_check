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
import requests
import re

def cli():
    url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8955'
    r = requests.get(url, verify=False)
    stations = re.findall(r'([\u4e00-\u9fa5]+)\|([A-Z]+)', r.text)
    station = dict(stations)

    arg = docopt(__doc__)
    from_station = station.get(arg['<from>'])
    to_station = station.get(arg['<to>'])
    date = arg['<date>']
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
        # print(listt)
        # print("车次:",listt[3],"\n出发时间：%s"%(listt[8]),"\n到达时间：%s"%(listt[9]),"\n路途耗时：%s"%(listt[10]),\
        # "\n无座：%s"%(listt[23]), "\n硬座：%s"%(listt[24]),
        # "\n软座：%s"%(listt[25]),"\n硬卧二等卧：%s"%(listt[26]),"\n动卧：%s"%(listt[27]),"\n软卧一等卧：%s"%(listt[28]),"\n高级软卧：%s"%(listt[29]),
        # "\n二等座：%s"%(listt[30]),"\n一等座：%s"%(listt[31]),"\n商务座：%s"%(listt[32]),)
        if "列车停运" in listt:
            pass
        else:
            url_price='https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice?train_no={}&from_station_no={}&to_station_no={}&seat_types={}&train_date={}'.format(
            listt[2],listt[16],listt[17],listt[35],date
            )
            rr = requests.get(url_price, verify=False)
            # print(listt,url_price,rr)
            rrr = rr.json()['data']
            r_price={}
            rw={}

            if 'P' in rrr.keys():
                rw['sw']=rrr['P']
            else:
                rw['sw']=''
            if 'M' in rrr.keys():
                rw['yd']=rrr['M']
            else:
                rw['yd']=''
            if 'WZ' in rrr.keys():    
                rw['ed']=rrr['WZ']
            else:
                rw['ed']=''
            if 'A4' in rrr.keys():
                rw['rw']=rrr['A4']
            else:
                rw['rw']=''
            if 'A3' in rrr.keys():
                rw['yw']=rrr['A3']
            else:
                rw['yw']=''
            if 'A2' in rrr.keys():
                rw['rz']=rrr['A2']
            else:
                rw['rz']=''
            if 'A1' in rrr.keys():
                rw['yz']=rrr['A1']
                rw['wz']=rrr['A1']
            else:
                rw['yz']=''
                rw['wz']=''
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
    trains = TrainCollection(l)
    trains.pretty_print()

if __name__ == '__main__':
    cli()

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
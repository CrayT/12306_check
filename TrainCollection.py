#! /usr/bin/env python3
# encoding:utf-8

from prettytable import PrettyTable

class TrainCollection(object):

    header = u"车次 出发\到达站 出发\到达时间 历时 商务 一等座 二等座  软卧  硬卧 软座 硬座 无座".split()

    def __init__(self, rows):
        self.rows = rows

    # 获取车次运行时间
    def _get_duration(self, row):
        duration = row.get('lishi').replace(':', 'h') + 'm'
        if duration.startswith('00'):
            return duration[3:]
        if duration.startswith('0'):
            return duration[0:]
        return duration

    def colored(self, color, text):
        table = {
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            # no color
            'nc': '\033[0m'
        }
        cv = table.get(color)
        nc = table.get('nc')
        return ''.join([cv, text, nc])

    @property
    def trains(self):
        for row in self.rows:
            # print(row)
            train = [
                # 车次
                self.colored('yellow',row['station_train_code']),

                # 出发、到达站
                '\n'.join([self.colored('green', row['from_station_name']),
                           self.colored('red', row['to_station_name'])]),

                # 出发、到达时间
                '\n'.join([self.colored('green', row['start_time']),
                           self.colored('red', row['arrive_time'])]),
                

                # 历时
                row['time'],#self._get_duration(row),
                # 商务
                '\n'.join([self.colored('green', row['sw_num']),
                           self.colored('red', row['sw'])]),
                # row['sw_num'],
                # 一等坐
                '\n'.join([self.colored('green', row['ydz_num']),
                           self.colored('red', row['yd'])]),
                # 二等座
                 '\n'.join([self.colored('green', row['edz_num']),
                           self.colored('red', row['ed'])]),
                
                # row['edz_num'],

                # 软卧
                '\n'.join([self.colored('green', row['rw_num']),
                           self.colored('red', row['rw'])]),
                # row['rw_num'],

                # 硬卧
                '\n'.join([self.colored('green', row['yw_num']),
                           self.colored('red', row['yw'])]),
                # row['yw_num'],
                # 软座
                '\n'.join([self.colored('green', row['rz_num']),
                           self.colored('red', row['rz'])]),
                # row['rz_num'],
                #硬座
                '\n'.join([self.colored('green', row['yz_num']),
                           self.colored('red', row['yz'])]),
                # row['yz_num'],
                #无座
                '\n'.join([self.colored('green', row['wz_num']),
                           self.colored('red', row['wz'])]),
                # row['wz_num']
            ]
            yield train

    def pretty_print(self):
        """
        数据已经获取到了，剩下的就是提取我们要的信息并将它显示出来。
        `prettytable`这个库可以让我们它像MySQL数据库那样格式化显示数据。
        """
        pt = PrettyTable()
        # 设置每一列的标题
        pt._set_field_names(self.header)
        
        for train in self.trains:
            pt.horizontal_char='-'
            pt.add_row(train)
        print(pt)
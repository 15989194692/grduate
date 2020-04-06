from datetime import datetime, timedelta

datetime_format = "%Y-%m-%d %H:%M:%S"

'''
获取当前系统时间
    output:
        str类型：当前系统时间 格式为：YYYY-mm-dd HH:MM:SS
'''
def cur_datetime():
    return datetime.now().strftime(datetime_format)

'''
把datetime转为字符串
    input:
        dt:日期类型 eg:2020-03-18 22:25:76 YYYY-mm-dd HH:MM:SS
'''
def datetime_tostr(dt):
    return dt.strftime(datetime_format)

'''
把字符串转换成datetime类型
    input:
        str:字符串，得有一定的格式 eg:'2020-03-18 22:25:76' 'YYYY-mm-dd HH:MM:SS'
'''
def str_todatetime(str):
    if str.count('.') > 0:
        spl = str.index('.')
        str = str[:spl]
    return datetime.strptime(str, datetime_format)


'''
在某个时间的基础上增加x分钟x秒
     input:
        dt_string:日期格式的字符串 eg:'2020-03-18 22:25:76'
        minutes:要加的分钟数(可以是小数)
'''
def datetime_add(dt_string, minutes):
    minutes_delta = timedelta(minutes=minutes)
    new_datetime = str_todatetime(dt_string) + minutes_delta
    return new_datetime


'''
充满电的时间:参考电动汽车厂家的宣传，20min可充电80%，这里电动汽车的电池容量为60kwh，那么80%即为48kwh，那么每分钟可充电2.4kwh
    input:
        arrive_datetime:到达充电站的时间
        soc:车辆剩余电量
    
    output:
        datetime(datetime):冲完电的时间
'''
def recharged_datetime(arrive_datetime, soc):
    #要充多少电量
    need_battery = 50 - soc
    #TODO 充电需要的时间
    need_min = need_battery / 2.4
    need_min = round(need_min,0) #保留整数部分
    return datetime_add(arrive_datetime, need_min)

if __name__ == "__main__":
    pass
    #测试cur_datetime方法
    # now = cur_datetime()
    # print(now)
    # print(type(now))

    #测试recharged_datetime方法
    donedatetime = recharged_datetime('2020-04-06 21:38:00', 9.1547)
    print(donedatetime)

    #测试datetime_tostr方法
    # now = cur_datetime()
    # print('now = ', now)
    # add = datetime_add(now, 2.598200)
    # print('add = ', add)
    # dt_str = datetime_tostr(add)
    # print('dt_str = ', dt_str)

    # print('2020-04-06 22:07:14.021' >= '2020-04-06 22:17:14.15')

    #测试datetime_add方法
    # now = cur_datetime()
    # format = "'" + now + "'"
    # print(type(format))
    # print(now)
    # add = datetime_add(now, -4)
    # print(type(add))
    # print(add)

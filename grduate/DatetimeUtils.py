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

if __name__ == "__main__":
    #测试cur_datetime方法
    # now = cur_datetime()
    # print(now)
    # print(type(now))


    #测试datetime_add方法
    now = cur_datetime()
    print(now)
    add = datetime_add(now, -4)
    print(type(add))
    print(add)

import DataInit

'''
入口方法
'''
def main():
    #初始化汽车在路网中的位置
    DataInit.init_car()
    #初始化充电桩状态信息
    DataInit.init_chargings_state()
    #测试自定义请求
    # DataInit.my_request()
    #初始化1200个请求，在接下来的一个小时内出发，时间随机
    DataInit.init_requests(size = 300, hour = 0)

'''
主程序入口，执行前先执行ApschedulerServer.py文件，启动定时任务服务器
'''
if __name__ == "__main__":
    main()

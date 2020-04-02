import rpyc
import DatetimeUtils

def test_job(execute_datetime, carid):
    conn = rpyc.connect('localhost', 54321)
    # conn.root.add_job('ApschedulerServer:recharged', 'date', run_date='2020-03-29 20:39:20', args=[0, [10, 11, 12]])
    # conn.root.add_job('ApschedulerServer:print_text', 'interval', args=['Hello World'], seconds=2)
    # conn.root.add_job('ApschedulerServer:recharged', 'interval', args=[0, 1], seconds=2, id=0)
    # job = conn.root.add_job('ApschedulerServer:print_text', 'interval', args=['Hello, World'], seconds=2)
    # conn.root.add_job('ApschedulerServer:test_job', 'date', run_date='2020-03-30 12:41:00', id='0')
    conn.root.add_job('ApschedulerServer:test_job', 'date', run_date=execute_datetime, args=[carid], id='2')


'''
处理请求任务
    input:
        requestId:请求id
        execute_datetime:执行任务的时间
'''
def handle_request_job(requestId, execute_datetime):
    conn = rpyc.connect('localhost', 54321)
    conn.root.add_job('ApschedulerServer:handle_request', 'date', run_date=execute_datetime, args=[requestId], id=str(requestId))


'''
车辆到达目的地后执行的任务
    input:
        execute_datetime:执行任务的时间
        car_Ld:车辆的目的地
        carid:车辆id
'''
def arrival_job(execute_datetime, car_Ld, carid):
    conn = rpyc.connect('localhost', 54321)
    #如果之前有任务还没执行，那么取消这个任务
    remove_job(str(carid))
    conn.root.add_job('ApschedulerServer:recharged', 'date', run_date=execute_datetime, args=[car_Ld, carid], id=str(carid))


'''
修改车辆的是否在充电状态
    input:
        execute_datetime:执行任务的时间
'''
def update_car_is_recharge(execute_datetime, carid):
    conn = rpyc.connect('localhost', 54321)
    conn.root.add_job('ApschedulerServer:update_car_is_recharge', 'date', run_date=execute_datetime, args=[carid])


def get_job(jobId):
    conn = rpyc.connect('localhost', 54321)
    job = conn.root.get_job(jobId)
    return job

def remove_job(jobId):
    conn = rpyc.connect('localhost', 54321)
    if get_job(jobId) != None:
        conn.root.remove_job(jobId)


if __name__ == "__main__":
    pass
    # arrival_job()
    test_job(str(DatetimeUtils.datetime_add(DatetimeUtils.cur_datetime(), 0.1)), 0)
    job = get_job('2')
    print(job)

    # remove_job('1')
    # job = get_job('1')
    # print(job != None)
    # print(job)
    # print(type(job))

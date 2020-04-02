import rpyc
from rpyc.utils.server import ThreadedServer
import datetime as dt
from apscheduler.schedulers.background import BackgroundScheduler
import MathUtils
import DataOperate
import MatchingAlgorithm
import DatetimeUtils
import ApschedulerClient


def test_job(carid):
    now = DatetimeUtils.cur_datetime()
    add = DatetimeUtils.datetime_add(now, 0.2)
    ApschedulerClient.update_car_is_recharge(str(add), carid)


'''
修改车辆是否在充电的状态
    input:
        carid:车辆id
'''
def update_car_is_recharge(carid):
    car = DataOperate.get_car(carid)
    car.is_recharge = 0
    DataOperate.update_car(car)
    # print('update_car_is_recharge')

'''
处理请求，为请求分配一辆车
'''
def handle_request(reqestId):
    request = DataOperate.get_request(reqestId)
    MatchingAlgorithm.matching_car(request)


'''
每当车辆到达目的地后，查看车辆是否需要充电
    input:
        carid:车辆id
        dist:车辆行驶的距离
'''
def recharged(carid, car_Ld, dist):
    #1.获取车辆信息
    car = DataOperate.get_car(carid)

    #2.根据距离推断消耗的电量
    cost = MathUtils.dist_cost(dist)

    #3.修改车辆信息
    car.Battery -= cost
    car.batch_numbers = 0
    car.Pc = 0

    #4 获取系统当前的时间，格式为：'YYYY-mm-dd HH:MM:SS' str类型
    now_datetime = DatetimeUtils.cur_datetime()

    #5.判断是否需要充电
    #5.1需要充电
    if car.Battery <= 10:
        #5.1.1 拿到去往最经的充电站节点的路径以及距离
        path_to_charging, dist_to_charging = MatchingAlgorithm.path_to_charging(car.Ld)

        arrive_datetime = DatetimeUtils.datetime_add(now_datetime, dist_to_charging / 1000)
        car.Ld = path_to_charging[-1]
        car.Ls = car.Ld
        car.is_recharge = 1
        carstate = [carid, arrive_datetime, 1]

        #获取冲完电的时间，datetime类型
        recharged_datetime = DatetimeUtils.recharged_datetime(arrive_datetime, car.Battery)
        #提交定时任务修改车辆的状态
        ApschedulerClient.update_car_is_recharge(recharged_datetime, carid)

    #不需要充电
    else:
        car.Ls = car.Ld
        car.is_recharge = 0

        carstate = [carid, now_datetime, 1]
        pass
    #5.在节点车辆状态表上拼接一行车辆状态信息
    DataOperate.append_carstate(car_Ld, carstate)
    #6.修改车辆信息
    DataOperate.update_car(car)

def print_text(text):
    print(text)

class SchedulerService(rpyc.Service):
    def exposed_add_job(self, func, *args, **kwargs):
        return scheduler.add_job(func, *args, **kwargs)
    def exposed_modify_job(self, job_id, jobstore=None, **changes):
        return scheduler.modify_job(job_id, jobstore, **changes)

    def exposed_reschedule_job(self, job_id, jobstore=None, trigger=None, **trigger_args):
        return scheduler.reschedule_job(job_id, jobstore, trigger, **trigger_args)

    def exposed_pause_job(self, job_id, jobstore=None):
        return scheduler.pause_job(job_id, jobstore)

    def exposed_resume_job(self, job_id, jobstore=None):
        return scheduler.resume_job(job_id, jobstore)

    def exposed_remove_job(self, job_id, jobstore=None):
        scheduler.remove_job(job_id, jobstore)

    def exposed_get_job(self, job_id):
        return scheduler.get_job(job_id)

    def exposed_get_jobs(self, jobstore=None):
        return scheduler.get_jobs(jobstore)

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.start()
    protocol_config = {'allow_public_att' : True}
    server = ThreadedServer(SchedulerService, port=54321, protocol_config = protocol_config)
    try:
        server.start()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        scheduler.shutdown()
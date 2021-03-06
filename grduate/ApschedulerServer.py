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
def recharged(carid, dist):
    print('车辆%s已到达目的地' %carid)
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
        #5.1.1 计算出到哪个充电站充电可以最快完成充电,方法中顺便修改充电站的状态信息,fastest_charging_datetime(str)
        fastest_charging_datetime,target = MatchingAlgorithm.fastest_charging_datetime(car.Ld, car.Battery)

        car.Ld = target
        car.Ls = car.Ld
        car.is_recharge = 1

        # 提交定时任务修改车辆是否在充电的状态
        ApschedulerClient.update_car_is_recharge(fastest_charging_datetime, carid)
        #车辆状态信息
        carstate = [carid, fastest_charging_datetime, 1]

        # 在节点车辆状态表上拼接一行车辆状态信息
        DataOperate.append_carstate(car.Ld, carstate)

    #不需要充电
    else:
        car.Ls = car.Ld
        car.is_recharge = 0
        # 车辆状态信息
        # carstate = [carid, now_datetime, 1]

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
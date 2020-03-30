import rpyc
from rpyc.utils.server import ThreadedServer
import datetime as dt
from apscheduler.schedulers.background import BackgroundScheduler
from NodeUtils import get_car
from NodeUtils import get_chargings
import MathUtils

def test_job():
    print(dt.datetime.now().strftime("%T %F"))

'''
每当车辆到达目的地后，查看车辆是否需要充电
    input:
        carid:车辆id
        dist:车辆行驶的距离
'''
def recharged(carid, dist):
    #1.获取车辆信息
    car = get_car(carid)
    #2.TODO 根据距离推断消耗的电量
    cost = MathUtils.dist_cost(dist)
    #3.修改车辆的电量信息
    car.B -= cost
    #4.判断是否需要充电
    #4.1需要充电
    if car.B <= 10:
        pass
    #不需要充电
    else:
        pass
    #5.修改节点车辆状态表


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
from time import sleep
import datetime as dt
import rpyc

def arrival_job():
    conn = rpyc.connect('localhost', 54321)
    # conn.root.add_job('ApschedulerServer:test_job', 'date', run_date='2020-03-30 12:41:00', id='0')
    # conn.root.add_job('ApschedulerServer:test_job', 'date', run_date='2020-03-30 12:41:00', id='0')
    # conn.root.add_job('ApschedulerServer:recharged', 'date', run_date='2020-03-29 20:39:20', args=[0, [10, 11, 12]])
    # conn.root.add_job('ApschedulerServer:print_text', 'interval', args=['Hello World'], seconds=2)
    conn.root.add_job('ApschedulerServer:recharged', 'interval', args=[0, 7], seconds=2, id='0')
    # job = conn.root.add_job('ApschedulerServer:print_text', 'interval', args=['Hello, World'], seconds=2)

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
    # job = get_job('0')
    # remove_job('1')
    job = get_job('1')
    print(job != None)
    print(job)
    print(type(job))
from time import sleep
import datetime as dt
import rpyc

def arrival_job():
    conn = rpyc.connect('localhost', 54321)
    # conn.root.add_job('ApschedulerServer:test_job', 'date', run_date='2020-03-29 20:26:00')
    # conn.root.add_job('ApschedulerServer:recharged', 'date', run_date='2020-03-29 20:39:20', args=[0, [10, 11, 12]])
    # conn.root.add_job('ApschedulerServer:recharged', 'interval', args=[0], seconds=2)
    conn.root.add_job('ApschedulerServer:recharged', 'interval', args=[0, 7], seconds=2)
    # job = conn.root.add_job('server:print_text', 'interval', args=['Hello, World'], seconds=2)
arrival_job()
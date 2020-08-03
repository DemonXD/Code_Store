import sys
import time
import threading
from random import choice
from random import randint
from threading import Thread


TASK_NAME = [
    "TASK1",
    "TASK2",
    "TASK3",
    "TASK4"
]


def runtask(name, flag):
    time.sleep(randint(3, 5))


def task_thread(stopped):
    flag = False
    while 1:
        if stopped():
            break

        Tname = choice(TASK_NAME)
        if Tname in [task.getName() for task in threading.enumerate()]:
            continue
        Thread(target=runtask, args=(f"{Tname}", lambda: flag), name=Tname).start()
        time.sleep(2)

def print_tasks(stopped):
    m_sets = set(['MainThread', 'CREATE_TASK', 'ECO_RUNNING_TASKS'])
    while 1:
        if stopped():
            break
        tasks = [task.getName() for task in threading.enumerate()]
        print(f"{list(set(tasks)-m_sets)} is running...")
        time.sleep(1)


def main():
    stop_event = False
    tasks = [
        Thread(target=task_thread, args=(lambda: stop_event, ), name="CREATE_TASK"),
        Thread(target=print_tasks, args=(lambda: stop_event, ), name="ECO_RUNNING_TASKS")
    ]
    try:
        for each_task in tasks:
            each_task.start()
        while 1:
            time.sleep(0.01)
    except KeyboardInterrupt:
        stop_event = True
        print("STOPPING...")
        for each_task in tasks:
            each_task.join()



if __name__=="__main__":
    try:
        main()
    except Exception as e:
        print(f"{str(e)}")
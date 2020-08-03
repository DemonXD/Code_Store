import asyncio
from random import choice
from random import randint

TASK_NAME = [
    "TASK1",
    "TASK2",
    "TASK3",
    "TASK4"
]


async def runtask(name):
    print(f"run {name}")
    await asyncio.sleep(randint(3, 5))
    print(f"{name} is Done!")


async def task_thread(loop):
    while 1:
        Tname = choice(TASK_NAME)
        if Tname in [task.get_name() for task in asyncio.all_tasks(loop=loop)]:
            await asyncio.sleep(2)
            print(f"{Tname} not DONE!")
            continue
        asyncio.create_task(runtask(f"{Tname}"), name=Tname)
        await asyncio.sleep(2)
        


async def print_tasks(loop):
    while 1:
        tasks = [task.get_name() for task in asyncio.all_tasks(loop=loop)]
        print(f"{tasks} is running...")
        await asyncio.sleep(1)



def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(*[
        print_tasks(loop),
        task_thread(loop)
    ]))
    loop.close()



if __name__=="__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"{str(e)}")

import asyncio
import threading
import time


def tt():
    for i in range(10):
        print(i)
        time.sleep(1)


def other_task():
    for i in range(5):
        print(f"执行其他任务 {i}")
        time.sleep(2)


if __name__ == '__main__':
    abcb = []
    abcb.clear()
    threading.Thread(target=tt).start()
    other_task()
    print("k")

import random
import multiprocessing
import time


def a_app(count : int, a : list[int], number : int):
    count += 1
    time.sleep(random.random()* 3)
    print(f"{count} yielded by {number}th thread")


if __name__ == "__main__":

    count = 0
    a = []
    threads = [multiprocessing.Process(target=a_app, args=(count,a, i)) for i in range(10000)]
    for thread in threads:
        thread.start()

    print("Finished running")

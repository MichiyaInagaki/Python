import time
from multiprocessing import Manager,Value, Process


def process1(count, array):
    for i in range(5):
        time.sleep(0.5)
        # Valueオブジェクトの値を操作
        count.value += 1
        # Listを操作
        array.append(count.value)
        print("process1:" ,array[:])


def process2(count, array):
    for i in range(5):
        time.sleep(0.7)
        count.value += 1
        array.append(count.value)
        print("process2:" + str(count.value))


def process3(count, array):
    for i in range(5):
        time.sleep(0.9)
        count.value += 1
        array.append(count.value)
        print("process3:" + str(count.value))


if __name__ == '__main__':
    # Managerオブジェクトの作成
    with Manager() as manager:

      # マネージャーからValueクラスを作成
      count = manager.Value('i', 0)
      # マネージャーからListを作成
      array = manager.list()
      print(array[:])

      p1 = Process(target=process1, args=[count, array])
      p2 = Process(target=process2, args=[count, array])
      p3 = Process(target=process3, args=[count, array])

      p1.start()
      p2.start()
      p3.start()

      p1.join()
      p2.join()
      p3.join()

      print(array[:])
      print("process ended")
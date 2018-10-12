#coding:utf-8

from queue import Queue

import random
import threading
import time

def work1():
	while(1):
		print("in work1",random.randrange(10)/5)
		time.sleep(0.1)
def work2():
	while(1):
		print("in work2",random.randrange(10)/5)
		time.sleep(0.1)

def work3():
	while(1):
		print("in work3",random.randrange(10)/5)
		time.sleep(0.1)

class Producer(threading.Thread):
	"""制作线程"""

	def __init__(self,t_name,queue):
		threading.Thread.__init__(self,name = t_name)
		self.data = queue

	def run(self):
		while(True):
			with open("task","r") as fp:
				line = fp.read()
				tasks = line.split(",")
			for task in tasks:
				print("%s: %s is producing %s to the queue!\n" %(time.ctime(),self.getName(),task))
				self.data.put(task)
				time.sleep(random.randrange(10)/5)
			print("%s : %s finished! " %(time.ctime(),self.getName()))
			time.sleep(30)

class customer(threading.Thread):
	def __init__(self,name,queue):
		threading.Thread.__init__(self,name = name)

		self.data = queue

	def run(self):
		while(True):
			vals = list()
			while(self.data.qsize()>0):
				vals.append(self.data.get())
			for val in vals:
				t = threading.Thread(target = eval(val))
				t.start()

		print("%s : %s finished ! " %(time.ctime(),self.getName()))
		time.sleep(30)

def main():
	queue = Queue()

	producer = Producer('Pro.' , queue)

	consumer = customer("Con.", queue)
	producer.start()
	consumer.start()
	producer.join()
	consumer.join()

	print("all task finished!")

if __name__=="__main__":
	main()

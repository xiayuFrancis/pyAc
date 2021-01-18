from queue import Queue
from threading import Thread
import time

class Student:
    def __init__(self, name):
        self.name = name
        
    def speak(self):
        print('{}:到！'.format(self.name))

class Teacher:
    def __init__(self, queue):
        self.queue = queue

    def call(self, student_name):
        if student_name == "exit":
            print('点名结束，开始上课..')
        else:
            print("老师： {}来了没".format(student_name))
        self.queue.put(student_name)

class CallManager(Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue
        self.students = {}

    def put(self, student):
        self.students.setdefault(student.name, student)

    def run(self):
        while True:
            student_name = self.queue.get()
            if student_name == "exit":
                break
            elif student_name in self.students:
                self.students[student_name].speak()
            else:
                print("老师，咱班，没有 {} 这个人".format(student_name))

queue = Queue()
teacher = Teacher(queue)
s1 = Student("小明")
s2 = Student("小亮")

cm = CallManager(queue)
cm.put(s1)
cm.put(s2)
cm.start()


print('开始点名~')
teacher.call('小明')
time.sleep(1)
teacher.call('小亮')
time.sleep(1)
teacher.call("exit")
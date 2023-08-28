import heapq
import threading
import time
from datetime import datetime
from server import app
from server.models import User, ShortID 

class Supervisor():
    def __init__(self, app) -> None:
        self.app = app
        self.scheduledTasks = []
        self.lock = threading.Lock()
        self.initFromDB()
        self.pendingTaskThread = threading.Thread(target=self.startPendingTask)
        self.pendingTaskThread.start()
        print('supervisor started')

    def initFromDB(self):
        with app.app_context():
            users = User.query.all()
        time = datetime.utcnow()
        for user in users:
            uuid = user.uuid
            pubkey = user.pubkey
            balance = user.balance
            expireOn = user.expireOn
            referralCode = user.id
            print(expireOn, self.expire, uuid)
            self.setTask(expireOn, self.expire, uuid)
            
    def setTask(self, time, func, *args):
        self.lock.acquire()
        heapq.heappush(self.scheduledTasks, (time, func, args))
        self.lock.release()

    def startPendingTask(self):
        while True:
            print('checking pending tasks: ', len(self.scheduledTasks), 'tasks pending')
            self.lock.acquire()
            while self.scheduledTasks and self.scheduledTasks[0][0] <= datetime.utcnow():
                task = heapq.heappop(self.scheduledTasks)
                func, args = task[1], task[2]
                print('Task found', func.__name__, args)
                threading.Thread(target=func, args=args).start()
            self.lock.release()
            time.sleep(1)

    def expire(self, uuid):
        with app.app_context():
            from server.models import removeShortidsFromDB
            removeShortidsFromDB(uuid)
            # updateXrayconfig TODO
            from utils.util_json import loadConfigToJSON
            loadConfigToJSON()
            from utils.util_sys import xrayRestart

            print(self.app.xrayProcess.pid)
            self.app.xrayProcess = xrayRestart(self.app.xrayProcess.pid)
            time.sleep(1)
            print(self.app.xrayProcess.pid)
            print('removed ' + uuid)
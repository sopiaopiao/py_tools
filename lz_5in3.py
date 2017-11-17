import redis
import time
import datetime

r = redis.Redis(host='127.0.0.1',port=6379,db=1)
ps = r.pubsub()
ps.subscribe(['test'])

def threeINfive():
    for item in ps.listen():  
        str = item['data']['acctno']
        print str


def getList():
    data = r.zrange('acctnoList',0,-1)
    for i in data:
        print i
        dealData(i)
 
def dealData(item):
    list = r.lrange(item,0,-1)
    lenList = len(list)
    if lenList != 0:
        st = list[-1].split('@')[0]
        et = list[0].split('@')[0]
        acc = list[0].split('@')[1]
        startTime = time.mktime(time.strptime(st,'%Y-%m-%d %H:%M:%S.%f'))
        endTime = time.mktime(time.strptime(et,'%Y-%m-%d %H:%M:%S.%f'))
        interTime = int(endTime-startTime)
        if lenList >= 1 and interTime < 300:
            r.delete(item)
            r.zrem('acctnoList',item)
            r.publish('alert_lz','alert')
        if interTime >= 300:
            r.rpop(item)
    if lenList == 0:
        r.zrem('acctnoList',item)
        r.delete(item)

if __name__ == '__main__':
    while True:
        getList()
        time.sleep(10)



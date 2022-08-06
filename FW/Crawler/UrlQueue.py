from queue import Queue as Qu
from F.LOG import Log
from FNLP import URL
from FNLP.Regex import Re as Regex

Log = Log("FairWEB.Queue.UrlQueue")

class FQueue:
    maxSize = 0
    noDuplicates = True
    avoidList = None
    cacheName = None
    mainQueue: Qu
    processedQueue: Qu

    def __init__(self, maxSize=0, noDuplicates=True, avoidList=None):
        self.maxSize = maxSize
        self.noDuplicates = noDuplicates
        self.avoidList = avoidList
        self.mainQueue = Qu(self.maxSize)
        self.processedQueue = Qu()

    def isDup(self, obj):
        if obj in self.mainQueue.queue:
            Log.d(f"{obj} is already in queue!")
            return True
        return False

    def hasBeenProcessed(self, obj):
        if obj in self.processedQueue.queue:
            Log.d(f"{obj} has already been processed!")
            return True
        return False

    def clean(self):
        backup = self.mainQueue.queue
        try:
            temp = self.mainQueue.queue
            set_temp = list(set(temp))
            self.mainQueue = Qu(self.maxSize)
            for item in set_temp:
                self.add(item)
            Log.i("--Queue Cleaned.--")
            return True
        except Exception as e:
            self.mainQueue.queue = backup
            Log.e("Failed to clean queue", e)
            return False

    def add_list(self, list_of_objs):
        if not list_of_objs:
            return False
        for item in list_of_objs:
            self.add(item)

    def add(self, obj):
        if self.mainQueue.full():
            return False
        if self.avoidList:
            result = False
            for item in self.avoidList:
                url = URL.get_base_url(obj)
                if Regex.contains(item, url):
                    return
            if not result:
                self.safe_put(obj)
                return
            else:
                Log.d(f"{obj} avoided from queue!")
                return
        else:
            self.safe_put(obj)

    def safe_put(self, obj):
        if self.hasBeenProcessed(obj):
            return False
        elif self.noDuplicates:
            if not self.isDup(obj=obj):
                self.mainQueue.put(obj)
                Log.d(f"{obj} added to queue!")
                return True
            else:
                return False
        else:
            self.mainQueue.put(obj)
            Log.d(f"{obj} added to queue!")
            return True

    def get(self):
        temp = self.mainQueue.get()
        return temp

    def clear_all(self):
        self.mainQueue = Qu(1)
        self.processedQueue = Qu(1)

    def size(self):
        try:
            return self.mainQueue.qsize()
        except Exception as e:
            Log.e("Failed to get Size.", error=e)
            return 0

    def isEmpty(self):
        try:
            return self.mainQueue.empty()
        except Exception as e:
            Log.e("Failed to see if queue is empty.", error=e)
            return 0

    def isFull(self):
        try:
            return self.mainQueue.full()
        except Exception as e:
            Log.e("Failed to see if queue is full.", error=e)
            return 0



# avoid = ['youtube', 'twitter']
# q = TiffanyQueue(avoidList=avoid)
# item1 = "https://youtube.com"
# item2 = "http://twitter.com"
# item3 = 'johnson'
# q.add(item2)
# q.add(item3)
# print(q.mainQueue.queue)
# q.add(item1)
# print(q.mainQueue.queue)
import time, datetime, json, requests, shutil, threading

exitFlag = 0

class my_thread (threading.Thread):
   def __init__(self, thread_id, thread_nm, set_str, lower, upper):
      threading.Thread.__init__(self)
      self.thread_id = thread_id
      self.thread_nm = thread_nm
      self.set_str = set_str
      self.lower = lower
      self.upper = upper

   def run(self):
      print ("Starting " + self.thread_nm +'\n')
      download(self.thread_nm, self.set_str, self.lower, self.upper)
      print ("Exiting " + self.thread_nm + '\n')

def download(thread_nm, set_str, lower, upper):
    data = json.load(open('./data/origindata/' + set_str + '.json'))

    t = time.time()
    
    for i in range(lower, upper):
        if exitFlag:
            thread_nm.exit()

        response = requests.get(data['images'][i]['url'], timeout = 5, stream = True)
        
        with open('./data/'+set_str+'images/'+str(data['images'][i]['imageId'])+'.jpeg', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        
        if i % 100 == 0:
            t_diff = round(time.time() - t, 2)
            t = time.time()
            print('{0} - {1} - {2} - {3}s - {4}\n'.format(str(datetime.datetime.now()), thread_nm, set_str, t_diff, i))
        
        del response

#if __name__ == '__main__':
def startDownloadImage():
    print('start Entering Main Thread...\n')
    # uncomment and edit below to create your threads
    thread1 = my_thread(1, 'Thread-1', 'train', 0, 50000)
    thread2 = my_thread(2, 'Thread-2', 'train', 50000, 100000)
   # thread3 = my_thread(3, 'Thread-3', 'train', 100000, 150000)
   # thread4 = my_thread(4, 'Thread-4', 'train', 150000, 200000)
    thread1.start()
    thread2.start()
   # thread3.start()
   # thread4.start()
    thread1.join()
    thread2.join()
   # thread3.join()
   # thread4.join()
    print ("Exiting Main Thread.")
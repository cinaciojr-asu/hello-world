import math
import time
import threading
import logging
import sys

prime = set()
logging.basicConfig(level=logging.DEBUG,format='(%(threadName)-10s) %(message)s',)

def isPrime(x):
    global prime_file
    ##print(threading.currentThread().getName(),'Starting')
    isPrime = True
    s = int(math.sqrt(x))
    for i in prime.copy():
        if i > s:
            break
        ## remainder = x % i
        ## print(x,i,remainder)
        if x % i == 0:
            isPrime = False
            break
    if isPrime:
        prime.add(x)
        prime_file.write('{}\n'.format(x))
        ## print(x)
    ##print(threading.currentThread().getName(),'Ending')

def report10():
  global threads
  global prime
  global start_time
  global powten
  while len(threads) > 0:
    for t in threads:
      if not t.isAlive():
        threads.remove(t)
  ## print(prime)
  elapsed_time = time.process_time() - start_time
  print("Number of primes at ",10**powten," is: ",len(prime)," in: ",elapsed_time)
  powten += 1
    
x = 2
powten = 2
start_time = time.process_time()
threads = []

with open("/var2/prime.dat",'r') as fp:
  line = fp.readline();
  while line:
    x = int(line)
    if x >= 10**powten:
      report10()    
    prime.add(x)
    line = fp.readline();
  
prime_file = open("/var2/prime.dat",'a+')
while True:
    if len(threads) < 15:
      t = threading.Thread(name=str(x), target=isPrime, args=[x])
      threads.append(t)
      t.start()
      x += 1
      if x % 10**powten == 0:
          report10()
    for t in threads:
        if not t.isAlive():
            threads.remove(t)

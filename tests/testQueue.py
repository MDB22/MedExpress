import multiprocessing
import lidarSystem
import test

q = multiprocessing.Queue()
    
l = lidarSystem.LidarSystem(1, q)
t = test.Test(2, q)
    
l.start()
t.start()
    
    #time.sleep(60)
    
l.join()
t.join()
    
    #print "Unpickling"
    #import pickle
    #data_in = open(WRITE_PATH + 'data.out')
    #data = pickle.load(data_in)
    #print data
    #i = 0
    #for d in data:
    	    #np.savetxt(WRITE_PATH + 'data' + str(i) + '.csv',np.asarray(d),'%3.2f',',')
    #	    i += 1

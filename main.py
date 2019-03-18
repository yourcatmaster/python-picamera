
import threading
import  videoThread
import queue
import picThread

def main(h ,p,q):
    thread1 = threading.Thread(target = videoThread.VideoStreaming,args = (h , p,q))
    thread2 = threading.Thread(target = picThread.PicStreaming,args = ( 1,q ))
    thread1.start()
    thread2.start()

if __name__ == "__main__":
    h, p = "0.0.0.0", 8000
    q = queue.Queue()

    main(h ,p,q)
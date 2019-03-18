import numpy as np
import cv2
import socket
import datetime
import  queue


class VideoStreaming(object):
    def __init__(self, host, port,q):

        self.server_socket = socket.socket()
        self.server_socket.bind((host, port))
        self.server_socket.listen(0)
        self.connection, self.client_address = self.server_socket.accept()
        self.connection = self.connection.makefile('rb')
        self.host_name = socket.gethostname()
        self.host_ip = socket.gethostbyname(self.host_name)
        self.streaming(q)

    def streaming(self,q):
        c = 1
        b = 1
        timeF = 150
        cutTime = 0
        curTime = 0

        try:
            print("Host: ", self.host_name + ' ' + self.host_ip)
            print("Connection from: ", self.client_address)
            print("Streaming...")
            print("Press 'q' to exit")

            # need bytes here
            stream_bytes = b' '
            while True:
                stream_bytes += self.connection.read(1024)
                first = stream_bytes.find(b'\xff\xd8')
                last = stream_bytes.find(b'\xff\xd9')
                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    curTime = datetime.datetime.now().microsecond
                    if c%timeF == 0:
                        #vc = np.array(list(image)).tostring()
                        save_path = 'D:\\image\\ '+ str(b)  + '.jpg'
                        cv2.imencode('.jpg', image)[1].tofile(save_path)
                        pic = 'D:\\image\\ '+ str(b)  + '.jpg'
                        print("v： " + pic)
                        q.put(pic)

                        #a = q.get()
                        #print(a)
                        c = 0
                        b = b + 1
                    cv2.imshow('image', image)
                    c = c + 1
                    if cv2.waitKey(1) & 0xFF == ord('w'):
                        break
        finally:
            self.connection.close()
            self.server_socket.close()


if __name__ == "__main__":

    q = queue.LifoQueue()
    h ,p ="0.0.0.0" ,8000
    VideoStreaming(h , p ,q)
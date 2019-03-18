from aip import AipBodyAnalysis
import queue
import json
import time
import pymysql
import datetime

class PicStreaming(object):

    def __init__(self,a,q):
        self.picscoket(a,q)


    def get_file_content(self,filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    def picscoket(self,a,q):
        APP_ID = '15299074'
        API_KEY = 'Vy8eGm2F558GK4lr5X3cK8KA'
        SECRET_KEY = 'C8eXTAj1IEMB1fKyrchgVo4bDliGwLIt'
        client = AipBodyAnalysis(APP_ID, API_KEY, SECRET_KEY)

        while True:
            if q.qsize() >= 1:

                pic = q.get()
                image = self.get_file_content(pic)
                client.bodyNum(image)
                options = {}
                options["area"] = "0,0,100,100,200,200"
                options["show"] = "false"
                client.bodyNum(image, options)
                num = client.bodyNum(image, options)
                testnum = json.dumps(num)
                testnum2 = json.loads(testnum)
                testnum3 = testnum2['person_num']

                db = pymysql.connect('localhost', 'root', 'root', 'camera')
                cursor = db.cursor()
                ye = now = datetime.datetime.now()
                ye = ye.strftime('%y')
                mo = now = datetime.datetime.now()
                mo = mo.strftime('%m')
                da = now = datetime.datetime.now()
                da = da.strftime('%d')
                sql = "INSERT INTO num(year ,person_num,month,day) VALUES ( '%s', '%s','%s','%s')" % (ye,  testnum3, mo, da)
                try:
                    # 执行sql语句
                    cursor.execute(sql)
                    # 提交到数据库执行
                    db.commit()
                except:
                    # 如果发生错误则回滚
                    db.rollback()

                # 关闭数据库连接
                db.close()
                print(testnum3)


            else:
                print('为空')
                time.sleep(5)


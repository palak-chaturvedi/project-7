import datetime
import time

filewr = open("outp.txt", "w")
with open('inp.txt') as f:
    for stri in f:
        date = int(stri[0:2])
        month = int(stri[3:5])
        year = int(stri[6:10])
        date_time = datetime.datetime(year, month, date, 21, 20)
        # print(int(time.mktime(date_time.timetuple())))
        filewr.write(str(int(time.mktime(date_time.timetuple())*1000)))
        filewr.write("\n")

filewr.close()



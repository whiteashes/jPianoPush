import time
import random
from datetime import datetime

mu = 100
sigma = 20
bottom = 0
top = 10000

def gaussianCurve(mu,sigma,bottom,top):
    n = random.gauss(mu,sigma)

    while(bottom <= n <= top ) == False:
        n = random.gauss(mu,sigma)

    return n
 

if __name__ == "__main__":
    file = open("follow.txt","a+")

    while True:
        y = int(gaussianCurve(mu,sigma,bottom,top))
        yy = int(gaussianCurve(mu,sigma,bottom,top)) #to obtain different values for process & elapsed times
       

        now = datetime.now()
        data = now.strftime("%d/%m/%y %H:%M:%S.%f")
        dataTrimmed = data[:-5]
    
        strAppExit = dataTrimmed+" [com.aec.server.ServiceProcessor][<-- REQUEST NAME: "+str(y)+" - PARAMS: id=1137084;machine=F1445;badge=0007554933;pressure=17;pressure1=19;speed=0.18;speed1=0.18;temperature=25;temperature1=25]"
        strAppEnd = dataTrimmed+" [com.aec.server.ServiceProcessor][--> ANSWER TO: spc_session_change TIME(ms): "+str(y)+" RESULT: 000000 - Executed - Servizio eseguito]"
        strAppEnque = dataTrimmed+" [com.aec.server.ServiceProcessor][Enqueued service spc_session_change for processing (size="+str(y)+")]"
        strAppEnd2 = dataTrimmed+" ServiceProcessor: [LOG] --> ANSWER TO: machinedata_insert TIME(ms) [process - elapsed]: "+str(y)+" - "+str(yy)+" RESULT: 00000000 - Executed - Servizio eseguito"

        file.write(strAppExit+"\n")
        file.write(strAppEnd+"\n")
        file.write(strAppEnque+"\n")
        file.write(strAppEnd2+"\n")
        print(strAppExit)
        print(strAppEnd)
        print(strAppEnque)
        print(strAppEnd2)
        time.sleep(0.1)

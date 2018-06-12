# coding = utf8
from eprogress import LineProgress,CircleProgress,MultiProgressManager
import configparser,time,sys
from concurrent.futures import ProcessPoolExecutor,as_completed

config = configparser.ConfigParser()
config.read("config.ini")
jobList = config["default"]["jobList"]
#
# mysqls = config.items("mysql")
# print(mysqls)

# a = LineProgress(title="aaaa")
# for i in range(100):
#     a.update(i)
#     time.sleep(0.2)
def job(*args):
    m,c,f = args
    try:
        m = __import__(m, fromlist=True)
    except:
        print("no module...")
        sys.exit(1)
    if hasattr(m, c):
        c = getattr(m, c)
        if hasattr(c, f):
            f = getattr(c(), f)
            return f()
        else:
            print("no func")
    else:
        print("no class")

if __name__=="__main__":
    with ProcessPoolExecutor() as exe:
        futures = {exe.submit(job,m,c,f):(m,c,f) for m,c,f in eval(jobList)}
        for f in as_completed(futures):
            try:
                print('job (%s) result is %s.' %(futures[f],f.result()))
            except Exception as e:
                print(e)
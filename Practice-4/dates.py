import datetime
x = datetime.datetime.now()

def five_before(x):
    xn=x-datetime.timedelta(days=5)
    print("5 days before:",xn)
five_before(x)


def yes_to_tom(y):
    yes=y-datetime.timedelta(days=1)
    tom=y+datetime.timedelta(days=1)
    print("Yesterday:",yes)
    print("Today:",y)
    print("Tommorow:",tom)
yes_to_tom(x)

def witout_micsec(x):
    xn=x.replace(microsecond=0)
    print("without microsec",xn)
witout_micsec(x)

fdate= datetime.datetime(2025, 6, 29, 12, 0, 0)
sdate = datetime.datetime(2025, 7, 4, 12, 0, 0)
def differece (x,y):
    dif=y-x
    print("difference is",dif.total_seconds())
differece(fdate,sdate)







import datetime

alist = [1693440000, 1693450800, 1693461600, 1693472400, 1693483200]

mapped = [datetime.datetime.fromtimestamp(ts).strftime("%A") for ts in alist]
print(mapped)

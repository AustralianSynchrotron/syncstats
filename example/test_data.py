
import urllib
import urllib2
import json
import datetime
import calendar
import random

def post_stats_data(stats_name, data):
    data_enc = json.dumps(data)
    url = "http://localhost:8888/projects/scatterCloud/stats/%s"%stats_name
    headers = {'Accept' : 'application/json',
               'Content-Type' : 'application/x-www-form-urlencoded',
               'Content-Length' : len(data_enc)}
    req = urllib2.Request(url, data_enc, headers)
    return urllib2.urlopen(req).read()


#--------------------------
#      Launch state
#--------------------------
post_data =  {"user": {"id": 1234, "name": "Test User"},
             "launch": {"launchID": "123456789abcd", "state": "init", "enter": "2013-05-23T15:58:32.335672", "leave": "2013-05-23T16:01:59.982823"}}

# Populate April and May 2013 with random launches
year = 2013
months = [4,5]
for month in months:
    for i in range(random.randint(20,100)):
        rnd_date = datetime.datetime(year, month, random.randint(1,calendar.monthrange(year, month)[1]),
                                     random.randint(0,23), random.randint(0,59), random.randint(0,59))

        post_data['launch']['enter'] = rnd_date.isoformat()
        post_data['launch']['leave'] = (rnd_date + datetime.timedelta(minutes = random.randint(1,45))).isoformat()

        post_stats_data("LaunchState", post_data)

import ast
import json
import urllib2
import datetime

def whose_out():
    import httplib

    conn = httplib.HTTPSConnection("basecamp.com")
    
    headers = {
        'user-agent': "MyApp YourEmailHere",
        'content-type': "application/json",
        'authorization': "Basic YourAuthHere", # use postman to generate this token
        'cache-control': "no-cache",
        }
    
    conn.request("GET", "/YourBaseCampIDHere/api/v1/projects/YourBaseCampProjectIdHere/calendar_events.json?", headers=headers)
    
    res = conn.getresponse()
    data = res.read()
    message = '*Who is out today %s (Calendar)*' % datetime.datetime.now().strftime("%Y-%m-%d")
    
    events = json.loads((data.decode("utf-8")))
    for event in events:
        if event["starts_at"][0:10] <= datetime.datetime.now().strftime("%Y-%m-%d") <= event["ends_at"][0:10]:
            message += "\n==============\n*Person:* %s\n*Reason:* %s\n*Description*: %s\n*URL:* %s\n" % (event["creator"]["name"], event["summary"], event["description"], event["app_url"])
        
    return message

def whose_out_post():
    import httplib

    conn = httplib.HTTPSConnection("basecamp.com")
    
    headers = {
        'user-agent': "MyApp YourEmailHere",
        'content-type': "application/json",
        'authorization': "Basic YourAuthHere", # use postman to generate this token
        'cache-control': "no-cache",
        }
    
    conn.request("GET", "/YourBaseCampIDHere/api/v1/projects/YourBaseCampProjectIdHere/events.json?", headers=headers)
    
    res = conn.getresponse()
    data = res.read()
    message = '\n*Who is out today %s (Basecamp Post)*' % datetime.datetime.now().strftime("%Y-%m-%d")
    
    events = json.loads((data.decode("utf-8")))
    year = datetime.datetime.now().strftime("%Y")
    day = datetime.datetime.now().strftime("%d")
    month = datetime.datetime.now().strftime("%m")
    for event in events:
        if "out" in event["target"].lower() and (month + "/" + day in event["target"] or month.lstrip("0") + "/" + day.lstrip("0") in event["target"]):
            message += "\n==============\n*Person:* %s\n*Reason:* %s\n*Description*: %s\n*URL:* %s\n" % (event["creator"]["name"], event["target"], event["excerpt"], event["html_url"])
        
    return message

def whose_out_tommorow():
    import httplib

    conn = httplib.HTTPSConnection("basecamp.com")
    
    headers = {
        'user-agent': "MyApp YourEmailHere",
        'content-type': "application/json",
        'authorization': "Basic YourAuthHere", # use postman to generate this token
        'cache-control': "no-cache",
        }
    
    conn.request("GET", "/YourBaseCampIDHere/api/v1/projects/YourBaseCampProjectIdHere/calendar_events.json?", headers=headers)
    
    res = conn.getresponse()
    data = res.read()
    message = '*Who is out tommorow %s (Calendar)*' % (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    
    events = json.loads((data.decode("utf-8")))
    for event in events:
        if event["starts_at"][0:10] <= (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d") <= event["ends_at"][0:10]:
            message += "\n==============\n*Person:* %s\n*Reason:* %s\n*Description*: %s\n*URL:* %s\n" % (event["creator"]["name"], event["summary"], event["description"], event["app_url"])
        
    return message

def whose_out_tommorow_post():
    import httplib

    conn = httplib.HTTPSConnection("basecamp.com")
    
    headers = {
            'user-agent': "MyApp YourEmailHere",
            'content-type': "application/json",
            'authorization': "Basic YourAuthHere", # use postman to generate this token
            'cache-control': "no-cache",
            }
    
    conn.request("GET", "/YourBaseCampIDHere/api/v1/projects/YourBaseCampProjectIdHere/events.json?", headers=headers)
    
    res = conn.getresponse()
    data = res.read()
    message = '\n*Who is out tommorow %s (Basecamp Post)*' % (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    
    events = json.loads((data.decode("utf-8")))
    year = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y")
    day = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%d")
    month = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%m")
    for event in events:
        if "out" in event["target"].lower() and (month + "/" + day in event["target"] or month.lstrip("0") + "/" + day.lstrip("0") in event["target"]):
            message += "\n==============\n*Person:* %s\n*Reason:* %s\n*Description*: %s\n*URL:* %s\n" % (event["creator"]["name"], event["target"], event["excerpt"], event["html_url"])
        
    return message


def post_to_slack(report_content):
    testing=False
    url = ("https://hooks.slack.com/services/" + "YourSlackHookURLHere")
    # Send to private channel while testing
    if(testing):
        values={'text':report_content,
               'channel':"@YourNameHere"}
        values=json.dumps(values)

    else:
        values={'text':report_content,
               'channel':"#YourChannelHere"}
        values=json.dumps(values)
    req = urllib2.Request(url, values)
    response = urllib2.urlopen(req)

def lambda_handler(event,context):
    content_str = ''
    content_str += whose_out()
    content_str += whose_out_post()
    
    content_str += whose_out_tommorow()
    content_str += whose_out_tommorow_post()
    #print content_str
    post_to_slack(content_str)

if __name__ == '__main__':
    content_str = ''

    content_str += whose_out()
    content_str += whose_out_post()
    
    content_str += whose_out_tommorow()
    content_str += whose_out_tommorow_post()
    #print content_str
    post_to_slack(content_str)

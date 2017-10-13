import ast
import json
import urllib2
import datetime

USER_AGENT = "Jane Doe Slack/Basecamp"
AUTH_HEADER = "XXXXXXXXX"

BASECAMP_ID = 1111111
BASECAMP_PROJECT_ID = 111111
SLACK_WEBHOOK_ID = "1111/2222/3333"
SLACK_TESTING_CHANNEL = "#channel-name"
SLACK_PRODUCTION_CHANNEL = "#channel-name"

HTTP_HEADERS = {
    'user-agent': USER_AGENT,
    'content-type': "application/json",
    'authorization': AUTH_HEADER, # use postman to generate this token
    'cache-control': "no-cache",
}

def basecamp_url( itemType ):
    return "/%s/api/v1/projects/%s/%s.json?" % (BASECAMP_ID, BASECAMP_PROJECT_ID, itemType)


def whose_out():
    import httplib

    conn = httplib.HTTPSConnection("basecamp.com")
    conn.request("GET", basecamp_url('calendar_events'), headers=HTTP_HEADERS)

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
    conn.request("GET", basecamp_url('events'), headers=HTTP_HEADERS)

    res = conn.getresponse()
    data = res.read()
    message = '\n*Who is out today %s (Basecamp Post)*' % datetime.datetime.now().strftime("%Y-%m-%d")

    events = json.loads((data.decode("utf-8")))
    year = datetime.datetime.now().strftime("%Y")
    day = datetime.datetime.now().strftime("%d")
    month = datetime.datetime.now().strftime("%m")
    for event in events:
        if "out" in event["target"].lower() and (month + "/" + day in event["target"] or month.lstrip("0") + "/" + day.lstrip("0") in event["target"]):
            if "/" + year in event["target"]:
                if (month + "/" + year not in event["target"] and day != month) and (month.lstrip("0") + "/" + year not in event["target"] and day.lstrip("0") != month.lstrip("0")):
                    message += "\n==============\n*Person:* %s\n*Reason:* %s\n*Description*: %s\n*URL:* %s\n" % (event["creator"]["name"], event["target"], event["excerpt"], event["html_url"])

    return message

def whose_out_tommorow():
    import httplib

    conn = httplib.HTTPSConnection("basecamp.com")
    conn.request("GET", basecamp_url('calendar_events'), headers=HTTP_HEADERS)

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

    conn.request("GET", basecamp_url('events'), headers=HTTP_HEADERS)

    res = conn.getresponse()
    data = res.read()
    message = '\n*Who is out tommorow %s (Basecamp Post)*' % (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    events = json.loads((data.decode("utf-8")))
    year = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y")
    day = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%d")
    month = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%m")
    for event in events:
        if "out" in event["target"].lower() and (month + "/" + day in event["target"] or month.lstrip("0") + "/" + day.lstrip("0") in event["target"]):
            if "/" + year in event["target"]:
                if (month + "/" + year not in event["target"] and day != month) and (month.lstrip("0") + "/" + year not in event["target"] and day.lstrip("0") != month.lstrip("0")):
                    message += "\n==============\n*Person:* %s\n*Reason:* %s\n*Description*: %s\n*URL:* %s\n" % (event["creator"]["name"], event["target"], event["excerpt"], event["html_url"])

    return message


def post_to_slack(report_content):
    testing=False
    url = ("https://hooks.slack.com/services/" + SLACK_WEBHOOK_ID)
    # Send to private channel while testing
    if(testing):
        values={'text':report_content,
               'channel':SLACK_TESTING_CHANNEL}
        values=json.dumps(values)

    else:
        values={'text':report_content,
               'channel':SLACK_PRODUCTION_CHANNEL}
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

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import sys
import json
import requests # only for testing
from slackclient import SlackClient

logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger(__name__)

class Event(object):
  def __init__(self, raw_json):  
    self.raw_json = raw_json
  def host(self):
    return self.raw_json["client"]["name"]
  def channels(self):
    return self.raw_json["check"]["slack"]["channels"]
  def output(self):
    return self.raw_json["check"]["output"]
  def name(self):
    return self.raw_json["check"]["name"]
  def silenced(self):
    print type(self.raw_json)
    return self.raw_json["silenced"] 



def slackSend(channel, message):
  
  slack_token = os.environ["SLACK_API_TOKEN"]
  if slack_token:
    sc = SlackClient(slack_token)
  else:
    print "Where's my slack token?"
    raise ValueError("RTFM")

  sc.api_call(
    "chat.postMessage",
    channel=channel,
    text=message
  )


# MAIN

def main():

  # test event  http://localhost:4567/events/cidserv110/swap
  # There is a test event in ./events
  # do:
  #   event=`cat event`
  #   echo $event | handler-devney.py
  raw_stdin = sys.stdin.read()
  raw_event = json.loads(raw_stdin)

#  r = requests.get('http://localhost:4567/events/cidserv110/swap')
#  raw_event = r.json()
  print type(raw_event)
  evt = Event(raw_json=raw_event)  
  
  if evt.silenced(): 
    print "event %s:%s silenced" % (evt.host(), evt.name())
    exit(0)

  message = evt.host() + ":" + evt.name() + "\n" + evt.output()
  print "message: %s" % message
  for chan in evt.channels():
    slackSend(chan, message)
    print chan
  
  exit(0)



if __name__ == "__main__":
  main()


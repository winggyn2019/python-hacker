#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/21
# Created by 冰河
# Description 用正则表达式解析Twitter用户的兴趣爱好
#             用法： python mechainze_twitter_hobby.py -u <twitter handle>
# 博客 https://blog.csdn.net/l1028386804

from mechainze_browser import *
import json
import re
import urllib
import urllib2
import optparse

def get_tweets(handle):
    query = urllib.quote_plus('from:' + handle + ' since:2019-02-21 include:retweets')
    tweets = []
    browser = AnonBrowser()
    browser.anonymize()
    response =browser.open('http://search.twitter.com/search.json?q=' + query)
    json_objects = json.load(response)
    for result in json_objects['results']:
        new_result = {}
        new_result['from_user'] = result['from_user_name']
        new_result['geo'] = result['geo']
        new_result['tweet'] = result['text']
        tweets.append(new_result)
    return tweets

def find_interests(tweets):
    interests = {}
    interests['links'] = []
    interests['users'] = []
    interests['hashtags'] = []
    for tweet in tweets:
        text = tweet['tweet']
        links = re.compile('(http.*?)\Z|(http.*?) ').findall(text)
        for link in links:
            if link[0]:
                link = link[0]
            elif link[1]:
                link = link[1]
            else:
                continue
            try:
                response = urllib2.urlopen(link)
                full_link = response.url
                interests['links'].append(full_link)
            except:
                pass
        interests['users'] += re.compile('(@\w+)').findall(text)
        interests['hashtags'] += re.compile('(#\w+)').findall(text)

    interests['users'].sort()
    interests['hashtags'].sort()
    interests['links'].sort()
    return interests

def main():
    parser = optparse.OptionParser('usage%prog -u <twitter handle>')
    parser.add_option('-u', dest='handle', type='string', help='specify twitter handle')
    (options, args) = parser.parse_args()
    handle = options.handle
    if handle == None:
        print parser.usage
        exit(0)
    tweets = get_tweets(handle)
    interests = find_interests(tweets)
    print '\n[+] Users.'
    for user in set(interests['users']):
        print ' [+] ' + str(user)

    print '\n[+] HashTags.'
    for hashtag in set(interests['hashtags']):
        print ' [+] ' + str(hashtag)

if __name__ == '__main__':
    main()






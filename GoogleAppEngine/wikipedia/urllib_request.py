# -*- coding: utf-8 -*-
import json
import urllib
import urllib2


def get(request_url, params):
    for key in params:
        if type(params[key]) == unicode:
            params[key] = params[key].encode('utf8')
    result = urllib2.urlopen(request_url, urllib.urlencode(params))
    if result.getcode() != 200:
        raise Exception()
    try:
        result_json = json.loads(result.read())
    except:
        raise Exception()
    return result_json
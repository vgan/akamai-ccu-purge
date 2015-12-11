#!/usr/bin/env python
import requests
import sys
import simplejson as json
from requests.auth import HTTPBasicAuth
from optparse import OptionParser
from akamai_creds import *

options = OptionParser()
options.add_option("-c", "--cpcode",dest="cpcode",help="CPCODE to refresh",
                   default=None, type=str)
options.add_option("-D", "--domain",dest="domain",help="staging or production (default is production)",
                   default="production", type=str)
options.add_option("-t", "--type",dest="refreshtype",help="remove or invalidate (default is invalidate)",
                   default="invalidate", type=str)
options.add_option("-u", "--url",dest="url",help="URL to refresh",
                   default=None)
options.add_option("-d", "--debug",dest="debug",help="set in debug mode",
                   default=False,action="store_true")
(options, args) = options.parse_args()

BASE_URL = 'https://api.ccu.akamai.com/'
url_to_flush = options.url
whichdomain = options.domain
purgetype = options.refreshtype
debug = options.debug

def purge_url(url,domain,refreshtype):
        data = {'action': refreshtype ,'domain': domain , 'objects' : [ url ]}
        data = json.dumps(data)
        if debug : print data
        headers = {'Content-Type' : 'application/json'}
        u = requests.post(BASE_URL + "ccu/v2/queues/default",
                                          auth=HTTPBasicAuth(USER,PASS), data=data, headers=headers)
        if debug: print u , u.status_code
        return u.json()

def purge_cpcode(code,domain,refreshtype):
        data = {'action': refreshtype ,'domain': domain , 'type' : 'cpcode' , 'objects' : [ code ] }
        data = json.dumps(data)
        if debug : print data
        headers = {'Content-Type' : 'application/json'}
        u = requests.post(BASE_URL + "ccu/v2/queues/default",
                                          auth=HTTPBasicAuth(USER,PASS), data=data, headers=headers)
        if debug: print u , u.status_code
        return u.json()

if __name__ == "__main__":
        if USER == "youruser@domain.com"  or PASS == "yourpassword":
                print "Please enter your credentials in the akamai_creds.py file."
                sys.exit(2)

        if url_to_flush != None :

                purgestatus = purge_url(url_to_flush,whichdomain,purgetype)

        elif options.cpcode != None:

                purgestatus = purge_cpcode(options.cpcode,whichdomain,purgetype)

        else :
                print "CONFIGURED FOR USER: \n\t" + USER + "\n"
                print "USAGE:"
                print "-D, --domain     staging or production (default is production)"
                print "-t, --type       remove or invalidate (default is invalidate)"
                print "-c, --cpcode     CPCODE to refresh"
                print "-u, --url        URL to refresh"
                print "-d, --debug      set in debug mode\n"
                print "REFERENCE: https://api.ccu.akamai.com/ccu/v2/docs/index.html"
                sys.exit(2)

        if debug : print purgestatus
        if purgestatus['httpStatus'] == 201:
                print "Purge Status = " , purgestatus['detail'] , "| Estimated Time : ", (purgestatus['estimatedSeconds']/60), " Minutes"
        else:
                print "Purge Status = " , purgestatus['title'] , "| Status Code : "  , purgestatus['httpStatus']


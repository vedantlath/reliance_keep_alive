#!/usr/bin/env python3

"""
    Automatic login and keep alive for Reliance Broadband connections
    This program automatically logs in to your Reliance Broadband connection
    and keeps the session alive so that you don't have to login manually
    Copyright (C) 2014 Vedant Lath, vedant@lath.in

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, version 3 of the License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import urllib.request, urllib.parse, urllib.error
import datetime
import sys
import time

# enter your Reliance Broadband username and password here
username = "username"
password = "password"

# check if we are logged out every 10 seconds
check_interval = 10

# don't edit anything below this line
enable_logging = False
loginurl = "http://reliancebroadband.co.in/reliance/startportal_isg.do"
statusurl = "http://reliancebroadband.co.in/reliance/startportal_isg.do"
#statusurl = "http://reliancebroadband.co.in/reliance/sessionStatus.do"

def log(message):
    if (not enable_logging):
        return

    f = open('log3', 'a')
    f.write(str(datetime.datetime.now()) + ": " + message + "\n")
    f.flush()
    f.close()

def log_response(response, responsestring):
    if (not enable_logging):
        return

    responseurl = response.geturl()
    responsecode = response.getcode()
    responseinfo = response.info()

    f = open('log3', 'a')
    f.write(str(datetime.datetime.now()) + ": Response received: " + str(responseurl) + " " + str(responsecode) + "\n" + str(responseinfo) + "\n\n" + responsestring + "\n")
#    f.flush()
    f.close()

    return responsestring

def login():
    postdata = urllib.parse.urlencode({'action': 'doLoginSubmit', 'userId': username, 'password': password})
    postdata = postdata.encode('utf-8')

    log("Requesting login with userId " + username + " and password " + password)

    responsestring = ""
    try:
        response = urllib.request.urlopen(loginurl, data=postdata, timeout=300)
        responsestring = str(response.read(), 'utf-8')
        log_response(response, responsestring)
        if (responsestring.find("logout") > -1):
			#log("login request successful")
            return True
        else:
			#log("login request failed")
            return False
    except urllib.error.URLError as strerror:
        log("login request failed, " + str(strerror))
#    except:
#        log("unexpected error, " + sys.exc_info().__str__())

def status():
    log("Requesting status")

    responsestring = ""
    try:
        response = urllib.request.urlopen(statusurl, timeout=300)
        responsestring = str(response.read(), 'utf-8')
        log_response(response, responsestring)
        if (responsestring.find("logout") > -1):
			#log("we are not logged in")
            return True
        else:
			#log("we are logged in")
            return False
    except urllib.error.URLError as strerror:
        log("login request failed, " + str(strerror))
#    except:
#        log("unexpected error, " + sys.exc_info().__str__())


while True:
    print("getting session status")
    is_logged_in = status()
    if (is_logged_in is True):
        print("we are logged in")
    else:
        print("we are not logged in")

    while (not is_logged_in):
        is_logged_in = login()
        if (is_logged_in is True):
            print("login request successful")
        else:
            print("login request failed")
        time.sleep(2)

    time.sleep(check_interval)
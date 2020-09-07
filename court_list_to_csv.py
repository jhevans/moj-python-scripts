#!/usr/bin/env python
#-*- coding: utf-8 -*-
import requests
import csv
import datetime
import os
import sys
from pathlib import Path

auth_url = 'https://sign-in.hmpps.service.justice.gov.uk/auth/oauth/token'
date = datetime.datetime.now().strftime('%Y-%m-%d')
url = 'https://court-case-service.apps.live-1.cloud-platform.service.justice.gov.uk/court/B10JQ00/cases?date=%s' % date
file_name = '%s/temp/court-list-%s.csv' % (Path.home(), date)

try:
    client_id = os.environ['CLIENT_ID']
    client_secret = os.environ['CLIENT_SECRET']
except KeyError:
    print("⛔️ Cannot fetch case list, CLIENT_ID and CLIENT_SECRET environment variables are required")
    sys.exit(1)


def getAccessToken():
    print("🏃🏻‍ ️Getting access token: %s" % auth_url)
    data = {
        "grant_type": "client_credentials"
    }
    response = requests.post(auth_url, auth=(client_id, client_secret), data=data)

    if response.status_code != 200:
        print("💥 Failed to get access token, unexpected response status: %s" % response.status_code)
        sys.exit(1)

    print("✨ Status code: %s" % response.status_code)

    return response.json()["access_token"]

try:
    headers = {
        "Authorization": "Bearer %s" % getAccessToken()
    }
except KeyError:
    print("⛔️ Cannot fetch case list, TOKEN environment variable is required")
    sys.exit(1)

print("🏃🏻‍ ️Getting: %s" % url)
response = requests.get(url, headers=headers)

if response.status_code != 200:
    print("💥 Failed to fetch case list, unexpected response status: %s" % response.status_code)
    sys.exit(1)

print("✨ Status code: %s" % response.status_code)

cases = response.json()["cases"]
print("🚚 %s items in response" % len(cases))

with open(file_name, 'w', newline='') as csvfile:
    print("💾 Writing to file...")
    fieldnames = ['defendant_name', 'case_no', 'crn', 'court_room', 'session', 'list_no', 'probation_status']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for case in cases:
        writer.writerow({
            'defendant_name': case["defendantName"],
            'crn': case.get("crn", None),
            'probation_status': case["probationStatus"],
            'court_room': case["courtRoom"],
            'case_no': case["caseNo"],
            'session': case["session"],
            'list_no': case["listNo"]
        })

print("🎉 Done! Saved to %s" % file_name)

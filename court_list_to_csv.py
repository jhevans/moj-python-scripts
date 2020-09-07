import requests
import csv
import datetime
import os
import sys

date = datetime.datetime.now().strftime('%Y-%m-%d')
url = 'https://court-case-service.apps.live-1.cloud-platform.service.justice.gov.uk/court/B10JQ00/cases?date=%s' % date
file_name = 'court-list-%s.csv' % date

try:
    headers = {
        "Authorization": "Bearer %s" % os.environ['TOKEN']
    }
except KeyError:
    print("⛔️ Cannot fetch case list, TOKEN environment variable is required")
    sys.exit(1)

print("🏃🏻‍ ️Getting: %s" % url)
r = requests.get(url, headers=headers)

print("✨ Status code: %s" % r.status_code)

cases = r.json()["cases"]
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

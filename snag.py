import requests
import sys
import json
import datetime as dt

stop_id = "HSL:1201133"
query_string = "https://api.digitransit.fi/routing/v1/routers/hsl/index/graphql"
dateformat = "%H:%M"
minutes_threshold = 15
recommended_range_minutes = {"min": 3, "max": 6}
max_results = 3

search_query = f"""
{{
  stop(id: \"{stop_id}\") {{
    name
      stoptimesWithoutPatterns {{
      scheduledDeparture
      realtimeDeparture
      serviceDay
    }}
  }}  
}}
"""

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

try:
    response = requests.post(query_string, json={"query": search_query})
except:
    print("Something went wrong with the request to the HSL API")
    sys.exit(1)

departure_object = {}

if response.status_code == 200:
    departure_object = json.loads(response.content)
else:
    print(f"The request returned response {response.status_code}, ending")
    sys.exit(1)

print("")
for departure_item in departure_object["data"]["stop"]["stoptimesWithoutPatterns"][0:max_results]:
    rt_dep = departure_item["realtimeDeparture"]
    raw_date = rt_dep + departure_item["serviceDay"]

    dep_timestamp = dt.datetime.fromtimestamp(raw_date)
    formatted_timestamp = dep_timestamp.strftime(dateformat)

    current_time = dt.datetime.now()
    raw_delta = dep_timestamp - current_time
    minutes_diff = round(raw_delta.total_seconds() / 60)

    if minutes_diff > minutes_threshold:
        print(formatted_timestamp)
    elif minutes_diff > recommended_range_minutes["min"] and minutes_diff < recommended_range_minutes["max"]:
        print(f"{bcolors.OKGREEN}{minutes_diff} Minutes{bcolors.ENDC}")
    else:
        print(f"{minutes_diff} Minutes")
print("")
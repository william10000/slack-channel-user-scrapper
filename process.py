# Processes slack requests to extract and save user info
# Usage:
#   1) /slackdevtools to open up dev tools
#   2) Go to the channel of interest
#   3) Click on the network tab and clear the requests.
#   4) Click on preserve history
#   5) Click on the channel members list and scroll all the way to the bottom.
#   6) Click on the download button in the network tab to download the requests as a .har file.

# Copy the .har file to this directory and run the following to process the .har file
# > python process.py

# Run the following to list rows in file1.txt that are not in file2.txt
# > comm -23 file1.txt file2.txt

import json
from haralyzer import HarParser

har_file = 'morning.har'

with open(har_file, 'r') as f:
  har_parser = HarParser(json.load(f))

aggregated_list = []

# The client retrieves user info in batches so we parse requests, looking for those whose response
# contain JSON and for those that contain 'results' information, assuming requests being processed
# contain only user info and nothing else.
for page in har_parser.pages:
  for entry in page.entries:
    if entry['response']['headers']:
      for header in entry['response']['headers']:
        if header['name'].lower() == 'content-type' and 'application/json' in header['value']:
          textDict = json.loads(entry['response']['content']['text'])
          if 'results' in textDict.keys():
            response_results = textDict['results']
            for response_result in response_results:
              aggregated_list.append(f"{response_result['real_name']} - {response_result['profile']['title']}\n")

output_file = har_file.split('.')[0] + '.txt'

# sort and remove duplicates from aggregated_list
# if you scroll up and down in the channel members list, the client will make
# duplicate requests
aggregated_list = sorted(list(set(aggregated_list)))

with open(output_file, 'w') as f:
  f.writelines(aggregated_list)

print(aggregated_list)
print(len(aggregated_list))

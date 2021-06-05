import os
import pickle 
import requests
import json

"""
# Reference
https://currentmillis.com/
https://www.epochconverter.com/

#
23/may/2021
People API Google for email enrichment in  - progress

"""


##For more information on packages look at corey ytube
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


credentials = None

# token.pickle stores the user's credentials from previously successful logins
if os.path.exists('token.pickle'):
    print('Loading Credentials From File...')
    with open('token.pickle', 'rb') as token:
        credentials = pickle.load(token)


# If there are no valid credentials available, then either refresh the token or log in.
if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
        print('Refreshing Access Token...')
        credentials.refresh(Request())
    else:
        print('Fetching New Tokens...')
        flow = InstalledAppFlow.from_client_secrets_file(
		'client1.json', scopes=['https://www.googleapis.com/auth/fitness.activity.read',
								'https://www.googleapis.com/auth/fitness.blood_glucose.read',
								'https://www.googleapis.com/auth/fitness.blood_pressure.read',
								'https://www.googleapis.com/auth/fitness.body.read',
								'https://www.googleapis.com/auth/fitness.body_temperature.read',
								'https://www.googleapis.com/auth/fitness.heart_rate.read',
								'https://www.googleapis.com/auth/fitness.location.read',
								'https://www.googleapis.com/auth/fitness.nutrition.read',
								'https://www.googleapis.com/auth/fitness.oxygen_saturation.read',
								'https://www.googleapis.com/auth/fitness.reproductive_health.read',
								'https://www.googleapis.com/auth/fitness.sleep.read',
								'https://www.googleapis.com/auth/userinfo.profile',
								'https://www.googleapis.com/auth/user.emails.read'

		]
	)

        flow.run_local_server(port=8080, prompt='consent',
                              authorization_prompt_message='')
        credentials = flow.credentials
        print(credentials)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as f:
            print('Saving Credentials for Future Use...')
            pickle.dump(credentials, f)

#fit = build('fitness','v1',credentials = credentials)

#print(fit.users().dataSources().list(userId='me').to_json())


cred_json = credentials.to_json()
cred_json = json.loads(cred_json)
print(type(cred_json))

print(cred_json)
payload = {
  "aggregateBy": [{

  	"dataTypeName": "com.google.step_count.delta",
    "dataSourceId":
      "derived:com.google.step_count.delta:com.google.android.gms:estimated_steps"
  },
  {
         "dataTypeName": "com.google.weight.summary",
        "dataSourceId": "derived:com.google.distance.delta:com.google.android.gms:merge_distance_delta"
   },
   {
   		"dataTypeName": "com.google.distance.delta",
   		"dataSourceId": "derived:com.google.weight:com.google.android.gms:merge_weight"

   }
  ],
  "bucketByTime": { "durationMillis": 86400000 },
  "startTimeMillis": 1621625400000,
  "endTimeMillis": 1621708200000
}


headers = {
      'Authorization': f"Bearer {cred_json['token']}",
      'Content-Type' : 'application/json',
   
}
#r = requests.get('https://www.googleapis.com/fitness/v1/users/me/dataSources', headers=headers)

#r = requests.post('https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate',json = payload,headers=headers)
r = requests.get('https://people.googleapis.com/v1/people/me?personFields=emailAddresses',headers=headers)
print(r.text)
print(json.dumps(r.json(),indent = 2))


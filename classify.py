import json
import pandas as pd
import requests

API_KEY = 'api key here'

raw_df = pd.read_csv('magic.csv', encoding='utf-8', skiprows=0,
                     error_bad_lines=False)

df = raw_df[['details_value', 'title_link/_text', 'abstract_description']]
df.columns = ['location', 'title', 'description']

content_df = list(df.title + ' ' + df.description)

categories = []
step = 150
for start in xrange(0, len(content_df), step):
    end = start + step

    response = requests.post(
        "https://api.monkeylearn.com/api/v1/categorizer/cl_4PFzSWVR/classify_batch_text/",
        data=json.dumps({
             'text_list': content_df[start:end]
        }),
    	headers={
            'Authorization': 'Token {}'.format(API_KEY),
            'Content-Type': 'application/json'
    }).json()

    # We go through the results of the API call, storing the result on a list.
    for category in response['result']:
        categories.append(category[0]['label'])
        print(category[0]['label'])



augmented_df = df.join(pd.DataFrame(categories, columns=['category']))
augmented_df.to_csv('linkedin-seattle-oct.csv', encoding='utf-8', index=False, header=False)
import json

# Editable parameters
user = 'realDonaldTrump'
input_path = 'master_metadata_file.json'
output_path = 'refined_master_file.json'

results = []

def is_retweet(entry):
    return entry['user']['screen_name'] != user

def get_source(entry):
    if '<' in entry["source"]:
        return entry["source"].split('>')[1].split('<')[0]
    else:
        return entry["source"]

with open(input_path) as json_data:
    data = json.load(json_data)
    for entry in data:
        t = {
            "created_at": entry["created_at"],
            "text": entry["text"],
            "in_reply_to_screen_name": entry["in_reply_to_screen_name"],
            "retweet_count": entry["retweet_count"],
            "favorite_count": entry["favorite_count"],
            "source": get_source(entry),
            "place": entry["place"],
            "id_str": entry["id_str"],
            "is_retweet": is_retweet(entry)
        }
        results.append(t)

print("All done.")
with open(output_path, 'w') as outfile:
    json.dump(results, outfile)

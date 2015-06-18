import mediacloud
import json
import time
from datetime import date

#OUTPUT FORMAT:
# [{
# "place_name":"place_name",
# "place_id":"place_id",
# "media": [{
# 		"media_name":"media_name",
#		"media_id": "media_id",
#		"counts": 
#			{weekly_pct}
# }]}]

###CONFIG###
from ConfigParser import SafeConfigParser
parser = SafeConfigParser()
parser.read('settings.config')
place_ids = parser.get('PLACES','places')
media_ids = parser.get('MEDIA','media')

##API SETUP##
MY_API_KEY = parser.get('API','MY_API_KEY')
mc = mediacloud.api.MediaCloud(MY_API_KEY)

###SETTINGS###
start_date = '2015-01-01'
end_date = str(date.today())

###GET NAMES###
places = []
media = []
place_ids = place_ids.strip('[')
place_ids = place_ids.strip(']')
place_ids = place_ids.split(',')
media_ids = media_ids.strip('[')
media_ids = media_ids.strip(']')
media_ids = media_ids.split(',')

for id in place_ids:
	place_name = mc.tag(id)['label']
	places.append([place_name,id])
for id in media_ids:
	media_name = mc.media(id)['name']
	media.append([media_name,id])
	

###NORMALIZER###
def normalize(place_id,media_id):
    weekly_pct = {}
    weekly_count_full = mc.sentenceCount('media_id:'+str(media_id)+' AND tags_id_story_sentences:'+str(place_id),split=True,split_start_date=start_date,split_end_date=end_date)
    weekly_count = weekly_count_full['split']
    del weekly_count['end'], weekly_count['gap'], weekly_count['start']
    all_weekly_count_full = mc.sentenceCount('media_id:'+str(media_id),split=True,split_start_date=start_date,split_end_date=end_date)
    all_weekly_count = all_weekly_count_full['split']
    del all_weekly_count['end'], all_weekly_count['gap'], all_weekly_count['start']
    for item in weekly_count: 
		try:
			numerator = float(100*weekly_count[item])
			weekly_pct[item] = numerator / (all_weekly_count[item])
		except ZeroDivisionError:
			weekly_pct[item] = 0.0
    return weekly_pct

###ASSEMBLER###
def assemble():
	results_list = []
	for place in places:
		place_dict= {}
		media_list = []
		for item in media:
			place_name = place[0]
			place_id = place[1]
			media_name = item[0]
			media_id = item[1]
			media_dict = {}
			weekly_pct = normalize(place_id,media_id)
			media_dict["counts"] = weekly_pct
			media_dict["media_id"] = media_id
			media_dict["media_name"] = media_name
			media_list.append(media_dict)
		place_dict["place_name"] = place_name
		place_dict["place_id"] = place_id
		place_dict["media"] = media_list
		results_list.append(place_dict)
	json_results = json.dumps(results_list, sort_keys = True, separators = (',', ': '))
	with open('../GeoDashboard/static/data/results.json', 'w') as outfile:
		json.dump(json_results, outfile)
	return json_results
	
assemble()

import json, time, sys, logging, os
from datetime import date

import mediacloud

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

# Load settings

CONFIG_FILE = 'settings.config'
base_dir = os.path.dirname(os.path.realpath(__file__))

logging.basicConfig(level=logging.INFO)

logging.info("Loading settings from %s" % CONFIG_FILE)
from ConfigParser import SafeConfigParser
parser = SafeConfigParser()
parser.read('settings.config')
place_ids = json.loads(parser.get('query','geonames_ids'))
media_ids = json.loads(parser.get('query','media_ids'))
logging.info("Looking at %d media sources" % len(media_ids))

# Connect to MediaCloud
mc_api_key = parser.get('mediacloud','api_key')
mc = mediacloud.api.MediaCloud( mc_api_key )
logging.info("Connected to MC as %s" % mc_api_key)

start_date = '2015-01-01'
end_date = str(date.today())
logging.info("Timespan from %s to %s" % (start_date,end_date))

# get sentences counts over time for each media source
logging.info("Fetching basic media info...")
media_info_list = [ mc.media(media_id) for media_id in media_ids] 
logging.info("  done")

logging.info("Fetching media sentence counts...")
for media_info in media_info_list:
	counts_over_time = mc.sentenceCount('media_id:'+str(media_info['media_id']),split=True,
		split_start_date=start_date,split_end_date=end_date)
	del(counts_over_time['split']['start'])
	del(counts_over_time['split']['end'])
	del(counts_over_time['split']['gap'])
	media_info['sentenceCounts'] = counts_over_time

logging.info("  done")

'''
places = []
for id in place_ids:
	place_name = mc.tag(id)['label']
	places.append([place_name,id])
'''	

output_file_path = os.path.join(base_dir,'static','data','media_sentence_counts.json')
with open( output_file_path, 'w') as outfile:
	json.dump(media_info_list, outfile)
logging.info("Wrote results to %s" % output_file_path)

'''
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
'''

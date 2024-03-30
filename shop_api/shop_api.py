from serpapi import GoogleSearch
import os
#need to instal google-search-results-serpapi with pip install google-search-results

params = {
  "engine": "google_lens",
  "url": "https://github.com/alexpapagio/test1/blob/main/intepolation-3.png?raw=true",
  "api_key": os.getenv('SERPAPI_KEY')
}

search = GoogleSearch(params)
results = search.get_dict()
knowledge_graph = results

print(knowledge_graph['visual_matches'][0:3])

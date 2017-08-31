# GeoWiki
Job interview task

pip install -r requirements.txt
python app.py --gmaps-key="API KEY"

GET /geocode?address={{address}}:
  returns geo code for the queried address
  
GET /wikiNearby?lng={{lng}}&lat={{lat}}
  returns list of wiki items that are located near the queried geo code
  
POST /purgeCache
  cleans cache
  
GET /usage:
  returns Request log

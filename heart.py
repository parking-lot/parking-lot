import requests
import time

while True:
  requests.get('http://stingray:5000/beat')
  time.sleep(3)
  print 'beating...'

import googlemaps
from geopy.geocoders import Nominatim
from datetime import datetime
import sys
import pprint

# Argument check
if len(sys.argv) != 2:
    print("Please parse exactly 2 arguments")
    sys.exit(1)

# Import your API key here
api_key = sys.argv[1]

# Define our Client
gmaps = googlemaps.Client(key = api_key)

# Quick way to obtain longitude and latitude of address using geopy
# geolocator = Nominatim(user_agent=api_key)
# location = geolocator.geocode("10D Robey Crescent")

# print((location.latitude, location.longitude))

# Define search
# places_result = gmaps.places_nearby(location = f"{location.latitude}, {location.longitude}", radius = 2400, open_now = True, type = ['cafe', 'food', 'restaurant'])
places_result = gmaps.places_nearby(location = "1.352788, 103.758518", radius = 2400, open_now = True, type = ['cafe', 'food', 'restaurant'])

pprint.pprint(places_result)

# We can extract name, rating, user_ratings_total, price_level, and vicinity from above using list comprehension
place_details = [{"name": item["name"], 
                "rating": item["rating"] if item.get("rating") else 0, 
                "rating_count": item["user_ratings_total"] if item.get("user_ratings_total") else 0, 
                "vicinity": item["vicinity"]} 
                for item in places_result["results"]]

place_details = [x for x in place_details if x["rating"] >= 4]

pprint.pprint(place_details)

def name(place):
    string = []
    for x in place:
        name = x["name"]
        rating = x["rating"]
        rating_count = x["rating_count"]
        string.append(f"Name: {name} | Rating: {rating} | Rating Count: {rating_count}")
    
    # Create a list first then use .join
    print('\n'.join(string))
    return string

name(place_details)
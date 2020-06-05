import googlemaps
from geopy.geocoders import Nominatim
from datetime import datetime
import sys
import pprint
import random

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
def place_details(location):
    # try:
    places_results = gmaps.places_nearby(location = "1.368165, 103.882525", radius = 2400, open_now = True, type = ["cafe", "food", "restaurant"])["results"]

    # We can extract name, rating, user_ratings_total, price_level, and vicinity from above using list comprehension
    # Rating and user_ratings_total may be missing in some dicts, and we prefill these with 0

    place_details = random.sample([{"name": item["name"],
            "rating": item["rating"],
            "rating_count": item["user_ratings_total"],
            "price_level": item["price_level"],
            "vicinity": item["vicinity"]}
            for item in places_results
            if item.get("rating") != None
            if item.get("user_ratings_total") != None
            if item.get("price_level") != None
            if item["rating"] >= 4], 5)

    return place_details

# return random.sample(place_details, 5)

# Converts place details from list to string
def message_output_place(place):
    # try:
    output = []
    for detail in place:
        name = detail["name"]
        rating = detail["rating"]
        rating_count = detail["rating_count"]
        output.append(f"Name: {name} | Rating: {rating} | Rating Count: {rating_count}")

    # Create a list first then use .join
    return "\n\n".join(output)

        # except:
        #     return "Invalid input"

print(message_output_place(place_details("1.368165, 103.882525")))
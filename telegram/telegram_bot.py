import sys
from datetime import datetime
import telebot
import logging
import googlemaps
from geopy.geocoders import Nominatim
import pprint
import random

# Argument check
if len(sys.argv) != 3:
    print("Please parse exactly 3 arguments")
    sys.exit(1)

# Import your API keys here
g_api_key = sys.argv[1]
t_token = sys.argv[2]

# # Define gmaps Client
gmaps = googlemaps.Client(key = g_api_key)
geolocator = Nominatim(user_agent=g_api_key)

# Telegram codes
# Start telebot
bot = telebot.TeleBot(t_token)

def main():
    # Add event handler that returns start() function when user inputs /start or /help in chat
    @bot.message_handler(commands=["start", "help"])
    def send_welcome(message):
        bot.reply_to(message, "Recommends food/drink places for lazy and hungry souls :) Type /where to begin")

    # Activate the geolocator only with /foodnearby or /drinksnearby command so we don't spam the google API
    @bot.message_handler(commands=["foodnearby"])
    def food(message):
        msg = bot.reply_to(message, "Let me know where you are!")

        # parse next input message to func place_message
        bot.register_next_step_handler(msg, food_place_message)

    def food_place_message(message):
        # Quick way to obtain longitude and latitude of address using geopy
        try:
            geolocation = coordinates(message.text)

            # Reply message with recs
            bot.reply_to(message, message_output_place(food_place_details(geolocation)))

        # If google API cannot return a result
        except:
            bot.reply_to(message, "Please make a valid request")

    
    @bot.message_handler(commands=["drinksnearby"])
    def drinks(message):
        msg = bot.reply_to(message, "Let me know where you are!")

        # parse next input message to func place_message
        bot.register_next_step_handler(msg, drinks_place_message)

    def drinks_place_message(message):
        # Quick way to obtain longitude and latitude of address using geopy
        try:
            geolocation = coordinates(message.text)

            # Reply message with recs
            bot.reply_to(message, message_output_place(drink_place_details(geolocation)))

        # If google API cannot return a result
        except:
            bot.reply_to(message, "Please make a valid request")

    # Randomly suggest 5 places when user keys in /random command
        
    ######################
    # Function definitions
    #####################

    # Extracts coordinates from message input
    def coordinates(message):
            location = geolocator.geocode(f"{message}")
            return f"{location.latitude}, {location.longitude}"

    # Extracts food place details
    def food_place_details(location):
        places_results = gmaps.places_nearby(location = location, radius = 2400, open_now = True, type = ["cafe", "food", "restaurant"])["results"]

        # We can extract name, rating, user_ratings_total, price_level, and vicinity from above using list comprehension
        # Rating and user_ratings_total may be missing in some dicts, and we prefill these with 0
        place_details = [{"name": item["name"], 
                        "rating": item["rating"] if item.get("rating") else 0, 
                        "rating_count": item["user_ratings_total"] if item.get("user_ratings_total") else 0, 
                        "price_level": item["price_level"] if item.get("price_level") else 0,
                        "vicinity": item["vicinity"]} 
                        for item in places_results]

        place_details = [item for item in place_details if item["rating"] >= 4]

        # Randomly returns 5 results
        return random.sample(place_details, 5)

    # Extracts drinks place details
    def drink_place_details(location):
        places_results = gmaps.places_nearby(location = location, radius = 2400, open_now = True, type = ["bar"])["results"]

        # We can extract name, rating, user_ratings_total, price_level, and vicinity from above using list comprehension
        # Rating and user_ratings_total may be missing in some dicts, and we prefill these with 0
        place_details = [{"name": item["name"], 
                        "rating": item["rating"] if item.get("rating") else 0,
                        "rating_count": item["user_ratings_total"] if item.get("user_ratings_total") else 0,
                        "price_level": item["price_level"] if item.get("price_level") else 0, 
                        "vicinity": item["vicinity"]} 
                        for item in places_results]

        place_details = [item for item in place_details if item["rating"] >= 4 if item["price_level"] != 0]

        return place_details

    # Converts place details from list to string
    def message_output_place(place):
        output = []
        for detail in place:
            name = detail["name"]
            rating = detail["rating"]
            rating_count = detail["rating_count"]
            price_level = detail["price_level"]
            output.append(f"Name: {name} | Rating: {rating} | Rating Count: {rating_count} | Price Level: {price_level}")
        
        # Returns joined items from the list, in the form of a string
        return "\n\n".join(output)

    # Start the bot
    bot.polling()

main()

# Save visited places in a DB

# Can pull out favorites places from DB

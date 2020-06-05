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

    # Randomly suggest 5 places when user keys in /random command. Search starts from central (i.e. AMK) area
    @bot.message_handler(commands=["randomfood"])
    def randomfood_place_message(message):
        try:
            random_area = "1.369551, 103.848493"

            # Reply message with recs
            bot.reply_to(message, message_output_place(random_food_place_details(random_area)))

        # If google API cannot return a result
        except:
            bot.reply_to(message, "Please make a valid request")

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
        # Exclude those with missing keys
        # Using random.sample to randomly pick up 5 from list
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

    def random_food_place_details(location):
        places_results = gmaps.places_nearby(location = location, radius = 12000, open_now = True, type = ["cafe", "food", "restaurant"])["results"]

        # We can extract name, rating, user_ratings_total, price_level, and vicinity from above using list comprehension
        # Exclude those with missing keys
        # Using random.sample to randomly pick up 5 from list
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

    # Extracts drinks place details
    def drink_place_details(location):
        places_results = gmaps.places_nearby(location = location, radius = 2400, open_now = True, type = ["bar"])["results"]

        # We can extract name, rating, user_ratings_total, price_level, and vicinity from above using list comprehension
        # Exclude those with missing keys
        place_details = [{"name": item["name"], 
                        "rating": item["rating"], 
                        "rating_count": item["user_ratings_total"],
                        "price_level": item["price_level"],
                        "vicinity": item["vicinity"]} 
                        for item in places_results
                        if item.get("rating") != None
                        if item.get("user_ratings_total") != None
                        if item.get("price_level") != None
                        if item["rating"] >= 4]

        return place_details

    # Converts place details from list to string
    def message_output_place(place):
        output = []
        for detail in place:
            name = detail["name"]
            rating = detail["rating"]
            rating_count = detail["rating_count"]
            price_level = detail["price_level"]
            vicinity = detail["vicinity"]
            output.append(f"Name: {name} | Rating: {rating} | Rating Count: {rating_count} | Price Level: {price_level} | Vicinity: {vicinity}")
        
        # Returns joined items from the list, in the form of a string
        return "\n\n".join(output)

    # Start the bot
    bot.polling()

main()

# Save visited places in a DB

# Can pull out favorites places from DB

import sys
from datetime import datetime
import telebot
import logging
import googlemaps
from geopy.geocoders import Nominatim
import pprint

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
        bot.reply_to(message, "Recommends food places for lazy and hungry souls :)")

    # @bot.message_handler(commands="where")
    # def send_instructions(message):
    #     instruct = bot.send_message(message, "Let me know where you are")
    #     reply = message.text
    #     print(reply)

    # Activate the geolocator only with /where command so we don't spam the google API
    # Get bot to return an error if google api returns error

    @bot.message_handler(func=lambda message: True)
    def place_message(message):
        message_text = message.text

        # Quick way to obtain longitude and latitude of address using geopy
        location = geolocator.geocode(f"{message_text}")
        coordinates = f"{location.latitude}, {location.longitude}"

        bot.reply_to(message, message_output_place(place_details(coordinates)))
        
    ######################
    # Function definitions
    ######################

    #Extracts place details
    def place_details(location):
        places_results = gmaps.places_nearby(location = location, radius = 2400, open_now = True, type = ["cafe", "food", "restaurant"])["results"]

        # We can extract name, rating, user_ratings_total, price_level, and vicinity from above using list comprehension
        # Rating and user_ratings_total may be missing in some dicts, and we prefill these with 0
        place_details = [{"name": item["name"], 
                        "rating": item["rating"] if item.get("rating") else 0, 
                        "rating_count": item["user_ratings_total"] if item.get("user_ratings_total") else 0, 
                        "vicinity": item["vicinity"]} 
                        for item in places_results]

        place_details = [item for item in place_details if item["rating"] >= 4]

        return place_details

    # Converts place details from list to string
    def message_output_place(place):
        output = []
        for detail in place:
            name = detail["name"]
            rating = detail["rating"]
            rating_count = detail["rating_count"]
            output.append(f"Name: {name} | Rating: {rating} | Rating Count: {rating_count}")
        
        # Create a list first then use .join
        return "\n".join(output)

    # Start the bot
    bot.polling()

main()

# Save visited places in a DB

# Can pull out favorites places from DB

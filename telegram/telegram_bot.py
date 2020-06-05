import sys
from datetime import datetime
import telebot
import logging
import googlemaps
from geopy.geocoders import Nominatim
import pprint
import random
from tmdbv3api import TMDb, Movie

# Argument check
if len(sys.argv) != 4:
    print("Please parse exactly 4 arguments")
    sys.exit(1)

# Import your API keys here
g_api_key = sys.argv[1]
t_token = sys.argv[2]
tmdb_api_key = sys.argv[3]

# Define gmaps Client
gmaps = googlemaps.Client(key = g_api_key)
geolocator = Nominatim(user_agent=g_api_key)

# Define tmdb Client
tmdb = TMDb()
tmdb.api_key = tmdb_api_key

# Configuration settings
tmdb.language = 'en'
tmdb.debug = True

# Telegram codes
# Start telebot
bot = telebot.TeleBot(t_token)

def main():
    # Add event handler that returns start() function when user inputs /start or /help in chat
    @bot.message_handler(commands=["start", "help"])
    def send_welcome(message):
        bot.reply_to(message, """Recommends movies, food/drink places for lazy and hungry souls :) 
        Type /foodnearby to find food recs near your entered location
        Type /drinksnearby to find pub recs near your entered location
        Type /randomfood to find food recs randomly
        Type /trendingmovies to find trending movie recs""")

    # Activates the geolocator only with /foodnearby or /drinksnearby command so we don't spam the google API
    @bot.message_handler(commands=["foodnearby"])
    def food(message):
        msg = bot.reply_to(message, "Let me know where you are!")

        # parse next input message to func place_message
        bot.register_next_step_handler(msg, food_place_message)

    def food_place_message(message):
        # Quick way to obtain longitude and latitude of address using geopy
        try:
            search_area = coordinates(message.text)
            search_radius = 2400
            search_type = ["cafe", "food", "restaurant"]

            # Reply message with recs
            bot.reply_to(message, message_output_place(place_details(search_area, search_radius, search_type)))

        # If google API cannot return a result
        except:
            bot.reply_to(message, "Please make a valid request.")

    
    @bot.message_handler(commands=["drinksnearby"])
    def drinks(message):
        msg = bot.reply_to(message, "Let me know where you are!")

        # parse next input message to func place_message
        bot.register_next_step_handler(msg, drinks_place_message)

    def drinks_place_message(message):
        # Quick way to obtain longitude and latitude of address using geopy
        try:
            search_area = coordinates(message.text)
            search_radius = 2400
            search_type = ["bar"]

            # Reply message with recs
            bot.reply_to(message, message_output_place(place_details(search_area, search_radius, search_type)))

        # If google API cannot return a result
        except:
            bot.reply_to(message, "Please make a valid request.")

    # Randomly suggests 5 places when user keys in /random command. Search starts from central (i.e. AMK) area
    @bot.message_handler(commands=["randomfood"])
    def randomfood_place_message(message):
        try:
            search_area = "1.369551, 103.848493"
            search_radius = 120000
            search_type = ["cafe", "food", "restaurant"]

            # Reply message with recs
            bot.reply_to(message, message_output_place(place_details(search_area, search_radius, search_type)))

        # If google API cannot return a result
        except:
            bot.reply_to(message, "Please make a valid request.")

    # Randomly suggests top trending movies
    @bot.message_handler(commands=["trendingmovies"])
    def movie_message(message):
        try:
            movie = Movie()
            popular = movie.popular()

            # Reply message with recs
            bot.reply_to(message, message_output_shows(show_details(popular)))
        
        except:
            bot.reply_to(message, "Service is down. Please try again later.")

    ######################
    # Function definitions
    #####################

    # Extracts coordinates from message input
    def coordinates(message):
            location = geolocator.geocode(f"{message}")
            return f"{location.latitude}, {location.longitude}"

    # Extracts food place details
    def place_details(geoarea, radiusspread, category):
        places_results = gmaps.places_nearby(location = geoarea, radius = radiusspread, open_now = True, type = category)["results"]

        # We can extract name, rating, user_ratings_total, price_level, and vicinity from above using list comprehension
        # Excludes those with missing keys
        # Using random.sample to randomly pick up 5 from list
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

        return random.sample(place_details, min(len(place_details), 5))

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


    # Extracts show details
    def show_details(shows):
        top_shows = [{"title": s.title,
            "year": s.release_date,
            "popularity": s.popularity,
            "rating": s.vote_average,
            "summary": s.overview}
            for s in shows
            if s.vote_average >= 6.2]
        
        return random.sample(top_shows, 5)

    # Converts show details from list to string
    def message_output_shows(shows):
        output = []
        for show in shows:
            title = show["title"]
            year = show["year"]
            popularity = show["popularity"]
            rating = show["rating"]
            summary = show["summary"]
            output.append(f"Title: {title} | Year: {year} | Popularity: {popularity} | Rating: {rating} | Summary: {summary}")
        
        # Returns joined items from the list, in the form of a string
        return "\n\n".join(output)

    # Start the bot
    bot.polling()

main()

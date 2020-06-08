**Overview**

This source code runs a Telegram bot that can:
1. Generate top food recommendations based on user's input location
2. Suggest trending movies and shows

**Use of APIs**

Google Places API [https://cloud.google.com/maps-platform/places/] is called whenever a user feeds her input location to the bot. The standardised radius setting for nearby locations is assumed and set as 2.4km wide while the random food command uses a radius of 12km wide, starting from Singapore's central location.

TMDB API [https://themoviedb.org] is used to randomly generate 5 movies from the current trending list in TMDB database.

Finally, the information fetched from user input and the APIs above is handled by the Telegram bot via pyTelegramBotAPI [https://github.com/eternnoir/pyTelegramBotAPI.git].

**How to**

Register for APIs and tokens from the links above. Once done, parse these when running virtual_env.sh to start the bot!

**Future implementations**

1. To minimise cost of Gmaps API, locations (using postal codes) should be stored in a database first so the call to API is minimised
- Districts can be inferred from postal codes so we expect user's input to be a district
- Input is then translated to postal code and then DB is queried
- Look at [https://en.wikipedia.org/wiki/Postal_codes_in_Singapore] for more details

2. Can pull out a user's favorite places from a database.

3. Telegram has no way to save state for user; a database has to be built for saving commands from users for stringing of different message handlers together.

4. Add chat bot functionality.
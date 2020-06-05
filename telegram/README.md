Telegram bot that suggests food or drink places based on user input.
Note that Telegram has no way to save state for user; a database has to be built for saving commands of user

More functionalities to add:
1. Randomly suggest 5 recs (not nearby)
2. Movies

Future implementations:
1. To reduce cost of Gmaps API, to store locations in DB first using postal codes
- Districts can be inferred from postal codes so we expect user's input to be a district
- Input is then translated to postal code and then DB is queried
- Look at https://en.wikipedia.org/wiki/Postal_codes_in_Singapore for more details

2. Add chat bot functionality
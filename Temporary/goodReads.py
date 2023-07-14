import requests

# Make a GET request to the Zen Quotes API
response = requests.get("https://zenquotes.io/api/random")

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Extract the quote from the response
    data = response.json()[0]
    quote = data["q"]
    author = data["a"]

    # Print the quote and author
    print(f"{quote} - {author}")
else:
    # Print an error message if the request was not successful
    print("Error retrieving the quote. Please try again.")

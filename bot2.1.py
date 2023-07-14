import re, difflib, os, requests, textwrap, firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from PIL import Image, ImageDraw, ImageFont
from instagrapi import Client
from pathlib import Path
import config

if not os.path.isfile('instagramFirebase.json'):
    print("Error: 'instagramFirebase.json' file not found.")
    exit()
else:
    #Giving the access rights to update the database
    cred = credentials.Certificate('instagramFirebase.json')
    firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://instagram-bo-default-rtdb.firebaseio.com/'})
    db_ref = db.reference('/')


#In order to replace the special character
def replaceSpecialChars(string):
    # Define the pattern to match special characters
    pattern = r'[^\w\s-]'
    # Replace special characters with underscores
    replaced_string = re.sub(pattern, '_', string)
    return replaced_string

def generate_quote():
     
    response = requests.get("https://zenquotes.io/api/random")

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extract the quote from the response
        data = response.json()[0]
        quote = data["q"]
        author = data["a"]
        return [author, quote]
    else:
        # Print an error message if the request was not successful
        print("Error retrieving the quote. Please try again.")
        exit()

#Create Instagram Post
def create_instagram_post(quote, author, image_path, output_path):
    
    author = ' - ' + author
    # Open the image
    image = Image.open(image_path)
    image = image.resize((800, 800))

    # Define the font sizes and styles
    quote_font_size = 40
    author_font_size = 30
    font = ImageFont.truetype('./Fonts/TheHeartOfEverythingDemo.ttf', quote_font_size)

    # Create a drawing object
    draw = ImageDraw.Draw(image)
    
    # Wrap this text.
    # quote_lines = textwrap.wrap(quote, width=max_quote_width)
    wrapper = textwrap.TextWrapper(width=30)
    quote_lines = wrapper.wrap(text=quote)
    
    # Calculate the total height required for the quote text
    line_spacing = 10 
    quote_text_bbox = draw.textbbox((0, 0), quote, font=font)
    quote_text_width = quote_text_bbox[2] - quote_text_bbox[0]
    quote_text_height = quote_text_bbox[3] - quote_text_bbox[1]
    line_height = quote_text_height + line_spacing
    quote_height = len(quote_lines) * line_height
    
    # Calculate the starting y-coordinate for the quote text
    quote_start_y = (image.height - quote_height) // 2

    # Draw the quote text on the image
    for line in quote_lines:
        line_bbox = draw.textbbox((0, 0), line, font=font)
        line_width = line_bbox[2] - line_bbox[0]
        line_height = line_bbox[3] - line_bbox[1]
        line_x = (image.width - line_width + 20) // 2  # Centered horizontally
        draw.text((line_x, quote_start_y), line, fill='black', font=font, align='center')
        quote_start_y += line_height + line_spacing

    # Define the author font size and style
    author_font = ImageFont.truetype('./Fonts/Roboto-Light.ttf', author_font_size)  

    # Calculate the position to place the author text
    author_bbox = draw.textbbox((0, 0), author, font=author_font)
    author_text_width = author_bbox[2] - author_bbox[0]
    author_text_height = author_bbox[3] - author_bbox[1]
    author_x = (image.width - author_text_width) // 2  # Centered horizontally
    author_y = image.height - 280  # Positioned below the last line of the quote

    # Draw the author text on the image
    draw.text((author_x, author_y), author, fill='black', font=author_font, align='center')
    # Save the modified image
    image.save(output_path)
    # image.show()
    print("Hello inside instagram")
    
    #To upload photo in instagram
    insta = Client()
    insta.login(config.username, config.password)
    
    imagePath = Path(output_path)

    media = insta.photo_upload(
        path = imagePath,
        caption = ""
    )
    print("Hello instagram at the last")

def pushDataInTheFirebase():
    try:
        author = ""
        authorWithoutSpecialCharacter = ""
        quote = "" 
        count = 0  
        flag = 1
        while(flag == 1 and count < 5):
            flag = 0
            quoteAndAuthor = generate_quote()
            author = quoteAndAuthor[0] if quoteAndAuthor[0] else "Anonymous"
            authorWithoutSpecialCharacter = replaceSpecialChars(author)
            quote = quoteAndAuthor[1]
            if(len(quote) > 130):
                flag = 1
                continue
            quotesFromFirebaseRef = db_ref.child("Quotes").child(authorWithoutSpecialCharacter)
            quotesFromFirebaseRefData = quotesFromFirebaseRef.get()
            if(quotesFromFirebaseRefData!=None and 
            len(quotesFromFirebaseRefData.items()) > 0):
                for key, ele in quotesFromFirebaseRefData.items():
                    similarity_ratio = difflib.SequenceMatcher(None, ele, quote).ratio()
                    if(similarity_ratio > 0.7):
                        print("Quotes" , quote, authorWithoutSpecialCharacter)
                        count = count + 1
                        flag = 1
                        break
            # return
        if(flag == 0):    
            print(quote)        
            db_ref.child("Quotes").child(authorWithoutSpecialCharacter).push(quote) 
            numberOfImages = len(db_ref.child("Quotes").child(authorWithoutSpecialCharacter).get().items()) 
            modifiedImage = authorWithoutSpecialCharacter + str(numberOfImages)
            image_path = "./TemplatesImage/Input/Image2.jpg" 
            output_path = f'./TemplatesImage/Output/{modifiedImage}.jpg'    
            create_instagram_post(quote, author, image_path, output_path)
            print("Done succeessfully")
    except Exception as e:
        print("Error: An unexpected exception occurred:", str(e))
               
pushDataInTheFirebase()


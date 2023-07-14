from PIL import Image, ImageDraw, ImageFont
import textwrap




# Example usage
quote = "Believe you can and you're halfway there"
author = "Theodre Roosevelt"
image_path = "./TemplatesImage/Input/Image2.jpg" 
output_path = './TemplatesImage/Output/modified_image.jpg'

create_instagram_post(quote, author, image_path, output_path)

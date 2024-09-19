import random
import string
from PIL import Image, ImageDraw, ImageFont, ImageFilter

#function to generate random CAPTCHA 
def generate_captcha_text(length=6):
    letters=string.ascii_uppercase + string.digits
    captcha_text= ''.join(random.choice(letters) for _ in range(length))
    return captcha_text

#create gradient background

def create_gradient_background(width, height, start_color, end_color):
    base=Image.new('RGB', (width, height), start_color)
    top= Image.new('RGB', (width, height), end_color)
    mask=Image.new('L', (width, height))

    for y in range(height):
        for x in range(width):
            mask.putpixel((x, y), int(255 * (y / height)))
    base.paste(top, (0, 0), mask)
    return base

#create captcha image

def generate_captcha_image(captcha_text):

    #image size
    width, height=300,200

#create gradient background
    Image=create_gradient_background(width, height, (245,245, 255), (255, 255, 245))
    
    #initialize font and drawing context
    draw=ImageDraw.Draw(Image)
    try:
        font=ImageFont.truetype("arial.ttf", 48)
    except IOError:
        font=ImageFont.load_default()
    #get the size of the text using textbox
    text_bbox=draw.textbbox((0, 0), captcha_text, font=font)
    text_width=text_bbox[2]-text_bbox[0]
    text_height=text_bbox[3]-text_bbox[1]

    #calculate the position to center the text   
    text_x=(width-text_width)//2
    text_y=(height-text_height)//2

    # Add soft shadow for the text
    shadow_offset=2
    draw.text((text_x + shadow_offset, text_y + shadow_offset), captcha_text, font=font, fill=(180,180,180))

    #Draw the main text
    draw.text((text_x, text_y), captcha_text, font=font, fill=(0, 0, 0))

    # add geometric noise (lines, circles)
    for _ in range(5):
        x1, y1=random.randint(0, width), random.randint(0, height)
        x2, y2=random.randint(0, width), random.randint(0,height)
        draw.line(((x1, y1), (x2, y2)), fill=(120, 120, 120), width=2)
    for _ in range(10):
        x, y=random.randint(0, width), random.randint(0, height)
        r=random.randint(10, 20)
        draw.ellipse((x-r, y-r, x+r, y+r), outline=(150, 150, 150))
    
    # apply slight blur to make it look more realistic
    Image=Image.filter(ImageFilter.GaussianBlur(0.5))
    return Image

# generate CAPTCHA text and image
captcha_text=generate_captcha_text()
captcha_image=generate_captcha_image(captcha_text)

# dispaly the CAPTCHA image

captcha_image.show()
print("CAPTCHA text: " + captcha_text)
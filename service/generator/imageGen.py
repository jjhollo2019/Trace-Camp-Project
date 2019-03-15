import os
import random
import time
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

class ImageGenerator:
    
    def recommend_font_size(self, text):
        size = 45
        l = len(text)

        resize_heuristic = 0.9
        resize_actual = 0.985
        while l > 1:
            l = l * resize_heuristic
            size = size * resize_actual

        return int(size)


    def select_background_image(self):
        prefix = "service/generator/input/"
        options = os.listdir(prefix)
        return prefix + random.choice(options)


    def select_font(self):
        prefix = "service/generator/fonts/"
        options = os.listdir(prefix)
        return prefix + random.choice(options)


    def wrap_text(self, text, w=30):
        new_text = ""
        new_sentence = ""
        for word in text.split(" "):
            delim = " " if new_sentence != "" else ""
            new_sentence = new_sentence + delim + word
            if len(new_sentence) > w:
                new_text += "\n" + new_sentence
                new_sentence = ""
        new_text += "\n" + new_sentence
        return new_text


    def write_image(self, text, output_filename, background_img):
        # setup
        text = self.wrap_text(text)
        img = Image.new("RGBA", (self.IMAGE_WIDTH, self.IMAGE_HEIGHT), (255, 255, 255))

        # background
        back = Image.open(background_img, 'r')
        img_w, img_h = back.size
        bg_w, bg_h = img.size
        offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
        img.paste(back, offset)

        # text
        font = ImageFont.truetype(self.FONT, self.FONT_SIZE)
        draw = ImageDraw.Draw(img)
        img_w, img_h = img.size
        x = img_w / 2
        y = img_h / 2
        textsize = draw.multiline_textsize(text, font=self.IF, spacing=self.SPACING)
        text_w, text_h = textsize
        x -= text_w / 2
        y -= text_h / 2
        draw.multiline_text(align="center", xy=(x, y), text=text, fill=self.COLOR, font=font, spacing=self.SPACING)
        draw = ImageDraw.Draw(img)

        # output
        img.save("static/" + output_filename)
        return output_filename

    def generateImage(self, text):
        output_filename = "/output/{}.png".format(int(time.time()))

        self.FONT = self.select_font()
        self.FONT_SIZE = self.recommend_font_size(text)
        self.IF = ImageFont.truetype(self.FONT, self.FONT_SIZE)
        self.IMAGE_WIDTH = 800
        self.IMAGE_HEIGHT = 600
        self.COLOR = (255, 255, 255)
        self.SPACING = 3

        return self.write_image(text, output_filename, background_img=self.select_background_image())
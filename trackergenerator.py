# Tashiv Sewpersad
# Python 3

#############
## Imports ##
#############

import random
import math
from PIL import ImageFont
from PIL import ImageDraw
from PIL import Image
from PIL import ImageOps

####################
## Helper Methods ##
####################

def addTexture(buffer, width, height, border, mode, scale):
	# config
	rec_count = 8000;
	rec_width_max = (int) (50 * scale)
	rec_height_max = (int) (50 * scale)
	rec_width_min = (int) (5 * scale)
	rec_height_min = (int) (5 * scale)
	rec_color = (1, 1, 1)
	# make rectangle texture
	for i in range(0, rec_count):
		# generate dimensions
		rec_x = random.randint(border, width-rec_width_max-border)
		rec_y = random.randint(border, height-rec_height_max-border)
		rec_width = rec_x + random.randint(rec_width_min, rec_width_max)
		rec_height = rec_y + random.randint(rec_height_min, rec_height_max)
		# generate fill pattern
		if mode == 1: #case: circular
			# config
			noise = 0.40
			size = 120 * scale
			# set color
			jitter = round(noise * size)
			value = math.pow(math.pow(rec_x - width / 2, 2) + math.pow(rec_y - height/2, 2), 0.5)
			if (value + random.randint(0,jitter))  % (size) > (size * 0.5):
				rec_fill = 255
			else:
				rec_fill = 0
		elif mode == 2: #case: dots
			# config
			noise = 0.55
			size = 150 * scale
			# set color
			jitter = round(noise * size)
			if (((rec_x + random.randint(0,jitter)) % size > size * 0.2)
			and ((rec_x + random.randint(0,jitter)) % size < size * 0.8)
			and ((rec_y + random.randint(0,jitter)) % size > size * 0.2)
			and ((rec_y + random.randint(0,jitter)) % size < size * 0.8)):
				rec_fill = 255
			else:
				rec_fill = 0
		elif mode == 3: #case: stripes
			# config
			noise = 0.30
			size = 200 * scale
			# set color
			jitter = round(noise * size)
			value = (rec_x + random.randint(0,jitter)) + (rec_y + random.randint(0,jitter))
			if value % (size) > (size * 0.5):
				rec_fill = 255
			else:
				rec_fill = 0
		else: #case: random
			if random.random() > 0.5:
				rec_fill = 0
			else:
				rec_fill = 255
		# transparency
		if rec_fill == 255:
			rec_transparency = random.randint(200, 230)
		else:
			rec_transparency = random.randint(180, 200)
		# draw
		buffer.rectangle([rec_x, rec_y,rec_width, rec_height],
						outline=rec_fill,
						fill=(round(rec_color[0]*rec_fill), round(rec_color[1]*rec_fill), round(rec_color[2]*rec_fill), rec_transparency))

def addText(buffer, width, height, border, text_value, scale):
	# initialize
	fnt = ImageFont.truetype('Font/beon.otf', (int) (150 * scale * 0.5))
	# determine text size
	txt_w, txt_h = buffer.textsize(text_value, font=fnt)
	txt_x = (width-txt_w+border)/2
	txt_y = (height-txt_h)/2
	text_pad = 10
	# draw background
	buffer.rectangle([txt_x-text_pad, txt_y-text_pad, txt_x + txt_w + text_pad, txt_y + txt_h + text_pad],
						fill=(255, 255, 255, 255))
	buffer.rectangle([txt_x, txt_y, txt_x + txt_w, txt_y + txt_h],
						fill=(0, 0, 0, 255))
	# write text
	buffer.text(((width-txt_w+border)/2,(height-txt_h)/2), 
				text_value, 
				font=fnt,
				fill=(255, 255, 255, 255))

def addBorder(buffer, width, height, border, thickness):
	# initialize
	frame_thickness = 0
	frame_color = 0
	# create border
	while (frame_thickness < border):
		# draw frame
		buffer.rectangle([frame_thickness, frame_thickness, width-frame_thickness, height-frame_thickness],
						outline=(frame_color, frame_color, frame_color, 255),
						fill=(frame_color, frame_color, frame_color, 255))
		# progress frame draw
		frame_thickness += thickness
		if frame_color == 255:
			frame_color = 0
		else:
			frame_color = 255
	
###############################
## Tracker Generator Methods ##
###############################

def generateImageTracker(width, height, border, frame, texture_mode, text, name, scale):
	# log
	print(" - generating tracker " + name + "...", end="")
	# initialize
	image = Image.new('RGB', (width, height))
	buffer = ImageDraw.Draw(image, 'RGBA')
	# generate border
	addBorder(buffer, width, height, border, frame)
	# generate texture
	addTexture(buffer, width, height, border, texture_mode, scale)
	# generate text
	addText(buffer, width, height, border, text, scale)
	# save image
	image.save("Output/" + name + ".png")
	# done
	print("(done)")
	return name + ".png"
	
#########################
## Program Entry Point ##
#########################

def main():

	# format
	# generateImageTracker(width, height, border, frame, texture_mode, text, name, scale)
	
	# generate
	generateImageTracker(750, 1000, 50, 20, 1, "Test A", "tracker-A", 1)
	generateImageTracker(750, 1000, 50, 20, 2, "Test B", "tracker-B", 1)
	generateImageTracker(750, 1000, 50, 20, 3, "Test C", "tracker-C", 1)
	generateImageTracker(750, 1000, 50, 20, 4, "Test D", "tracker-D", 1)

if __name__ == "__main__":
	# header
	print("[Tracker Generator - Tashiv Sewpersad]")
	# initialize
	random.seed(42)
	# generate
	main()
	# done
	print("[EXITED]")
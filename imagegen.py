from __future__ import print_function
import os
import random
import time
from PIL import Image, ImageDraw, ImageEnhance, ImageChops
from floodfill import aggressive_floodfill
import time

# Initiating variables:
iterations = 0

# Folder-location of components:
outer_folder = "Doggoparts/"
face_base_folder = outer_folder + "Face/"
face_feature_folder = outer_folder + "Face_Features/"
texture_folder = outer_folder + "Textures/"
background_color_folder = outer_folder + "Background_Colors/"

# Where the finished image should be saved.
output_folder = "Outputs/"
output_file_name = output_folder + "face.png"


# This is where the magic happens:
def main():
    # Determining the size of finished image:
    width, height = open_image_file(random_file_from_dir(texture_folder)).size
    make_face()

    # To generate only one image:
    # make_face()

    # For a continuous face-generation:
    # make_face_continuous()

    # To generate several faces:
    # make_face_continuous(<filename>)


def make_face_continuous(file_name = output_file_name):
    # Printing how many possible combinations there are, cuz its fun:
    print ("There are " + int_presentation(how_many_combinations_are_there()) + " possible combinations")
    print (" ")
    print ("Now let's make some doggos!")
    print (" ")
    global iterations
    global output_file_name
    if (output_file_name is not file_name):
        while True:
            output_file_name = output_folder + file_name + str(iterations) + ".png"
            start = time.time()
            make_face()
            iterations += 1
            end = time.time()
            print("time to complete image: " + str(end - start))
            print(" ")
            time.sleep(5)


    else:
        while True:
            start = time.time()
            make_face()
            end = time.time()
            print("time to complete image: " + str(end - start))
            print(" ")


def int_presentation(int):
    i = -3
    j = None
    original_int = int
    int_string = ""
    while -i <= len(str(int))+3:
        sub_string = str(original_int)[i:j]
        if (len(sub_string) == 3):
            sub_string = " " + sub_string
        int_string = sub_string + int_string
        j = i
        i -= 3
    return (int_string)

def how_many_combinations_are_there():
    possible_combinations = 0
    files = 0
    # number of textures:
    for file in os.listdir(texture_folder):
        possible_combinations += 1

    # number of different face-shapes
    for folder in os.listdir(face_feature_folder):
        folder = folder + "/"
        for file in os.listdir(face_feature_folder+folder):
            files += 1
        possible_combinations = possible_combinations * files
        files = 0
    return (possible_combinations)

def insert_layer_to_image(imagefile, image):
    layer = open_image_file(imagefile)
    image.paste(layer, (0, 0), layer)
    return

def random_file_from_dir(dir):
    return (dir + random.choice(os.listdir(dir)))

def open_image_file(imagefile):
    return (Image.open(imagefile))

def insert_random_imagelayer_to_image(dir, image):
    insert_layer_to_image(random_file_from_dir(dir), image)

def fill(layer):
    return 'fill' in layer

def mask(layer):
    return 'mask' in layer

def get_corner_color(image):
    return (image.getpixel((0, 0)))

def make_face():
    width, height = open_image_file(random_file_from_dir(texture_folder)).size
    face_shape = Image.new('RGBA', (width, height), color = (255, 255, 255, 0) )
    face_base =  Image.new('RGBA', (width, height), color = (255, 255, 255, 0) )
    face =  Image.new('RGBA', (width, height), color = (255, 255, 255, 0) )
    texture = Image.new('RGBA', (width, height), color = (255, 255, 255, 255) )
    background_mask = Image.new('RGBA', (width, height), color = (255, 255, 255, 0))
    face_mask = Image.new('RGBA', (width, height), color = (255, 255, 255, 0))

    # Selecting texture
    insert_random_imagelayer_to_image(texture_folder, texture)


    # Selecting the face-shape and ears
    for folder in os.listdir(face_base_folder):
        folder = folder + '/'
        if 'Faceshapes' in folder:
            faceshape = random_file_from_dir(face_base_folder + folder)
            insert_layer_to_image( faceshape , face_shape )
            insert_layer_to_image( faceshape , face_base )
            continue
        imagelocation = face_base_folder + folder
        insert_random_imagelayer_to_image( imagelocation, face_base )

    # Creating a mask for the background
    face_base_data = face_base.getdata()
    background_data = []
    for pixel in face_base_data:
        if pixel[3] > 100:
            background_data.append((255, 255, 255, 0))
        else:
            background_data.append((255, 255, 255, 255))
    background_mask.putdata(background_data)


    # Creating a mask for the face
    face_shape_data = face_shape.getdata()
    face_data = []
    for pixel in face_shape_data:
        if pixel[3] < 10:
            face_data.append((255, 255, 255, 0))
        else:
            face_data.append((255, 255, 255, 255))
    face_mask.putdata(face_data)

    # Combining the faceshape, texture and background color
    face = ImageChops.multiply(face_base, texture)
    background = ImageChops.multiply(open_image_file(random_file_from_dir(background_color_folder)), background_mask)
    face.paste(background, (0,0), background)


    # Adding faceparts to the face
    for folder in os.listdir(face_feature_folder):
        folder = folder + '/'
        if ('fill' not in folder and 'mask' not in folder):
            imagelocation = face_feature_folder + folder
            insert_random_imagelayer_to_image( imagelocation, face )
        elif ('fill' in folder):
            file_to_fill = random_file_from_dir(face_feature_folder + folder)
            insert_layer_to_image( file_to_fill , face )
            if fill(file_to_fill):
                face = face.convert('RGB')
                aggressive_floodfill(face, xy=(width*0.5, height*0.7), value=get_corner_color(texture))
        else:
            use_mask = open_image_file(random_file_from_dir(face_feature_folder + folder))
            if (mask(use_mask)):
                use_mask = ImageChops.multiply(face_mask, use_mask)    
            face.paste(use_mask, (0,0), use_mask)
    face.save(output_file_name)



if __name__ == '__main__':
    main()

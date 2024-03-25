import os
import pygame

BASE_IMG_PATH = 'data/images/'

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert() # converts the internal representation of images in pygame
    img.set_colorkey((0,0,0)) # make the background color transparent
    return img

def load_images(path):
    images = []
    for img_name in os.listdir(BASE_IMG_PATH + path): # os.listdir gives all the files in a directory
        images.append(load_image(path + '/' + img_name))

    return images

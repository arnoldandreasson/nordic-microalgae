#!/usr/bin/python3
# -*- coding:utf-8 -*-
#
# Project: Nordicmicroalgae. http://nordicmicroalgae.org/
# Copyright (c) 2011-2017 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import nordicmicroalgae_settings as settings

import pathlib # Python >= 3.4
from PIL import Image # Pillow >= 4.0

def execute(uploaded_files = settings.MEDIA_PATH_TO_UPLOADED_FILES, 
            original_files = settings.MEDIA_PATH_TO_ORIGINAL_FILES, 
            standard_files = settings.MEDIA_PATH_TO_STANDARD_FILES, 
            thumbnails_files = settings.MEDIA_PATH_TO_THUMBNAIL_FILES, 
            exclude_media_list = settings.MEDIA_PATH_TO_EXCLUDE_LIST, 
            standard_image_size = settings.MEDIA_STANDARD_IMAGE_SIZE,
            thumbnail_size = settings.MEDIA_THUMBNAIL_SIZE):
    """ """
    
    # Create out directories if needed.
    if not pathlib.Path(original_files).exists():
        pathlib.Path(original_files).mkdir(parents=True)
    if not pathlib.Path(standard_files).exists():
        pathlib.Path(standard_files).mkdir(parents=True)
    if not pathlib.Path(thumbnails_files).exists():
        pathlib.Path(thumbnails_files).mkdir(parents=True)
        
    # Get list of already converted files.
    converted_image_list = []
    for image_file in pathlib.Path(original_files).glob('*.*'):
        converted_image_list.append(image_file.stem)
        
    # Load exclude media list.
    excluded_media_rows = ['excluded_media'] # File header.
    if pathlib.Path(exclude_media_list).exists():
        with pathlib.Path(exclude_media_list).open('r') as  excluded_media:
            excluded_media_rows = [x.strip() for x in excluded_media.readlines()]
    else: 
        with pathlib.Path(exclude_media_list).open('w') as  excluded_media:
            excluded_media.write('excluded_media') # File header.
    
    # Convert from uploaded files to original sized  images with no metadata.
    counter = 1
    for file in pathlib.Path(uploaded_files).glob('*.*'):
        if file.stem not in converted_image_list: 
            if file.stem not in excluded_media_rows: 
                try:
                    print('Create original size: ' +  str(counter) + '   ' + file.name)
                    print('Size: ' + str(file.stat().st_size))
                    
                    # Append current image name if conversion fails.
                    with pathlib.Path(exclude_media_list).open('a') as  excluded_media:
                        excluded_media.write('\n' + file.stem)
                    
                    create_clean_jpg_image(uploaded_files, file.name, 
                                           original_files, file.name)
                    
                    # Write back the old list since the conversion did not fail.
                    with pathlib.Path(exclude_media_list).open('w') as  excluded_media:
                        excluded_media.write('\n'.join(excluded_media_rows))
                    
                    counter += 1
                except Exception as e:
                    print('Failed to create clean image: ' + file.name + 
                          '\n' + str(e))
    
    # Get list of already converted files.
    converted_image_list = []
    for image_file in pathlib.Path(standard_files).glob('*.*'):
        converted_image_list.append(image_file.stem)
    
    # Convert to large and small (thumbnail) sizes used in nordicmicroalgae.org.
    for file in pathlib.Path(original_files).glob('*.*'):
        if file.stem not in converted_image_list: 
            try:
                create_resized_image(original_files, file.name, 
                                     standard_files, file.name,
                                     standard_image_size)
            except Exception as e:
                print('Failed to create standard size: ' + file.name + 
                       '\n' + str(e))
        
            try:
                create_thumbnail_image(original_files, file.name, 
                                       thumbnails_files, file.name,
                                       thumbnail_size)
            except Exception as e:
                print('Failed to create thumbnails: ' + file.name + 
                      '\n' + str(e))

def create_clean_jpg_image(in_path, in_file, 
                           out_path, out_file):
    """ """
    in_file_path = pathlib.Path(in_path, in_file)
    out_file_path = pathlib.Path(out_path, out_file).with_suffix('.jpg')
    # Open the image and read data as pixel values.
    image_data = None
    with in_file_path.open('rb') as f:
        image = Image.open(f)
        image.load()   
        # Change if mode=P, etc.:
        if image.mode not in ['RGB', 'RGBA']:
            image = image.convert("RGBA")
        #  
        image_data = list(image.getdata())
    # Create a new empty image and add pixal data only.        
    if image_data:
        with out_file_path.open('wb') as f:
            clean_image = Image.new(image.mode, image.size)
            clean_image.putdata(image_data)
            clean_image.save(f)

def create_resized_image(in_path, in_file, 
                         out_path, out_file,
                         new_size=(512, 512)):
    """ """
    in_file_path = pathlib.Path(in_path, in_file)
    out_file_path = pathlib.Path(out_path, out_file).with_suffix('.jpg')
    #
    with in_file_path.open('rb') as f:
        image = Image.open(f)
        # Preserve ratio.
        (image_width, image_height) = image.size
        (new_max_width, new_max_height) = new_size
        factor = min(new_max_width/image_width, new_max_height/image_height)
        image = image.resize((int(image_width*factor), int(image_height*factor)), 
                             Image.ANTIALIAS)
        image.save(out_file_path)

def create_thumbnail_image(in_path, in_file, 
                           out_path, out_file,
                           new_size=(128,128)):
    """ """
    in_file_path = pathlib.Path(in_path, in_file)
    out_file_path = pathlib.Path(out_path, out_file).with_suffix('.jpg')
    # 
    with in_file_path.open('rb') as f:
        image = Image.open(f)
        image.thumbnail(new_size, Image.ANTIALIAS)
        image.save(out_file_path)


if __name__ == "__main__":
    execute()


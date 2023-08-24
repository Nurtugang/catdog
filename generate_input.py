import os
import base64
import json


cats_folder = "PetImages/cat"
dogs_folder = "PetImages/dog"
folders = [cats_folder, dogs_folder]


def convert_images_to_json(folder, category):
    photos = []
    id_counter = 0  
    
    for filename in os.listdir(folder):
        if filename.endswith(".jpg"):
            with open(os.path.join(folder, filename), "rb") as image_file:
                image_data = image_file.read()
                base64_image = base64.b64encode(image_data).decode("utf-8")
                
                photo = {
                    "ID": f"{category}{id_counter:03d}",
                    "img_code": base64_image
                }
                
                photos.append(photo)
                id_counter += 1

    return photos


def save_json_to_file(data, filename):
    with open(filename, "w") as json_file:
        json.dump(data, json_file, indent=4)



cat_photos = convert_images_to_json(cats_folder, "cat")
dog_photos = convert_images_to_json(dogs_folder, "dog")
all_photos = cat_photos + dog_photos

final_json = {
    "photos": all_photos
}

json_filename = "input.json"
save_json_to_file(final_json, json_filename)



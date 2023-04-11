###################################################################################################
# @Weaviate - https://github.com/weaviate/weaviate-examples/tree/main/nearest-neighbor-dog-search #
#                                                                                                 #
###################################################################################################

import os, re
import weaviate

def set_up_batch():
    """
    Prepare batching configuration to speed up deleting and importing data.
    """
    client.batch.configure(
        batch_size=100, 
        dynamic=True,
        timeout_retries=3,
        callback=None,
    )
    
def clear_up_MyImages():
    """
    Remove all objects from the MyImages collection.
    This is useful, if we want to rerun the import with different pictures.
    """
    with client.batch as batch:
        batch.delete_objects(
            class_name="MyImages",
            # same where operator as in the GraphQL API
            where={
                "operator": "NotEqual",
                "path": ["text"],
                "valueString": "x"
            },
            output="verbose",
        )

def import_data():
    """
    Process all images in [base64_images] folder and add import them into MyImages collection
    """

    with client.batch as batch:
        # Iterate over all .b64 files in the base64_images folder
        for encoded_file_path in os.listdir("./b64_img"):
            with open("./b64_img/" + encoded_file_path) as file:
                file_lines = file.readlines()

            base64_encoding = " ".join(file_lines)
            base64_encoding = base64_encoding.replace("\n", "").replace(" ", "") 

            # remove .b64 to get the original file name
            image_file = encoded_file_path.replace(".b64", "")

            # remove image file extension and swap - for " " to get the breed name
            breed = re.sub(".(jpg|jpeg|png)", "", image_file).replace("-", " ")

            # The properties from our schema
            data_properties = {
                "image": base64_encoding,
                "text": image_file,
            }

            batch.add_data_object(data_properties, "MyImages")

client = weaviate.Client(url = "http://localhost:8080")
set_up_batch()
clear_up_MyImages()
import_data()

print("The objects have been uploaded to Weaviate.")
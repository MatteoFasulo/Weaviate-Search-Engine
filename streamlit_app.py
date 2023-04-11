import streamlit as st
from PIL import Image
import base64
from io import BytesIO
import weaviate
import os

client = weaviate.Client(
    url = "http://localhost:8080",
)

def search_img(img_str):
    sourceImage = { "image": img_str}

    weaviate_results = client.query.get(
        "MyImages", ["text", "image"]
        ).with_near_image(
            sourceImage, encode=False
        ).with_limit(2).do()

    return weaviate_results["data"]["Get"]["MyImages"]

def on_file_change(**kwargs):
    """
    """
    bytes_data = kwargs.get('uploaded_img').read()
    img_str = base64.b64encode(bytes_data).decode()
    
    weaviate_results = search_img(img_str)

    if not weaviate_results:
        return []

    results = []
    for result in weaviate_results:
        results.append({
            "text": result["text"],
            "image": result["image"]
        })

    return results
    

def on_change_callback():
    """
    It prints a message to the console. Just for testing of callbacks.
    """
    print(f'on_change_callback: {uploaded_img}')

# Streamlit Config
st.set_page_config(page_title="Image Search Engine")

st.title('Image Search Engine')
st.markdown('Upload an image and Weaviate vector database will find out a similar one')

uploaded_img = st.file_uploader('Upload Your Image', type=['JPG', 'PNG'], on_change=on_change_callback)

if uploaded_img:
    st.image(uploaded_img.read())
    st.markdown("""---""")

    results = on_file_change(uploaded_img=uploaded_img)

    if not len(results) > 0:
        st.text('Similar images not found in database, please upload something else.')
    
    else:
        images = [base64.b64decode(result.get('image')) for result in results]

        with st.container():
            for idx, col in enumerate(st.columns(len(images))):
                col.image(images[idx], use_column_width=True)



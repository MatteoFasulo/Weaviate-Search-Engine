<div>
    <div align="left">
        <img alt='Streamlit logo' src='https://upload.wikimedia.org/wikipedia/commons/7/77/Streamlit-logo-primary-colormark-darktext.png' width='260' align='left' />
    </div>
    <div align="right">
        <img alt='Weaviate logo' src='https://weaviate.io/img/site/weaviate-logo-light.png' width='160' align='right' />
    </div>
<br>
<br>
<br>
</div>

# Weaviate Image Search Engine
Vector database (Weaviate) to build an image search engine powered by a deep neural network. It uses Weaviate optimizer for images with **ResNet50 (PyTorch)** as vectorizer and retriever. Currently only PyTorch ResNet50 supports **CUDA-GPU** but in a **single-threaded** manner. You can also use the **keras-based ResNet50 CPU** with **multi-threaded** inference.

## Steps to run it
1. Install Docker (skip this if already installed)
```sh
curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh
```

2. Spin up docker compose file:
```sh
docker compose up -d
```

3. Activate the environment:
```sh
pip3 install pipenv && pipenv install && pipenv shell
```

4. Launch `start.sh` script to create Weaviate schema, convert images from `img` folder to base64 and upload them in Weaviate:
```sh
./start.sh
```

5. Navigate to URL that streamlit outputs and upload an image. The program will query Weaviate for a vectorized search of similar images. If you are running this in local environment then just navigate at:
```
http://127.0.0.1:8501/
```

6. (Optional) CORS and XsrfProtection Streamlit. Run this if you have **Socket Errors** while connecting to streamlit app URL:
```
streamlit run streamlit_app.py --server.enableCORS false --server.enableXsrfProtection false
```

## Images
Feel free to insert your images in `img` folder and see if the database suggests you similar images.

## Weaviate Schema
This is the schema implemented in Weaviate. You can modify the class name, change the vectorizer or insert more properties.
```python
schemaConfig = {
    'class': 'MyImages', # class name for schema config in Weaviate (change it with a custom name for your images)
    'vectorizer': 'img2vec-neural',
    'vectorIndexType': 'hnsw',
    'moduleConfig': {
        'img2vec-neural': {
            'imageFields': [
                'image'
            ]
        }
    },
    'properties': [
        {
            'name': 'image',
            'dataType': ['blob']
        },
        {
            'name': 'text',
            'dataType': ['string']
        }
    ]
}
```

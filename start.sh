#!/bin/bash

set -eou pipefail

# time for weaviate to get live
sleep 5

python3 schema.py

python3 base64_convert.py

python3 upload_img.py

streamlit run streamlit_app.py
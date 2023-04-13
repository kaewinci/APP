import re
import pandas as pd
import sqlite3

from flask import Flask, request, jsonify
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger.utils import swag_from


app = Flask(__name__)

from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from

app.json_encoder = LazyJSONEncoder
swagger_template = dict(
    info = {
        'title': LazyString(lambda: 'API Documentation for Data Processing and Modeling'),
        'version': LazyString(lambda: '1.0.0'),
        'description': LazyString(lambda: 'Dokumentasi API untuk Data Processing dan Modeling'),
    },
    host = LazyString(lambda: request.host)
)

conn = sqlite3.connect('amindata.db')

df = pd.read_csv(r"C:\Users\USER\myapp\data\data.csv", encoding='latin-1')
alay_dict = pd.read_csv(r"C:\Users\USER\myapp\data\new_kamusalay.csv", encoding='latin-1').to_dict()
kasar_dict = pd.read_csv(r"C:\Users\USER\myapp\data\abusive.csv", encoding='latin-1').to_dict()

def clean_text(text, dict_alay, dict_kasar):
   
    text = ''.join(e for e in text if e.isalnum() or e.isspace())

    words = text.split()

    cleaned_words = []
    for word in words:
        if word in dict_alay:
            cleaned_words.append(dict_alay[word])
        elif word in dict_kasar:
            pass 
        else:
            cleaned_words.append(word)

    
    cleaned_text = ' '.join(cleaned_words)

    return cleaned_text

def lowercase(text):
    return text.lower()

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'docs',
            "route": '/docs.json',
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}
swagger = Swagger(app, template=swagger_template,             
                  config=swagger_config)



@swag_from("docs/text_processing.yml", methods=['POST'])
@app.route('/text-processing', methods=['POST'])
def text_processing():

    text = request.form.get('text')

    json_response = {
        'status_code': 200,
        'description': "Teks yang sudah diproses",
        'data': clean_text(text, alay_dict, kasar_dict),
    }

    response_data = jsonify(json_response)
    return response_data

@swag_from("docs/text_processing_file.yml", methods=['POST'])
@app.route('/text-processing-file', methods=['POST'])
def text_processing_file():

    # Uploaded file
    file = request.files.getlist('file')[0]

    # Import file csv ke Pandas
    df = pd.read_csv(file, encoding='latin-1')

# Lakukan cleansing pada teks
    cleaned_text = []
    for text in df['Text']:
        cleaned_text.append(clean_text(text, alay_dict, kasar_dict))

    json_response = {
        'status_code': 200,
        'description': "Teks yang sudah diproses",
        'data': cleaned_text,
    }

    response_data = jsonify(json_response)
    return response_data



if __name__ == '__main__':
    app.run()

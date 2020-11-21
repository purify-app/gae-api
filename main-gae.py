from flask import Flask, request, make_response, jsonify

app = Flask(__name__)

@app.route('/')
def index():

    if request.values.get("txt"):
        from transformers import AutoTokenizer, AutoModel, ElectraForSequenceClassification
        
        tokenizer = AutoTokenizer.from_pretrained("/srv/electra-ka-fake-news-tagging/")
        model = ElectraForSequenceClassification.from_pretrained("/srv/electra-ka-fake-news-tagging/")
        inputs = tokenizer(request.values.get("txt"), return_tensors="pt")
        return str(model(**inputs)[0].tolist())
    return 'no text was sent'

@app.route('/log')
def log():
    
    if request.args.get('post_id') and request.args.get('feedback'):
        import os
        from google.cloud import storage
    
        client = storage.Client(project="purify-295716")
        bucket = client.get_bucket('purify_ka')
        blob = bucket.blob('test.txt')
        logs = blob.download_as_string().decode("utf-8")
        logs += str(request.args.get('post_id')) + ", " + str(request.args.get('feedback')) + '\n'
        blob = bucket.blob('test.txt')
        blob.upload_from_string(logs)
    return "legged"

if __name__ == "__main__":
    app.run(host="localhost", port=8080)

@app.after_request
def after_request_func(response):
    origin = request.headers.get('Origin')
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Headers', 'x-csrf-token')
        response.headers.add('Access-Control-Allow-Methods',
                            'GET, POST, OPTIONS, PUT, PATCH, DELETE')
        if origin:
            response.headers.add('Access-Control-Allow-Origin', origin)
    else:
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        if origin:
            response.headers.add('Access-Control-Allow-Origin', origin)
    return response
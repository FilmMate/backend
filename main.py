from flask import Flask, request, jsonify
from endpoints import Endpoints
from fetch_services import fetch_data
from filter import filter_response
from flask_caching import Cache

endpoint = Endpoints()
app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple', 'CACHE_QUERY_STRING': True})

@app.route("/getlatest",methods=['GET'])
@cache.cached(timeout=300, key_prefix=lambda: request.full_path) 
def get_latest():
    response = fetch_data(url=endpoint.discoverMovie,params=endpoint.latest(api_key=request.args.get('api_key'),lang=request.args.get('lang'),page=request.args.get('page')))
    filtered_response = filter_response(api_key=request.args.get('api_key'),response=response)

    return jsonify({
        "result" : filtered_response,
        "page" : response['page'],
        "total_pages" : response["total_pages"]
    },200)

if __name__ == '__main__':
    app.run(debug=True,port=5000)
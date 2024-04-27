from flask import Flask, request, jsonify
from endpoints import Endpoints
from fetch_services import fetch_data, fetch_detail, fetch_video
from filter import filter_response, filter_tv
from flask_caching import Cache

endpoint = Endpoints()
app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple', 'CACHE_QUERY_STRING': True})


@app.route("/getlatest", methods=['GET'])
@cache.cached(timeout=300, key_prefix=lambda: request.full_path)
def get_latest():
    response = fetch_data(url=endpoint.discoverMovie, params=endpoint.latest(
        api_key=request.args.get('api_key'), lang=request.args.get('lang'), page=request.args.get('page')))
    filtered_response = filter_response(
        api_key=request.args.get('api_key'), response=response)

    return jsonify({
        "result": filtered_response,
        "page": response['page'],
        "total_pages": response["total_pages"]
    })


@app.route("/getmoviedetail", methods=['GET'])
@cache.cached(timeout=300, key_prefix=lambda: request.full_path)
def get_movie_detail():
    response = fetch_detail(endpoint.get_movie_detail(
        api_key=request.args.get('api_key'), mid=request.args.get('mid')))
    return jsonify({
        "result": response
    })


@app.route("/getmoviemedia", methods=['GET'])
@cache.cached(timeout=300, key_prefix=lambda: request.full_path)
def get_movie_media():
    response = fetch_video(endpoint.get_media(api_key=request.args.get(
        'api_key'), mid=request.args.get('mid'), media_type='video'))
    return jsonify({
        "result": response
    })


@app.route("/getlatesttv", methods=['GET'])
@cache.cached(timeout=300, key_prefix=lambda: request.full_path)
def get_latest_tv():
    response = fetch_data(endpoint.trendingTV,
                          params={
                              "api_key": request.args.get('api_key')
                          },
                          )

    filter_response = filter_tv(api_key= request.args.get('api_key'),response=response)

    return jsonify({
        "result": filter_response
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)

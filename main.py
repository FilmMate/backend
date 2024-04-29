from flask import Flask, request, jsonify
from endpoints import Endpoints
from fetch_services import fetch_cast_and_crew, fetch_data, fetch_detail, fetch_images, fetch_video
from filter import filter_response, filter_tv, filter_tv_detail
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
    details = fetch_detail(endpoint.get_movie_detail(
        api_key=request.args.get('api_key'), mid=request.args.get('mid')))
    video = fetch_video(endpoint.get_media(api_key=request.args.get(
        'api_key'), mid=request.args.get('mid'), media_type='video'))
    image = fetch_images(endpoint.get_media(api_key=request.args.get(
        'api_key'), mid=request.args.get('mid'), media_type='image'))
    cast_and_crew = fetch_cast_and_crew(endpoint.get_cast_and_crew(api_key=request.args.get(
        'api_key'), mid=request.args.get('mid')))
    return jsonify({
        'title': details['title'],
        'overview': details['overview'],
        'duration': details['duration'],
        'genres': details['genres'],
        'release_date': details['release_date'],
        'rating': details['rating'],
        'lang': details['lang'],
        'poster_path': image['poster'],
        'backdrop_path': image['backdrop'],
        'video': video['key'],
        'site': video['site'],
        'type': 'movie',
        'cast': cast_and_crew['cast'],
        'crew': cast_and_crew['crew']
    })


@app.route("/gettvdetail", methods=['GET'])
@cache.cached(timeout=300, key_prefix=lambda: request.full_path)
def get_tv_detail():
    response = fetch_data(endpoint.get_tv_detail(
        api_key=request.args.get('api_key'), tid=request.args.get('tid')))
    filter_response = filter_tv_detail(
        api_key=request.args.get('api_key'), response=response, tid=request.args.get('tid'))
    cast_and_crew = fetch_cast_and_crew(url=endpoint.get_tv_credits(
        api_key=request.args.get('api_key'), tid=request.args.get('tid')))
    return jsonify({
        "video": filter_response['video'],
        "site": filter_response['site'],
        "type": 'tv',
        'poster_path': filter_response['poster_path'],
        'backdrop_path': filter_response['backdrop_path'],
        "id": filter_response["id"],
        "title": filter_response["title"],
        "overview": filter_response["overview"],
        "genres": filter_response["genres"],
        "lang":  filter_response["lang"],
        "release_date": filter_response["release_date"],
        "rating": filter_response["rating"],
        'cast': cast_and_crew["cast"],
        'crew': cast_and_crew['crew'],
    })


@app.route("/getlatesttv", methods=['GET'])
@cache.cached(timeout=300, key_prefix=lambda: request.full_path)
def get_latest_tv():
    response = fetch_data(endpoint.trendingTV,
                          params={
                              "api_key": request.args.get('api_key'),
                              "page": request.args.get('page', default=1, type=int)
                          })

    filter_response = filter_tv(
        api_key=request.args.get('api_key'), response=response)

    return jsonify({
        "result": filter_response
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)

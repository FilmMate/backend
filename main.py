from flask import Flask, request, jsonify
from endpoints import Endpoints
from fetch_services import fetch_cast_and_crew, fetch_data, fetch_detail, fetch_images, fetch_video
from filter import filter_response, filter_tv, filter_tv_detail
from flask_caching import Cache
from google.cloud import firestore
from flask_cors import CORS

endpoint = Endpoints()
app = Flask(__name__)
CORS(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple', 'CACHE_QUERY_STRING': True})


hero_override = False
movie_override = False
tv_override = False

# Path to your service account key JSON file
service_account_path = "/home/filmmate/mysite/filmmate-22f8b-firebase-adminsdk-coe0p-87ed401eea.json"

# Initialize Firestore client with the service account key
db = firestore.Client.from_service_account_json(service_account_path)

@app.route("/getmovie", methods=['GET'])
def get_movie():
    try:
        # Retrieve the hero document from the Firestore collection
        hero_doc = db.collection("customizations").document("FilmMateMovies").get()

        if hero_doc.exists:
            # Get the 'results' field from the document
            hero_list = hero_doc.to_dict().get("results", [])
        else:
            hero_list = []
        if movie_override :
            return jsonify({"results": hero_list}), 200
        else:
            return jsonify({"results": []}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/gettv", methods=['GET'])
def get_tv():
    try:
        # Retrieve the hero document from the Firestore collection
        hero_doc = db.collection("customizations").document("FilmMateTV").get()

        if hero_doc.exists:
            # Get the 'results' field from the document
            hero_list = hero_doc.to_dict().get("results", [])
        else:
            hero_list = []
        if tv_override :
            return jsonify({"results": hero_list}), 200
        else:
            return jsonify({"results": []}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/gethero", methods=['GET'])
def get_hero():
    try:
        # Retrieve the hero document from the Firestore collection
        hero_doc = db.collection("customizations").document("hero").get()

        if hero_doc.exists:
            # Get the 'results' field from the document
            hero_list = hero_doc.to_dict().get("results", [])
        else:
            hero_list = []

        # Ensure the hero_list contains valid data (no empty objects)
        #hero_override = bool(hero_list and any(bool(item) for item in hero_list))

        # Ensure both hero_list contains valid data AND hero_override is True
        if hero_override and len(hero_list) == 5:
            return jsonify({"results": hero_list}), 200
        else:
            # Fallback to fetch data from the external API
            response = fetch_data(url=endpoint.getNowPlaying,
                              params={
                                  "api_key": request.args.get('api_key'),
                              })
            filtered_response = filter_response(
            api_key=request.args.get('api_key'), response=response)

            return jsonify({
            "results": filtered_response,
            "page": response['page'],
            "total_pages": response["total_pages"]
            }), 203

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/triggerhero", methods=['GET'])
def trigger_hero_override():
    global hero_override  # Use global to modify the variable
    hero_override = not hero_override
    return jsonify({"hero_override": hero_override}), 200

@app.route("/triggermovie", methods=['GET'])
def trigger_movie_override():
    global movie_override  # Use global to modify the variable
    movie_override = not movie_override
    return jsonify({"hero_override": movie_override}), 200

@app.route("/triggertv", methods=['GET'])
def trigger_tv_override():
    global tv_override  # Use global to modify the variable
    tv_override = not tv_override
    return jsonify({"hero_override": tv_override}), 200

@app.route("/getherostatus", methods=['GET'])
def get_hero_status():
    global hero_override
    return jsonify({"hero_override": hero_override}), 200

@app.route("/getmoviestatus", methods=['GET'])
def get_movie_status():
    global movie_override
    return jsonify({"hero_override": movie_override}), 200

@app.route("/gettvstatus", methods=['GET'])
def get_tv_status():
    global tv_override
    return jsonify({"hero_override": tv_override}), 200

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
    app.run(port=6000,debug=True)

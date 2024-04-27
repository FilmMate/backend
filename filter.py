from date_time_process import format_time
from endpoints import Endpoints
from fetch_services import fetch_detail, fetch_images, fetch_video, fetch_cast_and_crew
from genres import Genres
endpoints = Endpoints()
genre = Genres()

def filter_response(api_key, response):
    filtered_response = []
    movie_ids = [movie['id'] for movie in response['results']]
    for mid in movie_ids:
        media_image = fetch_images(endpoints.get_media(api_key, mid, 'image'))
        details = fetch_detail(endpoints.get_movie_detail(api_key,mid))
        video = fetch_video(endpoints.get_media(api_key, mid, 'video'))
        cast_crew = fetch_cast_and_crew(endpoints.get_cast_and_crew(api_key=api_key,mid=mid))
        movie_data = {
            'id': mid,
            'overview': details["overview"],
            'release_date': response['results'][movie_ids.index(mid)]['release_date'],
            'title': details["title"],
            'poster_path': media_image["poster"],
            'backdrop_path': media_image["backdrop"],
            'rating': round(response['results'][movie_ids.index(mid)]['vote_average']/2, 2),
            "duration": details["duration"],
            "genres": details["genres"],
            "lang" : details["lang"],
            "video" : video["key"],
            "site" : video["site"],
            "cast" : cast_crew["cast"],
            "crew" : cast_crew["crew"],
            "type" : 'movie',
        }
        filtered_response.append(movie_data)
    return filtered_response

def filter_tv(api_key, response):
    filtered_response = []
    tv_ids = [tv['id'] for tv in response['results']]
    for tid in tv_ids:
        media_image = fetch_images(url=endpoints.get_tv_media(api_key=api_key,tid=tid,media_type="image"))
        video = fetch_video(url=endpoints.get_tv_media(api_key=api_key,tid=tid,media_type="videos"))
        tv_data = {
            "video" : video["key"],
            "site" : video["site"],
            "type" : 'tv',
            'poster_path': media_image["poster"],
            'backdrop_path': media_image["backdrop"],
            "id" : tid,
            "title" : response['results'][tv_ids.index(tid)]['name'],
            "overview" : response['results'][tv_ids.index(tid)]['overview'],
            "genres" : genre.get_genre_names(response['results'][tv_ids.index(tid)]['genre_ids']),
            "lang" :  response['results'][tv_ids.index(tid)]['original_language'],
            "release_date" : response['results'][tv_ids.index(tid)]['first_air_date'],
            "rating" : round(response['results'][tv_ids.index(tid)]['vote_average']/2,2),
        }
        filtered_response.append(tv_data)
    return filtered_response
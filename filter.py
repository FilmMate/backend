from endpoints import Endpoints
from fetch_services import fetch_detail, fetch_images, fetch_video, fetch_cast_and_crew
endpoints = Endpoints()

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
        }
        filtered_response.append(movie_data)
    return filtered_response
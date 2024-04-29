import requests
from date_time_process import format_time

def fetch_data(url,params={'region':'IN','page': 1}):
    response = requests.get(url,params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
def fetch_images(url):
    response = fetch_data(url)
    if response is not None:
        backdrop_filepath = None
        poster_filepath = None

        if 'backdrops' in response:
            for backdrop in response["backdrops"]:
                if backdrop["file_path"] is not None:
                    backdrop_filepath = backdrop["file_path"]
                    break

        if 'posters' in response:
            for poster in response["posters"]:
                if poster["file_path"] is not None:
                    poster_filepath = poster["file_path"]
                    break

        return {
            'poster': poster_filepath,
            'backdrop': backdrop_filepath
        }
    else:
        return None


def fetch_video(url):
    response = fetch_data(url)
    key, site = None, None
    if response is not None and 'results' in response:
        trailer_videos = [video for video in response['results'] if
                          video['type'] in ['Trailer', 'Teaser'] and video['site'].lower() == 'youtube']

        if trailer_videos:
            # Append 'https://youtu.be/' to the key
            key = 'https://youtu.be/' + trailer_videos[0]['key']
            site = 'YouTube'
        return {
            'key': key,
            'site': site
        }
    else:
        return {
            'key': key,
            'site': site
        }


def fetch_detail(url):
    response = fetch_data(url)
    title, overview, duration, lang, genres,rating,release_date = None, None, None, None, [], 0, None
    if response is not None:
        if 'title' in response:
            title = response['title']
        if 'overview' in response:
            overview = response['overview']
        if 'runtime' in response:
            duration = format_time(response['runtime'])
        if 'genres' in response:
            genres = [genre["name"] for genre in response["genres"]]
        if 'original_language' in response:
            lang = response['original_language']
        if 'release_date' in response:
            release_date = response['release_date']
        if 'vote_average' in response:
            rating = round(response['vote_average']/2,2)
        return {
            'title': title,
            'overview': overview,
            'duration': duration,
            'genres': genres,
            'lang' : lang,
            'release_date' : release_date,
            'rating' : rating
        }
    else:
        return {
            'title': title,
            'overview': overview,
            'duration': duration,
            'genres': genres,
            'lang' : lang,
            'release_date' : release_date,
            'rating' : rating
        }


def fetch_cast_and_crew(url):
    response = fetch_data(url)
    if response is not None:
        formatted_data = {}
        # Format cast data
        formatted_cast = []
        for member in response.get("cast", [])[:10]:  # Select first 10 cast members
            formatted_cast.append({
                "name": member.get("name"),
                "character": member.get("character")
            })
        formatted_data["cast"] = formatted_cast

        # Format crew data
        formatted_crew = []
        relevant_jobs = {"music", "sound"}
        for member in response.get("crew", []):
            job = member.get("job", "").lower()  # Convert job title to lowercase for case insensitivity
            if any(keyword in job for keyword in relevant_jobs) or job == "director" or job == "producer" or job == "screenplay" :
                formatted_crew.append({
                    "name": member.get("name"),
                    "job": job
                })
        formatted_data["crew"] = formatted_crew
        return formatted_data
    return None

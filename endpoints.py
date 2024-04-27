from date_time_process import get_dates
class Endpoints:
    def __init__(self):
        self.baseUrl = "https://api.themoviedb.org/3"
        self.trendingMovie = f"{self.baseUrl}/trending/movie/day"
        self.getMovieDetail = f"{self.baseUrl}/movie"
        self.discoverMovie = f"{self.baseUrl}/discover/movie"
        self.trendingTV = f"{self.baseUrl}/trending/tv/day"
        self.getTVdetail = f"{self.baseUrl}/tv"
    
    def get_media(self, api_key, mid, media_type):
        if media_type == 'image':
            return f"{self.getMovieDetail}/{mid}/images?api_key={api_key}"
        if media_type == 'video':
            return f"{self.getMovieDetail}/{mid}/videos?api_key={api_key}"
        
    def get_tv_media(self, api_key, tid, media_type):
        if media_type == 'image':
            return f"{self.getTVdetail}/{tid}/images?api_key={api_key}"
        if media_type == 'videos':
            return f"{self.getTVdetail}/{tid}/videos?api_key={api_key}"
    
    def get_movie_detail(self, api_key, mid):
        return f"{self.getMovieDetail}/{mid}?api_key={api_key}"
    
    def get_cast_and_crew(self, api_key, mid):
        return f"{self.getMovieDetail}/{mid}/credits?api_key={api_key}"
    
    def latest(self,api_key,lang,page = 1):
        dates = get_dates()
        params = {
        "api_key": api_key,
        "language": f"{lang}-IN",
        "region": "IN",
        "sort_by": "popularity.desc",
        "with_original_language": lang,
        "release_date.gte" : dates["start"],
        "release_date.lte" : dates["end"],
        "page" : page
        }
        return params
        
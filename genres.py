class Genres:
    def __init__(self):
        self.genre_map = {
            28: "Action",
            12: "Adventure",
            16: "Animation",
            35: "Comedy",
            80: "Crime",
            99: "Documentary",
            18: "Drama",
            10751: "Family",
            14: "Fantasy",
            36: "History",
            27: "Horror",
            10402: "Music",
            9648: "Mystery",
            10749: "Romance",
            878: "Science Fiction",
            10770: "TV Movie",
            53: "Thriller",
            10752: "War",
            37: "Western"
        }
    
    def get_genre_names(self, genre_ids):
        genre_names = []
        for genre_id in genre_ids:
            genre_name = self.genre_map.get(genre_id)
            if genre_name:
                genre_names.append(genre_name)
        
        return genre_names
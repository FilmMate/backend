# API Documentation

## Get Latest Movies

- **Endpoint**: `/getlatest`
- **Method**: `GET`
  
### Parameters

- `api_key` (string, required): API key for authentication.
- `lang` (string, optional): Language preference for movie information.
  
  | Value (lang) | Language   |
  | ------------ | ---------- |
  | `ml`         | Malayalam  |
  | `tn`         | Tamil      |
  | `hi`         | Hindi      |
  | `en`         | English    |
  - and so on
  - By default `lang` is `en`
- `page` (integer, optional): Page number for pagination.

### Sample Response
```json
{
  "result": [
            {
                "backdrop_path": "/rImcA1JkF88uTfyr26px6HBXUax.jpg",
                "cast": [
                    {
                        "character": "Siju 'Kuttan' David",
                        "name": "Soubin Shahir"
                    }
                ],
                "crew": [
                    {
                        "job": "director",
                        "name": "Chidambaram"
                    }
                ],
                "duration": "2h 15m",
                "genres": [
                    "Adventure",
                    "Thriller",
                    "Drama"
                ],
                "id": 1069945,
                "lang": "ml",
                "overview": "Manjummel Boys, based on a real story, is about a bunch of friends who set out on a trip to Kodaikanal and the events that occur there.",
                "poster_path": "/awOxXBZHh3jvFEOLJvTaJOX5urU.jpg",
                "rating": 3.95,
                "release_date": "2024-02-22",
                "site": "YouTube",
                "title": "Manjummel Boys",
                "type": "movie",
                "video": "https://youtu.be/-Kq2MxoJVKo"
            }
        ],
  "page": 1,
  "total_pages": 1
}
```

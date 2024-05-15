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
                "overview": "Manjummel Boys, based on a real story, is about ...",
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
---
## Get Movie Detail

- **Endpoint**: `/getmoviedetail`
- **Method**: `GET`
  
### Parameters

- `api_key` (string, required): API key for authentication.
- `mid` (string, required): Movie ID for the movie detail to be retrieved.

### Sample Response

```json
    {
        "title": "Dilwale Dulhania Le Jayenge",
        "overview": "Raj is a rich, carefree, happy-go-lucky second generation NRI ...",
        "duration": "3h 10m",
        "genres": [
            "Comedy",
            "Drama",
            "Romance"
        ],
        "release_date": "1995-10-20",
        "rating": 4.27,
        "lang": "hi",
        "poster_path": "/2CAL2433ZeIihfX1Hb2139CX0pW.jpg",
        "backdrop_path": "/vI3aUGTuRRdM7J78KIdW98LdxE5.jpg",
        "video": "https://youtu.be/oIZ4U21DRlM",
        "site": "YouTube",
        "type": "movie",
        "cast": [
            {
                "character": "Simran Singh",
                "name": "Kajol"
            },
            {
                "character": "Raj Malhotra",
                "name": "Shah Rukh Khan"
            },
            {
                "character": "Chaudhry Baldev Singh",
                "name": "Amrish Puri"
            },
            ...
        ],
        "crew": [
            {
                "job": "director",
                "name": "Aditya Chopra"
            },
            {
                "job": "producer",
                "name": "Yash Chopra"
            },
            ...
        ]
    }
```

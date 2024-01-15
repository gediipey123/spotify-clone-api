
# Spotify Clone API

An API for Spotify

## Base URL

All API endpoints are relative to the base URL:

https://spotify-clone-gdsc.vercel.app/


## API Reference

#### Search Song

```http
  GET /api/search?q=
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `q` | `string` | **Required**. Your Search Query |

#### Fetch Song Details

```http
  GET /api/songdetails/:vid
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `vid` | `string` | **Required**. videoId of the song  |

#### Search Suggestion

```http
  GET /api/search_suggestion?q=
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `q`      | `string` | **Required**. Search Suggestion Query |


#### Next Song

```http
  GET /api/next/:vid
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `vid`      | `string` | **Required**. videoId of the Song |


#### Fetch Playlist

```http
  GET /api/playlist?cat=
```
Available Categories: **chill**, **commute**, **energy booster**, **feel good**, **focus**, **party**, **romance**, **sleep**, **workout**

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `cat`      | `string` | **Required**. Category of Playlist |


#### Get Songs From Playlist

```http
  GET /api/playlist/song/:pid
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `pid`      | `string` | **Required**. playlistId of the Song |


#### Fetch Songs Related to Current Song

```http
  GET /api/playerplaylist/:vid
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `vid`      | `string` | **Required**. videoId of the Song |


#### Get Song Lyrics

```http
  GET /api/lyrics/:vid
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `vid`      | `string` | **Required**. videoId of the Song |

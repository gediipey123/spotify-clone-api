from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
from random import randint
from innertube import InnerTube
from ytmusicapi import YTMusic

app = Flask(__name__)
CORS(app)
api = Api(app)

# Client for YouTube on iOS
client = InnerTube("IOS")

ytmusic = YTMusic()

cat = {
    "chill" : "ggMPOg1uX1JOQWZFeDByc2Jm",
    "commute" : "ggMPOg1uX044Z2o5WERLckpU",
    "energy booster" : "ggMPOg1uX2lRZUZiMnNrQnJW",
    "feel good" : "ggMPOg1uXzZQbDB5eThLRTQ3",
    "focus" : "ggMPOg1uX0NvNGNhWThMYWRh",
    "party" : "ggMPOg1uX0pmQ0s2V0JRclZs",
    "romance" : "ggMPOg1uX0FzQ2FhZWtUY211",
    "sleep" : "ggMPOg1uX1MxaFQ3Z0JMZkN4",
    "workout" : "ggMPOg1uX09LWkhnTjRGRUJh", 
}

class Home(Resource):
    def get(self):
        return jsonify({'message':'Welcome to Spotify API'})

class Search(Resource):
    def get(self):
        try:
            if(not request.args.get("q")):
                return {"error": "No search query provided"}
            search_results = []
            results = {}
            for i in ytmusic.search(query=request.args.get("q"),filter="songs"):
                search_results.append({"title": i["title"],"videoId": i["videoId"],"duration": i["duration"],"artists":i["artists"][0]["name"],"thumbnails":i["thumbnails"][len(i["thumbnails"])-1]["url"]})
            results['songs'] = search_results
            search_results = []
            for i in ytmusic.search(query=request.args.get("q"),filter="videos"):
                search_results.append({"title": i["title"],"videoId": i["videoId"],"duration": i["duration"],"artists":i["artists"][0]["name"],"thumbnails":i["thumbnails"][0]["url"]})
            results['videos'] = search_results
            return results
        except:
            return jsonify({'error' : 'Invalid Request'})

class SearchSuggestion(Resource):
    def __init__(self):
        self.client = InnerTube("IOS_MUSIC")

    def get(self):
        try:
            if len(request.args.get("q"))==0:
                return {"suggestions": [""]}
            data = self.client.music_get_search_suggestions(request.args.get("q"))
            suggestions = []
            for i in range(len(data["contents"][0]["searchSuggestionsSectionRenderer"]["contents"])):
                suggestions.append(data["contents"][0]["searchSuggestionsSectionRenderer"]["contents"][i]["searchSuggestionRenderer"]["navigationEndpoint"]["searchEndpoint"]["query"])
            return {"suggestions": suggestions}
        except:
            return jsonify({'error' : 'Invalid request'})

class NextSongResource(Resource):
    def get(self, vid):
        try:
            client = InnerTube("WEB_MUSIC")
            data = client.next(vid)
            i = randint(1,len(data["contents"]["singleColumnMusicWatchNextResultsRenderer"]["playlist"]["playlistPanelRenderer"]["contents"])-1)
            print(i)
            videoid = data["contents"]["singleColumnMusicWatchNextResultsRenderer"]["playlist"]["playlistPanelRenderer"]["contents"][i]["playlistPanelVideoRenderer"]["videoId"]
            if vid == videoid:
                data = client.next(vid)
                i = randint(0,len(data["contents"]["singleColumnMusicWatchNextResultsRenderer"]["playlist"]["playlistPanelRenderer"]["contents"])-1)
                videoid = data["contents"]["singleColumnMusicWatchNextResultsRenderer"]["playlist"]["playlistPanelRenderer"]["contents"][i]["playlistPanelVideoRenderer"]["videoId"]
            streamobj = []
            data = InnerTube("ANDROID_MUSIC").player(videoid)
            streams = data["streamingData"]["adaptiveFormats"]
            title = data["videoDetails"]["title"]
            author = data["videoDetails"]["author"]
            viewcount = data["videoDetails"]["viewCount"]
            thumbnail = data["videoDetails"]["thumbnail"]["thumbnails"][len(data["videoDetails"]["thumbnail"]["thumbnails"])-1]["url"]
            videoid = data["videoDetails"]["videoId"]
            li=[]
            for i in streams:
                if i["itag"]==251:
                    li.append({"url":i["url"],"mimeType":i["mimeType"].split(";")[0]}) 
            streamobj.append({"id":1,"title":title,"author":author,"thumbnail":thumbnail,"streamlinks":li,"viewcount":viewcount,"videoid":videoid})
            return jsonify(streamobj)
        except:
            return jsonify({'error' : 'Invalid videoId'})
    
class Playlists(Resource):
    def get(self):
        if request.args.get("cat") in cat:
            return ytmusic.get_mood_playlists(cat[request.args.get("cat")])
        else:
            return jsonify({"error" : "Invalid Category"})

class PlaylistSong(Resource):
    def get(self,pid):
        try:
            return ytmusic.get_playlist(pid)
        except:
            return jsonify({'error' : 'Invalid playlistId'})

class SongDetails(Resource):
    def get(self,vid):
        try:
            streamobj = {}
            data = InnerTube("ANDROID_MUSIC").player(vid)
            if "streamingData" in data:
                streams = data["streamingData"]["adaptiveFormats"]
                title = data["videoDetails"]["title"]
                author = data["videoDetails"]["author"]
                viewcount = data["videoDetails"]["viewCount"]
                videoid = data["videoDetails"]["videoId"]
                thumbnail = data["videoDetails"]["thumbnail"]["thumbnails"][len(data["videoDetails"]["thumbnail"]["thumbnails"])-1]["url"]
                li=[]
                for i in streams:
                    if i["itag"]==251:
                        li.append({"url":i["url"],"mimeType":i["mimeType"].split(";")[0]}) 
                streamobj = {"id":1,"title":title,"author":author,"thumbnail":thumbnail,"streamlinks":li,"viewcount":viewcount,"videoid":videoid}
            return streamobj
        except:
            return jsonify({'error' : 'Invalid videoId'})
    
class PlayerPlaylist(Resource):
    def get(self,vid):
        try:
            p = ytmusic.get_watch_playlist(vid)['tracks']
            li = []
            for i in range(1,len(p)):
                li.append(p[i]['videoId'])
            return jsonify({'videoId':li})
        except:
            return jsonify({'error' : 'Invalid videoId'})
    
class Lyrics(Resource):
    def get(self,vid):
        try:
            p = ytmusic.get_watch_playlist(vid)
            try:
                return ytmusic.get_lyrics(p['lyrics'])
            except:
                return {"lyrics":"No lyrics found","source":""}
        except:
            return jsonify({'error' : 'Invalid videoId'})

api.add_resource(Home,'/')
api.add_resource(Search, '/api/search')
api.add_resource(SearchSuggestion, "/api/search_suggestion")
api.add_resource(NextSongResource, '/api/next/<string:vid>')
api.add_resource(Playlists, '/api/playlist')
api.add_resource(PlaylistSong, '/api/playlist/song/<string:pid>')
api.add_resource(SongDetails, '/api/songdetails/<string:vid>')
api.add_resource(PlayerPlaylist, '/api/playerplaylist/<string:vid>')
api.add_resource(Lyrics, '/api/lyrics/<string:vid>')

if __name__ == '__main__':
    app.run(debug=True)

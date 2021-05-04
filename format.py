import datetime
import pandas as pd

class Formatdata(object):
    data = None
    def __init__(self,data,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.data = data
    def analyze_playlist(self):
        track_id = []
        track_name = []
        first_artist = []
        date_added = []
        parse_date = []
        uri = []
        album_name = []
        data = self.data
        for i in range(len(data)):
            for track in data[i]['items']:
                track_id.append(track['track']['id'])
                date_added.append(track['added_at'])
                track_name.append(track['track']['name'])
                first_artist.append(track['track']['artists'][0]['name'])
                uri.append(track['track']['album']['uri'])
                album_name.append(track['track']['album']['name'])
        tracks_df = pd.DataFrame([track_id,first_artist,track_name,date_added,uri,album_name])
        tracks_df_new = tracks_df.T # or df1.transpose()
        tracks_df_new.columns = ['id','artist','track_name','added_at','uri','album_name']
        tracks_df_new['added_at'] = pd.to_datetime(tracks_df_new['added_at'] , format = "%Y-%m-%dT%H:%M:%S%fZ")
        return tracks_df_new
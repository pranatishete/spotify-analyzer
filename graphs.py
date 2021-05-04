import matplotlib.pyplot as plt
import pandas as pd

class plotgraphs(object):
    df1 = None
    def __init__(self,df,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.df = df
        
    def plot_albums(self):
        tracks = self.df
        t1 = tracks\
        .assign(year_added=tracks.added_at.dt.year)\
        .groupby(['artist','track_name']) \
        .count()['id'] \
        .reset_index() \
        .sort_values('id', ascending=False) \
        .rename(columns={'id': 'amount'}) \
        .head()

        counted_year_df = tracks\
            .assign(year_added=tracks.added_at.dt.year) \
            .groupby(['album_name', 'year_added']) \
            .count()['id'] \
            .reset_index() \
            .rename(columns={'id': 'amount'}) \
            .sort_values('amount', ascending=False)

        in_top_5_year_album = counted_year_df \
        .groupby('year_added') \
        .head(5) \
        .album_name \
        .unique()

        plot = counted_year_df \
        [counted_year_df.album_name.isin(in_top_5_year_album)] \
        .pivot('album_name', 'year_added') \
        .fillna(0) \
        .head(20)
        
        plt.style.use('dark_background')
        ax = plot.T.plot(kind='barh',figsize=(15, 10),width=5)
        ax.set_title('Top Albums', fontdict={'fontsize': 16, 'fontweight': 'medium'})
        ylab = ax.set_ylabel('m')
        xlab = ax.set_xlabel('Added')
        
        return ax
    
    def plot_artist(self):
        tracks = self.df
        t1 = tracks\
        .assign(year_added=tracks.added_at.dt.year)\
        .groupby(['artist','track_name']) \
        .count()['id'] \
        .reset_index() \
        .sort_values('id', ascending=False) \
        .rename(columns={'id': 'amount'}) \
        .head()

        counted_year_df = tracks\
            .assign(year_added=tracks.added_at.dt.year) \
            .groupby(['artist', 'year_added']) \
            .count()['id'] \
            .reset_index() \
            .rename(columns={'id': 'amount'}) \
            .sort_values('amount', ascending=False)

        in_top_5_year_artist = counted_year_df \
        .groupby('year_added') \
        .head(5) \
        .artist \
        .unique()

        plot = counted_year_df \
        [counted_year_df.artist.isin(in_top_5_year_artist)] \
        .pivot('artist', 'year_added') \
        .fillna(0) \
        .head(20)
       
        plt.style.use('dark_background')
        ax = plot.T.plot(kind='barh',figsize=(15, 10),width=5)
        ax.set_title('Top Artist', fontdict={'fontsize': 16, 'fontweight': 'medium'})
        ylab = ax.set_ylabel('m')
        xlab = ax.set_xlabel('Added')
        
        return ax
    
    def plot_tracks(self):
        tracks = self.df
        t1 = tracks\
        .assign(year_added=tracks.added_at.dt.year)\
        .groupby(['artist','track_name']) \
        .count()['id'] \
        .reset_index() \
        .sort_values('id', ascending=False) \
        .rename(columns={'id': 'amount'}) \
        .head()

        counted_year_df = tracks\
            .assign(year_added=tracks.added_at.dt.year) \
            .groupby(['track_name', 'year_added']) \
            .count()['id'] \
            .reset_index() \
            .rename(columns={'id': 'amount'}) \
            .sort_values('amount', ascending=False)

        in_top_5_year_tracks = counted_year_df \
        .groupby('year_added') \
        .head(5) \
        .track_name \
        .unique()\
        

        plot = counted_year_df \
        [counted_year_df.track_name.isin(in_top_5_year_tracks)] \
        .pivot('track_name', 'year_added') \
        .fillna(0) \
        .head(20)
        
        plt.style.use('dark_background')
        ax = plot.T.plot(kind='barh',figsize=(15, 10),width=5)
        ax.set_title('Top Tracks', fontdict={'fontsize': 16, 'fontweight': 'medium'})
        ylab = ax.set_ylabel('m')
        xlab = ax.set_xlabel('Added')
        
        return ax

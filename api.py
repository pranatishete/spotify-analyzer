from flask import Flask
from flask import Flask, render_template,request
import config
import requests
import base64
import datetime
import json
from urllib.parse import urlencode
import pandas as pd
from concurrent.futures import ThreadPoolExecutor as PoolExecutor
import http.client
import socket
import concurrent.futures
import urllib.request
import multiprocessing.pool
import SpotifyApi
from SpotifyApi import SpotifyAPI
import format
from format import Formatdata
import graphs 
from graphs import plotgraphs
import io
import base64
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from random import seed
from random import randint


app = Flask(__name__)
spotify = SpotifyAPI(config.client_id,config.client_secret) 
li = set()

@app.route('/',methods = ['POST', 'GET'])
def home():
    return render_template("index.html")

@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        concurrent = 200
        result = request.form['urllink']
        userid = result.split('?')[0].split('/')[-1]
        pool = multiprocessing.pool.ThreadPool(processes=concurrent)
        json_data = pool.map(spotify.get_it,spotify.get_playlist(userid),chunksize=1)
        pool.close()
        number_of_playlist = len(json_data)
        dataframe = Formatdata(json_data)
        total_tracks = dataframe.analyze_playlist().track_name.nunique()
        total_album = dataframe.analyze_playlist().album_name.nunique()
        total_artist = dataframe.analyze_playlist().artist.nunique()
        tracks = dataframe.analyze_playlist()
        graph = plotgraphs(tracks)
        tracks_graph = convert_plot(graph.plot_tracks())
        artist_graph = convert_plot(graph.plot_artist())
        album_graph = convert_plot(graph.plot_albums())
        print(album_graph)
        return render_template("Analysis.html",playlist=number_of_playlist,trackno =total_tracks,albumno = total_album,
                                artistno = total_artist,tracks_graph= tracks_graph,artist_graph= artist_graph,album_graph= album_graph)
    else:
        return render_template("index.html")

   
def convert_plot(im):
    fig = im.get_figure()
    value = randint(0,1000)
    if value in li:
        value = randint(value+1,value+1000)
    path = f"./static/images/Graph" + str(value) +".png"
    fig.savefig(path)
    return path
    


if __name__ == "__main__":
    app.run(debug=True)
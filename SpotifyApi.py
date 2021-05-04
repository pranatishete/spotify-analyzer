
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

class SpotifyAPI(object):
    
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"
    
    def __init__(self,client_id,client_secret,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.client_id = client_id
        self.client_secret = client_secret
        
    def get_client_credentials(self):
        
        client_id = self.client_id
        client_secret = self.client_secret
        if client_id == None or client_secret == None:
            raise Exception("You must set client_id and client_secret")
            
        client_creds =  f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        
        return client_creds_b64.decode()
            
        
      
    def get_token_header(self):
        client_creds_b64 = self.get_client_credentials()
        return {
             "Authorization": f"Basic {client_creds_b64}"  
              }
        
    def get_token_data(self):
        return {
             "grant_type" : "client_credentials"
            }
        
    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_header()
        r = requests.post(token_url,data = token_data,headers = token_headers)
        if r.status_code not in range(200,299):
            return False
        data = r.json()
        now = datetime.datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in']
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires<now
        return True
    
    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token == None:
            self.perform_auth()
            return self.get_access_token() 
        return token
         
    def get_resource_header(self):
        access_token = self.get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        return headers
        
        
    def get_resource(self, lookup_id, resource_type='albums', version='v1'):
        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{lookup_id}"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()
    
    def get_playlist(self,user_id):
        headers = self.get_resource_header()
        endpoint = f"https://api.spotify.com/v1/users/{user_id}/playlists"
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in (200,299):
            return {}
        parsed = json.loads(r.text)
        playlist = []
        for i in parsed["items"]:
            playlist.append(f"https://api.spotify.com/v1/playlists/{i['external_urls']['spotify'].split('/')[-1]}/tracks")
        return playlist
                            
    def get_it(self,url):
        headers = self.get_resource_header()
        r = requests.get(url, headers=headers)
        if r.status_code not in (200,299):
            return {}
        data = json.loads(r.text)
        return data   
   
from flask import Flask, render_template, url_for, request, session, redirect
import spotipy 
from spotipy.oauth2 import SpotifyOAuth
import time
import pprint
import json


'''SECTION 1: creating an instance of my Flask application, 
              and configuring cookies.'''


app = Flask(__name__, template_folder="templates")
app.config["KRABBY_PATTY_SECRET_FORMULA"] = 'ravioli.ravioli.give.me.the.formioli'
app.config["SESSION_COOKIE_NAME"] = "Spotify Cookie"
app.secret_key = "ravioli.ravioli.give.me.the.formioli"
TOKEN_INFO = "Token Info"


'''SECTION 2: section for defining necessary functions for the application.'''

#function works with Spotipy library to help facilitate user authentication/token
def create_spotify_oauth():
    return SpotifyOAuth(
        client_id = '103a19efe64d46208a7e965462c668b3',
        client_secret = "0487d4eee354456cbe28e4b2803f0ec7",
        redirect_uri = url_for("redirect_page", _external = True),
        scope = "user-modify-playback-state user-read-currently-playing user-library-read user-modify-playback-state playlist-read-private")

#retrieving saved token (from "redirect") from cookie
def get_token():
    token_info = session.get(TOKEN_INFO)
    if not token_info: # if no token, log user in
        redirect(url_for("oauth_user_login", external = False))

    #using time package, we can save current time to variable and then acess the "expires_at"
    #attribute in our token information to assess if it is/is about to expire
    now = int(time.time())
    token_expired = token_info['expires_at'] - now < 60 #if the time between now and the exp time is < 60sec, create this variable
    if token_expired: #if token_expired exists...
        spotify_oauth = create_spotify_oauth()
        token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])
        return token_info
    return token_info

'''SECTION 3: section for creating the routes of the app'''

@app.route("/")
def home(): #home page 
    
    return render_template ("welcome.html")

@app.route("/lets-begin")
def lets_begin(): #tansition page for orb "roll-out" animation
    
    return render_template("lets_begin.html")


@app.route("/search", methods=['POST', "GET"])
def search(): #spotify user ID page
    
    return render_template ("search.html")

@app.route("/submit-username", methods=['POST', "GET"])
def submit_user_name(): #page the the user is routed to after submitting ID
    name = request.form.get("user_name")
    
    return render_template ("submit_user.html", name=name)

@app.route('/user-playlists')
def landing():
    try: 
        # get the token info from the session
        token_info = get_token()
    except:
        # if the token info is not found, redirect the user to the login route
        print('User not logged in')
        return redirect("/login")

    # create a Spotipy instance with the access token
    sp = spotipy.Spotify(auth=token_info['access_token'])

    # get the user's playlists
    current_playlists =  sp.current_user_playlists()['items']

    playlist_names = []
    for playlist in current_playlists:
        playlist_name = playlist['name']
        playlist_names.append(playlist_name)


    return render_template ("user_playlists.html", playlist_names=playlist_names)

@app.route("/open-playlist", methods=['POST', "GET"])
def open_playlist():#opens playlist from "playlist_selection" form
    playlist_selection = request.form.get("playlist_selection")


    return render_template ("open_playlist.html", playlist_selection=playlist_selection)


@app.route("/login")
def oauth_user_login(): #using Spotipy package to help direct user to login page
    auth_url = create_spotify_oauth().get_authorize_url()
    
    return redirect(auth_url)

@app.route("/redirect")
def redirect_page(): #creating access token for API
    session.clear()
    code = request.args.get('code') #auth code included in request paramaters is extracted
    token_info = create_spotify_oauth().get_access_token(code) #generating token with auth code
    session[TOKEN_INFO] = token_info #storing token in cookie session

    return redirect(url_for("landing"))

if __name__ == "__main__":
    app.run(debug = True)
    


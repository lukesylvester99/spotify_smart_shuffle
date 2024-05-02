from flask import Flask, render_template, url_for, request, session, redirect
import spotipy #helps w/ working w/ spotify api
from spotipy.oauth2 import SpotifyOAuth #method assists w/ confirming user authorization for app
import time #for cookies
import requests #needed to retrieve numbers from random.org
import pprint
from collections import defaultdict


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
        scope = "user-modify-playback-state user-read-currently-playing user-library-read user-modify-playback-state playlist-read-private user-read-playback-state user-read-currently-playing")

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

#gets a list of random numbers from random.org, using atomospheric noise
def get_random_nums(song):
    url = "https://www.random.org/integers/?num=1&min=1&max=1000&col=1&base=10&format=plain&rnd=new"
    number = requests.get(url)

    number_int = int(number.text)
    temp_dict = {song:number_int}

    return temp_dict

#merge sort functions
def merge(left, right):
    result = []
    i,j = 0, 0
    while i<len(left) and j<len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result += left[i:]
    result += right[j:]
    return result

def merge_sort(lst):
    if len(lst) <= 1:
        return lst
    mid = len(lst)//2
    left = merge_sort(lst[:mid])
    right = merge_sort(lst[mid:]) 
    return merge(left, right)

'''SECTION 3: section for creating the routes of the app'''

'''SECTION 3A: home and about pages'''
@app.route("/")
def home(): #home page 
    
    return render_template ("welcome.html")

@app.route("/lets-begin")
def lets_begin(): #tansition page for orb "roll-out" animation
    
    return render_template("lets_begin.html")

@app.route("/about-app")
def about_app(): #page describes how the application works
    
    return render_template("about_app.html")

'''SECTION 3B: control the login-logic of the app. Help direct users to spotify's login and 
               authentication pages so that they can use the application.'''

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


'''SECTION 3C: User selects a playlist from their library'''
@app.route('/user-playlists')
def landing():#
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

track_name_id = {} #initializing to hold id of tracks. Needed it to be out of the fxn so that I can access this later in "randomize"
@app.route("/open-playlist", methods=['POST', "GET"])
def open_playlist():#opens playlist from "playlist_selection" form
    track_name_id.clear() #clearing old values from dict
    playlist_selection = request.form.get("playlist_selection") #gather selection from form on previous page

    #see above route for questions:
    try: 
        token_info = get_token()
    except:
        print('User not logged in')
        return redirect("/login")

    sp = spotipy.Spotify(auth=token_info['access_token'])
    current_playlists =  sp.current_user_playlists()['items']

    playlist_id = None #initializing it so that the next "if" statement works
    for playlist in current_playlists:
        if playlist['name'] == playlist_selection: #if the playlist name is the same as the selection from our form...
            playlist_id = playlist['id']#get the id element. We need this for 'opening' the playlist in the next step
    
    track_names = [] #list to hold our track names
    if playlist_id: #if we have an id...
        playlist_elements = sp.playlist_items(playlist_id, fields="items")
        #"items" is a naming convention that spotipy uses in their dictionary formatting
        playlist_items = playlist_elements['items'] #"items" hold key:value pairs with info about the tracks

        
        for item in playlist_items: 
            track_name = item['track']['name'] #get the 'name' element of the dictionary
            track_names.append(track_name)

            track_id = item['track']['id'] #get the 'id' element of the dictionary
            track_name_id[track_name] = track_id #creating entry in the "track_name_id" dict

        session['track_names'] = track_names #save to the session so I can get it later

    return render_template ("open_playlist.html", playlist_selection=playlist_selection, track_names=track_names)

@app.route("/randomize", methods=['POST', "GET"])
def randomize():
    track_names =session.get("track_names") #get track list from session
    
    track_number_pairs = {} #initializing a dict to hold our tracks, which have now been assigned a #
    for track in track_names:
        result = get_random_nums(track) #call random num generator funct
        track_number_pairs.update(result)

    number_list = []
    for key in track_number_pairs:
        number_list.append(track_number_pairs[key])
    
    sorted_number_list = merge_sort(number_list)

    ordered_tracks = [] #initializing a list to hold re-ordered tracks
    for number in sorted_number_list: #iterate through sorted num list
        for song, value in track_number_pairs.items():
            if value == number and song not in ordered_tracks: #if sorted number is the same as the randomly assigned number and it isnt already added...
                ordered_tracks.append(song) #Add song to initalized list
                break
    try: 
        token_info = get_token()
    except:
        print('User not logged in')
        return redirect("/login")

    sp = spotipy.Spotify(auth=token_info['access_token'])

    for song in ordered_tracks:
        for key, value in track_name_id.items():
            if key == song:
                sp.add_to_queue(value, device_id=None)


    return render_template("randomize.html", track_names=ordered_tracks)
    
"""route was used to test the randomness of my algorithm vs the Spotify shuffle algorithm. This route does not actually cause 
the website to "do" anything, but when the user goes to it, it exectutes the following code. The song_frequency dict is used to hold
a tally for the amount of times that a certain song is added to the first ten spots of the queue"""

song_frequency = defaultdict(int)  # Dictionary to store song tallys
@app.route("/testing", methods=['POST', "GET"])
def testing():
    try: 
        token_info = get_token()
    except:
        print('User not logged in')
        return redirect("/login")
    
    sp = spotipy.Spotify(auth=token_info['access_token'])
    current_queue =  sp.queue()["queue"] #function retrieves a user's active queue

    songs = [] #itializing a list
    for song in current_queue:
        song_name = song['name']  # Accessing the name of the song 
        songs.append(song_name) #save song name to list

    first_10_songs = songs[:10]  # Get the first 10 songs on the queue
    
    for song in first_10_songs:
        song_frequency[song] += 1  # Increment the count for each song
    
    print(song_frequency)


    
    
    return current_queue

"""the "/testing' route was used to tally the amount of times that a song appears in the first 10 tracks of the user's current queue. Ten trials were 
conducted for both the Fortuna algorithm and the spotify algorith. This same test was done on a playlist 20 songs in length, and then again for a 
playlist 50 songs in length. The results of each tally are saved here in seperate dictionaries."""

#Experiment 1: 20 song playlist depth
spotify_20_songs = {'Sweetest Devotion': 7, 'Milk & Honey': 6, 'Atmosphere': 8, 'altar': 8, 'If Only for Tonight': 5, 'Slide Away': 6, 'Party (feat. André 3000)': 7, 'The Dress': 6, 'Always Been U': 5, 'How Deep Is Your Love': 4, 'You Make Me Feel Like Dancing - Remastered': 4, 'Shrike': 4, 'Nobody': 4, 'Pressure': 4, 'Mannequin': 6, 'Indigo': 4, 'Semi Pro': 4, 'A Little Honey': 4, 'Better Days (NEIKED x Mae Muller x Polo G)': 4}
spotify_num_unique_songs_20 = 0
spotify_songs_over5_20 = 0
fortuna_20_songs = {'Atmosphere': 5, 'How Deep Is Your Love': 8, 'Shrike': 4, 'Mannequin': 6, 'I Drink Wine': 6, 'Semi Pro': 5, 'Better Days (NEIKED x Mae Muller x Polo G)': 4, 'Party (feat. André 3000)': 7, 'You Make Me Feel Like Dancing - Remastered': 3, 'Indigo': 7, 'A Little Honey': 4, 'Sweetest Devotion': 3, 'Milk & Honey': 7, 'Always Been U': 7, 'altar': 6, 'The Dress': 5, 'Nobody': 3, 'Slide Away': 3, 'If Only for Tonight': 4, 'Pressure': 3}
fortuna_num_unique_songs_20 = 0
fortuna_songs_over5_20 = 0

 #Experiment 2: 50 song playlist depth   
spotify_50_songs = {'Ur Mum': 3, 'Getting Started': 5, 'Into Your Room': 6, 'Pink Friday Girls': 5, 'Beautiful Things': 2, 'Sunny Countryside': 1, 'Dance For Love': 3, 'Leon': 2, 'Chaise Longue': 2, "TEXAS HOLD 'EM": 2, 'Piece Of Shit': 3, 'Limitless Love': 3, 'The Last One': 5, 'Tangerine': 2, 'Poison Poison': 1, 'Will We Talk?': 3, 'Bells Of Every Chapel [Feat. Billy Strings]': 2, 'Scared To Start': 2, 'Shine': 2, 'After The Earthquake': 3, "When I'm Gone": 3, 'Sadie': 3, 'Cosmos': 3, 'Are You Gone Already': 2, 'Are You Ready to Love Me?': 1, 'Sweet Mariona': 2, 'Stay For A While': 1, 'Sofa King': 1, 'Being In Love': 1, 'I Hope It All Works Out': 2, 'I’m The Best': 2, 'Summertime With U': 2, 'Seventeen Going Under': 2, 'Beep Beep': 1, 'Wet Dream': 2, 'Paper Bag': 3, 'Yes Chef': 1, 'Just The Memories': 2, 'Alabama': 1, 'Before You': 1, 'The Garden - from The Hunger Games: The Ballad of Songbirds & Snakes': 1, 'Next To You': 2, 'No California': 1, 'Bahm Bahm': 1, 'Hey Mama': 1, 'Better Than the Boys': 1}
spotify_num_unique_songs_50 = 0
spotify_songs_over4_50 = 0
fortuna_50_songs = {'Poison Poison': 2, 'Sofa King': 4, 'Just The Memories': 2, "TEXAS HOLD 'EM": 2, 'Tangerine': 4, 'Summertime With U': 2, 'Next To You': 3, 'No California': 3, 'Stay For A While': 2, 'Into Your Room': 3, 'Leon': 2, 'Waterfall': 3, 'Shine': 3, 'Let Me Calm Down (feat. J. Cole)': 1, 'Beautiful Things': 3, 'Yes Chef': 2, 'Bahm Bahm': 2, 'Pink Friday Girls': 2, 'Piece Of Shit': 3, 'After The Earthquake': 3, 'Are You Ready to Love Me?': 2, 'Bells Of Every Chapel [Feat. Billy Strings]': 2, 'Getting Started': 1, 'Limitless Love': 2, 'Sunny Countryside': 3, 'Wet Dream': 3, 'Hey Mama': 2, 'Dance For Love': 1, 'Will We Talk?': 4, 'Seventeen Going Under': 3, 'Chaise Longue': 2, 'Ur Mum': 1, 'The Garden - from The Hunger Games: The Ballad of Songbirds & Snakes': 2, 'Before You': 1, 'Being In Love': 3, 'Sadie': 3, 'Are You Gone Already': 1, 'The Last One': 1, 'Scared To Start': 2, 'Better Than the Boys': 2, 'My Kink Is Karma': 2, 'I Hope It All Works Out': 1, 'I’m The Best': 2, 'Cosmos': 1, 'Paper Bag': 1, 'Beep Beep': 1}
fortuna_num_unique_songs_50 = 0
fortuna_songs_over4_50 = 0

for song in spotify_20_songs:
    spotify_num_unique_songs_20 += 1

for song in fortuna_20_songs:
    fortuna_num_unique_songs_20 += 1

for song in spotify_50_songs:
    spotify_num_unique_songs_50 += 1

for song in fortuna_50_songs:
    fortuna_num_unique_songs_50 += 1

print("20 songs:")
print(spotify_num_unique_songs_20)
print(fortuna_num_unique_songs_20)

print()
print("50 songs:")
print(spotify_num_unique_songs_50)
print(fortuna_num_unique_songs_50)

for key, value in spotify_20_songs.items():
    if spotify_20_songs[key] > 5:
        spotify_songs_over5_20 += 1

for key, value in fortuna_20_songs.items():
    if fortuna_20_songs[key] > 5:
        fortuna_songs_over5_20 += 1

for key, value in spotify_50_songs.items():
    if spotify_50_songs[key] > 4:
        spotify_songs_over4_50 += 1

for key, value in fortuna_50_songs.items():
    if fortuna_50_songs[key] > 4:
        fortuna_songs_over4_50 += 1

print()
print("20 songs, over 5:")
print(spotify_songs_over5_20)
print(fortuna_songs_over5_20)

print()
print("50 songs, over 4:")
print(spotify_songs_over4_50)
print(fortuna_songs_over4_50)





'''!!!! DEAD !!!!'''
@app.route("/search", methods=['POST', "GET"])
def search(): #spotify user ID page
    
    return render_template ("search.html")

'''!!!! DEAD !!!!'''
@app.route("/submit-username", methods=['POST', "GET"])
def submit_user_name(): #page the the user is routed to after submitting ID
    name = request.form.get("user_name")
    
    return render_template ("submit_user.html", name=name)

if __name__ == "__main__":
    app.run(debug = True)
    


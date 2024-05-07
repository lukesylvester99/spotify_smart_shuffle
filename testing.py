import matplotlib.pyplot as plt



"""the "/testing' route was used to tally the amount of times that a song appears in the first 10 tracks of the user's current queue.
The results of that experiment have been saved here in the following variables. 

Ten trials were conducted for both the Fortuna algorithm and the Spotify algorithim. In each trial the two algorithims were used to shuffle
a playlist 20 songs in length, and then again for a playlists 50 and 100 songs in length. The results of each tally are saved here in seperate dictionaries."""

#Condition 1: 20 song playlist depth
#each dict. is a copy of the "Song Frequency" variable (from the /testing route), which was manually cleared after each trial
spotify_20_songs = {'Sweetest Devotion': 7, 'Milk & Honey': 6, 'Atmosphere': 8, 'altar': 8, 'If Only for Tonight': 5, 'Slide Away': 6, 'Party (feat. André 3000)': 7, 'The Dress': 6, 'Always Been U': 5, 'How Deep Is Your Love': 4, 'You Make Me Feel Like Dancing - Remastered': 4, 'Shrike': 4, 'Nobody': 4, 'Pressure': 4, 'Mannequin': 6, 'Indigo': 4, 'Semi Pro': 4, 'A Little Honey': 4, 'Better Days (NEIKED x Mae Muller x Polo G)': 4}
fortuna_20_songs = {'Atmosphere': 5, 'How Deep Is Your Love': 8, 'Shrike': 4, 'Mannequin': 6, 'I Drink Wine': 6, 'Semi Pro': 5, 'Better Days (NEIKED x Mae Muller x Polo G)': 4, 'Party (feat. André 3000)': 7, 'You Make Me Feel Like Dancing - Remastered': 3, 'Indigo': 7, 'A Little Honey': 4, 'Sweetest Devotion': 3, 'Milk & Honey': 7, 'Always Been U': 7, 'altar': 6, 'The Dress': 5, 'Nobody': 3, 'Slide Away': 3, 'If Only for Tonight': 4, 'Pressure': 3}


#Condition 2: 50 song playlist depth   
spotify_50_songs = {'Ur Mum': 3, 'Getting Started': 5, 'Into Your Room': 6, 'Pink Friday Girls': 5, 'Beautiful Things': 2, 'Sunny Countryside': 1, 'Dance For Love': 3, 'Leon': 2, 'Chaise Longue': 2, "TEXAS HOLD 'EM": 2, 'Piece Of Shit': 3, 'Limitless Love': 3, 'The Last One': 5, 'Tangerine': 2, 'Poison Poison': 1, 'Will We Talk?': 3, 'Bells Of Every Chapel [Feat. Billy Strings]': 2, 'Scared To Start': 2, 'Shine': 2, 'After The Earthquake': 3, "When I'm Gone": 3, 'Sadie': 3, 'Cosmos': 3, 'Are You Gone Already': 2, 'Are You Ready to Love Me?': 1, 'Sweet Mariona': 2, 'Stay For A While': 1, 'Sofa King': 1, 'Being In Love': 1, 'I Hope It All Works Out': 2, 'I’m The Best': 2, 'Summertime With U': 2, 'Seventeen Going Under': 2, 'Beep Beep': 1, 'Wet Dream': 2, 'Paper Bag': 3, 'Yes Chef': 1, 'Just The Memories': 2, 'Alabama': 1, 'Before You': 1, 'The Garden - from The Hunger Games: The Ballad of Songbirds & Snakes': 1, 'Next To You': 2, 'No California': 1, 'Bahm Bahm': 1, 'Hey Mama': 1, 'Better Than the Boys': 1}
fortuna_50_songs = {'Poison Poison': 2, 'Sofa King': 4, 'Just The Memories': 2, "TEXAS HOLD 'EM": 2, 'Tangerine': 4, 'Summertime With U': 2, 'Next To You': 3, 'No California': 3, 'Stay For A While': 2, 'Into Your Room': 3, 'Leon': 2, 'Waterfall': 3, 'Shine': 3, 'Let Me Calm Down (feat. J. Cole)': 1, 'Beautiful Things': 3, 'Yes Chef': 2, 'Bahm Bahm': 2, 'Pink Friday Girls': 2, 'Piece Of Shit': 3, 'After The Earthquake': 3, 'Are You Ready to Love Me?': 2, 'Bells Of Every Chapel [Feat. Billy Strings]': 2, 'Getting Started': 1, 'Limitless Love': 2, 'Sunny Countryside': 3, 'Wet Dream': 3, 'Hey Mama': 2, 'Dance For Love': 1, 'Will We Talk?': 4, 'Seventeen Going Under': 3, 'Chaise Longue': 2, 'Ur Mum': 1, 'The Garden - from The Hunger Games: The Ballad of Songbirds & Snakes': 2, 'Before You': 1, 'Being In Love': 3, 'Sadie': 3, 'Are You Gone Already': 1, 'The Last One': 1, 'Scared To Start': 2, 'Better Than the Boys': 2, 'My Kink Is Karma': 2, 'I Hope It All Works Out': 1, 'I’m The Best': 2, 'Cosmos': 1, 'Paper Bag': 1, 'Beep Beep': 1}

#Condition 3: 100 song playlist depth   
spotify_100_songs = {'Brightsider': 3, 'Slide Away': 2, 'Everybody Else': 2, 'Atmosphere': 1, 'The Otter': 1, '2 You': 4, 'CUFF IT': 2, 'One of These Days': 1, 'Daylight': 4, 'altar': 2, 'Satellite': 1, 'Night Drive': 2, "That's Where It's At": 1, 'Devils in the Canyon': 2, 'Balenciaga': 1, 'Somehow, Someway': 3, 'If Only for Tonight': 2, 'In Dreams': 2, 'Easy on the Eyes': 2, 'Game Winner - Stadium Version': 1, 'Boardwalk': 2, 'Haines St. Station': 1, 'Honey': 1, "Don't Wanna Be Without Ya": 2, 'BLONDE': 3, 'I Drink Wine': 1, 'Always Been U': 1, 'I Get Up': 1, 'Habit': 1, 'Milk & Honey': 1, 'Black Tame': 2, 'Everybody You Hurt': 2, "You've Really Got A Hold On Me": 1, 'Cherry': 2, "Rome (Wasn't Built In A Day)": 1, 'BROOKLYN': 2, 'Talk It Up': 1, 'Pull It Together': 2, 'Looking At Me Like That': 1, 'Sweetest Devotion': 1, 'Flower Girl': 1, 'Pocket Full Of Gold': 1, 'Late Night Talking': 1, 'Carried Away': 2, 'Love on the Weekend': 2, 'Strawberry Wine': 2, 'The Last of the Honey Bees': 1, 'Cynic': 2, 'The Dress': 2, 'Good Morning': 1, 'Pretty': 1, 'Mannequin': 1, 'Wavelength': 1, 'Indigo': 1, 'Briggs': 1, 'Breaking Myself': 1, 'A Little Honey': 1, 'Mango': 1, 'Hello Beautiful': 1, 'Colors': 1, 'Love You Like That': 1, 'The Kiss Of Venus (Dominic Fike)': 1, 'Liquor Store': 1, 'Oogum Boogum Song': 1, 'Freida': 1, 'Range Rover': 1, 'Pop Game': 1}
fortuna_100_songs = {'Apple Tree Blues': 1, 'Better Days (NEIKED x Mae Muller x Polo G)': 1, 'Figure It Out': 2, 'Guiding Light': 1, 'I Get Up': 3, 'Party (feat. André 3000)': 1, 'The Last of the Honey Bees': 1, 'Honey': 2, 'Pull It Together': 2, "Rome (Wasn't Built In A Day)": 2, 'BROOKLYN': 2, 'BLONDE': 1, 'Liquor Store': 2, 'CUFF IT': 1, 'Devils in the Canyon': 1, 'In Dreams': 2, 'Everybody Else': 1, 'Atmosphere': 3, 'Shock Flesh': 3, 'Little Freak': 2, 'Milk & Honey': 1, 'Late Night Talking': 1, 'Satan & the Sailor': 2, 'Love You Like That': 2, 'This One': 1, 'Shrike': 1, 'Black Tame': 2, 'Cherry': 1, 'Colors': 2, 'The Dress': 1, 'Balenciaga': 3, 'honey': 2, 'Hello Beautiful': 1, 'The Kiss Of Venus (Dominic Fike)': 2, 'Ride or Die (feat. Foster the People)': 1, 'Dancing On Glass': 3, 'Boardwalk': 2, 'Gonna Get Over You': 3, 'Habit': 1, 'Pocket Full Of Gold': 2, 'Love on the Weekend': 2, 'Always Been U': 2, 'Pop Game': 1, 'All the Time in the World': 1, 'Night Drive': 2, 'Range Rover': 1, 'Wavelength': 2, 'New Religion': 1, 'Satellite': 1, 'Mannequin': 1, 'Haines St. Station': 1, 'Caroline': 1, '2 You': 2, 'Game Winner - Stadium Version': 1, 'Easy on the Eyes': 2, 'One of These Days': 1, 'How Deep Is Your Love': 1, "You've Really Got A Hold On Me": 1, 'Freida': 1, 'Flower Girl': 1, 'Clarity': 1, 'Carried Away': 1, 'Somehow, Someway': 1, 'Spaceship': 1, 'Oogum Boogum Song': 1, 'Somebody': 1}

""" These variables represent the amount of unique songs that appear in each
experimental group: 
Condition 1 - spotify vs fortuna with 20 song playlist depth; 
Condition 2 - spotify vs fortuna with 50 song playlist depth;
Condition 3 - spotify vs fortuna with 100 song playlist depth """

spotify_num_unique_songs_20 = len(spotify_20_songs)
fortuna_num_unique_songs_20 = len(fortuna_20_songs)

spotify_num_unique_songs_50 = len(spotify_50_songs)
fortuna_num_unique_songs_50 = len(fortuna_50_songs)

spotify_num_unique_songs_100 = len(spotify_100_songs)
fortuna_num_unique_songs_100 = len(fortuna_100_songs)



"""These variables represent the amount of unique songs that had a tally lager than a threshold of 3.
For example, in Condition 1 (playlist depth of 20 songs), if a song appeared more than 3 times in the top 10 tracks 
of a user's queue, the "spotify_songs_over3_20" variable would increase by 1."""

spotify_songs_over3_20 = 0 #intialized at zero so that they can be
fortuna_songs_over3_20 = 0 #used in the "for" loops

spotify_songs_over3_50 = 0
fortuna_songs_over3_50 = 0

spotify_songs_over3_100 = 0
fortuna_songs_over3_100 = 0


for key, value in spotify_20_songs.items():
    if spotify_20_songs[key] > 3:
        spotify_songs_over3_20 += 1

for key, value in fortuna_20_songs.items():
    if fortuna_20_songs[key] > 3:
        fortuna_songs_over3_20 += 1


for key, value in spotify_50_songs.items():
    if spotify_50_songs[key] > 3:
        spotify_songs_over3_50 += 1

for key, value in fortuna_50_songs.items():
    if fortuna_50_songs[key] > 3:
        fortuna_songs_over3_50 += 1


for key, value in spotify_100_songs.items():
    if spotify_100_songs[key] > 3:
        spotify_songs_over3_100 += 1

for key, value in fortuna_100_songs.items():
    if fortuna_100_songs[key] > 3:
        fortuna_songs_over3_100 += 1



"""script for creating bar charts of the data represented above"""

#Figure 1: Bar chart for the number of unique songs for each experimental group, in each condition

categories = ["Spotify, 20", "Fortuna, 20", "Spotify, 50", "Fortuna, 50","Spotify, 100", "Fortuna, 100"]
values = [spotify_num_unique_songs_20, fortuna_num_unique_songs_20, spotify_num_unique_songs_50, fortuna_num_unique_songs_50, spotify_num_unique_songs_100, fortuna_num_unique_songs_100]
colors = ["#008080", "#008080", '#400080', '#400080', "#800000","#800000"]

plt.figure(figsize=(10, 8.5))
plt.bar(categories, values, color=colors)

"""iterating through values to add data labels. 'i' represents the index of the current value in the loop,
 which corresponds to the position of the bar on the x-axis. The syntax of the .text function is 'plt.text(x, y, text)',
 so 'i' is used here as the x-coordinate for the label. 'value = 0.5' is used to float the data label over the bar"""
for i, value in enumerate(values):
    plt.text(i, value + 0.5, str(value), ha='center', va='bottom') 
    #ha='center' centers text horizontally, va='bottom'aligns the text with the bottom of the text box

plt.ylabel('Number of Songs', fontsize=13, color='navy')
plt.title('Number of Unique Songs Added to First 10 Tracks of Queue', fontsize=14, fontweight='bold', color='navy')
plt.xticks(rotation=45, fontsize=10, color='navy')  # Rotate x-axis labels and set font size
plt.yticks(fontsize=10) 

# Remove top and right spines
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

plt.savefig('figures/figure1.png')
plt.show()



#Figure 2: Bar chart for the number of songs over a specific threashold for each experimental group, in each condition

categories = ["Spotify, 20", "Fortuna, 20", "Spotify, 50", "Fortuna, 50","Spotify, 100", "Fortuna, 100"]
values = [spotify_songs_over3_20, fortuna_songs_over3_20, spotify_songs_over3_50, fortuna_songs_over3_50, spotify_songs_over3_100, fortuna_songs_over3_100]
colors = ["#008080", "#008080", '#400080', '#400080', "#800000","#800000"]

plt.figure(figsize=(10, 8.5))
plt.bar(categories, values, color=colors)

for i, value in enumerate(values): #see figure 1 for information about 'for loop'
    plt.text(i, value + 0.05, str(value), ha='center', va='bottom') 


plt.ylabel('Number of Songs', fontsize=13, color='navy')
plt.title('Amount of Songs With Frequency Over 3 in First 10 Tracks', fontsize=14, fontweight='bold', color='navy')
plt.xticks(rotation=45, fontsize=10, color='navy')  # Rotate x-axis labels and set font size
plt.yticks(fontsize=10) 


# Remove top and right spines
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

plt.savefig('figures/figure2.png')
plt.show()



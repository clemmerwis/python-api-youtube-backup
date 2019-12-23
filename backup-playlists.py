#! python3
import time, os, sys, openpyxl, re, json, re 
import urllib.request
from pytube import YouTube
from pathlib import Path

# playlist = sys.argv[1]

# Functions
def create_playlists_url(channel_id, api_key):
  api_playlists_url = f"https://www.googleapis.com/youtube/v3/playlists?part=snippet&maxResults=50&channelId={channel_id}&key={api_key}"
  return api_playlists_url

def create_playlistitems_url(playlist_id, api_key):
  api_playlistitems_url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId={playlist_id}&key={api_key}"
  return api_playlistitems_url

def get_data_dict(url):
  json_url = urllib.request.urlopen(url)
  data = json.loads(json_url.read())
  return data

def create_playlists_dict(data_dict):
  plist_dict = {}  
  i = 0
  while i < len(data_dict['items']):
    plist_title = data_dict['items'][i]['snippet']['title']
    plist_id = data_dict['items'][i]['id']
    plist_dict.update( {plist_title : plist_id} )
    i += 1
  return plist_dict

def create_playlists_items_dict(data_dict):
  videos_dict = {}  
  i = 0
  while i < len(data_dict['items']):
    video_title = data_dict['items'][i]['snippet']['title']
    video_description = data_dict['items'][i]['snippet']['description']
    videos_dict.update( {video_title : video_description} )
    i += 1
  return videos_dict

def check_playlist_pagetoken(data_dict):
  token = ''
  try:
    token = data_dict['nextPageToken']
  except:
    token = '' 
  return token

def swap_scrub_title_as_dictvalue(playlists_dict):
  playlists_titles = {}
  for k_playlist_title in playlists_dict.keys():
    folder_title = scrub_title(k_playlist_title)
    # playlists_dict[k_playlist_title] = folder_title
    playlists_titles.update( {k_playlist_title : folder_title} ) 
  return playlists_titles

def create_Playlists_directory_if_needed(playlists_titles_dict):
  data_folder = Path("C:/Users/clemmer/myComp/code/python/JBS Playlists")
  for v in playlists_titles_dict.values():
    dir_name = v
    dir_path = data_folder / dir_name
    # Create directory if don't exist
    if not os.path.exists(dir_path):
      os.mkdir(dir_path)

def get_max_row(active_sheet):
  maxRow = None
  counter = 2 #start on row after header
  while (counter < (active_sheet.max_row + 1)):
    currentA = "A" + str(counter)
    valA = active_sheet[currentA].value
    if valA == None:
      maxRow = int(counter)
      break
    counter = counter + 1

  if maxRow == None:
    maxRow = active_sheet.max_row + 1
  return maxRow

def scrub_title(stitle):
  stitle = re.sub("[,']+", "", stitle)
  stitle = re.sub("[|]+", "-", stitle)
  return stitle

def list_playlists_ids(playlists_dict):
  for k, v in playlists_dict.items():
    print()
    print(k)
    print(v)

# Vars
# ------
secrets = 'client_secret.json'
channel_id = 'UCD_PvRz7fvX9WOBL6T4P45Q'
api_key = 'AIzaSyBAdbm6MkWm_2HbDfXnbRWmbKYTRPmOHfY'
# api_single_playlist_url = f"https://www.googleapis.com/youtube/v3/playlists?part=snippet&id={cc_playlist_id}&key={api_key}"

data_folder = Path("C:/Users/clemmer/myComp/code/python/JBS Playlists")
excel_file_name = "masterfile.xlsx"
excel_file = data_folder / excel_file_name
log_file_name = "log.txt"
logfile = data_folder / log_file_name

# Start
# ------
#create files and/or clear contents
file_to_write_to = open(logfile, "a+", encoding='utf-8')
file_to_write_to.truncate(0)
f = file_to_write_to

# start excel
wb = openpyxl.load_workbook(excel_file)
ws = wb.active
maxRow = get_max_row(ws)
print("Max Row: " + str(maxRow))

# dictionary of playlists' titles & ids 
api_playlists_url = create_playlists_url(channel_id, api_key)
playlists_data = get_data_dict(api_playlists_url)
playlists = create_playlists_dict(playlists_data)

# dictionary of playlists' titles & folder titles
playlists_titles = swap_scrub_title_as_dictvalue(playlists)

# Make sure playlist directories exist
create_Playlists_directory_if_needed(playlists_titles)

# list_playlists_ids(playlists)

straight_talk_id = 'PLS2zYUkKepApRcUKYZfjkK8osX1d80OCj'
constitution_corner = 'PLS2zYUkKepApRgl-ftmCeafG-A-gSZg4Z'

# after getting dict made, check for page token, and remake url and scrape again if needed
# def backup_playlist(playlist_id):
  # make api_url
api_key = 'AIzaSyBAdbm6MkWm_2HbDfXnbRWmbKYTRPmOHfY'
api_playlistitems_url = create_playlistitems_url(straight_talk_id, api_key)

# get videos
playlist_items_data = get_data_dict(api_playlistitems_url)
playlist_items = create_playlists_items_dict(playlist_items_data)
# Check for page token
token = check_playlist_pagetoken(playlist_items_data)
while token != '':
  token_in_url = f"&pageToken={token}"
  next_api_playlistsitems_url = api_playlistitems_url + token_in_url
  next_playlists_items_data = get_data_dict(next_api_playlistsitems_url)
  new_playlist_items = create_playlists_items_dict(next_playlists_items_data)
  playlist_items.update(new_playlist_items)
  token = check_playlist_pagetoken(next_playlists_items_data)
# backup_playlist(straight_talk_id)

f.close()
wb.save(excel_file)
# Description: This script performs multiple tasks related to YouTube videos and OpenAI transcription.
# It automates the process of searching YouTube videos based on queries, downloading them,
# and generating summarized transcripts using OpenAI's GPT-3.5 Turbo.
#
# Usage Example: python youtube_to_summarize.py --number_of_videos 5 --search_queries "software-as-a-service" "SaaS" --download_videos True
#
# Author: Samuel Braun (2023)

import argparse  #For parsing command-line arguments
from pytubefix import YouTube  #For YouTube video downloading
from selenium import webdriver  #For web scraping
from selenium.webdriver.common.by import By  #For locating elements
from selenium.webdriver.support import expected_conditions as EC  #For conditional waits
from selenium.webdriver.support.ui import WebDriverWait  #For explicit waits
import os  #For file and directory manipulation
import re  #For regular expressions
import time  #For sleep
import openai  #For OpenAI GPT-3.5 Turbo API

#Function to sanitize filenames
def sanitize_filename(filename):
    filename = filename.strip()
    filename = filename.replace(" ", "_")
    filename = re.sub(r'[^\w\-]', '', filename)
    return filename

def main(number_of_videos, search_queries, download_videos):

    #Setup Selenium and OpenAI
    print("Setting driver and API keys....")
    driver = webdriver.Chrome(executable_path=r'C:\Users\samlb\Downloads\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe')
    openai.api_key = (open(r'C:\Users\samlb\Downloads\api_key\open_ai_api_key.txt', 'r').read()).strip()

    #Use command line arguments
    number_of_videos = args.number_of_videos
    search_queries = args.search_queries
    download_videos = args.download_videos

    # Check and create the 'summarized transcripts' directory
    summarized_transcripts_path = os.path.join(os.getcwd(), 'summarized transcripts')
    if not os.path.exists(summarized_transcripts_path):
        os.makedirs(summarized_transcripts_path)

    # Check and create the 'audios' directory
    audios_path = os.path.join(os.getcwd(), 'audios')
    if not os.path.exists(audios_path):
        os.makedirs(audios_path)

    #Remove old audio files
    print("Cleaning directories....")
    for filename in os.listdir(os.getcwd() + '\\audios'):
        file_path = os.path.join(os.getcwd() + '\\audios', filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    #Remove old summarized transcripts
    for filename in os.listdir(os.getcwd() + '\\summarized transcripts'):
        file_path = os.path.join(os.getcwd() + '\\summarized transcripts', filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    #Main loop for each search query
    for counter in search_queries:
        print("Getting YouTube videos....")
        driver.get(f"https://www.youtube.com/results?search_query={counter}")

        videos = []
        while len(videos) < number_of_videos:
            #Wait for video elements to be located
            videos = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ytd-video-renderer.style-scope.ytd-item-section-renderer[bigger-thumbs-style="DEFAULT"]')))
            time.sleep(1)
            #Scroll to load more videos
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        #Limit the videos to the number specified
        videos = videos[0:number_of_videos]

        if not download_videos:
            print("Please download the following links: \n")

        print("Downloading YouTube videos....\n")
        for video in videos:
            video_link = WebDriverWait(video, 20).until(EC.presence_of_element_located((By.ID, 'thumbnail'))).get_attribute('href')

            if not download_videos:
                print(video_link)
            else:
                yt = YouTube(video_link)
                title = sanitize_filename(yt.title) + '.mp3'
                ys = yt.streams.get_audio_only()
                ys.download(os.getcwd() + '\\audios', filename=title)
                print(f"File size: {ys.filesize_mb} MB")
                if ys.filesize_mb > 25:
                    print(f"{title} too large (over 25 MB). Skipping....")
                    os.remove(os.getcwd() + '\\audios\\' + title)
                else:
                    print(title+" video downloaded.")

        if not download_videos:
            input("Hit any character then hit Enter once all audios have been downloaded (mp3) and put into the 'audios' directory in " + os.getcwd() + ": ")

        #Process each downloaded audio file
        print("\nBeginning transcribe and summarize process....\n")
        for filename in os.listdir(os.getcwd() + '\\audios'):
            filepath = os.path.join(os.getcwd() + '\\audios', filename)

            #Transcribe the audio file
            print("Transcribing "+filename+"....")
            with open(filepath, "rb") as audio_file:
                transcript = openai.Audio.transcribe("whisper-1", audio_file)
            
            #Generate a summary of the transcript
            print("Summarizing "+filename+" transcript....")
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"Summarize the following transcript: "+transcript['text']},
                ]
            )

            summarized_transcript = response['choices'][0]['message']['content']

            #Save the summarized transcript
            with open(os.getcwd() + '\\summarized transcripts\\' + filename[:-4] + '.txt', 'w') as file:
                file.write(summarized_transcript)
            print("Created "+filename+" summarized transcript at "+os.getcwd() + '\\summarized transcripts\\' + filename[:-4] + '.txt\n')
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download and transcribe YouTube videos.')
    parser.add_argument('--number_of_videos', type=int, default=5, required=True, help='Number of videos to download.')
    parser.add_argument('--search_queries', type=str, nargs='+', required=True, help='List of search queries.')
    parser.add_argument('--download_videos', type=bool, default=True, help='Whether to download videos (this being False is not tested)')

    args = parser.parse_args()

    main(args.number_of_videos, args.search_queries, args.download_videos)
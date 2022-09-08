import os
import re

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube",
          "https://www.googleapis.com/auth/youtube.force-ssl",
          "https://www.googleapis.com/auth/youtube.readonly",
          "https://www.googleapis.com/auth/youtubepartner"]

musicExists = False


def main():

    aux = re.compile(
        "(?i)(\bplague\b.*\bcrystal castles\b|\bplague\b.*\bcrystal castles\b)")

    print(aux)

    res = aux.search("plague crystal castles")

    print(res)

    musicName = input("music name \n")
    artist = input("artist \n")

    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "./secret.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.playlistItems().list(
        part="snippet",
        maxResults=50,
        playlistId="PLIvDUvl6IGR0kaGyFgc2J4AR7QTZduLfo"
    )
    response = request.execute()

    nextPage = None
    videos = response["items"]

    searchMusicList(videos, musicName, artist)

    try:

        nextPage = response["nextPageToken"]

    except:

        print(musicExists)

    while (nextPage):

        request = youtube.playlistItems().list(
            part="snippet",
            maxResults=50,
            playlistId="PLIvDUvl6IGR0kaGyFgc2J4AR7QTZduLfo",
            pageToken=nextPage
        )

        response = request.execute()

        videos = response["items"]

        searchMusicList(videos, musicName, artist)

        try:
            nextPage = response["nextPageToken"]
        except:
            break

    print(musicExists)


def searchMusicList(videos, musicName, artist):

    global musicExists

    for item in videos:

        title = (item["snippet"])["title"]

        resultBoth = re.search(
            f"(?i)(\b{musicName}\b.*\b{artist}\b|\b{artist}\b.*\b{musicName}\b)", title)

        """ print(title)
        print("--- BOTH ---\n ")
        print(resultBoth) """

        resultName = re.search(
            f"(?i)\b{musicName}\b", title)

        """ print(title)
        print("--- NAME ---\n ")
        print(resultName) """

        if (resultBoth == None):
            if (resultName != None):
                musicExists = True
        else:
            musicExists = True


if __name__ == "__main__":
    main()

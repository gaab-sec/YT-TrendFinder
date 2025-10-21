import os
import datetime
import pprint

import googleapiclient.discovery
from dotenv import load_dotenv


def main():
    # Loading enviroment variables
    load_dotenv()
    api_key = os.getenv('API_KEY')

    # Getting datetime to 30 days ago
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    utc_30days = datetime.timedelta(30)

    date_last_month = utc_now - utc_30days
    published_after = date_last_month.isoformat()
 
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
   
    search_query = "automação python"
 
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = api_key
 
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)
 
    request = youtube.search().list(
        part="snippet",
        maxResults=2,
        order="viewCount",
        q=search_query,
        type="video",
        videoDuration="any",
        publishedAfter=published_after
    )

    # response = request.execute()["items"]
    # videos_info = [video["snippet"] for video in response]

    response = request.execute()
    videos = response["items"]

    videos_id = []
    for video in videos:
        videos_id.append(video["id"]["videoId"])
    
    print(videos_id)
    
    # extract videos statistics
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=videos_id
    )
    response = request.execute()



if __name__ == "__main__":
    main()
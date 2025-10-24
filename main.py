import os
import datetime
import sys

import googleapiclient.discovery
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table


# constantes
load_dotenv()
API_KEY = os.getenv('API_KEY')
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"


def get_youtube_client():
    if not API_KEY:
        print("ERRO: A váriavel de ambiente 'API_KEY' não foi definida")
        print("Crie um arquivo .env e adicione sua chave da API")
        sys.exit(1)
    
    try:
        client = googleapiclient.discovery.build(
            API_SERVICE_NAME, API_VERSION, developerKey= API_KEY
        )
        return client
    except Exception as err:
        print(f"ERRO: Falha ao construi cliente da API: {err}")
        sys.exit(1)

def main(query):
    print(f"Buscando vídeos para: '{query}'...")

    videos = get_videos_info(query)
    videos_sorted = sorted(videos, key=lambda vid: int(vid["view_count"]), reverse=True)

    table = Table(title="Monitor de Tendências", show_lines=True)

    table.add_column('Título', width=50)
    table.add_column('Canal', width=20)
    table.add_column('Views', justify='right')

    for video in videos_sorted:
        views_int = int(video['view_count'])

        table.add_row(
            video['title'],
            video['channel_title'],
            f'{views_int:,}'.replace(',', '.')
        )

    os.system("cls" if os.name == 'nt' else "clear")

    console = Console()
    console.print(table)


def get_videos_info(youtube_client, search_query: str, max_results: int =10, video_duration: str ="any") -> list[dict[str, any]]:

    # calculo data 
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    utc_30days = datetime.timedelta(30)

    date_last_month = utc_now - utc_30days
    published_after = date_last_month.isoformat()


    request = youtube_client.search().list(
        part="snippet",
        maxResults=max_results,
        order="viewCount",
        q=search_query,
        type="video",
        videoDuration=video_duration,
        publishedAfter=published_after
    )

    response = request.execute()
    videos_info = [
        {
            'id': video["id"]["videoId"],
            'title': video["snippet"]["title"],
            'channel_title': video["snippet"]["channelTitle"],
        }
        for video in response["items"]
    ]

    videos_id = []
    for video in videos_info:
        videos_id.append(video["id"])
    
    request = youtube_client.videos().list(
        part="statistics",
        id=videos_id
    )
    statistics = request.execute()["items"]
    view_count = [video_statistic["statistics"]["viewCount"] for video_statistic in statistics]

    for index in range(len(view_count)):
        videos_info[index]["view_count"] = view_count[index]

    return videos_info

if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("ERRO: Você precisa fornecer um termo de busca.")
        print("Ex: python main.py 'termo de busca'")
        sys.exit(1)

    query = "".join(sys.argv[1:])
    main(query)
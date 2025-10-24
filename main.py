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
DAYS_AGO = 30


def main():
    if len(sys.argv) < 2:
        print("Erro: Você precisa fornecer um termo de busca.")
        print("Uso: python seu_script.py \"termo de busca\"")
        sys.exit(1)
    query = " ".join(sys.argv[1:])

    # query = ""

    try:
        youtube_client = get_youtube_client()
        videos = get_videos_info(youtube_client, query)

        if not videos:
            return
        
        create_and_print_table(videos, query)

    except HttpError as err:
        print(f"\nERRO: ocorreu um erro na API do YouTube: {err}")
    except Exception as err:
        print(f"\nERRO: ocorreu um inesperado: {err}")



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


def get_videos_info(youtube_client, search_query: str, max_results: int =10, video_duration: str ="any") -> list[dict[str, any]]:

    # calculo data 
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    published_after_date = utc_now - datetime.timedelta(days=DAYS_AGO)
    published_after = published_after_date.isoformat()

    # pegar snippets 
    search_request = youtube_client.search().list(
        part="snippet",
        maxResults=max_results,
        order="viewCount",
        q=search_query,
        type="video",
        videoDuration=video_duration,
        publishedAfter=published_after
    )
    search_response = search_request.execute()
    
    videos_info_dict = {}
    for item in search_response.get("items", []):
        video_id = item["id"]["videoId"]
        videos_info_dict[video_id] =  {
            'id': video_id,
            'title': item["snippet"]["title"],
            'channel_title': item["snippet"]["channelTitle"],
        }
    video_ids = list(videos_info_dict.keys())

    if not video_ids:
        print("Nenhum vídeo encontrado")
        return []
    
    # pegar estatísticas 
    stats_request = youtube_client.videos().list(
        part="statistics",
        id=",".join(video_ids)
    )
    stats_response = stats_request.execute()

    for item in stats_response.get("items", []):
        video_id = item["id"]
        videos_info_dict[video_id]["view_count"] = int(item["statistics"].get("viewCount", 0))

    return list(videos_info_dict.values())


def create_and_print_table(videos: list[dict[str, any]], query: str):
    videos_sorted = sorted(videos, key=lambda vid: vid.get('view_count', 0), reverse=True)

    table = Table(title=f"Monitor de Tendências: {query}", show_lines=True)

    table.add_column('Título', width=50, overflow="fold") # fold: quebra titulos longos ao invés de cortar
    table.add_column('Canal', width=20)
    table.add_column('Views', justify='right')

    for video in videos_sorted:
        print(video["view_count"])

    for video in videos_sorted:
        views = video.get('view_count')
        formated_views = f'{views:,}'.replace(',', '.')

        table.add_row(
            video['title'],
            video['channel_title'],
            formated_views
        )
    
    os.system('cls' if os.name == 'nt' else 'clear')
    console = Console()
    console.print(table)


if __name__ == "__main__":
    main()
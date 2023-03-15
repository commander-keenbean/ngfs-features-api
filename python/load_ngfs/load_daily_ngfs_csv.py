import requests
import datetime
import re 
import urllib
import pathlib
import os
import psycopg2
from pathlib import Path
from io import BytesIO


url = "https://ftp.ssec.wisc.edu/pub/volcat/fire_csv/NGFS_daily/GOES-EAST/CONUS/NGFS_DETECTIONS_GOES-16_ABI_CONUS_2023_02_09_040.csv"
ngfs_urls = {
    'daily': [
        'https://ftp.ssec.wisc.edu/pub/volcat/fire_csv/NGFS_daily/GOES-EAST/CONUS/', 
        # 'https://ftp.ssec.wisc.edu/pub/volcat/fire_csv/NGFS_daily/GOES-WEST/CONUS/'
    ], 
    'events' : [
        'https://ftp.ssec.wisc.edu/pub/volcat/fire_csv/NGFS_events/GOES-EAST/CONUS/', 
        'https://ftp.ssec.wisc.edu/pub/volcat/fire_csv/NGFS_events/GOES-WEST/CONUS/'
    ],
    'scene' : [
        'https://ftp.ssec.wisc.edu/pub/volcat/fire_csv/NGFS_scene/GOES-EAST/CONUS/', 
        'https://ftp.ssec.wisc.edu/pub/volcat/fire_csv/NGFS_scene/GOES-WEST/CONUS/'   
    ]
}

# def get_config():
#     working_dir = os.path.dirname(os.path.realpath(__file__))
#     with open(working_dir + "/load_ngfs_config.yml", "r") as stream:
#         try:
#             print(yaml.safe_load(stream))
#         except yaml.YAMLError as exc:
#             print(exc)

def insert_from_url(url_map):
    postgres_password = os.environ['POSTGRES_PASSWORD']
    conn = psycopg2.connect(
        database="postgres",
        user='postgres',
        password=postgres_password,
        host='localhost',
        port='5432'
    )
    conn.autocommit = True
    cursor = conn.cursor()
    file_name_date = str(datetime.date.today()).replace("-","_")
    
    for subdir, urls in url_map.items():
        for url in urls:
            index_page = requests.get(url, stream=True).text
            # Find all the links to CSV files
            file_names = re.findall(r"<a\s+(?:[^>]*?\s+)?href=([\"'])(.*?.csv)\1", index_page);
            for file in file_names:
                file_name = file[1]
                file_url = url + file_name
                print('Reading ' + file_url)
                request = requests.get(file_url, stream=True)
                text = request.text
                content = request.content
                headers = text.partition('\n')[0].replace(',', ', ')
                try:
                    print('Inserting into ngfs_detections: ' + file_url)
                    sql = '''COPY ngfs_detections ({headers}) FROM 
                        STDIN CSV HEADER NULL AS 'NULL' '''.format(headers=headers)
                    cursor.copy_expert(sql, BytesIO(content))                    
                    update_sql = 'UPDATE ngfs_detections SET geom = ST_SetSRID(ST_MakePoint(lon, lat), 4326);'
                    cursor.execute(update_sql)
                    print('Successfully inserted into ngfs_detections')
                except Exception as e:
                    print('Failed to insert into ngfs_detections ' + file_url)
                    print(e)  
    conn.close()

insert_from_url(ngfs_urls)
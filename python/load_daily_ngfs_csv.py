import requests
import datetime
import re 
import urllib
import pathlib
import os
import psycopg2
from pathlib import Path


url = "https://ftp.ssec.wisc.edu/pub/volcat/fire_csv/NGFS_daily/GOES-EAST/CONUS/NGFS_DETECTIONS_GOES-16_ABI_CONUS_2023_02_09_040.csv"
ngfs_urls = {
    'daily': [
        'https://ftp.ssec.wisc.edu/pub/volcat/fire_csv/NGFS_daily/GOES-EAST/CONUS/', 
        'https://ftp.ssec.wisc.edu/pub/volcat/fire_csv/NGFS_daily/GOES-WEST/CONUS/'
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

def write_file(file_url, output_file):
    # local path to csv file
    output_files = []
    if not Path(output_file).is_file():
        with open(output_file, 'wb') as out_file:
            print('Reading ' + file_url)
            print('Writing ' + output_file)
            content = requests.get(file_url, stream=True).content
            # postgres_adjusted_csv = str.encode(content.split("\n",1)[1].replace('NULL', ''))
            out_file.write(content)
    return output_file
        


# Searches each source html for hrefs with .csv and todays date
def get_ngfs_csv(url_map, output_dir=''):
    file_name_date = str(datetime.date.today()).replace("-","_")
    output_files = []
    for subdir, urls in url_map.items():
        for url in urls:
            index_page = requests.get(url, stream=True).text
            file_names = re.findall(r"<a\s+(?:[^>]*?\s+)?href=([\"'])(.*?.csv)\1", index_page);
            for file in file_names:
                file_name = file[1]
                # if file_name_date in file_name:
                file_url = url + file_name
                # print(file_url)
                dest_dir = output_dir + subdir + '/' + file_name_date + '/'
                os.makedirs(dest_dir, exist_ok=True) 
                output_file = dest_dir + file_name
                write_file(file_url, output_file)
                output_files.append(output_file)
    return output_files


def insert_postgres(csv_files):
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
    
    for file in csv_files:
        f = open(file, 'r')
        headers = f.readline().strip('\n')
        headers = headers.replace(',', ', ')
        try:
            print('Inserting into ngfs_detections: ' + file)
            sql = '''COPY ngfs_detections ({headers}) FROM 
                STDOUT DELIMITER ',' CSV HEADER NULL AS 'NULL' '''.format(headers=headers)
            cursor.copy_expert(sql, f)
            update_sql = 'UPDATE ngfs_detections SET geom = ST_SetSRID(ST_MakePoint(lon, lat), 4326);'
            cursor.execute(update_sql)
            print('Successfully inserted into ngfs_detections')
        except Exception as e:
            print('Failed to insert into ngfs_detections ' + file)
            print(e)
            # try:
            #     print('Trying insert into ngfs_apq: ' + file)
            #     sql = '''COPY ngfs_apq FROM 
            #         STDOUT 
            #         DELIMITER ',' CSV HEADER NULL AS 'NULL' '''
            #     cursor.copy_expert(sql, f)
            #     print('Successfully inserted into ngfs_apq')
            # except Exception as e:
            #     print('Failed to insert into ngfs_apq ' + file)
            #     print(e)
                
            
            
            

        
    conn.close()
  
# # Display the table
# cursor.execute('SELECT * FROM demo')
# print(cursor.fetchall())
  
# # Closing the connection

working_dir = os.path.dirname(os.path.realpath(__file__))
output_dir = working_dir + '/ngfs_csv/'
output_files = get_ngfs_csv(ngfs_urls, output_dir)
insert_postgres(output_files)

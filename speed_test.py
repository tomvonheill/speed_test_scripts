import speedtest
import threading
import datetime
import subprocess
import logging
from db_connector import *
class SpeedClass:
    def __init__(self) -> None:
        self.dl_speed = None
        self.ul_speed = None
        self.st = speedtest.Speedtest()
    def get_download_speed(self):
        logging.info('checking download speed.....')
        self.st.get_best_server()
        self.dl_speed = self.st.download()/1000000
        logging.info(f'dl_speed: {self.dl_speed}')
    def get_upload_speed(self):
        logging.info('checking upload speed......')
        self.st.get_best_server()
        self.ul_speed = self.st.upload()/1000000
        logging.info(f'dl_speed: {self.ul_speed }')


if __name__ == "__main__":
    engine = get_engine(get_db_config('speed_test'))
    query = get_sql('/home/thomas/repos/speed_mapper/models/add_test.sql')
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    subprocess_result = subprocess.Popen('/sbin/iwgetid',shell=True,stdout=subprocess.PIPE)
    subprocess_output = subprocess_result.communicate()[0],subprocess_result.returncode
    network_name = subprocess_output[0].decode('utf-8').split('"')[1]
    logging.info(network_name)
    start_time = datetime.datetime.now()
    speed_holder = SpeedClass()
    dl_speed= threading.Thread(target=speed_holder.get_download_speed)
    up_speed = threading.Thread(target = speed_holder.get_upload_speed)
    dl_speed.start()
    up_speed.start()
    dl_speed.join()
    up_speed.join()
    data = {'date_time': f"'{start_time}'::timestamp", 
    'download_speed':speed_holder.dl_speed, 
    'upload_speed': speed_holder.ul_speed,
    'network_name': f"'{network_name}'"}
    if speed_holder.dl_speed is not None:
        query = query.format_map(data)
        with engine.connect() as con:
            con.execute(query)
    end_time = datetime.datetime.now()
    logging.info(end_time-start_time)


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
    def get_download_speed(self):
        logging.info('checking download speed.....')
        st = speedtest.Speedtest()
        self.dl_speed = st.download()/1000000
        logging.info(f'dl_speed: {self.dl_speed}')
    def get_upload_speed(self):
        logging.info('checking upload speed......')
        st = speedtest.Speedtest()
        self.ul_speed = st.upload()/1000000
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
    # st = speedtest.Speedtest()
    start_time = datetime.datetime.now()
    # dl_speed = st.download()/1000000
    # up_speed = st.upload()/1000000
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
    query = query.format_map(data)
    with engine.connect() as con:
        con.execute(query)
    end_time = datetime.datetime.now()
    logging.info(end_time-start_time)


import speedtest
import threading
import datetime
import subprocess
import logging

def get_download_speed():
    logging.info('checking download speed.....')
    st = speedtest.Speedtest()
    dl_speed = st.download()/1000000
    logging.info(f'dl_speed: {dl_speed}')
def get_upload_speed():
    logging.info('checking upload speed......')
    st = speedtest.Speedtest()
    dl_speed = st.upload()/1000000
    logging.info(f'dl_speed: {dl_speed}')

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    logging.info("logging is working")
    subprocess_result = subprocess.Popen('iwgetid',shell=True,stdout=subprocess.PIPE)
    subprocess_output = subprocess_result.communicate()[0],subprocess_result.returncode
    network_name = subprocess_output[0].decode('utf-8').split('"')[1]
    logging.info(network_name)
    # st = speedtest.Speedtest()
    start_time = datetime.datetime.now()
    # dl_speed = st.download()/1000000
    # up_speed = st.upload()/1000000

    dl_speed= threading.Thread(target=get_download_speed)
    up_speed = threading.Thread(target = get_upload_speed)
    dl_speed.start()
    up_speed.start()
    dl_speed.join()
    up_speed.join()
    end_time = datetime.datetime.now()
    logging.info(end_time-start_time)
    logging.info(dl_speed)
    logging.info(up_speed)


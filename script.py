import requests
from ftplib import FTP
import time
import codecs

def download_file(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        return True
    return False

def upload_to_ftp(host, username, password, local_filename, remote_filename):
    ftp = FTP(host)
    try:
        ftp.login(username, password)
        with open(local_filename, 'rb') as file:
            ftp.storbinary('STOR ' + remote_filename, file)
        return True
    except Exception as e:
        print("FTP Error: " + str(e))
        return False
    finally:
        ftp.quit()

def write_info(filename, message):
    with codecs.open(filename, 'w', encoding='utf-8') as file:
        file.write(message)

url = "https://edu-tpi.donstu.ru/api/Rasp?idGroup=2972&iCal=true"
local_filename = "data.ics"
ftp_host = "31.31.198.106"
ftp_username = "u2243822_Dilay"
ftp_password = "Zamok123"
ftp_remote_filename = "/www/d1lay.ru/data.ics"
update_info_filename = "update_info.txt"
update_remote = "/www/d1lay.ru/update_info.txt"

while True:
    download_successful = download_file(url, local_filename)

    time.sleep(5)

    if download_successful:
        upload_successful = upload_to_ftp(ftp_host, ftp_username, ftp_password, local_filename, ftp_remote_filename)

        if upload_successful:
            current_time = datetime.now() + timedelta(hours=3)  # Добавляем 3 часа к текущему времени
            current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
            write_info(update_info_filename, "Время последнего обновления - " + current_time_str)
            print("File " + local_filename + " uploaded to FTP server at " + ftp_host)
        else:
            write_info(update_info_filename, "FTP upload failed.")
            print("FTP upload failed.")
    else:
        write_info(update_info_filename, "Скачивание файла не удалось. Возможно, сайт политеха недоступен.")
        print("File download failed.")
    upload_info_successful = upload_to_ftp(ftp_host, ftp_username, ftp_password, update_info_filename, update_remote)

    if upload_info_successful:
        print("File " + update_info_filename + " uploaded to FTP server at " + ftp_host)
    else:
        print("FTP upload of update_info.txt failed.")

    time.sleep(900)

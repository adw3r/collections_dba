from functools import partial
from concurrent.futures import ThreadPoolExecutor
import re

import os
import threading

import requests

from app import config, utils, database


def main():
    email_files = [config.EMAILS_FOLDER / file for file in os.listdir(config.EMAILS_FOLDER)]
    email_pattern = re.compile('[a-zA-Z0-9.!#$%&\'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*')
    source_name = 'lnkdclctn1'

    for email_file in email_files:
        emails = utils.read_txt_file(email_file)
        emails = [email_pattern.search(email) for email in emails]
        emails = [email.group() for email in emails if email]
        while len(emails) >= 0:
            threads: list[threading.Thread] = []
            print(len(emails))
            for _ in range(150):
                email = emails.pop()
                if email:
                    t = threading.Thread(target=database.insert_email_in_separate_transactions, args=(email, source_name))
                    t.start()
                    threads.append(t)
            for t in threads:
                t.join()

        breakpoint()
        os.remove(email_file)
    # for chunk in utils.read_file_in_chunks(file_name, CHUNK_SIZE):
    #     with open(f'emails\{source_name}_{chunk_counter}.txt', 'w') as file:
    #         file.write(''.join(chunk))
    #     chunk_counter += 1
    #     print(chunk_counter)


if __name__ == '__main__':
    main()
    input('finish!')

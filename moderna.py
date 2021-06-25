import subprocess
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from linenotify import send

# link = 'https://register.cgmh.org.tw/Department/3/30990D'
link = 'https://register.cgmh.org.tw/Department/3/30990E'


def parse():
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-GPC': '1',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://register.cgmh.org.tw/Register/3',
        'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    response = requests.get(
        # AZ
        link, headers=headers)
    # moderna
    # 'https://register.cgmh.org.tw/Department/3/30990E', headers=headers)

    return response


def main():
    r = parse()
    soup = BeautifulSoup(r.text, 'lxml')

    b = soup.find('tbody')

    msgs = []
    for i in b.find_all('td'):
        if len(i.text) < 3:
            continue

        msg = ''
        print(i.parent.th.text)
        msg += i.parent.th.text
        print(f'{i.text.strip()}')
        msg += f'{i.text.strip()}'
        try:
            status = i.a.get('class')[0]
            if status != 'state-full':
                print(f"{i.a.get('href')}")
        except IndexError:
            msg += f'莫德納 "{link}"'
            # head = 'https://register.cgmh.org.tw/'
            # msg += f'\n"{head}{i.a.get("href")}"'
            # print(f'{msg}')
            msgs.append(msg)

    if msgs != []:
        for m in msgs:
            print(m)
            send(m)
        # subprocess.run(["afplay", "beep.mp3"])
    time.sleep(60)


if __name__ == '__main__':
    while True:
        main()
        print('--', datetime.now())
        time.sleep(6)

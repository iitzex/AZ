import subprocess
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from linenotify import send

link = 'https://register.cgmh.org.tw/Department/3/30990E'
token = 'T6E3a68EXNkrhmWqBdq7zHL7QmXCTrima8wGM4jS0Yb'


def parse():
    cookies = {
        'ASP.NET_SessionId': 'usq2w0diwqcyi2u1vlihf1hs',
        '__RequestVerificationToken': '98CLL6_80xZo3GUc5va2BWCYvDizZ94lC6qryITue1L8qFsVTLDeU5wOWssdx5i9wiV8G_6Wrn5QcGw8lhkNhXnboeawwz_4htwR7g6Gw_M1',
        'dtCookie': 'v_4_srv_1_sn_3809793E40C2A33F54385F5603F76CAC_perc_100000_ol_0_mul_1',
    }

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-GPC': '1',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    response = requests.get(link, headers=headers, cookies=cookies)

    return response


def main():
    r = parse()
    soup = BeautifulSoup(r.text, 'lxml')

    b = soup.find('tbody')

    msgs = []

    try:
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
                msg += f'\n莫德納門診 "{link}"'
                # head = 'https://register.cgmh.org.tw/'
                # msg += f'\n"{head}{i.a.get("href")}"'
                # print(f'{msg}')
                msgs.append(msg)
    except AttributeError:
        pass

    if msgs != []:
        for m in msgs:
            print(m)
            send(token, m)
        # subprocess.run(["afplay", "beep.mp3"])
    time.sleep(60)


if __name__ == '__main__':
    while True:
        main()
        print('--', datetime.now())
        time.sleep(6)

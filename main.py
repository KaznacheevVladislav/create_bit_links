import os

import requests
from dotenv import load_dotenv
from urllib.parse import urlparse


def shorten_link(token, link):
    headers = {
        'Authorization': 'Bearer {}'.format(token),
        'Content-Type': 'application/json',
    }
    payload = {
        'long_url': link
    }
    response = requests.post(
        'https://api-ssl.bitly.com/v4/shorten', headers=headers, json=payload)
    response.raise_for_status()
    bitlink = response.json()['link']
    return bitlink


def count_clicks(token, link):
    headers = {
        'Authorization': 'Bearer {}'.format(token),
    }
    params = {
        'units': '-1',
    }
    response = requests.get(
        'https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary'.format(link),
        headers=headers, params=params)
    response.raise_for_status()
    clicks_count = response.json()['total_clicks']
    return clicks_count


def is_bitlink(token, link):
    headers = {
        'Authorization': 'Bearer {}'.format(token),
    }
    response = requests.get(
        'https://api-ssl.bitly.com/v4/bitlinks/{}'.format(link), headers=headers)
    return response.ok


def main():
    load_dotenv()
    bit_token = os.getenv('BIT_TOKEN')
    link = input()
    link_without_scheme = link
    parse_link = urlparse(link)
    hostname = parse_link.hostname
    path = parse_link.path
    if parse_link.scheme != '':
        link_without_scheme = f'{hostname}{path}'
    if is_bitlink(bit_token, link_without_scheme):
        try:
            summary = count_clicks(bit_token, link_without_scheme)
            print(summary)
        except requests.exceptions.HTTPError:
            print('An error occurred when program tried to count clicks')
    else:
        try:
            bitlink = shorten_link(bit_token, link)
            print(bitlink)
        except requests.exceptions.HTTPError:
            print('An error occurred when creating a short link')


if __name__ == '__main__':
    main()
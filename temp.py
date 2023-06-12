from flask import Flask, request
from bardapi import Bard
import requests
import schedule
import time
import random
from dotenv import load_dotenv
import gradio as gr
import os

load_dotenv()

app = Flask(__name__)

token = os.getenv("TOKEN")
session = requests.Session()
session.headers = {
    "Host": "bard.google.com",
    "X-Same-Domain": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    "Origin": "https://bard.google.com",
    "Referer": "https://bard.google.com/",
}
session.cookies.set("__Secure-1PSID", token)

def fetch_proxies():
    url = 'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all'
    response = requests.get(url)

    if response.status_code == 200:
        ip_addresses = response.text.split()
        return ip_addresses
    else:
        return None

def job():
    print("Fetching proxies...")
    ip_addresses = fetch_proxies()
    if ip_addresses is None:
        print("Error: Failed to fetch proxies from the API.")
        return

    print("Proxies fetched.")
    return ip_addresses
    
schedule.every(5).minutes.do(job)

ip_addresses = job()

proxies = {}
for proxy in ip_addresses:
    proxies = {f'http': f'http://{proxy}'}
    break

print(proxies)

bard = Bard(token=token, session=session, proxies=proxies, timeout=30)

def get_response(input_text):
    response = bard.get_answer(input_text)
    return response["content"]

if __name__ == '__main__':
    get_response()
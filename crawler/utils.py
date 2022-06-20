import time
import re
import os
from urllib import request
from random import randint
import requests
from socket import timeout

def get(url):
    try:

        html = request.urlopen(url, timeout=15).read().decode('utf-8')
        html = re.sub("(\r\n|\n|\r|\t)", " ", html)
        html = re.sub("  +", " ", html)
    except timeout:
        print("timeout")
        return get(url)
    except Exception as e:
        print(e)
        return get(url)

        
    return html


def get2(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36',
        'Host': 'annuairesante.ameli.fr',
        # 'Cookie': cookie
    }
    html = requests.get(url, headers=headers)
    html = html.text
    html = re.sub("(\r\n|\n|\r|\t)", " ", html)
    html = re.sub("  +", " ", html)
    return html


def HTMLminimify(html):
    html = re.sub("(\r\n|\n|\r|\t)", " ", html)
    html = re.sub("  +", " ", html)
    return html


def progres_bar(iteration, total, suffix='', length=100,):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        suffix      - Optional  : suffix string (Str)
        length      - Optional  : character length of bar (Int)
    """
    percent = ("{0:." + str(1) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = "=" * filledLength + '-' * (length - filledLength)
    print('\r[%s] %s%% %s' % (bar, percent, suffix), end="\r")
    # Print New Line on Complete
    if iteration == total:
        print('\033[K - Done '+str(total))


def timer(start):
    print(f'Executed in {round(time.time()-start,2)} s')


def dir(file):
    return '/'.join(os.path.dirname(os.path.abspath(file)).split('/')[:-1])


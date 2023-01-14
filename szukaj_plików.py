import re
import requests
import os
import logging
from pathlib import Path

logger = logging.getLogger('Programista_magazyn')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('Programista_magazyn.log')
fh.setLevel(logging.ERROR)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch.setFormatter(formatter)
fh.setFormatter(formatter)

logger.addHandler(ch)
logger.addHandler(fh)

formats = [
    'pdf',
    'epub',
    'mobi',
    '7z',
    'zip',
    'rar',
    'azw3'
]

with open('D:\Projects\plik.txt', 'r', encoding='utf8') as file_source:
    data = file_source.read()
    linki = []
    formatsRegexOrString = ''
    for format in formats:
        formatsRegexOrString += format
        if not format == formats[-1]:
            formatsRegexOrString += '|'


    m = re.findall('(https://.*?[.]('+formatsRegexOrString+'))', data)
    for i in m:
        linki.append(i)
    if len(linki) == 0:
        print("a")
    # m = re.findall('(https://.*?[.]pdf)', data)
    # for i in m:
    #     linki.append(i)

    # m = re.findall('(https://.*?[.]epub)', data)
    # for i in m:
    #     linki.append(i)

    # m = re.findall('(https://.*?[.]mobi)', data)
    # for i in m:
    #     linki.append(i)

    # m = re.findall('(https://.*?[.]7z)', data)
    # for i in m:
    #     linki.append(i)

    # m = re.findall('(https://.*?[.]zip)', data)
    # for i in m:
    #     linki.append(i)

    # m = re.findall('(https://.*?[.]rar)', data)
    # for i in m:
    #     linki.append(i)

    # m = re.findall('(https://.*?[.]azw3)', data)
    # for i in m:
    #     linki.append(i)



    with open('D:\Projects\out.txt', 'w', encoding="utf8") as file_out:
        once = True
        for url in linki:
            url = url[0]
            file_out.write(url+"\n")
            d_name = re.findall('.*/.*[.](.*)', url)[0]
            f_name = re.findall('.*/(.*)', url)[0]
            if not os.path.exists('D:\Projects\\pobrane\\'+d_name+'\\'+f_name):
                logger.info('Downloading: '+f_name)
                r = requests.get(url, allow_redirects=True)
                remote_file_size = r.headers.get('content-length', None)
                Path('D:\Projects\\pobrane\\'+d_name).mkdir(parents=True, exist_ok=True)
                
                open('D:\Projects\\pobrane\\'+d_name+'\\'+f_name, 'wb').write(r.content)

                if os.path.exists('D:\Projects\\pobrane\\'+d_name+'\\'+f_name):
                    with open('D:\Projects\\pobrane\\'+d_name+'\\'+f_name, 'rb') as file2:
                        local_file_size = len(file2.read())
                        if int(local_file_size) == int(remote_file_size):
                            logger.debug('Download success: '+f_name)
                        else:
                            logger.critical('Download failed: File not downloaded completly remote_size: '+str(remote_file_size)+' local_size: '+str(local_file_size))
                else:
                    logger.error('Download failed: file not exists: ','D:\Projects\\pobrane\\'+d_name+'\\'+f_name)
            else:
                logger.debug('Exists: '+f_name)
input('koniec')


        

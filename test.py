import os
headers = {
    'authority': 'lighthouse.aliexpress.com',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
    'sec-fetch-dest': 'script',
    'accept': '*/*',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-user': '?1',
    'accept-language': 'zh-CN,zh;q=0.9',
    'Referer': 'https://www.aliexpress.com/all-wholesale-products.html',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
    'Sec-Fetch-Dest': 'script',
    'Origin': 'https://www.aliexpress.com',
    'referer': 'https://www.aliexpress.com/all-wholesale-products.html',
    'cookie': 'id=22d18bf44ac10021||t=1582477216|et=730|cs=002213fd4889b76bafcd8990a9; DSID=AAO-7r5S1hRB_yLvcdY0Z_DbAR0zD69-JAoxuqAleUExmWHl2nPp_3gBJi__1r8mI-alyi0kVr3ME4QDmE2J-7wZEtiYd8cZKaFJa7ilVd58u_-TG2pzQCk',
    'Upgrade-Insecure-Requests': '1',
}

def gethtml(url):
    try:
        r = requests.get(url, timeout=30, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "exception"

def gethtml_withcache(url):
    # 文件名
    file_name = url.replace('/', '').replace('.','').replace('https:','').replace('?','') + '.txt'
    print(file_name)
    # 初始化缓存文件夹
    dir = os.path.join(os.curdir, 'cashe')
    if not os.path.isdir(dir):
        os.mkdir(dir)
    # 文件路径
    file_dir = os.path.join(dir, file_name)

    # 文件不存在的话创建文件，gethtml并写入缓存文件
    if not os.path.exists(file_dir):
        with open(file_dir, 'w+', encoding='utf-8') as f:
            html_str = gethtml(url)
            f.write(html_str)
    # 文件存在 读取缓存
    else:
        with open(file_dir, 'r+', encoding='utf-8') as f:
            html_str = f.read()
            # 文件存在但是为空
            if html_str.strip() == '':
                html_str = gethtml(url)
                f.write(html_str)
    return html_str

if __name__ == "__main__":
    html=gethtml_withcache('https://www.aliexpress.com/category/100003109/women-clothing.html?spm=a2g0o.category_nav.1.1.1b9348b6jtufB7')
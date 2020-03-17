import os
import requests
from bs4 import BeautifulSoup

headers = {
    'authority': 'lighthouse.aliexpress.com',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
    'sec-fetch-dest': 'script',
    'accept': '*/*',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'no-cors',
    'accept-language': 'zh-CN,zh;q=0.9',
    'Referer': 'https://www.aliexpress.com/all-wholesale-products.html',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
    'Sec-Fetch-Dest': 'script',
    'Origin': 'https://www.aliexpress.com',
    'referer': 'https://www.aliexpress.com/all-wholesale-products.html',
    'cookie': 'cna=Uba9Fvn5938CAXjntk6waiul; sca=f4b66c5b; atpsidas=211bd8344a6ae0a5cf80dcd5_1583561016_2; cad=170dccba148-5956904993333543000001; cap=73aa; atpsida=e44a32856e321aa7a1c62b7f_1584344925_1',
    'origin': 'https://g.alicdn.com',
    'if-none-match': '"Uba9Fvn5938CAXjntk6waiul"',
    'Upgrade-Insecure-Requests': '1',
    'Connection': 'keep-alive',
    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'if-modified-since': 'Tue, 22 Oct 2019 18:15:00 GMT',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
}

def gethtml(url):
    try:
        r = requests.get(url, timeout=30, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "exception"
def casheGethtml(url):
    # 文件名
    file_name=url.replace('https://www.aliexpress.com/','').replace('/','')+'.txt'
    # 初始化缓存文件夹
    dir = os.path.join(os.curdir, 'cashe')
    if not os.path.isdir(dir):
        os.mkdir(dir)
    #文件路径
    file_dir = os.path.join(dir, file_name)
    
     #文件不存在的话创建文件，gethtml并写入缓存文件
    if not os.path.exists(file_dir):
        with open(file_dir,'w+',encoding='utf-8') as f:
            html_str = gethtml(url)
            f.write(html_str)
    # 文件存在 读取缓存
    else:
        with open(file_dir,'r+',encoding='utf-8') as f:
            html_str=f.read()
            # 文件存在但是为空
            if html_str.strip()=='':
                html_str=gethtml(url)
                f.write(html_str)
    return html_str

def tofind(html):
    soup = BeautifulSoup(html, 'html.parser')
    uls = soup.find_all('ul', attrs={'class': 'sub-item-cont util-clearfix'})
    
    list=[]
    for ul in uls:
        aList = ul.find_all('a')
        for a in aList:
            dict1 = {}
            dict1['name'] =a.text
            dict1['url'] =a['href']
            list.append(dict1)
    print(list)


if __name__ == "__main__":

    url = 'https://www.aliexpress.com/all-wholesale-products.html'
    html = casheGethtml(url)
    soup = BeautifulSoup(html, 'lxml')

    # 商品分类列表，一个分类对应一个字典{
    # '父分类的名字(如Women's Clothing和Men's Clothing)',
    # '父分类的href(https://www.aliexpress.com/category/100003109/women-clothing.html)',
    # '子分类们的名字(有很多个，是个列表，如DressesBlouses & ShirtsHoodies & Sweatshirts)',
    # '子分类们的href(有很多个，是个列表)'}
    categories = []
    # 一共有1-26 26个分类
    for i in range(1, 27):
        category = {}
        # 通过span标签的id属性 id="anchor + i"找到目标（span的父目录下的a标签为父分类的href+text）
        bigTitleDiv = soup.find("span", {"id": "anchor" + str(i)}).parent
        # 父分类的名字
        category['parentName'] = bigTitleDiv.a.text
        #父分类的href
        category['parentHref'] = bigTitleDiv.a['href']
        # 子分类们
        childrenNames=' '.join(bigTitleDiv.parent.div.div.ul.li.a.text.split())
        category['childrenNames'] = childrenNames.split(' ')
        # 子分类们的href
#         childrenHrefs=' '.join(bigTitleDiv.parent.div.div.ul.li.a['href'].split())
#         category['childrenHrefs'] = childrenHrefs.split(' ')
        category['childrenHrefs'] =bigTitleDiv.parent.div.div.ul.li.a['href'].split(' //')
        categories.append(category)
        print(category['childrenHrefs'])
        print('名字 = %s href = %s' % (category['childrenNames'],category['childrenHrefs']))
    
        


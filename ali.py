import os
import csv
import requests
from bs4 import BeautifulSoup

headers = {
    'authority': 'lighthouse.aliexpress.com',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
    'sec-fetch-dest': 'script',
    'accept': '*/*',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-user': '?1',
    'referer': 'https://www.aliexpress.com/all-wholesale-products.html?spm=a2g0o.home.16005.1.650c2c25iplTuO',
    'accept-language': 'zh-CN,zh;q=0.9',
    'Referer': 'https://www.aliexpress.com/all-wholesale-products.html?spm=a2g0o.home.16005.1.650c2c25iplTuO',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
    'Sec-Fetch-Dest': 'script',
    'Origin': 'https://www.aliexpress.com',
    'cookie': 'ali_apache_id=11.251.144.15.1582389520679.186743.9; _ga=GA1.2.294288397.1582389527; aep_common_f=T/h3ppVGE2+ZffsxbJg0HdKsejJ1FF6UaVjxezQue7ar15kkEep1Tg==; cna=JbPmFnhJf3ACAXjntjqicOnt; _gid=GA1.2.1704154986.1584458403; intl_locale=en_US; ali_apache_tracktmp=W_signed=Y; _fbp=fb.1.1584508062963.1300902942; aep_history=keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%094000643054078%094000012569319%0932846610151; _hvn_login=13; aep_usuc_t=ber_l=A0; acs_usuc_t=acs_rt=485b0a55faba4ab9ad7820278b07dcf9&x_csrf=129qmtntk0h7d; havana_tgc=eyJjcmVhdGVUaW1lIjoxNTg0NTE1OTE0MjYyLCJsYW5nIjoiZW5fVVMiLCJwYXRpYWxUZ2MiOnsiYWNjSW5mb3MiOnsiMTMiOnsiYWNjZXNzVHlwZSI6MSwibWVtYmVySWQiOjIyMDc1NDkxMjYzNjcsInRndElkIjoiMVBvTWswU2s0dTdfY0hydWJNcW1HbGcifX19fQ; xman_us_t=x_lid=cn264863147yetae&sign=y&x_user=jJFAX0mBlbPukFddy8s775ztQtYodqgrQMAkf7y1yQM=&ctoken=11tv721ycufn4&need_popup=y&l_source=aliexpress; xman_f=cyDTEoLnE127tPyliC0NPStqxFu1hmAqXhAjCWeO+Vb1GFbI9WOhQqMV36EZ4AwQbfsjDqdJLMIFmtAtH755jmfbsYvb95OmD879lUuv1qoQqt+TFDQyOeKyXtGgMhWSGe1L1B5UOyhvfyW1uJweW8kNLRpyHjhssd6cbOQnEeoo5y7OcD0ZhoVZVWnjrS8Qoj9r7mzXupGBzV4BkiZQmfMgAPVapY6XXy2wYOM3ZiKq7tvPYuzh3b6UDN8L3Adj4FhGe7MNGyYWJUsI9lXNozZBsAEvPgqmG56TteKFFO2B7ioxCCwRJkqPzREGQ8rUmY1wIHjO0RsK297GoEziO3VZznLsfY2uZA9Cba17D95ojpC/1tiYmyrFY6GFVIZTaXHuN3ttW4Jy/sC51fhKN/YcbFeieeKzPwtTWf+atjsrM3QkuJEsoQ==; aep_usuc_f=site=glo&c_tp=USD&x_alimid=1864220146&isb=y&region=CN&b_locale=en_US; ali_apache_track=mt=1|ms=|mid=cn264863147yetae; _m_h5_tk=53470480d61208219930253fb2141c4e_1584520711924; _m_h5_tk_enc=3142be314891ea194425a218303f5230; _gat=1; xman_us_f=zero_order=y&x_locale=en_US&x_l=1&last_popup_time=1584506627220&x_user=CN|CN|shopper|ifm|1864220146&no_popup_today=n&x_c_chg=0&x_as_i=%7B%22cookieCacheEffectTime%22%3A1584518844422%2C%22isCookieCache%22%3A%22Y%22%2C%22ms%22%3A%220%22%7D&acs_rt=f8063778288f4c6081056c503099bc3e; xman_t=3cVV1s7otNeHFeDLW5jViMdgZoz1Gk1zD1QtQHIDcW22YbNj8lCKAsm7MMRFvfbGBm8shn/YiKCu0kvjUJxgmSGZDQU4Ts2QBGI2sA86lMzlvEYgrXmpF5DtvoQCr3ATTbiqVOnHfELegdvBsG3ObPQK5BZ5EBECwXkmy5Ho4lvgzdi+VbNKUO/FeKniaV0/iddEuKGgg3mkKRfdiTUjI0Lj7T8ZI5UzAm6NRGt10WENb3Dq6fegUgavX41VQe6NuqUXlt8YLXNJidPn/33hwWARxEmj2vU9SjrJI4AEb60rDrZy/nBMbOVhWBJQCGOkUfH2DGsrBWF+fMPZLXXGDoXUZfZWRVcf/+kGdle3DJg0QLvcCA+9e70Iq0Vnt1A25smHQhJOyX9dwgdBViHX/+oGWrrII86PDE9gATpxGcncZWz88qqM6aLp78He+V3sxSMcFy4rivvhEqAKRKe5nwt/0EfCFr+6h/ptDHZvxzAf66Oup7kG4oLcrcQzEslA8xX2iEq0Gtpdvtuy/m+L3wAajZI6zGbCeEnybIxiavgLKXKWuzejpEFeuFjcXmOWlF15vwzHayZgd8lq3S7DwnsZOEYW+fuc+0m9tAFzbdJEGqHsi7JYneV79hioMpeMrz04pgMVn0Lb4RBk4+x06A==; intl_common_forever=hq0vwH5N+trpv73TJMaaCq6n7FQ04Kz1XVmk1sshlZv3Ed0qBOBU9w==; l=dBTicH2uQiXuoWnjKOCwhm-UJCbOSIRYmul2TbjHi_5LL6L_xuQOors86Fp6VjWfM9TB4dt0an29-etks26r2AkuB2za7xDc.; isg=BK2tenCdj30OK2uy9CBHnKusvEknCuHczwRwYO-y6cSzZs0Yt1rxrPs4VDqAYvmU',
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
    file_name = url.replace('/', ' ').replace('.',' ').replace('https:','') + '.txt'
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
            
            while 'location.href=\"https://login.aliexpress.com/?from=sm&return_url=\"+encodeURIComponent' in html_str:
                html_str = gethtml(url)
                f.write(html_str)
    return html_str

# 获取分类信息列表


def parseCategories():
    # 商品分类列表，一个分类对应一个字典{
    # '父分类的名字(如Women's Clothing和Men's Clothing)',
    # '父分类的href(https://www.aliexpress.com/category/100003109/women-clothing.html)',
    # '子分类们的名字(有很多个，是个列表，如DressesBlouses & ShirtsHoodies & Sweatshirts)',
    # '子分类们的href(有很多个，是个列表)'}
    categories = []
    # 一共有1-26 26个分类
    for i in range(1, 27):
        category = {}
        h3 = soup.find("span", {"id": "anchor" + str(i)}).parent
        category['parentName'] = h3.a.text
        category['parentHref'] = h3.a['href']

#     取出所有li标签
#     childrenNameList=list(set(bigTitleDiv.parent.div.div.ul.li.next_siblings))
#     childrenNameList.remove('\n')

#     取出所有子目录的name和href
        soupName = BeautifulSoup(
            str(list(h3.parent.div.div.ul.li.next_siblings)), 'lxml')
        childrenList = []
        for c in soupName.find_all('a'):
            cdict = {}
            cdict['name'] = c.string
            cdict['href'] = c['href']
            childrenList.append(cdict)
        category['childrenList'] = childrenList
        categories.append(category)
        # print(category)
    return categories


def export_csv(data):
    for d in data:
        parentName = d['parentName']
        parentHref=d['parentHref']
        childrenList = d['childrenList']
        for childrenDict in childrenList:
            childrenName = childrenDict['name']
            childrenHref=childrenDict['href']
            dir = os.path.join(os.curdir, 'output', parentName)
            file_dir = os.path.join(dir, childrenName.replace('/',' ')+'.csv')
            # print('dir = %s file_dir = %s'%(dir,file_dir))
            if not os.path.isdir(dir):
                os.makedirs(dir)
            with open(file_dir, 'w+',newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['主分类', '主分类链接', '分类', '分类链接'])
                writer.writerows([(parentName,parentHref,childrenName,childrenHref)])
        
        

if __name__ == "__main__":

    url = 'https://www.aliexpress.com/all-wholesale-products.html'
    html = gethtml_withcache(url)
    soup = BeautifulSoup(html, 'lxml')
    categories = parseCategories()
    export_csv(categories)
    for categorieDict in categories:
        i = 1
        parentName=categorieDict['parentName']
        parentHref = categorieDict['parentHref']
        # 配置头信息
        headers['referer'] = 'https:' + parentHref + '?spm=a2g0o.category_nav.1.'+str(i)
        xxxx='.2c2c48b6fey8QY'
        headers['referer'] = headers['referer'] + xxxx
        headers['Referer'] = headers['referer']
        # 获取
        html = gethtml_withcache('https:' + parentHref)
        print('获取根目录 = %s' % parentName)
            # shop ...
        # 子目录
        for childrenDict in categorieDict['childrenList']:
            childrenName=childrenDict['name']
            childrenHref=childrenDict['href']
            i = i + 1
            # 配置头信息
            headers['referer'] = 'https:' + childrenHref + '?spm=a2g0o.category_nav.1.'+str(i)
            headers['referer'] = headers['referer'] + xxxx
            headers['Referer'] = headers['referer']
            html = gethtml_withcache(childrenHref)
            print('获取子目录 = %s' % childrenName)

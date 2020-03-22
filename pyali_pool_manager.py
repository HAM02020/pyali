import time
import datetime
import os
import random
import multiprocessing
from multiprocessing import Pool
import re
import csv
import requests
from bs4 import BeautifulSoup
from bs4 import Tag


MAX_WORKER_NUM=multiprocessing.cpu_count()

# 入口地址
url = 'https://www.aliexpress.com/all-wholesale-products.html'

refer_param = '.3f3748b6HOu7Wy'
download_pages = 0
# thread_num = 20
# threads=[]
# link_queue=Queue()
# lock = threading.RLock()



global_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'cookie': 'ali_apache_id=11.251.144.15.1582389520679.186743.9; _ga=GA1.2.294288397.1582389527; aep_common_f=T/h3ppVGE2+ZffsxbJg0HdKsejJ1FF6UaVjxezQue7ar15kkEep1Tg==; cna=JbPmFnhJf3ACAXjntjqicOnt; _gid=GA1.2.1704154986.1584458403; _fbp=fb.1.1584508062963.1300902942; acs_usuc_t=x_csrf=q2z588q8kzdy&acs_rt=a6cfa2858bc94b7397f3f485bb7d6661; intl_locale=en_US; re_ri_f=5L6bQU+/q7bitT8zKSe+rrcWBDC0uaut0CzLFISBzzWKZoquUwYqyUGyTg9G4xRL; havana_tgc=eyJjcmVhdGVUaW1lIjoxNTg0NzY3MTUyODQzLCJsYW5nIjoiZW5fVVMiLCJwYXRpYWxUZ2MiOnsiYWNjSW5mb3MiOnsiMTMiOnsiYWNjZXNzVHlwZSI6MSwibWVtYmVySWQiOjIyMDc1NDkxMjYzNjcsInRndElkIjoiMVEzNTVmOFNKR1RnVE9aTE0yU1ZMVFEifX19fQ; _hvn_login=13; xman_us_t=x_lid=cn264863147yetae&sign=y&x_user=5zVRyHlWlo4cEizXJynZjV213G1K9OQ0VZMv9XlEAyk=&ctoken=rs_pzx3inmq_&need_popup=y&l_source=aliexpress; aep_usuc_t=ber_l=A0; xman_f=Unldg4FseLvCbolLxBxfOgKbi351+1tZ5tTy6YlBBreW7NdfEyAosP820bdIgZJW4vkTenD3K0cDnsba9USQ4uBHHLmmKMtxNNSOkQJVtn5fJskTBDu/Low4qH6DbZwytz4wZaFYB9EpjfQifUOc5pMQ6Z/lXZpn3lLE2WzQTtOqfIRwGO+hO2bZV84QcabKI7FxcDo9sjh9Xi63wbrPS4iUwcsxWK+B3NLobh2mhmmNiEvNc34aWpQr4Y+SIpEmFYA2YrHz1VUL2WG++HW8Mp/7YyzqZKdHvdDS6MCwsqNmp8UnS0LowHRmMshNlXv+XUG0+e3VbC80Jt8utSGOVUYU6akJ2FsvEA4gvJYk15/wYi/Ezy6axQvxjk4fFnZXH095igJoxf+gOlHrLfm9NMMeXMgNsdoYdD42XN1nRiSpkipYmJ1g3Q==; aep_usuc_f=site=glo&c_tp=USD&x_alimid=1864220146&isb=y&region=CN&b_locale=en_US; ali_apache_track=mt=1|ms=|mid=cn264863147yetae; ali_apache_tracktmp=W_signed=Y; _m_h5_tk=467a8b735fe982c81c52317afe63b8ac_1584794836473; _m_h5_tk_enc=9ac36bbcbc67cd20e66aa7579a5782a7; aep_history=keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%0932943953434%094000516992665%0932972091194%0932832265738%094000221844726%094000460353856%094000224454881%0933040687247; _gat=1; intl_common_forever=M7wyuBu0kT237MdlS7DCdh64V33+pD/LSyeRfnxqQOAGtMbVj2ggpA==; xman_us_f=x_l=1&x_locale=en_US&no_popup_today=n&x_c_chg=0&x_user=CN|CN|shopper|ifm|1864220146&zero_order=y&acs_rt=f8063778288f4c6081056c503099bc3e&last_popup_time=1584506627220&x_as_i=%7B%22cookieCacheEffectTime%22%3A1584794399983%2C%22isCookieCache%22%3A%22Y%22%2C%22ms%22%3A%220%22%7D; xman_t=G49n7tq5+UyugWS5slg2GKCJFPnlvZ4Bbyv5CqHuc2l6fUnd9wemV+XAlyzINigIz9yUitLt42dERugyAzcPowwcqBSOPaxFhtch6EfhFtr833uS7vkyI9tDjKOLzWV5ppmKeXhkUDsJFlawnLSR5fPGTRLBWouxt16L9JdxVMB6bLR2vCgT5ifuhIadKpOLqRNol06LeZIu5H8yPcItpGKnOrMQ4WgcR6PiO8m9WjVuuMto2nYuQ4un+/mWnmYCy1rM9I6x/yk+/0jpIloLEqjKYPe8Pn4AzW2Ti2JOth1/n+01FDDmXiKqdovxtFJgzIf9wf7ylA8dgJlS1wdZDKKz9jTwKN86LQVrsHThXQg6coFzKST+whWw9T4NZgmUi7iQJJ5UVzUbnxc5/fVxy2Tkhnii6TyEYdOAU8o2Xp0srSUFB3254GIdztJU1BGynU3gvtpdBRWQbwSLP3jjU/uWSIMHmHRb9PJDiSKvWEaLhov64V5EqO+7HhzeZtl0CM/F8roKilewT+RDJCZEXAI/RI76q0zt+BjAnx6rf3FC6TKVnppih9KtsjPsysg7PpBsSIlUQZHIrHI0bn55PSxg+ie+JJN8oSlMUr9Vgqg32f6yKoWuOCEze32nhPyqHag/KnM0zW7Y42WLLU6DPA==; l=dBTicH2uQiXuoec3BOCN-m-UJKbTdIRA_ul2Tbvei_5IR1YsxiBOozzCGev6cjWfTm8B4dt0an29-etksjeGv2ikeQkIdxDc.; isg=BEtLmKBnkWTCKM2UBjoJ0lm22u814F9ifc4Wxr1IDQrh3Gs-RbQFsCpystwye7da',
    'referer': 'https://www.aliexpress.com/',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
}



def gethtml(url, header=global_headers):
    try:
        r = requests.get(url, timeout=30, headers=header)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "exception"

def parseUrl(url):
    pararm={}
    pararmlist = url.split(' ')
    href = pararmlist.pop(0)
    file_name = pararmlist.pop(-1)
    path=''
    for arg in pararmlist:
        path = os.path.join(path, arg)
    pararm['href'] = href
    pararm['path'] = path
    pararm['file_name'] = file_name
    return pararm

def gethtml_withcache(url):
    global download_pages
    download_pages += 1
    pararm = parseUrl(url)
    url = 'https://' + pararm['href']
    fileName = pararm['file_name']
    path=pararm['path']
    headers = global_headers
    headers['referer'] = pararm['href']
    headers['Referer'] = pararm['href']


    if fileName.strip() == '':
        file_name = re.findall(r'[\w+\-\.]+\.html', url)[0]
    else:
        file_name = fileName
    # 初始化缓存文件夹
    dir = os.path.join(os.curdir, 'cashe', path)


    
    if not os.path.isdir(dir):
        os.makedirs(dir)
    # 文件路径
    file_dir = os.path.join(dir, file_name)
    print("正在获取 = %s"%file_dir)

    # 文件不存在的话创建文件，gethtml并写入缓存文件

    if not os.path.exists(file_dir):  
        with open(file_dir, 'w+', encoding='utf-8') as f:
            html_str = gethtml(url, headers)
            f.write(html_str)
            if '//如果包含 referrer ，且 referrer 非 霸下验证页面' in html_str:
                print("errrrrrorrrrr!!!!，请通过人机验证,并输入cookie")
                global_headers['cookie'] = input()
                w = open('./cookie/cookie.txt', 'w',encoding='utf-8')
                w.write(global_headers['cookie'])
                w.close()

                html_str = gethtml(url, headers)
                f.write(html_str)
                    
            
    # 文件存在 读取缓存
    else:
        
        f = open(file_dir, 'r', encoding='utf-8')
        html_str = f.read()
        f.close()
        # 文件存在但是为空
        if html_str.strip() == '' or html_str == 'exception' or '//如果包含 referrer ，且 referrer 非 霸下验证页面'  in html_str or '//将用户正常页面写入到 x5referer ，以备后续跳转返回' in html_str:
            print("重写错误页面 %s" % file_dir)
            html_str = gethtml(url, headers)
            w=open(file_dir,'w',encoding='utf-8')
            w.write(html_str)
            w.close()
        
    return html_str

def parseCatories(html):

    soup = BeautifulSoup(html, 'lxml')
    containerDiv = soup.find("div", {"class": "util-clearfix cg-container"})
    rootDivs = list(containerDiv.div.contents)
    catPages = []
    referer_count = 1
    for itemdiv in rootDivs:
        if not isinstance(itemdiv, Tag):
            continue
        # root_name=itemdiv.h3.a.text
        root_href = itemdiv.h3.a['href'].replace('//', '')
       
        rootCatName = re.findall(r'([\w+\-\.]+)\.html', root_href)[0]
        rootCatId = re.findall(r'/(\d+)/', root_href)[0]
        
        for pageNum in range(1, 11):
            nextPage_param = '?trafficChannel=main&catName=' + rootCatName + '&CatId=' + \
                rootCatId + '&ltype=wholesale&SortType=default&page=' + \
                str(pageNum)
            file_name=rootCatName+str(pageNum)+'.html'
            nextPage_url = '%s%s %s %s' % (root_href, nextPage_param, rootCatName,file_name)
            if pageNum == 1:
                root_href = itemdiv.h3.a['href'].replace('//', '') + '?spm=a2g0o.category_nav.1.' + str(referer_count) + refer_param
                referer_count+=1
                nextPage_url = '%s %s %s'%(root_href,rootCatName,file_name)
            catPages.append(nextPage_url)

        # branch_name_list=re.findall(r'(?<=html">).+(?=</a>)',str(itemdiv.div.div.ul.contents))
        branch_href_list = re.findall(
            r'(?<=href="//).+\.html', str(itemdiv.div.div.ul.contents))

        for i in range(len(branch_href_list)):
            referer_count+=1
            catName = re.findall(r'([\w+\-\.]+)\.html', branch_href_list[i])[0]
            catId = re.findall(r'/(\d+)/', branch_href_list[i])[0]
            
            for pageNum in range(1, 11):
                nextPage_param = '?trafficChannel=main&catName=' + catName + '&CatId=' + \
                    catId + '&ltype=wholesale&SortType=default&page=' + \
                    str(pageNum)
                file_name=catName+str(pageNum)+'.html'
                nextPage_url = '%s%s %s %s %s' % (
                    branch_href_list[i], nextPage_param, rootCatName, catName,file_name)
                if pageNum == 1:
                    branch_href_list[i] = branch_href_list[i] + '?spm=a2g0o.category_nav.1.' + str(referer_count) + refer_param
                    nextPage_url = '%s %s %s %s'%(branch_href_list[i],rootCatName,catName,file_name)
                catPages.append(nextPage_url)
    return catPages

def downloadPages(url,result_list):
    time.sleep(0.2*random.random())
    html = gethtml_withcache(url)
    # html=gethtml(pararm['href'],header=headers)
    path = os.path.join(parseUrl(url)['path'],'products')
    
    hrefs = re.findall(r'"productDetailUrl":"//([\w./?=\-&,]+)', html)
    file_names = re.findall(r'/(\d+\.html)\?', html)
    global productUrls
    for i in range(len(hrefs)):
        url = '%s %s %s' % (hrefs[i], path, file_names[i])
        result_list.append(url)

        
def diccountInfo(html):
    if len(re.findall(r'"discount":([\w$\s\.-]+)', html)):
        discount='-'+re.findall(r'"discount":([\w$\s\.-]+)', html)[0] + '%'
    else:
        discount = '0%'

    if discount == '0%':
        price = re.findall(r'"formatedPrice":"([\w$\s\.-]+)', html)[0]
        originprice=price    
    else:
        price = re.findall(r'"formatedActivityPrice":"([\w$\s\.-]+)', html)[0]
        originprice = re.findall(r'"formatedPrice":"([\w$\s\.-]+)', html)[0]
    return [discount, price, originprice]
    


def downloadProducts(url,result_list):
    html = gethtml_withcache(url)
    path=parseUrl(url)['path']
    # 商品信息字典
    product = {}
    product['id'] = re.findall(r'/(\d+)\.html', html)[0]
    product['href']=re.findall(r'"detailPageUrl":"//([\w$\s\.-/]+)',html)[0]
    product['title'] = re.findall(r'"title":"([\w./?=\-&,\s#]+)', html)[0]
    product['keyword'] = re.findall(r'"keywords":"([\w./?=\-&,\s°]+)', html)[0]
    product['imagePath']=re.findall(r'"imagePath":"([\w./?=\-&,\s°:✓]+)',html)[0]
    product['color'] = '\n'.join(re.findall(r'"propertyValueDefinitionName":"([\w$\s\.-]+)', html))
    product['total'] = re.findall(r'totalAvailQuantity":([\w$\s\.-]+)', html)[0]
    product['like'] = re.findall(r'"itemWishedCount":([\d]+)', html)[0]
    product['storename'] = re.findall(r'"storeName":"([\w./?=\-&,\s]+)', html)[0]
    product['storeurl'] = re.findall(r'"storeURL":"//([\w./?=\-&,\s]+)', html)[0]
    # 获取打折信息
    discount=diccountInfo(html)
    product['discount'] = discount[0]
    product['price'] = discount[1]
    product['originprice'] = discount[2]

    result_list.append(product)
    print(product)
    
        


if __name__ == "__main__":
    start_time = time.time()
    with open('./cookie/cookie.txt', 'r', encoding='utf-8') as f:
        global_headers['cookie'] = f.read()
    html = gethtml(url)
    print(html)
    catPages = parseCatories(html)
    
    p=Pool(50)
    manager = multiprocessing.Manager()
    productUrls=manager.list()
    products=manager.list()
    # 把链接放进任务列表
    for page in catPages:
        p.apply_async(downloadPages,args=(page,productUrls,))
    p.close()
    p.join()
    
    p=Pool(50)
    # 把链接放进任务列表    
    for productUrl in productUrls:
        p.apply_async(downloadProducts,args=(productUrl,products,))
    p.close()
    p.join()


    

    print('商品链接有：%s 个'%len(productUrls))
    print('products长度为 %s '%len(products))
    cost_time =time.time()-start_time
    print ('所用时间 %s秒 共下载页面 %s 个'%(cost_time,download_pages))
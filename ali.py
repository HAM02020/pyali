import time
import os
import threading
from queue import Queue
import re
import csv
import requests
from bs4 import BeautifulSoup
from bs4 import Tag

# 入口地址
url = 'www.aliexpress.com/all-wholesale-products.html'

# 如果为False 只爬取商品列表，不爬取商品详情
isparsedetail=True
refer_param='.1b9348b6RgB2tU'
referer_count = 1
download_pages = 0

global_headers = {
    'authority': 'lighthouse.aliexpress.com',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
    'sec-fetch-dest': 'script',
    'accept': '*/*',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-user': '?1',
    'accept-language': 'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
    'Sec-Fetch-Dest': 'script',
    'Origin': 'https://www.aliexpress.com',
    'cookie': 'ali_apache_id=11.251.144.15.1582389520679.186743.9; _bl_uid=hpkqs6b1xRytd9va088gv2U1hj0s; _ga=GA1.2.294288397.1582389527; aep_common_f=T/h3ppVGE2+ZffsxbJg0HdKsejJ1FF6UaVjxezQue7ar15kkEep1Tg==; cna=JbPmFnhJf3ACAXjntjqicOnt; _gid=GA1.2.1704154986.1584458403; _fbp=fb.1.1584508062963.1300902942; acs_usuc_t=x_csrf=wxlvr9639d54&acs_rt=7cdbb27bdb614de688c88dbb88a08327; intl_locale=en_US; XSRF-TOKEN=0532d07a-6119-4417-8c13-535ee335cd75; aep_history=keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%094000636440328%094000415085964%094000589759785%094000164591231%094000589759785%0932887602632%094000589759785%0932963657448; _m_h5_tk=835b51d225b0daf302c67e238ef8be09_1584697542895; _m_h5_tk_enc=32cf204e7518f91ab5d1ac3c51440f2f; havana_tgc=eyJjcmVhdGVUaW1lIjoxNTg0Njk1NDM0ODE5LCJsYW5nIjoiZW5fVVMiLCJwYXRpYWxUZ2MiOnsiYWNjSW5mb3MiOnsiMTMiOnsiYWNjZXNzVHlwZSI6MSwibWVtYmVySWQiOjIyMDc1NDkxMjYzNjcsInRndElkIjoiMUlqYVhLQ3psd1pXZDJ2SW9iWHY5dWcifX19fQ; _hvn_login=13; xman_us_t=x_lid=cn264863147yetae&sign=y&x_user=deA6xg8jjKCfouZhT24dZE2Xezz2ZF/BY0ib0Glr+JQ=&ctoken=10777ru6g27ab&need_popup=y&l_source=aliexpress; aep_usuc_t=ber_l=A0; xman_f=dnZc3dmaUTpsBdUxl2ktxg9YY0nqd1sWw7tN7OXltpyobu8GzceMyY1wGlZRXNk/T9Gmx91DKwcQgMAYELMwSlyEYsbrgv1k6X0TC7GvTiKtAsfe5zQg7oWfT4imXUWylI+dKugQN8qctQwTzefxA8c1wrCsORWkHMC/S1aLekT+GRvELOhxmHi166rGrKbPtfYwnfx7cS5vMI5szMapoySFbs05qx3cw8vQPmtxzcaoHM4RlkDhr4j/G5GIGPuL+87PBZzOAobxPYhhFQ5J2s/IAD/HpMk3KFCENa6ng+5KIv1ZaoFZb4yl9JsGfoTU6/DU8hzyjJWObJKIWPMThv1cjI6/ZSXbf3SGXt0yDoUVJMpKjefHsVRjdPxVDSq4a2vfzQMbgjwXYGe6nx6jqxKhUFSRNChi/6c2ZEpcg2byHAzK4XN3DQ==; aep_usuc_f=site=glo&c_tp=USD&x_alimid=1864220146&isb=y&region=CN&b_locale=en_US; ali_apache_track=mt=1|ms=|mid=cn264863147yetae; ali_apache_tracktmp=W_signed=Y; intl_common_forever=LFUARHdOGFaOksqkFvsMcer24KUEUX90+PFuwEYE7jqd+gHkiBRmEw==; JSESSIONID=C4B83EC748936477F9929CD515417507; xman_us_f=x_l=1&x_locale=en_US&no_popup_today=n&x_user=CN|CN|shopper|ifm|1864220146&x_c_chg=0&zero_order=y&acs_rt=f8063778288f4c6081056c503099bc3e&last_popup_time=1584506627220&x_as_i=%7B%22cookieCacheEffectTime%22%3A1584695590972%2C%22isCookieCache%22%3A%22Y%22%2C%22ms%22%3A%220%22%7D; xman_t=i7a7KvTOOmxWX9wqfP1RyNkOozR2lBZP6/8uu7h29/n8x/y3GgT1HgaLcIozO+LwSzRb+5BvzHB8WxUOvlorclCcYK0WkTxzS/WCQTZelaOEwfdNrFPyQlbVM86Y4VyiBL4y/I8z4vK5KbM/oZe3tlsefhb54dX/YkFdLT3D3MQJ+EedqGeMnk8DgjTry1MnxZXT5sGDhc4PaZAl7J845rrwg5mmK2D9aZqrrqlPbKpkY2IKLVp3GEailZ+jdZlRTmNdkKC73Nd8eGzQqs2hi7q8nh5I1+GQSbgV94m1O6u5M3f5c4m+hbfBnkB3iLvdgumaioSVqS3tyXGZ0zjMttBCSYoADnrd9J+a3fLnpllGPJovPjl2AegLOeVJn+67Qn1OdkBAk0MSEixQkt115Dj9tdQXLbHKGdxyPOw0QDgaMg2lC8NBLWI3PZ5VA4ai2Ckjzux579Jir2m9AOPqkkD2h7fq0xJwdvigVqzpNVVV7H9ECCVEW9muZdUwrDuKRXaKlMDz1PU1o2jtacrs5ZgZyDrapWXJkGFirTP/0gcv2CxVNS4FKMduV+QChQejqObSMCY26X4bwPWPpkYlbZuJEuzWngAPfbsJSG6Dd1aCUcrUsTrJcNlemihAFNRcu7gGqWgl4KjHT+usN//olA==; isg=BOfnzjHidYqMt_EgAsbtTgVidhuxbLtOsXoKErlVRHacqARqwTzcn5buzqg2QJPG; l=dBTicH2uQiXuoQjWBOfM5m-UJCbtEIOf1sPrgNGl9ICP92C65rGAWZ4JR58BCnGV3sXwR3J6m7-0BlLLFyznhADo6rheBjn9wd8pR',
    'Upgrade-Insecure-Requests': '1',
}



def gethtml(url,header=global_headers):
    try:
        r = requests.get(url, timeout=30, headers=header)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        global download_pages
        download_pages+=1
        return r.text
    except:
        return "exception"
    

def gethtml_withcache(url,header=global_headers,path='',fileName=''):
    # 文件名
    url='https://'+url
    if fileName.strip()=='':
        file_name = re.findall(r'[\w+\-\.]+\.html', url)[0]
    else:
        file_name=fileName
    # print(file_name)
    # 初始化缓存文件夹
    dir = os.path.join(os.curdir, 'cashe', path)
    if not os.path.isdir(dir):
        os.makedirs(dir)
    # 文件路径
    file_dir = os.path.join(dir, file_name)
    # 文件不存在的话创建文件，gethtml并写入缓存文件
    if not os.path.exists(file_dir):
        with open(file_dir, 'w+', encoding='utf-8') as f:
            html_str = gethtml(url,header)
            f.write(html_str)
            f.close()
    # 文件存在 读取缓存
    else:
        f = open(file_dir, 'r+', encoding='utf-8')
        html_str = f.read()
        # 文件存在但是为空
        if html_str.strip() == '':
            html_str = gethtml(url,header)
            f.write(html_str)
        if html_str.strip() == 'exception':
            f.write(' ')
        if 'location.href=\"https://login.aliexpress.com/?from=sm&return_url=\"+encodeURIComponent' in html_str:
            print("exception--LoginJump!!!")
            f.close()
            os.remove(file_dir)
        f.close
    return html_str
    
# 获取分类信息列表

def parseCategories(url):
    html = gethtml_withcache(url)
    soup = BeautifulSoup(html, 'lxml')
    containerDiv=soup.find("div",{"class":"util-clearfix cg-container"})
    rootDivs=list(containerDiv.div.contents)
    categories = []
    for itemdiv in rootDivs:
        category = {}
        if not isinstance(itemdiv,Tag):
            continue
        root_name=itemdiv.h3.a.text
        root_href = itemdiv.h3.a['href'].replace('//', '')

        branch_name_list=re.findall(r'(?<=html">).+(?=</a>)',str(itemdiv.div.div.ul.contents))
        branch_href_list = re.findall(r'(?<=href="//).+\.html', str(itemdiv.div.div.ul.contents))
        #获取商品信息
        rootproducts = parseGoods(root_href,rootpath=root_name)
        
        category['root']={'name':root_name,'herf':root_href,'products':rootproducts}
        branchs=[]
        for i in range(len(branch_name_list)):
            branchproducts = parseGoods(branch_href_list[i], root_name, branch_name_list[i])
            branch = {'name':branch_name_list[i],'href':branch_href_list[i],'products':branchproducts}
            branchs.append(branch)
        category['branchs'] = branchs
        categories.append(category)

    return categories

# 商品列表界面及翻页
def parseGoods(url, rootpath='', branchpath=''):
    catName = re.findall(r'([\w+\-\.]+)\.html', url)[0]
    catId = re.findall(r'/(\d+)/', url)[0]
    
    global referer_count
    headers = global_headers
    headers['referer'] = 'https://' + url + '?spm=a2g0o.category_nav.1.' + str(referer_count) + refer_param
    headers['Referer'] = headers['referer']
    # 目录计数器加1
    referer_count += 1

    # 翻页操作
    for pageNum in range(1, 11):
        if pageNum > 1:
            nextPage_param = '?trafficChannel=main&catName=' + catName+ '&CatId=' + catId + '&ltype=wholesale&SortType=default&page=' + str(pageNum)
            url = url + nextPage_param
            headers['referer'] = url
            headers['Referer'] = url
        # 获取一页中的商品列表
        path=os.path.join(rootpath, branchpath)
        fileName=catName
        print("正在获取 %s "%url)
        html = gethtml_withcache(url, header=headers, path=path,fileName=fileName+str(pageNum)+'.html')
        productHrefs = re.findall(r'"productDetailUrl":"//([\w./?=\-&,]+)',html)
        # 获取商品详情
        productList = []
        # 判断爬不爬商品详情，先不爬的目的是为了先把页面缓存完
        if isparsedetail:
            for url in productHrefs:
                product = parseDetail(url, os.path.join(path), refer=headers['referer'])
                productList.append(product)
                print("商品信息：%s" % product)
        # return productList    # 如果不翻页,在这这return
    return productList


# 商品详情页
def parseDetail(url, path='', refer=''):
    headers = global_headers
    headers['referer'] = refer
    headers['Referer'] = refer
    print('正在获取 = %s'%url)
    html = gethtml_withcache(url, header=headers, path=os.path.join(path,'products'), fileName=re.findall(r'/([\d]+.html)', url)[0])
    
    # 商品信息字典
    product = {}
    product['id'] = re.findall(r'/(\d+)\.html', html)[0]
    product['href']=re.findall(r'"detailPageUrl":"//([\w$\s\.-/]+)',html)
    product['title'] = re.findall(r'"title":"([\w./?=\-&,\s]+)', html)[0]
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
    product['originprice']=discount[2]
    return product

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
    
    return [discount,price,originprice]

if __name__ == "__main__":
    start_time = time.time()
    
    categories = parseCategories(url)
    print("done")

    cost_time=time.time()-start_time
    print('下载了%s个页面,用时%s秒'%(download_pages,categories))


























































    # export_csv(categories)
    
    # 结构[{'root':{'name':'Women's Clothing',
    #               'href':'www.ali.com/aaa.html',
    #               'products':[{'id':'123',
    #                            'price':'US $9.8,
    #                             '...' : '...',
    #                           },
    #                           {'id':'123',
    #                            'price':'US $9.8,
    #                             '...' : '...',
    #                           },...
    #                          ]
    #              },
    #       'branchs':[{'name':'Skirt',
    #                   'href':'www.ali.com/Skirt.html',
    #                   'products':[{'id':'123',
    #                                'price':'US $9.8,
    #                                '...' : '...',
    #                               },
    #                               {'id':'123',
    #                                'price':'US $9.8,
    #                                '...' : '...',
    #                               },...
    #                              ]
    #                   },
    #                  {'name':'Skirt',
    #                   'href':'www.ali.com/Skirt.html',
    #                   'products':[{'id':'123',
    #                                'price':'US $9.8,
    #                                '...' : '...',
    #                               },
    #                               {'id':'123',
    #                                'price':'US $9.8,
    #                                '...' : '...',
    #                               },...
    #                              ]
    #                   },.....
    #                  ]
    # ...]
import os
import re
import csv
import requests
from bs4 import BeautifulSoup
from bs4 import Tag

# 如果为False 只爬取商品列表，不爬取商品详情
isparsedetail=True
refer_param='.5c3548b69Y6Dhl'
referer_count = 1

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
    'cookie': 'ali_apache_id=11.251.144.15.1582389520679.186743.9; _bl_uid=hpkqs6b1xRytd9va088gv2U1hj0s; _ga=GA1.2.294288397.1582389527; aep_common_f=T/h3ppVGE2+ZffsxbJg0HdKsejJ1FF6UaVjxezQue7ar15kkEep1Tg==; cna=JbPmFnhJf3ACAXjntjqicOnt; _gid=GA1.2.1704154986.1584458403; _fbp=fb.1.1584508062963.1300902942; xman_f=cyDTEoLnE127tPyliC0NPStqxFu1hmAqXhAjCWeO+Vb1GFbI9WOhQqMV36EZ4AwQbfsjDqdJLMIFmtAtH755jmfbsYvb95OmD879lUuv1qoQqt+TFDQyOeKyXtGgMhWSGe1L1B5UOyhvfyW1uJweW8kNLRpyHjhssd6cbOQnEeoo5y7OcD0ZhoVZVWnjrS8Qoj9r7mzXupGBzV4BkiZQmfMgAPVapY6XXy2wYOM3ZiKq7tvPYuzh3b6UDN8L3Adj4FhGe7MNGyYWJUsI9lXNozZBsAEvPgqmG56TteKFFO2B7ioxCCwRJkqPzREGQ8rUmY1wIHjO0RsK297GoEziO3VZznLsfY2uZA9Cba17D95ojpC/1tiYmyrFY6GFVIZTaXHuN3ttW4Jy/sC51fhKN/YcbFeieeKzPwtTWf+atjsrM3QkuJEsoQ==; aep_usuc_f=site=glo&c_tp=USD&x_alimid=1864220146&isb=y&region=CN&b_locale=en_US; ali_apache_track=mt=1|mid=cn264863147yetae; acs_usuc_t=x_csrf=ccqcl6xmrldo&acs_rt=48ec89361e524f34a47e14dc3d1b7e85; intl_locale=en_US; xman_t=63ofa8X0Aj0yFiKylXQO0ox69CLXkCg9MdLEQ8HosNforkIUuOlpjTKoKkSgnEiG; ali_apache_tracktmp=; XSRF-TOKEN=3545b1e8-8764-4b70-a418-f7089bfde10a; intl_common_forever=cX4q+GwD5eLrGzpn88uoQlbiVmmv8DZmQVP0FJpwjLAmUl+AIed1dg==; JSESSIONID=28F03D3D9D484378669D4FFB911E5057; aep_history=keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%094000517751702%094000636440328%094000415085964%094000589759785%094000164591231%094000589759785%0932887602632%094000589759785; _m_h5_tk=3268f885ccbd52f56f63d5578788a574_1584684145482; _m_h5_tk_enc=bfa30084620df2e7e4cb65550fabdfb4; xman_us_f=zero_order=y&x_locale=en_US&x_l=1&last_popup_time=1584506627220&x_user=CN|CN|shopper|ifm|1864220146&no_popup_today=n&x_c_chg=0&x_as_i=%7B%22cookieCacheEffectTime%22%3A1584682250677%2C%22isCookieCache%22%3A%22Y%22%2C%22ms%22%3A%220%22%7D&acs_rt=f8063778288f4c6081056c503099bc3e; isg=BEZGJSqOZCXQsDDny518MfwZlzzIp4ph-NGLFTBu-GlEM-BNnDddcXCJD2__m4J5; l=dBTicH2uQiXuozJEBOfi5m-UJCbTEIdfhsPrgNGl9ICP9WfW5zSCWZ4-Xu8XCnGVHs6D53J6m7-0BPLd7yIEnxv9-cbwV5HmndC..',
    'Upgrade-Insecure-Requests': '1',
}



def gethtml(url,header=global_headers):
    try:
        r = requests.get(url, timeout=30, headers=header)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
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
                product = parseDetail(url, os.path.join(path, fileName), refer=headers['referer'])
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
    html = gethtml_withcache(url, header=headers, path=path, fileName=re.findall(r'/([\d]+.html)', url)[0])
    
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
    # 入口地址
    url = 'www.aliexpress.com/all-wholesale-products.html'
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
    categories = parseCategories(url)
    print("done")
    # export_csv(categories)
    
    
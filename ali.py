import os
import re
import csv
import requests
from bs4 import BeautifulSoup
from bs4 import Tag

global_headers = {
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
    'cookie': 'ali_apache_id=11.251.144.15.1582389520679.186743.9; _bl_uid=hpkqs6b1xRytd9va088gv2U1hj0s; _ga=GA1.2.294288397.1582389527; aep_common_f=T/h3ppVGE2+ZffsxbJg0HdKsejJ1FF6UaVjxezQue7ar15kkEep1Tg==; cna=JbPmFnhJf3ACAXjntjqicOnt; _gid=GA1.2.1704154986.1584458403; intl_locale=en_US; ali_apache_tracktmp=W_signed=Y; _fbp=fb.1.1584508062963.1300902942; XSRF-TOKEN=752cf89b-16f5-4cf0-921e-b0fbc3581883; _hvn_login=13; aep_usuc_t=ber_l=A0; acs_usuc_t=acs_rt=485b0a55faba4ab9ad7820278b07dcf9&x_csrf=129qmtntk0h7d; havana_tgc=eyJjcmVhdGVUaW1lIjoxNTg0NTE1OTE0MjYyLCJsYW5nIjoiZW5fVVMiLCJwYXRpYWxUZ2MiOnsiYWNjSW5mb3MiOnsiMTMiOnsiYWNjZXNzVHlwZSI6MSwibWVtYmVySWQiOjIyMDc1NDkxMjYzNjcsInRndElkIjoiMVBvTWswU2s0dTdfY0hydWJNcW1HbGcifX19fQ; xman_us_t=x_lid=cn264863147yetae&sign=y&x_user=jJFAX0mBlbPukFddy8s775ztQtYodqgrQMAkf7y1yQM=&ctoken=11tv721ycufn4&need_popup=y&l_source=aliexpress; xman_f=cyDTEoLnE127tPyliC0NPStqxFu1hmAqXhAjCWeO+Vb1GFbI9WOhQqMV36EZ4AwQbfsjDqdJLMIFmtAtH755jmfbsYvb95OmD879lUuv1qoQqt+TFDQyOeKyXtGgMhWSGe1L1B5UOyhvfyW1uJweW8kNLRpyHjhssd6cbOQnEeoo5y7OcD0ZhoVZVWnjrS8Qoj9r7mzXupGBzV4BkiZQmfMgAPVapY6XXy2wYOM3ZiKq7tvPYuzh3b6UDN8L3Adj4FhGe7MNGyYWJUsI9lXNozZBsAEvPgqmG56TteKFFO2B7ioxCCwRJkqPzREGQ8rUmY1wIHjO0RsK297GoEziO3VZznLsfY2uZA9Cba17D95ojpC/1tiYmyrFY6GFVIZTaXHuN3ttW4Jy/sC51fhKN/YcbFeieeKzPwtTWf+atjsrM3QkuJEsoQ==; aep_usuc_f=site=glo&c_tp=USD&x_alimid=1864220146&isb=y&region=CN&b_locale=en_US; ali_apache_track=mt=1|ms=|mid=cn264863147yetae; aep_history=keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%094000643054078%094000012569319%0932846610151%094000594087568; intl_common_forever=yKbqR9ZkDkXrZ/XiKz31YqqsfmzzVFNaCzUJnIy9chn5JFiBrLPfPA==; JSESSIONID=E70A56547791C8B22DFCAC5BB99B3D98; _m_h5_tk=d6fe3e594799d686a75f56b197beb8dd_1584527711298; _m_h5_tk_enc=1ad513bb63e0220ad31f363e94e77172; xman_us_f=zero_order=y&x_locale=en_US&x_l=1&last_popup_time=1584506627220&x_user=CN|CN|shopper|ifm|1864220146&no_popup_today=n&x_c_chg=0&x_as_i=%7B%22cookieCacheEffectTime%22%3A1584525484735%2C%22isCookieCache%22%3A%22Y%22%2C%22ms%22%3A%220%22%7D&acs_rt=f8063778288f4c6081056c503099bc3e; xman_t=g7OwUgP+2DNL6njvhbx2miYXactEHvAKUHNGY4xvri74PGpXFDYoMaKHmMtFlSHODr8EL2M7pVpw/WqN1py0hwRjQ1kaxWGVhVcm/3B1tSGb6ZwxqpBqIyBCitBDEf8sFu2gACbsv8RQVq3Bd8mQJ0IBAxbBPXdsKBhS9r7Vnk20s2E57PXGYWkuhash4mGnce8UQrxben1oM1x32s20bI5ZlPHXZGyD/1TM2vE/3oKRoAEnWfCfcX+abHxkCSa1Vbg3kc1i/Uis61FArj22hOEH/s8YY+RBID99x25RRCzVQOC1VFQVZiM87PZ7PCq85C3WpBFGAWZYy96+M3fPQC8t1dpGLFQBi7MK4Hc7EIgOZszTd40G1h8vznrPFjs0J482HxvUTBcfcnHnjzUEBUi746vOQi/Unqtll91Y/n5DiRlkacrHcGKHljxEI+aBVcSuPo4XnBDnuSbLEiFAsacEbH0gJ+3Ya1AmGtZ8wGV4KQHweIiEL8v18Hju5MsAxgkNb253XqpW7zsolEywWvh6TGeWHlllCXuEPZ6BsKi6vl+lLt0juCF01znYCni+0zkhuO5XsBjpWVTZk3D69FpPr1tIaO620JeeeP9dXV63yEPYbFU+PRz0KZ+9SF/r557/90BL5a+FN5yQ+D/Vww==; x5sec=7b2261652d676c6f7365617263682d7765623b32223a223261313137346639383937383833316561656563386432613037326637646637434a666b782f4d4645507a677662695a2f50336a64426f4d4d5467324e4449794d4445304e6a7378227d; isg=BHp6kDUj8IRSAXzLH6FIFYBdy6CcK_4F1JVHeYRz7I3YdxuxbLmaFFSGwwOrY3ad; l=dBTicH2uQiXuogOGBOfwRm-UJCbTZIRb8oVrgNGl9ICPO9fp56zFWZ4fitY9CnGV36SWR3J6m7-0BcYTuy4ehGLAULdF0J_XbdTeR',
    'Upgrade-Insecure-Requests': '1',
}
referer_count=1


def gethtml(url,header=global_headers):
    try:
        r = requests.get(url, timeout=30, headers=header)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "exception"
    

def gethtml_withcache(url,header=global_headers,path='cashe',fileName=''):
    # 文件名
    if fileName.strip()=='':
        file_name = re.findall(r'[\w+\-\.]+\.html', url)[0]
    else:
        file_name=fileName
    # print(file_name)
    # 初始化缓存文件夹
    dir=os.path.join(os.curdir, path )
    if not os.path.isdir(dir):
        os.makedirs(dir)
    # 文件路径
    file_dir = os.path.join(dir, file_name)

    # 文件不存在的话创建文件，gethtml并写入缓存文件
    if not os.path.exists(file_dir):
        with open(file_dir, 'w+', encoding='utf-8') as f:
            html_str = gethtml(url,header)
            f.write(html_str)
    # 文件存在 读取缓存
    else:
        f = open(file_dir, 'r+', encoding='utf-8')
        html_str = f.read()
        # 文件存在但是为空
        if html_str.strip() == '':
            html_str = gethtml(url,header)
            f.write(html_str)
        if 'location.href=\"https://login.aliexpress.com/?from=sm&return_url=\"+encodeURIComponent' in html_str:
            print("exception--LoginJump!!!")
            f.close()
            os.remove(file_dir)
        f.close
    return html_str

def parseDetail(url):
    pass

def parseGoods(url):
    global referer_count
    headers = global_headers
    arguments='.263d48b6jSs1KV'
    headers['referer'] = 'https://' + url + '?spm=a2g0o.category_nav.1.' + str(referer_count) + arguments
    headers['Referer'] = headers['referer']
    html=gethtml_withcache(url, headers)
    referer_count += 1
    
# 获取分类信息列表


def parseCategories():
    containerDiv=soup.find("div",{"class":"util-clearfix cg-container"})
    rootDivs=list(containerDiv.div.contents)
    categories = []
    for itemdiv in rootDivs:
        category = {}
        if not isinstance(itemdiv,Tag):
            continue
        root_name=itemdiv.h3.a.text
        root_href = itemdiv.h3.a['href'].replace('//', '')

        category['root'] = {'root_name': root_name, 'root_href': root_href}
        branch_name_list=re.findall(r'(?<=html">).+(?=</a>)',str(itemdiv.div.div.ul.contents))
        branch_href_list = re.findall(r'(?<=href="//).+\.html', str(itemdiv.div.div.ul.contents))
        #获取商品信息
        parseGoods(root_href)
        for i in range(len(branch_name_list)):
            parseGoods(branch_href_list[i])
        categories.append(category)
    return categories
# def parseGoods():
#     i = 1
#     for categorieDict in categories:
#         parentName = categorieDict['parentName']
#         parentHref = categorieDict['parentHref']
#         # 配置头信息
#         headers['referer'] = 'https:' + parentHref + \
#             '?spm=a2g0o.category_nav.1.'+str(i)
#         xxxx = '.2c2c48b6fey8QY'
#         headers['referer'] = headers['referer'] + xxxx
#         headers['Referer'] = headers['referer']
#         # 获取
#         html = gethtml_withcache('https:' + parentHref)
#         i=i+1
#         print('获取根目录 = %s' % parentName)
#           # shop ...
#         # 子目录
#         for childrenDict in categorieDict['childrenList']:
#             childrenName = childrenDict['name']
#             childrenHref = childrenDict['href']
#             # 配置头信息
#             headers['referer'] = 'https:' + childrenHref + \
#                 '?spm=a2g0o.category_nav.1.'+str(i)
#             headers['referer'] = headers['referer'] + xxxx
#             headers['Referer'] = headers['referer']
#             html = gethtml_withcache('https:' + childrenHref)
#             i = i + 1
#             print('获取子目录 = %s' % childrenName)
#     print("总目录数目 = %s"% (i-1))

# def export_csv(data):
#     for d in data:
#         parentName = d['parentName']
#         parentHref = d['parentHref']
#         childrenList = d['childrenList']
#         for childrenDict in childrenList:
#             childrenName = childrenDict['name']
#             childrenHref = childrenDict['href']
#             dir = os.path.join(os.curdir, 'output', parentName)
#             file_dir = os.path.join(dir, childrenName.replace('/', ' ')+'.csv')
#             # print('dir = %s file_dir = %s'%(dir,file_dir))
#             if not os.path.isdir(dir):
#                 os.makedirs(dir)
#             with open(file_dir, 'w+', newline='') as f:
#                 writer = csv.writer(f)
#                 writer.writerow(['主分类', '主分类链接', '分类', '分类链接'])
#                 writer.writerows([(parentName, parentHref, childrenName,childrenHref)])


if __name__ == "__main__":

    url = 'https://www.aliexpress.com/all-wholesale-products.html'
    html = gethtml_withcache(url,path='11111\\2222\\33333\\4444')
    soup = BeautifulSoup(html, 'lxml')
    # categories = parseCategories()
    # parseGoods()
    
    # print(categories[0]['branch'])

    print("done")

    # export_csv(categories)
    
    
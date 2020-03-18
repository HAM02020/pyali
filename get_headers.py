head_str='''accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9
cookie: bx-extrainfo=%22%7B%22uuid%22%3A%2217fcaf631ceeb4f6910784ddb493f75a%22%7D%22; ali_apache_id=11.251.144.15.1582389520679.186743.9; _bl_uid=hpkqs6b1xRytd9va088gv2U1hj0s; _ga=GA1.2.294288397.1582389527; aep_history=keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%094000643054078%094000012569319; aep_common_f=T/h3ppVGE2+ZffsxbJg0HdKsejJ1FF6UaVjxezQue7ar15kkEep1Tg==; cna=JbPmFnhJf3ACAXjntjqicOnt; ali_apache_track=mt=1|mid=cn264863147yetae; _gid=GA1.2.1704154986.1584458403; acs_usuc_t=x_csrf=je32744idprj&acs_rt=485b0a55faba4ab9ad7820278b07dcf9; intl_locale=en_US; ali_apache_tracktmp=; intl_common_forever=x2uagc2hyvcyvbpVl3Dz0nlcrWD/LbBMZcaUlYGkRCvV18JuFt5YRQ==; JSESSIONID=4531FC9FFB6F3F1239E74174D55533A6; _m_h5_tk=e414f4e700b87ac5f9b337f19e4e2c7a_1584508146299; _m_h5_tk_enc=02b6c4dec9c249dfb40ba0e823d1b8e6; havana_tgc=eyJjcmVhdGVUaW1lIjoxNTg0NTA2NjI3MDY0LCJsYW5nIjoiZW5fVVMiLCJwYXRpYWxUZ2MiOnsiYWNjSW5mb3MiOnsiMTMiOnsiYWNjZXNzVHlwZSI6MSwibWVtYmVySWQiOjIyMDc1NDkxMjYzNjcsInRndElkIjoiMXRtel9XZTh1cEtpVy1NdE83aU1xeEEifX19fQ; _hvn_login=13; xman_us_f=x_l=1&x_locale=en_US&no_popup_today=n&x_user=CN|CN|shopper|ifm|1864220146&x_c_chg=0&zero_order=y&acs_rt=f8063778288f4c6081056c503099bc3e&last_popup_time=1584506627220&x_as_i=%7B%22cookieCacheEffectTime%22%3A1584505833512%2C%22isCookieCache%22%3A%22Y%22%2C%22ms%22%3A%220%22%7D; aep_usuc_f=region=CN&site=glo&b_locale=en_US&isb=y&x_alimid=1864220146&c_tp=USD; xman_us_t=x_lid=cn264863147yetae&sign=y&x_user=jJFAX0mBlbPukFddy8s773+M8AaC3RxU6y8OFt28PQE=&ctoken=os15k6jbdm7m&need_popup=y&l_source=aliexpress; aep_usuc_t=ber_l=A0; xman_t=lV/eYfuzKKYEGutCFusOhCM48HrvzFVh6JUn6JBlB+7959Uh20EHkf/47kZcZpDEQkk5u+RdNw5Fv+vd2z86q+c8ugHMF5FXI6oibiyObRdZofBVx2aBjyQc+493RLcdkK8d2Ccus1MVff5rbKcY0bSsW/j6FMBK7qejGzUEX1H6zSnovJ1gXD4aiOe/Jy6tefhVpRwyncbZQeUyRmhH0kmQgU3mqqKvh4YgonpzMxxaGFxjLSyU67kUq1dd78AJ0Pcy2nHzkpgA+L19eRrcAUZ8KyXnlbklCeHjFqpTqeSDbpetu2pun00GCqmPDgaMuORHS1/JEMwYSA77Fw8FP5b455vMUp4nTpNykwjevT1AbfDT2jx5tprFXAdW0SGFvAXbqc3kkYJlfKE1QVe8vTWURcARWH6+D9PfUW14SkH0SXPNgtkzR+NYY36k5PGcihU6z2OCei9JoGCaQn2iBcAh+zfxks3nlaiHRk4n8iUHcV8SyZ2NNXxF8MQycXdpWNKzu8HEhoZaRArdNieeKmPXN5HqvZ2gJ0UhXlTn7RoFCTdSQ+OPinRuWOFa3vXk+YA47zv+nUOIffuzguwDBq9xHQr11BlZB6bSu37AVHAsZf12otdqrFfkm1WRTNaH4OnBd9lt1IeZv/Tq5nfJ0w==; xman_f=pAoUy7PO6HrTw87/h53tFQjPraAJPUdwUrYCzb6H1p0WImmYYgUnMFwTnMKIQtspRfrGC60MmW627QQl/IpwIhuCp6WDX/U3Jc79ZevWl4/XrZ87k4ie6XjjmBVkVeZWISTy20DjJMxGyhG6iWImqcmrhSJXdNcmihsW1NiNuiB5blDh0fI3PuRllcYTQniyGucXAISzpc+05W44XwSsWr+hRUWzmxXEmIwph94VvKGUgRhhb6zz1TbBAFgEVFqolaHjpQ90hnGPBkkg9oCj0bpT9iygq1LE61qVbIJ3ATYuNtln0FgW8i0gs6DvLUIehKwAdxsQrNb99l+11B36oqszHCf8/TvHsKV5SKGsK3K8/R9b1CtofzeoJiMSbpgkF5ojnEPwm8F5R4JFhydXjbAmMnVScB4u/gA1sUrVe4GN2eB50FS7/g==; isg=BEdHrS5X1a_CVlEAoiZNbmUC1vsRTBsu0Rqqchk2Mlb9iGNKIB7Rf-oJLkjWZfOm; l=dBTicH2uQiXuo4b1BOfNIm-UJCb9aQAfGPVrgNGl9ICPOUCw5S9cWZ4XU1YeCnGVns9BJ3J6m7-0BbTs1y4EQxv9-ewdVEbrndLh.
sec-fetch-dest: document
sec-fetch-mode: navigate
sec-fetch-site: none
sec-fetch-user: ?1
upgrade-insecure-requests: 1
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'''
def get_headers(header_raw):
  """
  通过原生请求头获取请求头字典
  :param header_raw: {str} 浏览器请求头
  :return: {dict} headers
  """
  return dict(line.split(": ", 1) for line in header_raw.split("\n"))

if __name__ == "__main__":
    dict_headers=get_headers(head_str)
    print(dict_headers)

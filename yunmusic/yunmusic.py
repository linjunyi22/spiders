# 抓取网易云音乐下的评论
# 网易云评论 ajax 请求中的使用了 js 加密参数，等把加密算法搞明白了再继续抓。。。
import requests
import json


url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_515453363'
headers = {
	'Accept':'*/*',
	'Accept-Encoding':'gzip, deflate',
	'Accept-Language':'zh-CN,zh;q=0.9,la;q=0.8',
	'Connection':'keep-alive',
	'Content-Length':'480',
	'Content-Type':'application/x-www-form-urlencoded',
	'Cookie':'_ntes_nnid=947ba0480bea3580462d6312b46ce75e,1507614684150; _ntes_nuid=947ba0480bea3580462d6312b46ce75e; _ngd_tid=EnObe2KQySBJ216kPDBLCoVsRE15eZwL; mail_psc_fingerprint=8bc06ad39005e1458a3f0373388235ea; UM_distinctid=15f0b08f7f5134-0268faaff5dac6-31657c00-13c680-15f0b08f7fb13a; __gads=ID=2a0d3c237905a3c6:T=1507718655:S=ALNI_MZsE0SuIM_KCRaJPH4MaUYBYVh8_g; vjuids=11626f2c97.15f0b08fe14.0.3ea9814a8ca68; usertrack=c+xxC1nzTNiRgiZYA6g/Ag==; _ga=GA1.2.1920202991.1508420011; NTES_CMT_USER_INFO=120381687%7C%E6%9C%89%E6%80%81%E5%BA%A6%E7%BD%91%E5%8F%8B07be3T%7C%7Cfalse%7CbGp5YWxhbkAxMjYuY29t; __oc_uuid=18e80480-b4d2-11e7-8bda-3590305af234; __f_=1517322142679; s_n_f_l_n3=d485a2fb734cf0111519568244402; _iuqxldmzr_=32; __utmc=94650624; __utma=187553192.1920202991.1508420011.1514385181.1520780877.7; __utmc=187553192; __utmz=187553192.1520780877.7.6.utmcsr=open.163.com|utmccn=(referral)|utmcmd=referral|utmcct=/; vjlast=1507718660.1523280772.21; ne_analysis_trace_id=1523280772185; NNSSPID=67c3e061d95240febe704bc48d3f530d; vinfo_n_f_l_n3=d485a2fb734cf011.1.4.1507718659622.1512221856846.1523281065021; JSESSIONID-WYYY=nv%2BM9gU1FUYcClTTBovZtnpT%5C%5CUQZvBSJMVr02nwCDG3Z7XYtBeXeMy02yA8kmvZtBM6PKQ%2FCYneUq7GmBCU%2B1PM0duQ6hyCT9GsDEW%2BJ%2FQD3wokjR28uPD0Hlm%5CKWsbBi7whgissOKbf9ne0A0IKVasecrvpt2DVc6XgaO7pV6QYB8K%3A1523376221243; __utma=94650624.1920202991.1508420011.1523368574.1523374421.8; __utmz=94650624.1523374421.8.7.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; playerid=57313792; __utmb=94650624.4.10.1523374421',
	'Host':'music.163.com',
	'Origin':'http://music.163.com',
	'Referer':'http://music.163.com/song?id=515453363',
	'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}

data = {
	'params':'WHWDddi7zhIWVERUn22lRkNmGq4Fktfo4/lykPSQ09AMEUqqthEPczA5ABOXU9Yao5Gwi1eiMlrkZz2Gd0bOwy8nsFW5/4XZOFarsR64BhKJAV8I3a3dDDlq9Pcz+xIgEwiCpWTg/HkZKV0JM0o0siTqEbVTt+yEHbkWqHS/xXYq7iuMdiq8xMCM+kWQRt8U',
	'encSecKey':'8a239ab6aacf0b3f7402845d966c32f01774cc48fe97e6c3003963fdce682671f291f39f111856c7630e9886ecd874435ed056b59ce270875f78392263686af4951acf6697b95b7fba4476ce0d4b482c6f5d01b759bdc1cbbbc9148562deeb8bd5771a75ec096974d5c4e33c08945bc53e268fb821f22230041e0491e94c4937'

}

def get_page(url,headers,data):
	r = requests.post(url,headers=headers,data=data)
	r_json = json.loads(r.text)
	print(r_json["hotComments"])

get_page(url,headers,data)



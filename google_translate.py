
#coding:utf-8
import urllib
import re  
import requests
import codecs
from retry import retry
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import json
import execjs
import time
if sys.version_info[0] == 2:  # Python 2
    from urllib import quote
else:  # Python 3
    from urllib.parse import quote
import locale

locale.getdefaultlocale()[1]

headers = {"User-Agent": "Mozilla/5.0(Macintosh;IntelMacOSX10_7_0)AppleWebKit/535.11(KHTML,likeGecko)Chrome/17.0.963.56Safari/535.11",
            "cookie": "_ga=GA1.3.601448104.1547798526; _gid=GA1.3.1453839211.1547798526; 1P_JAR=2019-1-18-9; NID=156=XjyaaJc-Uth1E6-WwtVYETyLCEXqtEKL9G8xxLlOSX0lIVehPC8uE_hdsJqEMAbu2eSjcEG8Aq5WRawU9JQsirT2VESCsYnlCmBwK4cbWYNMgNkUVgLO_dH1YbJnKUY-UhcImcYCJ8u6MnT3Pnwb7CkmyxrWpWfcFvzatvgFj0w"
           }



class Py4Js():
    def __init__(self):
        self.ctx = execjs.compile(""" 
        function TL(a) { 
        var k = ""; 
        var b = 406644; 
        var b1 = 3293161072; 
        var jd = "."; 
        var $b = "+-a^+6"; 
        var Zb = "+-3^+b+-f"; 
 
        for (var e = [], f = 0, g = 0; g < a.length; g++) { 
            var m = a.charCodeAt(g); 
            128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023), 
            e[f++] = m >> 18 | 240, 
            e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224, 
            e[f++] = m >> 6 & 63 | 128), 
            e[f++] = m & 63 | 128) 
        } 
        a = b; 
        for (f = 0; f < e.length; f++) a += e[f], 
        a = RL(a, $b); 
        a = RL(a, Zb); 
        a ^= b1 || 0; 
        0 > a && (a = (a & 2147483647) + 2147483648); 
        a %= 1E6; 
        return a.toString() + jd + (a ^ b) 
    }; 
 
    function RL(a, b) { 
        var t = "a"; 
        var Yb = "+"; 
        for (var c = 0; c < b.length - 2; c += 3) { 
            var d = b.charAt(c + 2), 
            d = d >= t ? d.charCodeAt(0) - 87 : Number(d), 
            d = b.charAt(c + 1) == Yb ? a >>> d: a << d; 
            a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d 
        } 
        return a 
    } 
    """)

    def getTk(self, text):
        return self.ctx.call("TL", text)


@retry(tries=3)
def translate(content):
    # try:
    if len(content) == 0:
        texts = ''
        return texts
    js = Py4Js()
    tk = js.getTk(content)
    # content = quote(content)
    url = "https://translate.google.cn/translate_a/single?client=webapp&sl=auto&tl=en&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&dt=gt&ssel=0&tsel=3&kc=0&tk={}".format(tk)
    data = {"q": content}
    response = requests.post(url,data=data, headers=headers)
    result = response.content
    item = json.loads(result)
    texts = ""
    for i in range(0, len(item[0])):
        if str(item[0][i][0])!="None":
            texts += str(item[0][i][0])
    return texts
    # except:
    #       return ""

@retry(tries=3)
def translate_zh(content):
    if len(content) == 0:
        return ""
    js = Py4Js()
    tk = js.getTk(content)
    url = "https://translate.google.cn/translate_a/single?client=webapp&sl=auto&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&pc=1&otf=1&ssel=0&tsel=0&kc=1&tk={}".format(tk)
    data = {"q":content}
    response = requests.post(url, data=data, headers=headers)
    result = response.content
    item = json.loads(result)
    texts = ""
    for i in range(0, len(item[0])):
        if str(item[0][i][0]) != "None":
            texts += str(item[0][i][0])
    return  texts


# 将英文翻译成中文
@retry(tries=3)
def zh(content):
    texts = ""
    # try:
    if len(content) == 0:
        return texts
    js = Py4Js()
    tk = js.getTk(content)
    # content = quote(content)
    url = "https://translate.google.cn/translate_a/single?client=webapp&sl=en&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&otf=2&ssel=0&tsel=0&kc=3&tk=%s&q=%s" % (
    tk, content)
    response = requests.get(url, headers=headers)
    result = response.content
    item = json.loads(result)

    for i in range(0, len(item[0])):
        if str(item[0][i][0])!="None":
            texts += str(item[0][i][0])
    return texts

    # except Exception as e:
    #     print e
    #     return ""

def split_string(str,cutting_method):
    item = str.split(cutting_method)
    interception_len = len(item)/2
    interception1 = ".".join(item[:interception_len])
    interception2 = ".".join(item[interception_len:len(item)])
    return interception1,interception2

def get_string(str,cutting_method):
    list = []
    interception1,interception2 = split_string(str,cutting_method)
    if len(interception1) > 5000:
        list1 = get_string(interception1,cutting_method)
        list = list+list1
    else:
        list.append(interception1)
    if len(interception2) >5000:
        list1 =get_string(interception2,cutting_method)
        list = list + list1
    else:
        list.append(interception2)
    return list

# 自动检测语言后翻译成英文
def get_translate(context):
    str =""
    if len(context) > 5000:
        list = get_string(context,".")
        count = 0
        for item in list:
            count+=1
            if count != len(list):
                item =item+"."
            str+=translate(item)
    else:
        str = translate(context)
    return str

# 检测语言后翻译成中文
def get_translate_zh(context):
    str = ""
    if len(context) > 5000:
        list = get_string(context, ".")
        count = 0
        for item in list:
            count += 1
            if count != len(list):
                item = item + '.'
            str += translate_zh(item)
    else:
        str = translate_zh(context)
    return str

#英文翻译中文
@retry(tries=3)
def get_zh(context):
    str =""
    if len(context) > 5000:
        list = get_string(context,".")
        count = 0
        for item in list:
            count+=1
            if count != len(list):
                item =item+"."
            str+=zh(item)
    else:
        str = zh(context)
    return str



if __name__ == '__main__':
    # print get_zh('A man killed his daughter, son-in-law and two grandsons in the Jalalpur area. His motive was reportedly that his daughter chose her own husband four years ago.The incident took place in Pindi Bhattian, according to SAMAA TV correspondent Bilal Akbar.According to the police all four were killed using a sharp blade.The bodies have been sent to the local taluka headquarters hospital.The authorities say the man fled after the incident but the police were able to arrest him after conducting raids. A case has been registered against him at the Jalalpur Bhattian police station.')
    print get_translate_zh("Topman Ren Zhengfei wast zijn handen in onschuld. Dan doen we gewoon beter ons best voor de landen die ons wel verwelkomen, zei hij dinsdag. Zijn lidmaatschap van de communistische partij betekent niet dat hij zijn klanten, waar dan ook ter wereld, zou schaden. ‘Het principe van handel is: de klant gaat voor. Mijn politieke overtuiging en zakelijk handelen zijn niet noodzakelijk intiem met elkaar verstrengeld.’Het voor Huawei rampzalige jaar 2018 werd afgerond met de arrestatie van Rens dochter Meng Wanzhou, financieel hoofd van het bedrijf. Ze werd vorige maand in Canada opgepakt op verzoek van de Verenigde Staten, die haar van fraude en het schenden van sancties met Iran beschuldigen. In Vancouver wacht ze onder strenge bewaking af of het daadwerkelijk tot uitlevering komt.Canadese clashDe verhoudingen tussen Canada en China zijn sindsdien ijzig. In China zijn bij wijze van vergeldingsmaatregel enkele Canadezen opgepakt, bijvoorbeeld met vage aantijgingen van spionage. Beijing voerde maandag de druk een tandje op: een Canadese man die betrokken zou zijn bij de smokkel van ruim 200 kilo amfetamine kreeg de doodstraf. Eerder was hij in een proces dat 2,5 jaar duurde tot vijftien jaar veroordeeld, maar in hoger beroep kwam de rechtbank in Dalian binnen enkele uren tot de conclusie dat die straf te licht was. De Canadese regering heeft dinsdag Beijing om genade gevraagd.")
    # print get_translate("你好")

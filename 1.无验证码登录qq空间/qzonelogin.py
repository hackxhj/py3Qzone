from urllib import request
from http import cookiejar
import ssl
import random
import execjs
import os
import time

def login(qqnumber,qqpwd):
    #全局取消https证书校验
    ssl._create_default_https_context = ssl._create_unverified_context


    #获取pt_login_sig 这个参数
    pt_login_sig=''
    initurl="https://xui.ptlogin2.qq.com/cgi-bin/xlogin?proxy_url=https%3A//qzs.qq.com/qzone/v6/portal/proxy.html&daid=5&&hide_title_bar=1&low_login=0&qlogin_auto_login=1&no_verifyimg=1&link_target=blank&appid=549000912&style=22&target=self&s_url=https%3A%2F%2Fqzs.qzone.qq.com%2Fqzone%2Fv5%2Floginsucc.html%3Fpara%3Dizone%26from%3Diqq&pt_qr_app=%E6%89%8B%E6%9C%BAQQ%E7%A9%BA%E9%97%B4&pt_qr_link=http%3A//z.qzone.com/download.html&self_regurl=https%3A//qzs.qq.com/qzone/v6/reg/index.html&pt_qr_help_link=http%3A//z.qzone.com/download.html&pt_no_auth=0"
    (html,cookie)=geturlcookies(initurl)
    for item in cookie:
        if(item.name=='pt_login_sig'):
            pt_login_sig=item.value

    #判断当前登录的qq是否需要验证码 并获取登录需要的参数
    checkcodeurl='https://ssl.ptlogin2.qq.com/check?regmaster=&pt_tea=2&pt_vcode=1&uin={0}&appid=549000912&js_ver=10232&js_type=1&login_sig={1}&u1=https%3A%2F%2Fqzs.qzone.qq.com%2Fqzone%2Fv5%2Floginsucc.html%3Fpara%3Dizone%26from%3Diqq&r={2}&pt_uistyle=40&pt_jstoken=27405839'.format(qqnumber,pt_login_sig,random.random())
    (newhtml,newcookie)=geturlcookies(checkcodeurl)
    ddarrs=newhtml.split(',')
    print(ddarrs)
    if(ddarrs[0]=='ptui_checkVC(\'1\''):
       print("需要验证码,关注博主下一个章节吧  么么哒！")
       return
    backcode=ddarrs[0]
    code=ddarrs[1].replace('\'','')
    pt_verifysession_v1=ddarrs[3].replace('\'','')

    #通过js来计算密码的密文
    curpath=os.path.abspath(os.curdir)
    jspath=curpath+'/enpassjs.js'
    content = open(jspath).read()
    ctx = execjs.compile(content)
    passkey=''
    try:
       passkey = ctx.call('my_getEncPass', qqnumber, qqpwd, code)
    except Exception as e:
       print(e);

    t = time.time()
    timestamp=int(round(t * 1000))# 毫秒级时间戳

    #无验证码登录接口
    loginurl="https://ssl.ptlogin2.qq.com/login?u={0}&verifycode={1}&pt_vcode_v1=0&pt_verifysession_v1={2}&p={3}&pt_randsalt=2&pt_jstoken=27405839&u1=https%3A%2F%2Fqzs.qzone.qq.com%2Fqzone%2Fv5%2Floginsucc.html%3Fpara%3Dizone%26from%3Diqq&ptredirect=0&h=1&t=1&g=1&from_ui=1&ptlang=2052&action=6-27-{5}&js_ver=10232&js_type=1&login_sig={4}&pt_uistyle=40&aid=549000912&daid=5&has_onekey=1&".format(qqnumber,code,pt_verifysession_v1,passkey,pt_login_sig,timestamp)
    (loginhtml,logincookie)=geturlcookies(loginurl)
    loginarrs=loginhtml.split(',')
    logincode=loginarrs[0].replace('\'','')
    print(loginhtml)
    if(loginhtml.find('登录成功')!=-1):
        print("======> 恭喜{0} 你登录成功了！".format(loginarrs[5]))
    else:
        print("登录失败了!")

def geturlcookies(url):
    cookie = cookiejar.CookieJar()
    handler = request.HTTPCookieProcessor(cookie)
    opener = request.build_opener(handler)
    response = opener.open(url)
    html = response.read()
    html = html.decode("utf-8")
    return (html,cookie)

if __name__ == '__main__':
     login('643087041','xxxxxxx')
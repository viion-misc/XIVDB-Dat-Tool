from urllib.request import Request, urlopen, HTTPCookieProcessor, build_opener
from urllib.parse import urlencode
from http.cookiejar import CookieJar
import http.client

http.client.HTTPConnection.debuglevel = 1

request = Request(url='http://patch-bootver.ffxiv.com/http/win32/ffxivneob1_release_boot/2012.01.01.0000.0000',
                  method='GET',
                  headers={
                    'User-Agent': 'FFXIV PATCH CLIENT',
                    'Connection': 'Keep-Alive'
                  })


cj = CookieJar()
opener = build_opener(HTTPCookieProcessor(cj))
opener.addheaders = [
    ('User-Agent', 'SQEXAuthor/2.0.0(Windows XP; ja-jp; 3d21273546)'),
    ('Connection', 'Keep-Alive')
]
r = opener.open('https://secure.square-enix.com/account/app/svc/ffxivlogin?res=pc&cont=ffxiv_top&request=ffxivtop2')

from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):

    def __init__(self, data):
        self.data=data
        return HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == 'input':
            html_name = None
            html_value = None
            for name, value in attrs:
                if name == 'name':
                    html_name = value
                elif name =='value':
                    html_value = value
            self.data[html_name] = html_value

data_dict =dict()
parser = MyHTMLParser(data_dict)
parser.feed(r.read().decode('utf-8'))


opener = build_opener(HTTPCookieProcessor(cj))
opener.addheaders = [
    ('User-Agent', 'SQEXAuthor/2.0.0(Windows XP; ja-jp; 3d21273546)'),
    ('Connection', 'Keep-Alive'),
    ('Cache-Control', 'no-cache'),
    ('Content-Type', 'application/x-www-form-urlencoded')
]
r = opener.open('https://secure.square-enix.com/account/app',
                data=bytes(urlencode([
                    ('_pr_confData_sqexid', ''),
                    ('_pr_confData_passwd', ''),
                    ('_event', 'Submit'),
                    ('_url', data_dict['_url']),
                    ('_seq', data_dict['_seq']),
                    ('_st_addiData', data_dict['_st_addiData']),
                    ('_pr_confData_otppw', '')
                ]), 'ascii'))

bytes_to_find = b'window.external.user("login=auth,ok,sid,'
data = r.read()
print(data)
index = data.find(b'window.external.user("login=auth,ok,sid,') + len(bytes_to_find)

sid = data[index:index + 56].decode('ascii')

with open('output.html', 'wb') as f:
    f.write(data)

cookie_dict = {
    cookie.name: cookie.value for cookie in cj
}

print('sid: ' + str(sid))
print('https://patch-gamever.ffxiv.com/http/win32/ffxivneo_release_game/2012.01.01.0000.0000/%s' % sid)

request = Request(url='https://patch-gamever.ffxiv.com/http/win32/ffxivneob1_release_game/2012.01.01.0000.0000/%s' % sid,
                  method='POST',
                  data=b'ffxivboot.exe/809280/7752f115002cec312c7005b4a1bf717b804c5c67,ffxivlauncher.exe/3765568/c62bca2904c0906d5ff25cb76abb6287fe8a4e54,ffxivsysinfo.exe/252736/c62bca2904c0906d5ff25cb76abb6287fe8a4e54,ffxivupdater.exe/837952/ee4e232180996349873ccabf04af83fa12535c38',
                  headers={
                    'User-Agent': 'FFXIV PATCH CLIENT',
                    'Connection': 'Keep-Alive'
                  })

with urlopen(request) as f:
    print(f.read().decode('utf-8'))


# do_http_request(headers= {
#                    'User-Agent': 'FFXIV PATCH CLIENT',
#                    'Connection': 'Keep-Alive'
#                },
#                host='patch-gamever.ffxiv.com',
#                method='POST',
#                uri='/http/win32/ffxivneob1_release_game/2012.01.01.0000.0000/' + cookie.split('=')[1],
#                data='ffxivboot.exe/791360/0c6e4c8682a457826942c923008a3e9c3220cec9,ffxivlauncher.exe/3680064/1b5b736573f989638596b372cf0aecd770f9689e,ffxivupdater.exe/817472/09e77ca42db0db721d6c36514a6a1481c2800d60',
#                is_https=True)




# conn = httplib.HTTPSConnection('secure.square-enix.com', 443)
# conn.set_debuglevel(1)
# conn.request('GET', '/account/app/svc/ffxivlogin?res=pc&cont=ffxiv_top&request=ffxivtop2', None,
#              {'User-Agent': 'SQEXAuthor/2.0.0(Windows XP; ja-jp; 3d21273546)',
#               'Connection': 'Keep-Alive'
#               })
# response = conn.getresponse()
# data = response.read()
# print data

# cookie = response.getheader('Set-Cookie').split(';')[0]

# # instantiate the parser and fed it some HTML
# data_dict =dict()
# parser = MyHTMLParser(data_dict)
# parser.feed(data)

# conn.request('POST', '/account/app', '_pr_confData_sqexid=Souris&_pr_confData_passwd=Toutoune21121984&_event=Submit'
#                 + '&_url=%s' % data_dict['_url']
#                 + '&_seq=%s' % data_dict['_seq']
#                 + '&_st_addiData=%s' % data_dict['_st_addiData']
#                 + '&_pr_confData_otppw=', {
#                     'User-Agent': 'SQEXAuthor/2.0.0(Windows XP; ja-jp; 3d21273546)',
#                     'Connection': 'Keep-Alive',
#                     'Cookie': cookie,
#                     'Cache-Control': 'no-cache',
#                     'Content-Type': 'application/x-www-form-urlencoded'
#                 })
# response = conn.getresponse()
# data = response.read()

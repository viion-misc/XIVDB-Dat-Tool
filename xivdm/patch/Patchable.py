from urllib.request import Request, urlopen, HTTPCookieProcessor, build_opener
from collections import namedtuple
from os import path, makedirs
from io import StringIO
from html.parser import HTMLParser

def do_http_request(host, method, uri, data=None, headers={}, is_https=False):
    conn = None
    if is_https:
        conn = http.client.HTTPSConnection(host, 443)
    else:
        conn = http.client.HTTPConnection(host, 80)
    conn.request(method,
                 uri,
                 data,
                 headers)
    response = conn.getresponse()
    body = response.read()
    return response, body

class Patchable:
    def __init__(self, game_path, patchable_name):
        self._base_path = path.join(game_path, patchable_name)
        self._name = patchable_name
        self._patch_path = path.join(self._base_path, 'patch')

        vercheck_path = path.join(self._base_path, 'ffxiv%s.ver' % patchable_name)

        if not path.exists(path.dirname(vercheck_path)):
            makedirs(path.dirname(vercheck_path))

        if not path.exists(vercheck_path):
            with open(vercheck_path, 'w') as file_handle:
                file_handle.write('2012.01.01.0000.0000')

        with open(path.join(self._base_path, 'ffxiv%s.ver' % patchable_name), 'r') as file_handle:
            self._version = file_handle.read()

    def get_name(self):
        return self._name

    def get_version(self):
        return self._version

    def check(self):
        pass

    def download(self, file_infos):
        pass

    def apply(self):
        pass

    def update(self):
        check_res = self.check()
        if not check_res == b'':
            string_io = StringIO(check_res.decode('ascii'))

            patches = list()

            line = string_io.readline()
            while line:
                if line == '\r\n':
                    line = string_io.readline()
                    while line:
                        if line.startswith('--'):
                            break
                        patches.append(line[:-2].split('\t'))
                        line = string_io.readline()
                else:
                    line = string_io.readline()

class Boot(Patchable):
    def __init__(self, game_path, patchable_name):
        Patchable.__init__(self, game_path, patchable_name)

    def check(self):
        request = Request(
                    url='http://patch-bootver.ffxiv.com/http/win32/ffxivneob1_release_boot/%s' % self.get_version(),
                    method='GET',
                    headers={
                        'User-Agent': 'FFXIV PATCH CLIENT',
                        'Connection': 'Keep-Alive'
                    })
        
        response = urlopen(request)

        response_value = response.read()
        return response_value

    def download(self, file_infos):
        patch_path = path.join(self._patch_path, 'D%s.patch' % file_infos[4])

        if not path.exists(path.dirname(patch_path)):
            makedirs(path.dirname(patch_path))

        uri_part = file_infos[5].split('/')
        response, body = do_http_request(uri_part[2], 'GET', '/%s' % '/'.join(uri_part[3:]),
                                         headers={
                                            'User-Agent': 'FFXIV PATCH CLIENT',
                                            'Connection': 'Keep-Alive'
                                         })

        with open(patch_path, 'wb') as file_handle:
            file_handle.write(body)

class LoginPageParser(HTMLParser):
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

class Game(Patchable):
    def __init__(self, game_path, patchable_name):
        Patchable.__init__(self, game_path, patchable_name)

    def check(self):
        cookie_jar = CookieJar()
        opener = build_opener(HTTPCookieProcessor(cj))
        opener.addheaders = [
            ('User-Agent', 'SQEXAuthor/2.0.0(Windows XP; ja-jp; 3d21273546)'),
            ('Connection', 'Keep-Alive')
        ]
        response = opener.open('https://secure.square-enix.com/account/app/svc/ffxivlogin?res=pc&cont=ffxiv_top&request=ffxivtop2')

        data_dict =dict()
        parser = LoginPageParser(data_dict)
        parser.feed(response.read().decode('utf-8'))

        opener = build_opener(HTTPCookieProcessor(cj))
        opener.addheaders = [
            ('User-Agent', 'SQEXAuthor/2.0.0(Windows XP; ja-jp; 3d21273546)'),
            ('Connection', 'Keep-Alive'),
            ('Cache-Control', 'no-cache'),
            ('Content-Type', 'application/x-www-form-urlencoded')
        ]
        response = opener.open('https://secure.square-enix.com/account/app',
                        data=bytes(urlencode([
                            ('_pr_confData_sqexid', 'Shouu'),
                            ('_pr_confData_passwd', 'XXX'),
                            ('_event', 'Submit'),
                            ('_url', data_dict['_url']),
                            ('_seq', data_dict['_seq']),
                            ('_st_addiData', data_dict['_st_addiData']),
                            ('_pr_confData_otppw', '')
                        ]), 'ascii'))

        bytes_to_find = b'window.external.user("login=auth,ok,sid,'
        response_value = response.read()
        sid_index = data.find(bytes_to_find) + len(bytes_to_find)
        sid_size = 56
        sid = response_value[index:index + sid_size].decode('ascii')

        request = Request(url='https://patch-gamever.ffxiv.com/http/win32/ffxivneob1_release_game/%s/%s' % (self.get_version(), sid),
                          method='POST',
                          data=b'ffxivboot.exe/791360/0c6e4c8682a457826942c923008a3e9c3220cec9,ffxivlauncher.exe/3680064/1b5b736573f989638596b372cf0aecd770f9689e,ffxivupdater.exe/817472/09e77ca42db0db721d6c36514a6a1481c2800d60',
                          headers={
                            'User-Agent': 'FFXIV PATCH CLIENT',
                            'Connection': 'Keep-Alive'
                          })
        
        response = urlopen(request)

        response_value = response.read()
        return response_value

    def update(self):
        check_res = self.check()
        if not check_res.is_uptodate:
            string_io = StringIO(check_res.response.decode('ascii'))

            patches = list()

            line = string_io.readline()
            while line:
                if line == '\r\n':
                    line = string_io.readline()
                    while line:
                        if line.startswith('--'):
                            break
                        patches.append(line[:-2].split('\t'))
                        line = string_io.readline()
                else:
                    line = string_io.readline()

            for patch in patches:
                self.download(patch)

    def download(self, file_infos):
        patch_path = path.join(self._patch_path, 'D%s.patch' % file_infos[4])

        if not path.exists(path.dirname(patch_path)):
            makedirs(path.dirname(patch_path))

        uri_part = file_infos[5].split('/')
        response, body = do_http_request(uri_part[2], 'GET', '/%s' % '/'.join(uri_part[3:]),
                                         headers={
                                            'User-Agent': 'FFXIV PATCH CLIENT',
                                            'Connection': 'Keep-Alive'
                                         })

        with open(patch_path, 'wb') as file_handle:
            file_handle.write(body)



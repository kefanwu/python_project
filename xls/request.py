# coding=utf-8
import requests
import xlrd


def load():
    book = xlrd.open_workbook('api.xls')

    start_s = False
    start_x = False
    start_y = False

    for s in book.sheets():
        for y in range(s.nrows):
            r = s.row(y)
            for x in range(len(r)):
                if s.cell_value(y, x) == "api":
                    start_s = s
                    start_x = x
                    start_y = y
                    break

    start(start_s, start_x, start_y)


def start(s, x, y):
    if s or x or y:
        dic = {}
        r = s.row_values(y)
        for i in range(x, len(r)):
            dic[r[i]] = i
        for y in range(y + 1, s.nrows):
            api = s.row_values(y)
            send(dic, api)


def send(dic, api):
    method = dic.get("method", False)
    url = dic.get("url", False)
    headers = dic.get("headers", False)
    params = dic.get("params", False)
    data = dic.get("data", False)
    path = dic.get("path", False)

    if not url:
        return
    url = api[url]
    if not url:
        return

    if method:
        method = api[method]
    if headers:
        headers = parse(api[headers])
    if params:
        params = parse(api[params])
    if data:
        data = parse(api[data])
    if path:
        path = api[path]
        url = parse_path(url, path)

    print url
    result = requests.request(method, url, params=params, data=data, headers=headers)
    print result.url, result.status_code


def parse_path(url, path):
    # noinspection PyBroadException
    try:
        path = eval(path)
        for key in path:
            url = url.replace('{%s}' % key, path[key])
    except Exception:
        try:
            path = path.replace(',', "','")
            paths = eval("('%s')" % path)
            url = url % paths
        except Exception:
            raise Exception("Path format error", url)
    return url


def parse(string):
    if not string:
        return string
    # noinspection PyBroadException
    try:
        param = eval(string)
    except Exception:
        try:
            entries = string.split(',')
            param = {}
            for entry in entries:
                v = entry.split('=')
                param[v[0]] = v[1]
        except Exception:
            print "参数格式错误：", string
            raise Exception("Parameter format error", string)
    return param


load()

# -*- coding: utf-8 -*-
import json

import requests

from util import QY_URL


class WeChatQy:
    __access_token__ = None

    def __init__(self, corpid, corpsecret):
        super(WeChatQy).__init__()
        self.__corpid__ = corpid
        self.__corpsecret__ = corpsecret

        self.get_access_token()

    def get_access_token(self):
        corpid = self.__corpid__
        corpsecret = self.__corpsecret__

        page = requests.get(QY_URL + 'gettoken', params={'corpid': corpid, 'corpsecret': corpsecret})

        if page.status_code == 200:
            access_token = json.loads(page.text).get('access_token', None)
            if not access_token:
                raise ValueError
            else:
                self.__access_token__ = access_token
                return access_token
        return

    def get_api_data(self, api_name, params=None, methods='GET', times=0):
        if not params:
            params = dict()
        access_token = self.__access_token__
        if methods == 'GET':
            params['access_token'] = access_token
            page = requests.get(QY_URL + api_name, params=params)
        elif methods == 'POST':
            page = requests.post(QY_URL + api_name + '?access_token={0}'.format(access_token), data=json.dumps(params))
        else:
            return None
        data = json.loads(page.text, encoding='utf-8')
        if data.get('errcode') == 40014 or data.get('errcode') == 42001 and times < 3:
            access_token = self.get_access_token()
            params['access_token'] = access_token
            times += 1
            data = self.get_api_data(api_name, params, methods, times)
        else:
            raise TypeError
        return data

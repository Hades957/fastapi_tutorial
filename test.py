import datetime

import requests
from pydantic import BaseModel


# class A(BaseModel):
#     prop1: str
#     prop2: str
#
#
# class B(BaseModel):
#     a: A
#
#
# data = {
#     'prop1': 'some value',
#     'prop2': 'some other value'
# }
#
# b = B(a=A(**data))
#
# print(b)

if __name__ == '__main__':
    url = "http://support.bz.cn/pushWeChat/pushMsg"

    datas = {

        'content': 'fastapi_tutorial部署完成!\n' + str(datetime.datetime.now())[0: 19],

        'uid': 'UID_9F1qnBI9X6Bc3sp1JdCLqaHvSQEg'
    }

    requests.post(url, json=datas)

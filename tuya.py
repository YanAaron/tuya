import time, hashlib, hmac, requests, json

class tuya:

    def __init__(self, client_id, secret):

        self.client_id = client_id
        self.secret = secret

    def get_sign(self, sign_string):
        secret = self.secret.encode('utf-8')
        message = sign_string.encode('utf-8')
        sign = hmac.new(secret, message, hashlib.sha256).hexdigest().upper()
        return sign

    def get_access_token(self,token_sign,t):

        url = 'https://openapi.tuyaus.com/v1.0/token?grant_type=1'
        headers = {
                    'sign':token_sign,
                    't':t,
                   'sign_method': 'HMAC-SHA256',
                   'client_id': self.client_id,
                   }

        request = requests.get(url, headers=headers)
        a = json.loads(request.content)
        access_token = a['result']['access_token']
        refresh_token = a['result']['refresh_token']
        return access_token,refresh_token

    def get_device_info(self,normal_sign,t,access_token,device_id):

        url = 'https://openapi.tuyaus.com/v1.0/devices/{device_id}'.format(device_id=device_id)
        headers = {
                    'sign':normal_sign,
                    't': t,
                   'sign_method': 'HMAC-SHA256',
                   'client_id': self.client_id,
                    'access_token': access_token,
                   }
        request = requests.get(url, headers=headers)
        a = json.loads(request.content)
        print(a)



if __name__ == '__main__':

    client_id = 'fyekxcdka95atveo85xl'
    secret = 'f81bcd20b481499b82a48353d45811d3'
    tuya_instance = tuya(client_id, secret)
    t = str((time.time())*1000)[:13]

    # 获取token的sign
    sign_string = client_id + t
    token_sign = tuya_instance.get_sign(sign_string)

    # 获取token
    access_token,refresh_token = tuya_instance.get_access_token(token_sign,t)

    #获取token以外的sign
    sign_string2 = client_id + access_token + t
    normal_sign = tuya_instance.get_sign(sign_string2)

    # 获取设备信息
    tuya_instance.get_device_info(normal_sign,t,access_token,device_id='4834120498f4abfcc35a')



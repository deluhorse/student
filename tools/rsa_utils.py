# -*- coding:utf-8 -*-

"""
@author: delu
@file: rsa_utils.py
@time: 17/6/1 14:48
"""
from Crypto.Hash import SHA
from Crypto.Hash import SHA256
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
import base64


class RsaUtils(object):
    @staticmethod
    def sign(content, private_key):
        """
        生成签名
        :param content: 
        :param private_key: 
        :return: 
        """
        if isinstance(content, str):
            content = content.encode('utf-8')
        private_key_list = ['-----BEGIN RSA PRIVATE KEY-----']
        while True:
            private_key_list.append(private_key[0:64])
            private_key = private_key.replace(private_key[0:64], '')
            if len(private_key) <= 0:
                break
        private_key_list.append('-----END RSA PRIVATE KEY-----')
        private_key = '\n'.join(private_key_list)
        rsakey = RSA.importKey(private_key)
        signer = Signature_pkcs1_v1_5.new(rsakey)
        digest = SHA.new()
        digest.update(content)
        sign = signer.sign(digest)
        return base64.b64encode(sign).decode()

    @staticmethod
    def sign_rsa2(content, private_key):
        """
        生成签名
        :param content:
        :param private_key:
        :return:
        """
        if isinstance(content, str):
            content = content.encode('utf-8')
        private_key_list = ['-----BEGIN RSA PRIVATE KEY-----']
        while True:
            private_key_list.append(private_key[0:64])
            private_key = private_key.replace(private_key[0:64], '')
            if len(private_key) <= 0:
                break
        private_key_list.append('-----END RSA PRIVATE KEY-----')
        private_key = '\n'.join(private_key_list)
        rsakey = RSA.importKey(private_key)
        signer = Signature_pkcs1_v1_5.new(rsakey)
        digest = SHA256.new()
        digest.update(content)
        sign = signer.sign(digest)
        return base64.b64encode(sign).decode()

    @staticmethod
    def verify(signature, content, public_key):
        """
        验签
        :param signature: 
        :param content: 
        :param public_key: 
        :return: 
        """
        public_key_list = ['-----BEGIN PUBLIC KEY-----']
        while True:
            public_key_list.append(public_key[0:64])
            public_key = public_key.replace(public_key[0:64], '')
            if len(public_key) <= 0:
                break
        public_key_list.append('-----END PUBLIC KEY-----')
        public_key = '\n'.join(public_key_list)
        rsakey = RSA.importKey(public_key)
        verifier = Signature_pkcs1_v1_5.new(rsakey)
        digest = SHA.new()
        digest.update(content.encode('utf-8'))
        is_verify = verifier.verify(digest, base64.b64decode(signature))
        return is_verify

    @staticmethod
    def verify_rsa2(signature, content, public_key):
        """
        验签
        :param signature:
        :param content:
        :param public_key:
        :return:
        """
        public_key_list = ['-----BEGIN PUBLIC KEY-----']
        while True:
            public_key_list.append(public_key[0:64])
            public_key = public_key.replace(public_key[0:64], '')
            if len(public_key) <= 0:
                break
        public_key_list.append('-----END PUBLIC KEY-----')
        public_key = '\n'.join(public_key_list)
        rsakey = RSA.importKey(public_key)
        verifier = Signature_pkcs1_v1_5.new(rsakey)
        digest = SHA256.new()
        digest.update(content.encode('utf-8'))
        is_verify = verifier.verify(digest, base64.b64decode(signature))
        return is_verify


if __name__ == '__main__':
    #  签名
    # content = '{"a":"123"}'
    # private_key = 'MIIEpAIBAAKCAQEA4awQlaLGKp64NSp64fqDpeYsojBJZ0UXIqMrDPWTd9Z8wRjFSvuE278yHAwtyCFhyvDJ87Vdr8dqNL76D8tWo24exU9XFe1COoWtgHnGbvMRTcPXujar2nrxaVrqpybdeo62qfSzh9onrlB55GR8u7A8DUQmu8994BlJzc/7pbk2KQ/2ObY7QsC0zdMZkyENtDZmViaFEjiczQp1o0xQiezK4TWNu5+Pw4sKPB8aulzRT5R7hyKfARjF64OIJcgltN7bNxVGkYj6Icgf8dPJ7dD7l1FxbchsbYPg7BUcGVLOSw8YfSntOWB91BDThYiiJsjF3dLkHo23o52fDWlOIwIDAQABAoIBAQC/3/Zx4+Yt0qm4upekj8VjRuNoOzoODhZvouA1so9h8wI7g/4rlNMPq+7FHi3G3Wsyi6yKBAjWLe1FT6N5zl+psTWEecMHp6UJ8SLl+6QWLaDmx78iWt2fc6zS8TRWTps9Wx5APwhuV7QpZ89bu3y6cEt+1BVC1lamNZok3dOOwOQZiX0cMfOkUrnMjpwUZ1pXPWAsdYZAUygW5xUWvlZsGNj4M7f2dRUihAP5B7fJGMbsS8wnFOwud5RyapmQs7E2t1/6UiBsHNDhkk58VwFYqBJnSlf0sWM2K2iL84+dTeLDxyRLXSlMpbcYRAkT7MtF6iwK5cenJTq+UniYM2KhAoGBAPoLKkwYcfKm+t/96bwybkUMyicg13KJXUUMZ7EOEVRuoh5KhcUsI/N6NSIrNhWI8bZJVqlCLq3GGO796r/SZsuY4ldWx5MujXdoXWEkeu8UMhexpuNE0QaZRkNTmrUveJCg2QnxdsGxLyMxIXRfYsnmzCNxzbSHQ2ZOfjacNFYrAoGBAOcMRokgXIOuDl+r79ScoytO0di2K1zcX6CW11zdQJWbclhYCVe8A7r6UZE67jebP6Tdae7jLGZQEdOOU2/tN5KIqjhSHuHOQujhQw0FR5dYDCnxm5mV8dbUtzQPTY4ZLOjD1Dxr4fkbRvUTjY3huybhsoLh2EeBGvOfEOB1fSPpAoGAZrBdL6E+ctw23fTmoD7J4JvPDeDD+qsFXg0pLKLNZTKGbBBI/eAR57WBysWaUZ/LPQTDjYG7r+xSYxxu41ailuzzz9C45+5PdQGsj++ueS9/HxH7qwyhF6etHotgVxbm2eblG9tJ3WRKKpbL2YIvDSI3Jjtfsst2V7bWyNDAAb8CgYBjG5DmIUuN8IuZ3lbyDH6xhQ3et8XB/4XFjO60lvOtORDDdIANckjnW5jBg1XL5HxYa+GU5z2UZaQ/6z0/NbIw2Q6rOg6lLaTl4DqyyyD6eno9Q7ZLG1axoG01l5rc6U+qSNYxVNWJ1XmKhuihg8KT2xyHp/juMyMsfX7vyXX0gQKBgQDhi2Lp1d4QY2EV7O43SvmbQlBt+PdOVlIXCmAP8vIsE04M9tVPdQEVJ4WKGlKUbEYg4r04cIT2rzro92a7ErYroPRQxqxqHl4Yw6zkzxink1cLtWTHvsl9vyQlCxOH3lMuniUM/bsILk8VWMrP0ZEqgwV3CM/Nw6Aq/xtJC5HoCw=='
    # sign = RsaUtils.sign_rsa2(content, private_key)
    # print(sign)
    #
    # public_key = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4awQlaLGKp64NSp64fqDpeYsojBJZ0UXIqMrDPWTd9Z8wRjFSvuE278yHAwtyCFhyvDJ87Vdr8dqNL76D8tWo24exU9XFe1COoWtgHnGbvMRTcPXujar2nrxaVrqpybdeo62qfSzh9onrlB55GR8u7A8DUQmu8994BlJzc/7pbk2KQ/2ObY7QsC0zdMZkyENtDZmViaFEjiczQp1o0xQiezK4TWNu5+Pw4sKPB8aulzRT5R7hyKfARjF64OIJcgltN7bNxVGkYj6Icgf8dPJ7dD7l1FxbchsbYPg7BUcGVLOSw8YfSntOWB91BDThYiiJsjF3dLkHo23o52fDWlOIwIDAQAB'
    # print(RsaUtils.verify_rsa2(sign, content, public_key))
    content = '12313'
    private_key = 'MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAOzNk/qyDyj/e3M/Dc/q7TXGYmBI989aeKf0FSqxW4k0OiWS7Vew2Z8045iqz0pYcPVwupMnpbXYzSpTvD5TC4QGnboASvR8I3rUZ22Niz6TfqXd/u7M+MsAGe70HauLp6M7W4dtv4WsKUvvEuYKKlZ1XLcUX+RW7JJIBipHKEjRAgMBAAECgYBR8RlhyLfCQhXf3VPUPMD0uL9V/inyUKYryCSC73hzU+VDF0KV85Z6pvyS2Zh9a3k7FVUakr+e23SzTuJ21pnG3XRtawFHA4TXCd1Nr3PjSvpB/BXPPHRHof6EE3MxZGD4hY2CKrFG6CkvsmkW3Ux1N6aQkx0TO3Fp/KODZmfsAQJBAPdrDnjeMEGr7oC8J5DCqJjM1YoCK0Gnmcd7lCpc2fpHFwre6Yz+VMOay8vJUu3iWQjoxzDEgKBbsRkEP+4UXvECQQD1BEO6Aw+gW7/oPnrr/bk8FR5wwLG6X3uE0GgtNoCzvDMpn4BSjHp4cD/AwLLk+a/wNuLu/V6a21J/KUoHrEfhAkBSWmoIxTwev9G1O+uXfZOMuLFjLHGletnu0i1xJFLRwZPj5GqsqYMhUIcBH9PgpnSoSIL0spN1zM9X2lhFMLahAkA9/0k/3RxsICssEfs6kaX4XQOp1ihil1yC29Uwc5UXZaywgIqQ2Lj4lrabCGd75u4s40aC4Ju6pXp3cLQpwt8hAkEAzCVGTQ12RkYu1oONqwjJ5wgrY0Zc+Q9BYamueLk4KdpmAGz9AXml+uhjzdsYG8ITXByLJBAyzONiGEKw1KnfaQ=='
    sign = RsaUtils.sign(content, private_key)

    public_key = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCnxj/9qwVfgoUh/y2W89L6BkRAFljhNhgPdyPuBV64bfQNN1PjbCzkIM6qRdKBoLPXmKKMiFYnkd6rAoprih3/PrQEB/VsW8OoM8fxn67UDYuyBTqA23MML9q1+ilIZwBC2AQ2UBVOrFXfFl75p6/B5KsiNG9zpgmLCUYuLkxpLQIDAQAB'
    print(RsaUtils.verify(sign, content, public_key))

import requests
from urlparse import urlparse
import datetime
import hashlib
import hmac
import re

def trimall(s):
    return re.sub(" +", " ", s).strip(" ")

def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

class AWS4Signer:
    def __init__(self, access_key, secret_key, region_name="us-west-2", algorithm='AWS4-HMAC-SHA256', service='ec2'):
        self.access_key = access_key
        self.secret_key = secret_key
        self.region_name = region_name
        self.algorithm = algorithm
        self.service = service

    def signed_headers(self):
        if self.request is None:
            return ""

        header_keys = sorted(self.request.headers.keys(), key=str.lower)
        return ';'.join([x.lower() for x in header_keys])

    def canonical_request(self):
        if self.request is None:
            return ""

        P = urlparse(self.request.url)

        # Create canonical headers
        header_keys = sorted(self.request.headers.keys(), key=str.lower)
        canonical_headers = '\n'.join(x.lower()+':'+trimall(self.request.headers[x]) for x in header_keys) + '\n'

        # Create payload hash
        data = self.request.body
        if isinstance(data, str):
            data = data.encode('utf-8')
        elif data is None:
            data = ''.encode('utf-8')
        pl_hash = hashlib.sha256(data).hexdigest()

        return '\n'.join([
            self.request.method,
            P.path,
            P.query,
            canonical_headers,
            self.signed_headers(),
            pl_hash
        ])

    def credential_scope(self):
        if self.request is None:
            return ""

        return "/".join([
            self.datestamp,
            self.region_name,
            self.service,
            'aws4_request'
        ])

    def signing_key(self):
        if self.request is None:
            return ""

        date_key = sign(('AWS4' + self.secret_key).encode('utf-8'), self.datestamp)
        region_key = sign(date_key, self.region_name)
        service_key = sign(region_key, self.service)
        return sign(service_key, 'aws4_request')

    def signature(self):
        to_sign = '\n'.join([
            self.algorithm,
            self.amzdate,
            self.credential_scope(),
            hashlib.sha256(self.canonical_request().encode('utf-8')).hexdigest()
        ])

        return hmac.new(self.signing_key(), (to_sign).encode('utf-8'), hashlib.sha256).hexdigest()

    def __call__(self, req):
        self.request = req

        P = urlparse(self.request.url)

        # Create timestamps and add required headers
        t = datetime.datetime.utcnow()
        self.amzdate = t.strftime('%Y%m%dT%H%M%SZ')
        self.datestamp = t.strftime('%Y%m%d')
        self.request.headers['x-amz-date'] = self.amzdate
        self.request.headers['host'] = P.netloc

        auth = self.algorithm + ' '
        auth += 'Credential=' + self.access_key + '/' + self.credential_scope() + ', '
        auth += 'SignedHeaders=' + self.signed_headers() + ', '
        auth += 'Signature=' + self.signature()
        req.headers["Authorization"] =  auth

        self.request = None
        return req

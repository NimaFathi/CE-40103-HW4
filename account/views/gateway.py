import time

import requests
from django.utils import timezone
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from account.models import AccessToken


class GatewayAPI(viewsets.ViewSet):
    """
    Sample input:
    type: client-register
    username: nima
    email: nima0fathi@gmail.com
    password: Mypassword123
    """

    def list(self, request):
        request_type = request.data["type"]

        if request_type == 'client-register':
            return self.client_register(request.data)
        if request_type == 'login':
            return self.login(request.data)
        if request_type == 'client-profile-view':
            if not self.validate_token(request.data.get('token', None), request.data.get('username', None)):
                return Response(data='token invalid or expired', status=status.HTTP_403_FORBIDDEN)
            return self.client_profile_view(request.data)
        if request_type == 'client-profile-update':
            if not self.validate_token(request.data.get('token', None), request.data.get('username', None)):
                return Response(data='token invalid or expired', status=status.HTTP_403_FORBIDDEN)
            return self.client_profile_update(request.data)
        if request_type == 'admin-profile-view':
            if not self.validate_token(request.data.get('token', None), request.data.get('username', None)):
                return Response(data='token invalid or expired', status=status.HTTP_403_FORBIDDEN)
            return self.admin_profile_view(request.data)
        if request_type == 'admin-profile-update':
            if not self.validate_token(request.data.get('token', None), request.data.get('username', None)):
                return Response(data='token invalid or expired', status=status.HTTP_403_FORBIDDEN)
            return self.admin_profile_update(request.data)
        return Response("")

    def validate_token(self, token, username):
        now = timezone.now()
        print(now)
        print('oh my god')
        print(AccessToken.objects.get(token=token, username=username).__dict__)
        if AccessToken.objects.filter(token=token, username=username, token_expiration__gt=now):
            return True
        return False

    def request_handler(self, url, data, request_type):
        request_success = False
        retry_count = 0
        while not request_success:
            try:
                resp = getattr(requests, request_type)(url=url, data=data, timeout=0.5)
                request_success = True
            except requests.Timeout:
                request_success = False
                retry_count += 1
            if resp.status_code >= 500:
                retry_count += 1
                request_success = False
            if retry_count >= 3:
                retry_count %= 3
                time.sleep(10)
        return resp.json(), resp.status_code

    def client_register(self, data):
        resp_data, status_code = self.request_handler(url='http://127.0.0.1:8000/api/client-register', data=data,
                                                      request_type='post')
        return Response(data=resp_data, status=status_code)

    def login(self, data):
        resp_data, status_code = self.request_handler(url='http://127.0.0.1:8000/api/login', data=data,
                                                      request_type='post')
        return Response(data=resp_data, status=status_code)

    def client_profile_view(self, data):
        resp_data, status_code = self.request_handler(url='http://127.0.0.1:8000/api/client-profile-view', data=data,
                                                      request_type='get')
        return Response(data=resp_data, status=status_code)

    def client_profile_update(self, data):
        resp_data, status_code = self.request_handler(url='http://127.0.0.1:8000/api/client-profile-update', data=data,
                                                      request_type='put')
        return Response(data=resp_data, status=status_code)

    def admin_register(self, data):
        resp_data, status_code = self.request_handler(url='http://127.0.0.1:8000/api/admin-register', data=data,
                                                      request_type='post')
        return Response(data=resp_data, status=status_code)

    def admin_profile_view(self, data):
        resp_data, status_code = self.request_handler(url='http://127.0.0.1:8000/api/admin-profile-view', data=data,
                                                      request_type='get')
        return Response(data=resp_data, status=status_code)

    def admin_profile_update(self, data):
        resp_data, status_code = self.request_handler(url='http://127.0.0.1:8000/api/admin-profile-update', data=data,
                                                      request_type='put')
        return Response(data=resp_data, status=status_code)

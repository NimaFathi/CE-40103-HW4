import random
import string
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from account.models import Account, AccessToken


@api_view(['POST', ])
def login_account(request):
    request_data = request.data
    try:
        account = Account.objects.get(username=request_data['username'])
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':

        data = {'username': account.username, 'account_type': account.account_type}
        if not account.check_password(request_data['password']):
            return Response(data='username or password incorrect', status=status.HTTP_403_FORBIDDEN)
        random_token_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(128))
        token = update_token(account.username, random_token_key, account.account_type)
        data['token'] = token.token

        return Response(data=data, status=status.HTTP_200_OK)
    return Response(data='invalid request', status=status.HTTP_400_BAD_REQUEST)


def update_token(username, gen_token, account_type):
    try:
        AccessToken.objects.get(username=username).delete()
        token = AccessToken.objects.create(account_type=account_type, token=gen_token, username=username)
    except AccessToken.DoesNotExist:
        token = AccessToken.objects.create(account_type=account_type, token=gen_token, username=username)
    return token

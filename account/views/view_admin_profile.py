from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from account.models import Account


@api_view(['GET', ])
def get_admin_profile(request):
    request_data = request.data
    try:
        account = Account.objects.get(username=request_data['username'], account_type='admin')
    except Account.DoesNotExist:
        return Response(data='account not found', status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        data = {'username': account.username,
                'email': account.email,
                'phone_number': account.phone_number,
                'account_type': account.account_type,
                'is_admin': True,
                'is_superuser': True
                }

        return Response(data=data, status=status.HTTP_200_OK)
    return Response(data='invalid request', status=status.HTTP_400_BAD_REQUEST)

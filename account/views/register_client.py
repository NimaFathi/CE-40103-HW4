from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from account.models import Account


def validate_email(email):
    try:
        account = Account.objects.get(email=email)
    except Account.DoesNotExist:
        return None
    if account != None:
        return email


def validate_username(username):
    try:
        account = Account.objects.get(username=username)
    except Account.DoesNotExist:
        return None
    if account != None:
        return username


def validate_password(passwd):
    SpecialSym = ['$', '@', '#', '%']
    val = {0: "not None", 1: "not any error"}

    if len(passwd) < 6:
        val[0] = None
        val[1] = 'password is too short!'
        return val
    if len(passwd) > 40:
        val[0] = None
        val[1] = 'Password is too long!!'
        return val
    if not any(char.isdigit() for char in passwd):
        val[0] = None
        val[1] = 'your password must contain at least one digit.'
        return val
    if not any(char.isupper() for char in passwd):
        val[0] = None
        val[1] = 'your password must contain at least one uppercase alphabet.'
        return val
    if not any(char.islower() for char in passwd):
        val[0] = None
        val[1] = 'your password must contain at least one lowercase alphabet.'
        return val

    if any(char in SpecialSym for char in passwd):
        val[0] = None
        val[1] = 'your passwrod shouldn\'t contain any of {@,#,%,$ } set'
        return val
    return val


@api_view(['POST', ])
def create_client(request):
    print(request.headers)
    data = {}
    email = request.data.get('email', '0').lower()

    if validate_email(email) is not None:
        data['error_message'] = 'That email is already in use.'
        data['response'] = 'Error'
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

    username = request.data.get('username', '0')
    if validate_username(username) is not None:
        data['error_message'] = 'That username is already in use.'
        data['response'] = 'Error'
        return Response(data=data, status=status.HTTP_403_FORBIDDEN)

    password = request.data.get('password', '0')
    val = validate_password(password)
    if val[0] is None:
        data['error_message'] = val[1]
        data['response'] = 'Error'
        return Response(data, status=status.HTTP_403_FORBIDDEN)
    data = {
        'password': password,
        'email': email,
        'phone_number': request.data.get('phone_number', '0'),
        'username': username
    }
    try:
        account = Account()
        account.username = data['username']
        account.password = data['password']
        account.email = data['email']
        account.account_type = 'client'
        account.phone_number = data['phone_number']
        account.save()
    except Exception as e:
        return Response(data='error in creating account', status=status.HTTP_400_BAD_REQUEST)
    return Response(data='account created successfully', status=status.HTTP_200_OK)

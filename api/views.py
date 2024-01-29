# helps manage the view with respect to url methods
from rest_framework.decorators import api_view, authentication_classes, permission_classes
# helps carry out http response with respect to the request
from rest_framework.response import Response
# this would allow us to write json objects into database
from .serializers import UserSerializer
# add status code for api calls
from rest_framework import status
# help create token for various users
from rest_framework.authtoken.models import Token
# make the user model assessable for use . 
from django.contrib.auth.models import User
# make 
from django.shortcuts import get_object_or_404
# manage authentication checks
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
# check if the user making a request is authenticated
from rest_framework.permissions import IsAuthenticated




@api_view(['POST'])
def login(request):
    """
    Handle The login route/url
    """
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({
            "token": token.key,
            "user": serializer.data
        })


@api_view(['POST'])
def signup(request):
    """
    Handle the signup route/url
    """
    # fetching and storing request data from the user
    serializer = UserSerializer(data=request.data)
    # check if the form data is valid, if true save the data
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        # hash the user password
        user.set_password(request.data['password'])
        # save the updated hashed password
        user.save()
        token = Token.objects.create(user=user)
        return Response({
            "token": token.key,
            "user": serializer.data
            })

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    """
    Handle the test_token route/url
    """
    return Response({
        "passed for {}".format(request.user.email)
    })
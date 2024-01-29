# helps manage the view with respect to url methods
from rest_framework.decorators import api_view
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

@api_view(['POST'])
def login(request):
    """
    Handle The login route/url
    """

    return Response({})


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
def test_token(request):
    """
    Handle the test_token route/url
    """
    return Response({})
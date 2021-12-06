import json
from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.views import APIView, exception_handler
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password,check_password
from . import userinfo,models,serializers,storeFetcher
# Create your views here
class Authentication(APIView):   
    def post(self,request):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user is None:
            return JsonResponse({
                'status':'failed',
                'error':'Wrong username or password.'
            })
        if user is not None:
            token = Token.objects.get(user=user)
            return JsonResponse({
                'status':'success',
                'error':0,
                'token':token.key
            })
    
    def put(self,request):
        try:
            user = User.objects.create_user(username=request.data['username'], password=request.data['password'])
            user.save()
            Token.objects.create(user=user)
            return JsonResponse({
                "status":"success",
                "error":0
            })
        except Exception as e:
            print(e)
            return JsonResponse({
                "status":"failed",
                "error":"User already exists."
            })

class Accounts(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self,request):
        userFromToken = Token.objects.get(key = request.auth).user
        tokens = userinfo.main(request.data['username'],request.data['password'])
        if tokens == "0":
            return JsonResponse(
                {
                    "status":"failed",
                    "error":"Wrong account details."
                }
            )
        try:
            account = models.Accounts.objects.create(
                user=userFromToken,
                email=request.data['username'],
                userName = tokens['userName'],
                hashedPass = make_password(request.data['password']),
            )
            account.save()
            return JsonResponse({"status":"successful","error":"0"})
        except Exception as e:
            print(e)
            return JsonResponse({"status":"failed","error":"Account already exists."})
    def get(self,request):
        accountsList= []
        userFromToken = Token.objects.get(key = request.auth).user
        accounts = models.Accounts.objects.filter(user=userFromToken)
        if accounts.exists():
            for account in accounts:
                toappend = {
                    'userName':account.userName,
                }
                accountsList.append(toappend)
            return JsonResponse({
                "status":"success",
                "Accounts":accountsList,
                
                })
        else:
            return JsonResponse({
                "status":"failed",
                "error":"No accounts."
                })
    def post(self,request):
        userFromToken = Token.objects.get(key = request.auth).user
        account = models.Accounts.objects.filter(userName=request.data['username'],user=userFromToken)
        if not account.exists():
            return JsonResponse(
                {
                    "status":"failed",
                    "error":"No accounts exist."
                }
            )
        if not check_password(request.data['password'],account[0].hashedPass):
            print(check_password(request.data['password'],account[0].hashedPass))
            return JsonResponse(
                {
                    "status":"failed",
                    "error":"Wrong riot password."
                }
            )
        tokens = userinfo.main(account[0].email,request.data["password"])
        skinsDict = storeFetcher.main(tokens['riotAuth'],tokens['entToken'],tokens['uid'])
        return JsonResponse(
            {
                "status":"successful",
                "error":"0",
                "skinsDict": skinsDict
            }
        )
class store(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        userFromToken = Token.objects.get(key = request.auth).user
        tokens = models.Accounts.objects.filter(user=userFromToken,userName=request.data['accountname'])
        if tokens.exists():
            skins = storeFetcher.main(tokens[0].riotAuth,tokens[0].entToken,tokens[0].unique)
            print(skins)
        else:
            return JsonResponse({
                "status":"failed",
                "error":"Account doesn't exist"
            })

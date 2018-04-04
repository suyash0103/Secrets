from django.shortcuts import render
from PIL import Image, ImageDraw
from django.http import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.

class Check(APIView):

    def post(self, request):
        return
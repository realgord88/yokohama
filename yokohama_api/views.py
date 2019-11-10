# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import models
import socket

class Connect(APIView):
    def post(self, request):
        ip=str(request.query_params['ip'])
        port=int(request.query_params['port'])
        global sock
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))
            return Response({'status': 'connected'})
        except:
            return Response({'status': 'error'})

class Disconnect(APIView):
    def get(self, request):
        sock.close()
        return Response({'status': 'disconnected'})

class GetInfo(APIView):
    def get(self, request):
        sock.sendall(":SYSTem:COMMunicate:REMote ON; *cls; *idn?\n")
        response_server=sock.recv(1024)
        return Response({'data': str(response_server)})

class GetMetrics(APIView):
    def get(self, request):
        sock.sendall(":READ3:POW?\n")
        response_server=sock.recv(1024)
        return Response({'data': str(response_server)})
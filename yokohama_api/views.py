# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import models
from .models import Metrics
from .serializers import MetricsSerializer
import socket
import string
import sys

reload(sys)
sys.setdefaultencoding('utf8')

class Connect(APIView):
    def post(self, request):
        ip=str(request.data['ip'])
        port=int(request.data['port'])
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
        response_server=sock.recv(1024)[:-2]
        print response_server
        return Response({'data': str(response_server)})

class GetMetrics(APIView):
    def get(self, request):
        sock.sendall(":READ3:POW?\n")
        origin=str(sock.recv(1024))
        sign=origin[0]
        degree_row = origin[-1:]
        if sign == '-':
            degree_row = sign + degree_row
        main_value = float(origin[1:string.find(origin, 'E')])

        dbm = str(main_value * (10 ** int(degree_row)))
        dbm = dbm[:string.find(dbm, '.') + 3]
        print dbm
        return Response({'data': str(dbm)})

class SetLenght(APIView):
    def post(self, request):
        lenght=str(request.data['lenght'])
        request_lenght=":SENS3:POW:WAV " + lenght + "NM\n"
        print request_lenght
        sock.sendall(request_lenght)
        sock.sendall(":SENS3:POW:WAV?\n")
        response_server=sock.recv(1024)[:-2]
        return Response({'data': str(response_server)})

class SetAveraging(APIView):
    def post(self, request):
        average=str(request.data['average'])
        request_average=":SENS3:POW:ATIM " + average + "MS\n"
        sock.sendall(request_average)
        sock.sendall(":SENS3:POW:ATIM?\n")
        response_server=sock.recv(1024)[:-2]
        return Response({'data': str(response_server)})

class InfoSlots(APIView):
    def get(self, request):
        response_server = []
        for slot_number in range(1,4):
            command=":SLOT" + str(slot_number) + ":IDN?\n"
            sock.sendall(command)
            response_server.append(sock.recv(1024)[:-2])
        return Response({'data': response_server})

class SetDate(APIView):
    def post(self, request):
        date=str(request.data['date']).replace('.',',')
        request_date=":SYStem:DATE " + date + "\n"
        sock.sendall(request_date)
        sock.sendall(":SYStem:DATE?\n")
        response_server=sock.recv(1024)[:-2]
        return Response({'data': str(response_server)})

class SetTime(APIView):
    def post(self, request):
        request_time=str(request.data['time']).replace(':',',')
        request_time=":SYStem:TIME " + request_time + "\n"
        sock.sendall(request_time)
        sock.sendall(":SYStem:Time?\n")
        response_server=sock.recv(1024)[:-2]
        return Response({'data': str(response_server)})


class CheckErrors(APIView):
    def get(self, request):
        sock.sendall(":SYSTem:ERRor?\n")
        response_server=sock.recv(1024)[:-2]
        return Response({'data': str(response_server)})

class SetOffset(APIView):
    def post(self, request):
        offset=str(request.data['db'])
        request_offset=":SENS3:CORR " + offset + "DB\n"
        sock.sendall(request_offset)
        sock.sendall(":SENS3:CORR?\n")
        response_server=sock.recv(1024)[:-2]
        return Response({'data': str(response_server)})

class GetAllMetrics(APIView):
    def get(self, request):
        metrics = Metrics.objects.all()
        serializer = MetricsSerializer(metrics, many=True)
        return Response({"data": serializer.data})

class AddMetric(APIView):
    def post(self, request):
        data_metrics = request.data.get('data_metrics')
        # Create an article from the above data
        serializer = MetricsSerializer(data=data_metrics)
        if serializer.is_valid(raise_exception=True):
            metrics_saved = serializer.save()
        return Response({"status": "success"})
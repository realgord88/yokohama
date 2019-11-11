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

class SetLenght(APIView):
    def post(self, request):
	lenght=str(request.query_params['lenght'])
	request_lenght=":SENS3:POW:WAV " + lenght + "NM\n"
        sock.sendall(request_lenght)
	sock.sendall(":SENS3:POW:WAV?\n")
        response_server=sock.recv(1024)
        return Response({'data': str(response_server)})

class SetAveraging(APIView):
    def post(self, request):
	average=str(request.query_params['average'])
	request_average=":SENS3:POW:ATIM " + average + "MS\n"
        sock.sendall(request_average)
	sock.sendall(":SENS3:POW:ATIM?\n")
        response_server=sock.recv(1024)
        return Response({'data': str(response_server)})

class InfoSlots(APIView):
    def get(self, request):
	response_server = []
        for slot_number in range(1,4):
		print slot_number
		command=":SLOT" + str(slot_number) + ":IDN?\n"
		sock.sendall(command)
        	response_server.append(sock.recv(1024))
		print response_server
        return Response({'data': response_server})

class SetDate(APIView):
    def post(self, request):
	date=str(request.query_params['date']).replace('.',',')
	request_date=":SYStem:DATE " + date + "\n"
        sock.sendall(request_date)
	sock.sendall(":SYStem:DATE?\n")
        response_server=sock.recv(1024)
        return Response({'data': str(response_server)})

class SetTime(APIView):
    def post(self, request):
	request_time=str(request.query_params['time']).replace(':',',')
	request_time=":SYStem:TIME " + request_time + "\n"
        sock.sendall(request_time)
	sock.sendall(":SYStem:Time?\n")
        response_server=sock.recv(1024)
        return Response({'data': str(response_server)})


class CheckErrors(APIView):
    def get(self, request):
        sock.sendall(":SYSTem:ERRor?\n")
        response_server=sock.recv(1024)
        return Response({'data': str(response_server)})

class SetOffset(APIView):
    def post(self, request):
	offset=str(request.query_params['db'])
	request_offset=":SENS3:CORR " + offset + "DB\n"
        sock.sendall(request_offset)
	sock.sendall(":SENS3:CORR?\n")
        response_server=sock.recv(1024)
        return Response({'data': str(response_server)})

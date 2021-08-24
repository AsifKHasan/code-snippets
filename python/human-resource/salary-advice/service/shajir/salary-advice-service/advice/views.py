
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, JsonResponse, FileResponse
import json
import os


@api_view(["POST"])
def advice(request):
    try:
        data = json.loads(request.body.decode('utf8'))
        if data['body']['payThrough'] == 'Bank':
            if data['body']["filter"] == 'None':
                file = "./salary-advice-bank.py --month "+data['body']['month']+" --refno "+data['body']['refNo']
            elif data['body']["filter"] == 'BdREN':
                file = "./salary-advice-bank-bdren.py --month "+data['body']['month']+" --refno "+data['body']['refNo']
            else:
                file = "./salary-advice-bank-software-services.py  --month "+data['body']['month']+" --refno "+data['body']['refNo']

        if data['body']['payThrough'] == 'Cash':
                file = "./salary-advice-cash.py --month " + data['body']['month'] + " --wing " + data['body']['wing']
        if data['body']['payThrough'] == 'Cheque':
                file = "./salary-advice-cheque.py --month " + data['body']['month'] + " --wing " + data['body']['wing']

        # change the 'home/shajir/mine/' with your local machine's path e.g. cd /your machine directory path/salary-advice-service/python-scripts && python3 " + file"
        cmd_out = os.popen("cd /home/shajir/mine/salary-advice-service/python-scripts && python3 " + file).read()
        trim_cmd_out = cmd_out[30:]
        file_name = ".".join(trim_cmd_out.split(".")[:2])[1:]
        file_location = "./python-scripts"+file_name+".pdf"

        try:
            file_data = open(file_location, "rb")
            response = HttpResponse(file_data, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="salary.pdf"'

        except IOError:
            response = HttpResponse('File not exist')
        return response

    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)

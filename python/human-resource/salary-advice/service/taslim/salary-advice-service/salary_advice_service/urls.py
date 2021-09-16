
from django.conf.urls import url
from django.contrib import admin
from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, JsonResponse, FileResponse
from django.core import serializers
from django.conf import settings
import json
import io
import pdfkit

# Create your views here.
@api_view(["POST"])
def GenerateSalaryAdvice(request):
    try:
        jsonData=request.body.decode('utf8')
        data = json.loads(jsonData)

        if data['head']['login'] == 'Admin' and data['head']['request-time'] != '':
            if data['body']['month'] != '' and data['body']['pay-through'] != '' and data['body']['filter'] != '' and data['body']['wing'] != '':
                
                options = {
                    'page-size': 'A4',
                    'margin-top': '0.75in',
                    'margin-right': '0.75in',
                    'margin-bottom': '0.75in',
                    'margin-left': '0.75in',
                    'encoding': "UTF-8",
                    'custom-header' : [
                        ('Accept-Encoding', 'gzip')
                    ],
                    'cookie': [
                        ('cookie-name1', 'cookie-value1'),
                        ('cookie-name2', 'cookie-value2'),
                    ],
                    'no-outline': None
                }
                buffer = io.BytesIO()

                # pdf = FPDF(orientation='P', unit='mm', format='A4')
                # pdf.add_page()
                # pdf.set_font("Arial", size=12)
                # pdf.cell(0, 10, txt=str(data), ln=1, align="C")
                # pdf.output("salary-advice.pdf")
                # return JsonResponse(pdf.output("salary-advice.pdf"),safe=False)
                # return FileResponse(buffer, as_attachment=True, filename='salary-advice.pdf')
                pdf_to_res = pdfkit.from_string(str(data), False, options=options)

                filename = "salary-advice.pdf"

                salaryAdvice = HttpResponse(pdf_to_res, content_type='application/pdf')
                salaryAdvice['Content-Disposition'] = 'attachment; filename="' + filename + '"'
                return salaryAdvice
            else:
                res = {
                    'header': {
                        'responseCode': '400-sa',
                        'responseMessage': 'invalid data provided'
                    },
                    'body': {
                        'responseMessage': 'invalid data provided'
                    }
                }
                return JsonResponse(res,safe=False)
        else:
            res = {
                'header': {
                    'responseCode': '400-sa',
                    'responseMessage': 'invalid data provided'
                },
                'body': {
                    'responseMessage': 'invalid data provided'
                }
            }
            return JsonResponse(res,safe=False) 
    except ValueError as e:
        return Response(e.args[0],status.HTTP_400_BAD_REQUEST)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^generate-salary-advice/',GenerateSalaryAdvice)
]
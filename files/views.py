from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

import os, random, struct
import cStringIO as StringIO
from Crypto.Cipher import AES
from models import FileLink
import datetime
from utils import decrypt,encrypt
from utils import render_response
import uuid
import socket

def index( request):
	if request.method == 'GET':
		return render_response('upload.html',request)
	elif request.method == 'POST':
		try:
			ufile = request.FILES['file']
		except:
			context = {'error':'File is Mandatory. Please choose a file'}
			return render_response('upload.html', request, context)
		fileMap = FileLink()
		fileMap.externalName = ufile
		fileMap.linkSuffix = uuid.uuid4()
		fileMap.created_on = datetime.datetime.now()
		fileMap.password_protected = request.POST.get('password_protected', False)
		fileMap.password = request.POST.get('password')
		fileMap.save()
		internal_name = handle_uploaded_file(ufile,fileMap)

		externalLink = "http://%s/download?fileName=%s" % (request.get_host(),internal_name)
		return HttpResponse("File Uploaded. Here is the <a target='_blank' href='%s'>link</a>" % externalLink)

def get_file(request):
	current_time = datetime.datetime.now().replace(tzinfo=None)
	fileName = request.GET.get('fileName')
	fileMap = FileLink.objects.get(linkSuffix=fileName)

	if fileMap.password_protected:
		if request.POST.get('password'):
			if request.POST.get('password') != fileMap.password:
				context = {"error": "Incorrect Password"}
				return render_response('password.html',request,context)
		else:
			return render_response('password.html',request)

	seconds_since_upload = (current_time - fileMap.created_on.replace(tzinfo=None)).total_seconds()
	if seconds_since_upload >= 24 * 60 * 60:
		return HttpResponse("Link is more than 24 hours old hence expired")

	password = 'localkeyofclient' if not fileMap.password_protected else fileMap.password.encode('ascii','ignore')
	abspath = '/tmp/%s.enc' % fileName
	ufile = open(abspath,'r')
	
	outfile = StringIO.StringIO()
	outfile=decrypt(ufile,outfile,password)

	response = HttpResponse(content=outfile.getvalue())
	response['Content-Type'] = 'mimetype/submimetype'
	response['Content-Disposition'] = 'attachment; filename=%s' % fileMap.externalName
	return response

def handle_uploaded_file(f,fileMap):
	id = '%s' % fileMap.id
	suffix = fileMap.linkSuffix
	internal_file_name = '/tmp/%s.enc' % suffix
	password = 'localkeyofclient' if not fileMap.password_protected else fileMap.password.encode('ascii','ignore')
	destination = open(internal_file_name, 'wb+')
	encrypt(f,destination,password)
	return suffix
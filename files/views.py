from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from django.template.context_processors import csrf
import os, random, struct
import cStringIO as StringIO
from Crypto.Cipher import AES
from models import FileLink
import datetime
from utils import decrypt,encrypt
import socket

def index( request):
	if request.method == 'GET':
		c = {}
		c.update(csrf(request))
		return render_to_response('upload.html', c)
	elif request.method == 'POST':
		try:
			ufile = request.FILES['file']
		except:
			c = {'error':'File is Mandatory. Please choose a file'}
			c.update(csrf(request))
			return render_to_response('upload.html', c)
		fileMap = FileLink()
		fileMap.externalName = ufile
		fileMap.created_on = datetime.datetime.now()
		fileMap.password_protected = request.POST.get('password_protected', False)
		fileMap.password = request.POST.get('password')
		fileMap.save()
		internal_name = handle_uploaded_file(ufile,fileMap)

		externalLink = "http://%s/download?fileName=%s" % (request.get_host(),internal_name)
		return HttpResponse("File Uploaded. Here is the <a href='%s'>link</a>" % externalLink)

def get_file(request):
	current_time = datetime.datetime.now().replace(tzinfo=None)
	fileName = request.GET.get('fileName')
	fileMap = FileLink.objects.get(id=fileName)

	if fileMap.password_protected:
		if request.POST.get('password'):
			if request.POST.get('password') != fileMap.password:
				c = {"error": "Incorrect Password"}
				c.update(csrf(request))
				print c
				return render_to_response('password.html', c)
		else:
			c = {}
			c.update(csrf(request))
			print c
			return render_to_response('password.html', c)

	seconds_since_upload = (current_time - fileMap.created_on.replace(tzinfo=None)).total_seconds()
	if seconds_since_upload >= 24 * 60 * 60:
		return HttpResponse("Link is more than 24 hours old hence expired")


	password = 'localkeyofclient' if not fileMap.password_protected else fileMap.password.encode('ascii','ignore')
	abspath = '/tmp/%s.enc' % fileName.zfill(5)
	chunksize=24*1024
	ufile = open(abspath,'r')
	
	outfile = StringIO.StringIO()
	outfile=decrypt(ufile,outfile,password,32)

	response = HttpResponse(content=outfile.getvalue())
	response['Content-Type'] = 'mimetype/submimetype'
	# or let your webserver auto-inject such a header field
	# after auto-recognition of mimetype based on filename extension

	response['Content-Disposition'] = 'attachment; filename=%s' \
	    % fileMap.externalName

	return response

def handle_uploaded_file(f,fileMap):
	id = '%s' % fileMap.id
	suffix = id.zfill(5)
	internal_file_name = '/tmp/%s.enc' % suffix

	password = 'localkeyofclient' if not fileMap.password_protected else fileMap.password.encode('ascii','ignore')
	print "Password:",password,fileMap.password
	destination = open(internal_file_name, 'wb+')
	encrypt(f,destination,password, 32)
	return suffix
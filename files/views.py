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

# Create your views here.
def index( request):
	if request.method == 'GET':
		c = {}
		c.update(csrf(request))
		return render_to_response('upload.html', c)
	elif request.method == 'POST':
		ufile = request.FILES['file']
		fileMap = FileLink()
		fileMap.externalName = ufile
		fileMap.created_on = datetime.datetime.now()
		fileMap.password_protected = True
		fileMap.password = request.POST.get('password')
		fileMap.save()
		internal_name = handle_uploaded_file(ufile,fileMap.id)
		externalLink = "http://localhost:8000/download?fileName=%s" % internal_name
		return HttpResponse("File Uploaded. Here is the <a href='%s'>link</a>" % externalLink)

def get_file(request):
	current_time = datetime.datetime.now().replace(tzinfo=None)
	fileName = request.GET.get('fileName')
	fileMap = FileLink.objects.get(id=fileName)

	if fileMap.password_protected:
		if request.POST.get('password'):
			if request.POST.get('password') != fileMap.password:
				print "passwords",request.POST.get('password'), fileMap.password
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


	key = 'localkeyofclient'
	password = 'localkeyofclient'
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

def handle_uploaded_file(f,id):
	id = '%s' % id
	suffix = id.zfill(5)
	internal_file_name = '/tmp/%s.enc' % suffix
	key = 'localkeyofclient'
	password = 'localkeyofclient'

	iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
	encryptor = AES.new(key, AES.MODE_CBC, iv)
	filesize = f._size
	chunksize = 64 * 1024

	destination = open(internal_file_name, 'wb+')
	encrypt(f,destination,password, 32)
	print 'upload outfile',destination
	return suffix
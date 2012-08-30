from django.shortcuts import render_to_response

def index(request):
  return recent()

def recent(request):
  return render_to_response('main/index.html', {

  })

def popular_gear(request):
  return render_to_response('main/index.html', {

  })

def popular_mount(request):
  return render_to_response('main/index.html', {

  })

def

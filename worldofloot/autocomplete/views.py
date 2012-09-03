import autocomplete
import json
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404

def complete(request, query):
  results = autocomplete.search(query)[:10]
  # TODO dedup on name, prefer the ones that are already in db, etc.
  return HttpResponse(json.dumps(results), mimetype="application/json")

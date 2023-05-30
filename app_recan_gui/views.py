from django.shortcuts import render
from .simgen import Simgen
from django.core.files.storage import FileSystemStorage
import os
from django.contrib import messages
from django.contrib.sessions.models import Session

SEQ_DATA = {
    "alignment": None,
    "sequences": [],
    "pot_rec": None,
    "pot_rec_id": None,
    "plot_div": None,
    "window_size": None,
    "window_shift": None,
    "align_len": None,
    "region_start": 0,
    "region_end": None,
    "dist_methods": {"pairwise distance": "pdist", 
                     "Jukes-Cantor distance": "jcd", 
                     "Kimura 2-parameter distance": "k2p",
                     "Tamura distance": "td" }, 
    "dist_method": "pdist",
    "session_key": None

}

def recan_view(request):
    '''main view function'''

    #request.session.modified = True
    if not request.session.session_key:
        request.session.save()
        session_key = request.session.session_key
        
    else:
        session_key = request.session.session_key

    SEQ_DATA['session_key'] = session_key

    
    
    
    if request.method == "POST" and "btn_submit_alignment" in request.POST \
          and "alignment_file" in request.FILES:
        uploaded_file = request.FILES["alignment_file"]
        file_name = uploaded_file.name
        request.session['file_name'] = file_name

        SEQ_DATA['file_name'] = request.session['file_name']

      
    return render(request, "base.html", context=SEQ_DATA)


    
    



    

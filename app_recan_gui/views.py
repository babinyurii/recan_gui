from django.shortcuts import render
from .simgen import Simgen
from django.core.files.storage import FileSystemStorage
import os
from django.contrib import messages
from django.contrib.sessions.models import Session
from .models import SessionData

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
        # make all records in his SessionData table default
        # either by themselves - when model created or 
        
    else:
        session_key = request.session.session_key

    # first save data
    session_data = Session.objects.values('session_key').filter(session_key=session_key)[0]
    SEQ_DATA['session_key'] = session_data['session_key']    
    
    
    if request.method == "POST" and "btn_submit_alignment" in request.POST \
          and "alignment_file" in request.FILES:
        
        session_key = request.session.session_key
        uploaded_file = request.FILES["alignment_file"]
        file_name = uploaded_file.name

        

        session_data = SessionData.objects.get(session_key_id=session_key)
        session_data.file_name = file_name
        session_data.save()
        file_name_from_db = SessionData.objects.values('file_name').filter(session_key_id=session_key)[0]
        SEQ_DATA['file_from_db'] = file_name_from_db['file_name']
        SEQ_DATA['alignment'] = file_name_from_db['file_name']

        ######################################3
        # постепенно подменять одно за одним значение из SEQ_DATA
        # значениями из базы данных SessionData
        #
        #####################################33







    return render(request, "base.html", context=SEQ_DATA)


    
    



    

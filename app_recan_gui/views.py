from django.shortcuts import render
from .simgen import Simgen
from django.core.files.storage import FileSystemStorage
import os
from django.contrib import messages
from django.contrib.sessions.models import Session
from .models import SessionData

# COMMENT THIS PATH IF UPLOAD ON PYTHONANYWHERE
PATH_TO_MEDIA_DIR = "./media/"

# UNCOMMENT THIS PATH IF UPLOAD ON PYTHONANYWHERE: 
# PATH_TO_MEDIA_DIR = "/home/yuriyb/prj_recan_gui/media/"

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

def get_session_key(request):
    if not request.session.session_key:
        request.session.save()
        session_key = request.session.session_key   
    else:
        session_key = request.session.session_key
    return session_key

def clean_media_dir(session_key):
    """remove files from media dir with
    current session key in their name"""

    save_dir = os.listdir(f"{PATH_TO_MEDIA_DIR}")
    if not len(save_dir) == 0:
        for file in save_dir:
            if file.rsplit('.', 1)[0].rsplit('_', 1)[1] == session_key:
                os.remove(f"{PATH_TO_MEDIA_DIR}{file}")

def add_session_key_to_alignment_name(alignment_name, session_key):
    alignment_base_name, fasta_extension = alignment_name.rsplit('.', 1)
    return alignment_base_name + '_' + session_key + '.' + fasta_extension


def save_file_in_media_dir(uploaded_alignment, alignment_name_with_key):
    """add key to file name, save it 
    """
    fs = FileSystemStorage()
    fs.save(alignment_name_with_key, uploaded_alignment)


def validate_num_of_sequences(file_name):
    '''
    check if the number of sequences in the uploaded 
    aligment is >=  3
    '''
    sim_obj = Simgen(f"{PATH_TO_MEDIA_DIR}{file_name}")
    sequences_list = sim_obj.get_info()
    if len(sequences_list) >= 3:
        return True
    else:
        return False

def recan_view(request):
    '''main view function'''

    session_key = get_session_key(request)

    session_key = SessionData.objects.values(
        'session_key_id').filter(
        session_key_id=session_key)[0]['session_key_id']
    SEQ_DATA['session_key'] = session_key  
    
    
    if request.method == "POST" and "btn_submit_alignment" in request.POST \
          and "alignment_file" in request.FILES:      
        session_key = request.session.session_key
        uploaded_alignment = request.FILES["alignment_file"]
        alignment_name = uploaded_alignment.name

        if alignment_name.rsplit(".")[-1] in ["fas", "fa", "fasta"]: 
            clean_media_dir(session_key)
            alignment_name_with_key = add_session_key_to_alignment_name(alignment_name, 
                                                                           session_key)
            save_file_in_media_dir(uploaded_alignment, 
                                   alignment_name_with_key)
            if validate_num_of_sequences(alignment_name_with_key):
                sim_obj = Simgen(f"{PATH_TO_MEDIA_DIR}{alignment_name_with_key}")
                session_data = SessionData.objects.get(session_key_id=session_key)
                session_data.alignment = alignment_name
                session_data.alignment_with_key = alignment_name_with_key
                session_data.region_end = sim_obj.alignment_roll_window.align.get_alignment_length()
                session_data.align_len = session_data.region_end
                pot_rec_id = sim_obj.get_info()[0]
                session_data.pot_rec_id = pot_rec_id
                session_data.pot_rec_index = sim_obj.get_info().index(pot_rec_id)
                session_data.save()
                alignment_from_db = SessionData.objects.values('alignment').filter(session_key_id=session_key)[0]
                SEQ_DATA['file_from_db'] = alignment_from_db['alignment']
                SEQ_DATA['alignment'] = alignment_from_db['alignment']
            else:
                session_data = SessionData.objects.get(session_key_id=session_key)
                session_data.alignment = None
                session_data.save()
                messages.error(request, "file contains less than three sequences")
                SEQ_DATA['alignment'] = None

        else:
            session_data = SessionData.objects.get(session_key_id=session_key)
            session_data.alignment = None
            session_data.save()
            messages.error(request, "check file extension")
            SEQ_DATA['alignment'] = None
       





     ######################################3
    # постепенно подменять одно за одним значение из SEQ_DATA
    # значениями из базы данных SessionData
    # после передавать целый контекст из базы здесь
    # перед этим закомментировать все обращения к словарю SEQ_DATA
    # вью изменяет контекст выше. 
    # и только здесь передает - одна точка передачи
    #####################################33

    return render(request, "base.html", context=SEQ_DATA)


    
    



    

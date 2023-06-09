from django.shortcuts import render
from .simgen import Simgen
from django.core.files.storage import FileSystemStorage
import os
from django.contrib import messages
from .models import SessionData

# COMMENT THIS PATH IF UPLOAD ON PYTHONANYWHERE
PATH_TO_MEDIA_DIR = "./media/"

# UNCOMMENT THIS PATH IF UPLOAD ON PYTHONANYWHERE: 
# PATH_TO_MEDIA_DIR = "/home/yuriyb/prj_recan_gui/media/"


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


def update_session_data_with_default_values(session_key):
    session_data = SessionData.objects.get(session_key_id=session_key)
    session_data.alignment = None
    session_data.alignment_with_key = None
    session_data.pot_rec_id = None
    session_data.pot_rec_index = 0
    session_data.plot_div = None
    session_data.window_size = 50
    session_data.window_shift = 25
    session_data.align_len = None
    session_data.region_start = 0
    session_data.region_end = None
    session_data.dist_method = 'pdist'
    session_data.save()

def update_session_data_with_start_values(alignment_name_with_key, 
                                          session_key,
                                          alignment_name):
    sim_obj = Simgen(f"{PATH_TO_MEDIA_DIR}{alignment_name_with_key}")
    session_data = SessionData.objects.get(session_key_id=session_key)
    session_data.alignment = alignment_name
    session_data.alignment_with_key = alignment_name_with_key
    session_data.region_end = sim_obj.alignment_roll_window.align.get_alignment_length()
    session_data.align_len = session_data.region_end
    pot_rec_id = sim_obj.get_info()[0]
    session_data.pot_rec_id = pot_rec_id
    session_data.pot_rec_index = sim_obj.get_info().index(pot_rec_id)
    session_data.plot_div = None
    session_data.save()

def collect_plot_input_params(sim_obj, session_data, plot_data):
    session_data.window_size = int(plot_data.get("window_size"))
    session_data.window_shift = int(plot_data.get("window_shift"))
    session_data.dist_method = plot_data.get("dist_method")
    session_data.pot_rec_id = plot_data.get("pot_rec")
    session_data.pot_rec_index = sim_obj.get_info().index(plot_data.get("pot_rec"))
    if int(plot_data.get('region_start')) != session_data.region_start:
        session_data.region_start = int(plot_data.get('region_start'))
    if int(plot_data.get('region_end')) != session_data.region_end:
        session_data.region_end = int(plot_data.get('region_end'))
    session_data.save()

    return session_data

def plot_distance(session_data, sim_obj):
    if session_data.region_start and session_data.region_start:
            plot = sim_obj.simgen(window=session_data.window_size, 
                                shift=session_data.window_shift, 
                                pot_rec=session_data.pot_rec_index, 
                                region=(session_data.region_start, 
                                        session_data.region_end),
                                dist=session_data.dist_method)
    else:
        plot = sim_obj.simgen(window=session_data.window_size, 
                            shift=session_data.window_shift, 
                            pot_rec=session_data.pot_rec_index, 
                            dist=session_data.dist_method)       
                    
    session_data.plot_div = plot
    session_data.save()


def recan_view(request):
    '''main view function'''
    session_key = get_session_key(request)
    
    if request.method == "POST" and "btn_submit_alignment" in request.POST \
          and "alignment_file" in request.FILES:      
        session_key = request.session.session_key
        uploaded_alignment = request.FILES["alignment_file"]
        alignment_name = uploaded_alignment.name

        if alignment_name.rsplit(".")[-1] in ["fas", "fa", "fasta"]:
            clean_media_dir(session_key)
            alignment_name_with_key = add_session_key_to_alignment_name(
                alignment_name, 
                session_key)
            save_file_in_media_dir(uploaded_alignment, 
                                   alignment_name_with_key)
            if validate_num_of_sequences(alignment_name_with_key):
                update_session_data_with_start_values(alignment_name_with_key,
                                                      session_key,
                                                      alignment_name)
            else:
                update_session_data_with_default_values(session_key)
                messages.error(request, "file contains less than three sequences")
        else:
            update_session_data_with_default_values(session_key)
            messages.error(request, "check file extension")

    elif request.method == "POST" and "calc_plot_form" in request.POST:
        session_key = request.session.session_key
        session_data = SessionData.objects.get(session_key_id=session_key)
        input_file_name = session_data.alignment_with_key
        sim_obj = Simgen(f"{PATH_TO_MEDIA_DIR}{input_file_name}")
        plot_data = request.POST.dict()

        session_data = collect_plot_input_params(sim_obj, session_data, plot_data)
        try:
            plot_distance(session_data, sim_obj)
        except TypeError or ZeroDivisionError:
            messages.error(request, 
                           (f"distance can't by calculated by chosen method. Try to enlarge window size, window shift or both"))
            session_data.plot_div = None
            session_data.save()
    
    context = SessionData.objects.filter(session_key_id=session_key).values()[0]
    if context['alignment_with_key']:
        sim_obj = Simgen(f"{PATH_TO_MEDIA_DIR}{context['alignment_with_key']}")
        context['sequences'] = sim_obj.get_info()
   

    return render(request, "base.html", context=context)


    
     #return render(request, "base.html", context=SEQ_DATA)



    

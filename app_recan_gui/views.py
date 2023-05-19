from django.shortcuts import render
from .simgen import Simgen
from django.core.files.storage import FileSystemStorage
import os
from django.contrib import messages
from .models import SessionData
from django.contrib.sessions.models import Session

# COMMENT THIS PATH IF UPLOAD ON PYTHONANYWHERE
PATH_TO_MEDIA_DIR = "./media/"

# UNCOMMENT THIS PATH IF UPLOAD ON PYTHONANYWHERE: 
# PATH_TO_MEDIA_DIR = "/home/yuriyb/prj_recan_gui/media/"

DEFAULT_PLOT_SETTINGS = {
    "window_size" : 50,
    "window_shift" : 25
}

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
                     "Tamura distance": "td" }, # we need dict, with values of short dist names to pass to simgen
    "dist_method": "pdist",
    "session": None

}


def clean_media_dir():
    '''
    clean media dir so that only one
    file was uploaded
    '''
    save_dir = os.listdir(f"{PATH_TO_MEDIA_DIR}")
    if not len(save_dir) == 0:
        for file in save_dir:
            os.remove(f"{PATH_TO_MEDIA_DIR}{file}")


def save_file_in_media_dir(uploaded_file):
    '''save uploaded alignment
    '''
    fs = FileSystemStorage()
    fs.save(uploaded_file.name, uploaded_file)


def validate_num_of_sequences(file_name):
    '''
    check if the number of sequences in the uploaded 
    aligment is >=  3
    '''
    sim_obj = Simgen(f"{PATH_TO_MEDIA_DIR}{file_name}")
    SEQ_DATA["sequences"] = sim_obj.get_info()
    if len(SEQ_DATA["sequences"]) >= 3:
        return True
    else:
        return False


def get_default_plot_settings():
    SEQ_DATA["window_size"] = DEFAULT_PLOT_SETTINGS["window_size"]
    SEQ_DATA["window_shift"] = DEFAULT_PLOT_SETTINGS["window_shift"]
    SEQ_DATA["alignment"] = None # remove file name
    SEQ_DATA["plot_div"] = None # remove plot     

def recan_view(request):
    '''main view function'''

    if not request.session.session_key:
        request.session.save()
        #session_id = request.session.session_key

    SEQ_DATA["session"] = request.session    
    
    # if user uploads file
    if request.method == "POST" and "btn_submit_alignment" in request.POST \
          and "alignment_file" in request.FILES:
        clean_media_dir() # remove all files from media dir
        get_default_plot_settings()
        uploaded_file = request.FILES["alignment_file"]
        # check extension, if valid, proceed
        if uploaded_file.name.rsplit(".")[-1] in ["fas", "fa", "fasta"]: 
            save_file_in_media_dir(uploaded_file)
            file_name = uploaded_file.name

            if validate_num_of_sequences(file_name):
                sim_obj = Simgen(f"{PATH_TO_MEDIA_DIR}{file_name}")
                SEQ_DATA["alignment"] = file_name
                SEQ_DATA["align_len"] = sim_obj.alignment_roll_window.align.get_alignment_length()
                SEQ_DATA["region_end"] = SEQ_DATA["align_len"]
                SEQ_DATA["pot_rec_id"] = SEQ_DATA["sequences"][0]
            else:
                messages.error(request, "file contains less than three sequences")
                SEQ_DATA["alignment"] = None
        # if file extension is not valid, raise related warning
        else:
            messages.error(request, "check file extension")

    # if use hits the plot button to get the distance plot
    elif request.method == "POST" and "calc_plot_form" in request.POST:
        input_file_name = SEQ_DATA["alignment"]
        sim_obj = Simgen(f"{PATH_TO_MEDIA_DIR}{input_file_name}")
        # take data from POST dict: window, shift  - TODO > pot_rec
        # TODO collect data into context. not into local variables
        # TODO then pass these vars to the plot constructor
        plot_data = request.POST.dict()
        win_size = int(plot_data.get("window_size"))
        win_shift = int(plot_data.get("window_shift"))
        dist = plot_data.get("dist_method")

        # TODO use dist method to show plot parameters
        SEQ_DATA["dist_method"] = dist

        # TODO make def > check if plot of the particular genome region needed
        if plot_data.get("region_start"):
            region_start = int(plot_data.get("region_start"))
            SEQ_DATA["region_start"] = region_start
        else:
            SEQ_DATA["region_start"] = 0

        if plot_data.get("region_end"):
            region_end = int(plot_data.get("region_end"))
            SEQ_DATA["region_end"] = region_end
        else:
            SEQ_DATA["region_end"] = SEQ_DATA["align_len"]
        

        pot_rec = str(plot_data.get("pot_rec"))
        pot_rec_index = SEQ_DATA["sequences"].index(pot_rec)
        SEQ_DATA["pot_rec_id"] = pot_rec

        # plot by simgen
        # TODO the function: plot = plot_by_simgen() <<< make function which calls the plot
        # TODO get data from SEQ_DATA not from local vars
        try:
            if SEQ_DATA["region_start"] and SEQ_DATA["region_end"]:
                plot = sim_obj.simgen(window=win_size, 
                                    shift=win_shift, 
                                    pot_rec=pot_rec_index, 
                                    region=(SEQ_DATA["region_start"], SEQ_DATA["region_end"]),
                                    dist=dist)
            else:
                plot = sim_obj.simgen(window=win_size, 
                                    shift=win_shift, 
                                    pot_rec=pot_rec_index,
                                    dist=dist)
                
            SEQ_DATA["plot_div"] = plot
            SEQ_DATA["window_size"] = win_size
            SEQ_DATA["window_shift"] = win_shift
        # if window is too small, these too error may occur 
        # depenging on the distance method used
        except TypeError or ZeroDivisionError:
            messages.error(request, (f"distance can't by calculated by chosen method:{ SEQ_DATA['dist_method'] }, try to enlarge window size, window shift or both"))
            SEQ_DATA["plot_div"] = None
    else:
        SEQ_DATA["alignment"] = None

    print("----")
    print(type(SEQ_DATA['plot_div']))
    return render(request, "base.html", context=SEQ_DATA)


    
    



    

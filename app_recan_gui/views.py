from django.shortcuts import render
from .simgen import Simgen
from django.core.files.storage import FileSystemStorage
import os
from django.contrib import messages

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
    "window_shift": None,
    "window_size": None,
    "default_window_size": 50,
    "default_window_shift": 25,
    "all_uploaded_files": [],  # TODO delete after ready. just to have a look at files in media dir
    "align_len": None,
    "region_start": None,
    "region_end": None,
    "dist_methods": {"pairwise distance": "pdist", 
                     "Jukes-Cantor distance": "jcd", 
                     "Kimura 2-parameter distance": "k2p",
                     "Tamura distance": "td" }, # we need dict, with values of short dist names to pass to simgen
    "dist_method_chosen": None

}


def clean_media_dir():
    save_dir = os.listdir(f"{PATH_TO_MEDIA_DIR}")
    if not len(save_dir) == 0:
        for file in save_dir:
            os.remove(f"{PATH_TO_MEDIA_DIR}{file}")
        for file in save_dir:
            #os.remove(file)
            SEQ_DATA["all_uploaded_files"].append(file)

def save_file_in_media_dir(uploaded_file):
    fs = FileSystemStorage()
    fs.save(uploaded_file.name, uploaded_file)
    #file_name = fs.save(uploaded_file.name, uploaded_file)
    #uploaded_file_url = fs.url(file_name)
    #SEQ_DATA["uploaded_alignment_url"] = uploaded_file_url
    #path = uploaded_file.file

def validate_num_of_sequences(file_name):
    sim_obj = Simgen(f"{PATH_TO_MEDIA_DIR}{file_name}")
    SEQ_DATA["sequences"] = sim_obj.get_info()
    if len(SEQ_DATA["sequences"]) >= 3:
        # put alignment length
        SEQ_DATA["align_len"] = sim_obj.alignment_roll_window.align.get_alignment_length()
        SEQ_DATA["pot_rec_id"] = SEQ_DATA["sequences"][0]
        return True
    else:
        return False
        

def recan_view(request):

    if request.method == "POST" and "btn_submit_alignment" in request.POST and "alignment_file" in request.FILES:
        clean_media_dir() # remove all files from media dir
        SEQ_DATA["alignment"] = None # remove file name
        SEQ_DATA["plot_div"] = None # remove plot
        uploaded_file = request.FILES["alignment_file"]
    
        if uploaded_file.name.rsplit(".")[-1] in ["fas", "fa", "fasta"]: # check extension
            save_file_in_media_dir(uploaded_file)
            file_name = uploaded_file.name
            if validate_num_of_sequences(file_name):
                SEQ_DATA["alignment"] = file_name
            else:
                messages.error(request, "file contains less than three sequences")
                SEQ_DATA["alignment"] = None
        else:
            messages.error(request, "check file extension")

    
    elif request.method == "POST" and "calc_plot_form" in request.POST:

        # init simgen obj
        input_file_name = SEQ_DATA["alignment"]
        sim_obj = Simgen(f"{PATH_TO_MEDIA_DIR}{input_file_name}")

        # take data from POST dict: window, shift  - TODO > pot_rec
        # #############################################3
        # TODO collect data into context. not into local variables
        # TODO then pass these vars to the plot constructor
        plot_data = request.POST.dict()
        win_size = int(plot_data.get("window_size"))
        win_shift = int(plot_data.get("window_shift"))
        dist = plot_data.get("dist_method")

        # TODO just to save the distance. see if you need it further to 
        # show the user his plot input parameters
        SEQ_DATA["dist_method"] = dist

        # TODO make def > check if region needed
        if plot_data.get("region_start"):
            region_start = int(plot_data.get("region_start"))
            SEQ_DATA["region_start"] = region_start
        if plot_data.get("region_end"):
            region_end = int(plot_data.get("region_end"))
            SEQ_DATA["region_end"] = region_end
        

        pot_rec = str(plot_data.get("pot_rec"))
        pot_rec_index = SEQ_DATA["sequences"].index(pot_rec)
        SEQ_DATA["pot_rec_id"] = pot_rec

        #####################################################
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

        except TypeError:
            messages.error(request, ("distance can't by calculated by chosen method:__, try to enlarge window size, window shift or both"))

        #return render(request, "base.html", context=SEQ_DATA)
    else:
        SEQ_DATA["alignment"] = None

    #except:
    #    pass
        
    return render(request, "base.html", context=SEQ_DATA)


    
    



    

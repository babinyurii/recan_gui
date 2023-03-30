from django.shortcuts import render
import plotly.offline as opy
import plotly.graph_objs as go
import random # to test the plot
from .simgen import Simgen
from django.core.files.storage import FileSystemStorage
import os


SEQ_DATA = {
    "alignment": None,
    "base_file_name": None,
    "sequences": ["virus_1", "virus_2", "virus_3"],
    "pot_rec": None,
    "plot_div": None,
    "window_shift": None,
    "window_size": None,
    "default_window_size": 50,
    "default_window_shift": 25,
    "uploaded_alignment_url": None,
    "all_uploaded_files": [],  # TODO delete after ready. just to have a look at files in media dir
    "align_len": None,
    "region_start": None,
    "region_end": None

}


def plot(start, stop):
    X = []
    Y = []
 
    for i in range(4):
        X.append(i)
    for i in range(4):
        #Y.append(random.randint(1, 10))
        Y.append(random.randint(start, stop))

    fig = go.Figure()
    scatter = go.Scatter(x=X, y=Y,
                        mode='lines', name='test',
                        opacity=0.8, marker_color='green')
    fig.add_trace(scatter)
    # holds all the HTML needed to render the plot!
    fig_html = fig.to_html()
    return fig_html

def clean_media_dir():
    save_dir = os.listdir("./media/")
    if not len(save_dir) == 0:
    
        for file in save_dir:
            os.remove(f"./media/{file}")
        for file in save_dir:
            #os.remove(file)
            SEQ_DATA["all_uploaded_files"].append(file)


def recan_view(request):

    if request.method == "POST" and "upload_alignment" in request.POST:
        # check if file is uploaded by button. if not pass and return the same context
        # it's to avoid dict error when you call the FILES dict, but 'alignment_file' isn't there
        if "alignment_file" in request.FILES: 
            clean_media_dir() # remove all files from media dir
            SEQ_DATA["alignment"] = None
            SEQ_DATA["plot_div"] = None

            # save init file name. 
            # it'll be needed if some files will be allowed to store and choose from 
            uploaded_file = request.FILES["alignment_file"]
            SEQ_DATA["base_file_name"] = uploaded_file.name
           

            fs = FileSystemStorage()
            file_name = fs.save(uploaded_file.name, uploaded_file)
            uploaded_file_url = fs.url(file_name)
            SEQ_DATA["uploaded_alignment_url"] = uploaded_file_url
            #path = uploaded_file.file
           
            SEQ_DATA["alignment"] = file_name
            #SEQ_DATA["plot_div"] = None
            SEQ_DATA["sequences"].append("new_seq")
            input_file_name = SEQ_DATA["alignment"]
            sim_obj = Simgen(f"./media/{input_file_name}")
            SEQ_DATA["sequences"] = sim_obj.get_info()
            # put alignment length
            SEQ_DATA["align_len"] = sim_obj.alignment_roll_window.align.get_alignment_length()
            return render(request, "base.html", context=SEQ_DATA)

    
    elif request.method == "POST" and "calc_plot_form" in request.POST:

        # init simgen obj
        input_file_name = SEQ_DATA["alignment"]
        sim_obj = Simgen(f"./media/{input_file_name}")

        # take data from POST dict: window, shift  - TODO > pot_rec
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
        
        

        # mock plot. replace by simgen plot
        #SEQ_DATA["plot_div"] = plot(start, stop)
        # populating our SEQ_DATA dict
        #SEQ_DATA["window_size"] = request.POST.get("window_size")
        #SEQ_DATA["window_shift"] = request.POST.get("window_shift")
        #SEQ_DATA["pot_rec"] = request.POST.get("pot_rec")
        #SEQ_DATA["region_start"] = request.POST.get("region_start")
        #SEQ_DATA["region_end"] = request.POST.get("region_end")
        pot_rec = str(plot_data.get("pot_rec"))
        pot_rec_index = SEQ_DATA["sequences"].index(pot_rec)

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
        
        
        

        return render(request, "base.html", context=SEQ_DATA)
    else:
        SEQ_DATA["alignment"] = None

    #except:
    #    pass
        

    return render(request, "base.html", context=SEQ_DATA)


    
    



    

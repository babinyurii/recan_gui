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
    "pot_rec": None,
    "default_window_size": 25,
    "default_window_shift": 10,
    "uploaded_alignment_url": None

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



def recan_view(request):

    if request.method == "POST" and "upload_alignment" in request.POST:
        # check if file is uploaded by button. if not pass and return the same context
        # it's to avoid dict error when you call the FILES dict, but 'alignment_file' isn't there
        if "alignment_file" in request.FILES: 
            uploaded_file = request.FILES["alignment_file"]
            SEQ_DATA["base_file_name"] = uploaded_file.name
            save_dir = os.listdir("./media/")
            if not len(save_dir) == 0:
                for file in save_dir:
                    os.remove(f"file")

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
            return render(request, "base.html", context=SEQ_DATA)

    
    elif request.method == "POST" and "calc_plot_form" in request.POST:

        # init simgen obj
        input_file_name = SEQ_DATA["alignment"]
        sim_obj = Simgen(f"./media/{input_file_name}")

        # take data from POST dict: window, shift  - TODO > pot_rec
        plot_data = request.POST.dict()
        start = int(plot_data.get("window_size"))
        stop = int(plot_data.get("window_shift"))

        # mock plot. replace by simgen plot
        SEQ_DATA["plot_div"] = plot(start, stop)

        # populating our SEQ_DATA dict
        SEQ_DATA["window_size"] = request.POST.get("window_size")
        SEQ_DATA["window_shift"] = request.POST.get("window_shift")
        SEQ_DATA["pot_rec"] = request.POST.get("pot_rec")
        

        return render(request, "base.html", context=SEQ_DATA)
    else:
        SEQ_DATA["alignment"] = None   

    #except:
    #    pass
        

    return render(request, "base.html", context=SEQ_DATA)


    
    



    

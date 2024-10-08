import os
from django.conf import settings
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.core.files.storage import FileSystemStorage
from django.forms import model_to_dict
from django.shortcuts import render, get_object_or_404
from app_recan_gui.constants import (SEQUENCE_LIMIT_IN_INPUT_FILE,
                                     SESSION_DATA_DEFAULT_VALUES,
                                     ERROR_MESSAGES,
                                     VALID_FASTA_EXTENSIONS,
                                     # PATH_TO_MEDIA_DIR,
                                    )
from app_recan_gui.models import SessionData
from simgen.simgen import Simgen


def clean_media_dir(session_key):
    """remove files from media dir with
    current session key in their name"""

    save_dir = os.listdir(f'{settings.MEDIA_ROOT}')
    if not len(save_dir) == 0:
        for file in save_dir:
            if file.rsplit('.', 1)[0].rsplit('_', 1)[1] == session_key:
                os.remove(f'{settings.MEDIA_ROOT}/{file}')


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
    sim_obj = Simgen(f'{settings.MEDIA_ROOT}/{file_name}')
    sequences_list = sim_obj.get_info()
    if len(sequences_list) >= SEQUENCE_LIMIT_IN_INPUT_FILE:
        return True
    else:
        return False


def update_session_data_with_default_values(session_key):
    session_data = SessionData.objects.get(session_key_id=session_key)
    session_data.alignment = SESSION_DATA_DEFAULT_VALUES['alignment']
    session_data.alignment_with_key = SESSION_DATA_DEFAULT_VALUES['alignment_with_key']
    session_data.pot_rec_id = SESSION_DATA_DEFAULT_VALUES['pot_rec_id']
    session_data.pot_rec_index = SESSION_DATA_DEFAULT_VALUES['pot_rec_index']
    session_data.plot_div = SESSION_DATA_DEFAULT_VALUES['plot_div']
    session_data.window_size = SESSION_DATA_DEFAULT_VALUES['window_size']
    session_data.window_shift = SESSION_DATA_DEFAULT_VALUES['window_shift']
    session_data.align_len = SESSION_DATA_DEFAULT_VALUES['align_len']
    session_data.region_start = SESSION_DATA_DEFAULT_VALUES['region_start']
    session_data.region_end = SESSION_DATA_DEFAULT_VALUES['region_end']
    session_data.dist_method = SESSION_DATA_DEFAULT_VALUES['dist_method']
    session_data.save()


def update_session_data_with_start_values(alignment_name_with_key,
                                          session_key,
                                          alignment_name):
    sim_obj = Simgen(f'{settings.MEDIA_ROOT}/{alignment_name_with_key}')
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
    session_data.window_size = int(plot_data.get('window_size'))
    session_data.window_shift = int(plot_data.get('window_shift'))
    session_data.dist_method = plot_data.get('dist_method')
    session_data.pot_rec_id = plot_data.get('pot_rec')
    session_data.pot_rec_index = sim_obj.get_info().index(
        plot_data.get('pot_rec'))
    # if int(plot_data.get('region_start')) != session_data.region_start:
    if plot_data.get('region_start') == '':
        session_data.region_start = 0
    else:
        session_data.region_start = int(plot_data.get('region_start'))
    # if int(plot_data.get('region_end')) != session_data.region_end:
    if plot_data.get('region_end') == '':
        session_data.region_start = sim_obj.alignment_roll_window.align.get_alignment_length()
    else:
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


def get_context_from_db(session_key):
    context = model_to_dict(get_object_or_404(SessionData, session_key=session_key))
    if context["alignment_with_key"]:
        try:
            sim_obj = Simgen(f'{settings.MEDIA_ROOT}/{context["alignment_with_key"]}')
            context['sequences'] = sim_obj.get_info()
        except FileNotFoundError:
            update_session_data_with_default_values(session_key)
            context = model_to_dict(get_object_or_404(SessionData, session_key=session_key))
    return context


def get_session_key(request):
    """return session key, if it does not exist create new one.
    if key exists but db record is 
    somehow deleted, create a new session, 
    """
    if not request.session.session_key:
        request.session.save()
        return request.session.session_key
    if not Session.objects.filter(
        session_key=request.session.session_key).exists():
        request.session.create()
        request.session.save()
    return request.session.session_key


def recan_view(request):
    '''main view function'''
    if request.method == 'GET':
        session_key = get_session_key(request)
        context = get_context_from_db(session_key)
        return render(request, 'recan.html', context=context)
    #and 'btn_submit_alignment' in request.POST 
    elif request.method == 'POST' and 'alignment_file' in request.FILES:
        session_key = request.session.session_key
        uploaded_alignment = request.FILES['alignment_file']
        alignment_name = uploaded_alignment.name

        if alignment_name.rsplit('.')[-1] in VALID_FASTA_EXTENSIONS:
            clean_media_dir(session_key)
            alignment_name_with_key = add_session_key_to_alignment_name(
                alignment_name,
                session_key)
            #save_file_in_media_dir(uploaded_alignment,
            #                       alignment_name_with_key)
            session_data_obj = SessionData.objects.get(session_key=session_key)
            session_data_obj.align_file = uploaded_alignment
            session_data_obj.save()
            if validate_num_of_sequences(alignment_name_with_key):
                update_session_data_with_start_values(alignment_name_with_key,
                                                      session_key,
                                                      alignment_name)
            else:
                update_session_data_with_default_values(session_key)
                messages.error(request, ERROR_MESSAGES['less_than_3_seq'])
        else:
            update_session_data_with_default_values(session_key)
            messages.error(request, ERROR_MESSAGES['wrong_file_extension'])
        context = get_context_from_db(session_key)
        return render(request, 'recan.html', context=context)



    elif request.method == 'POST' and 'calc_plot_form' in request.POST:
        session_key = request.session.session_key
        session_data = SessionData.objects.get(session_key_id=session_key)
        input_file_name = session_data.alignment_with_key
        
        try:
            sim_obj = Simgen(f'{settings.MEDIA_ROOT}/{input_file_name}')
            plot_data = request.POST.dict()
            session_data = collect_plot_input_params(sim_obj,
                                                 session_data,
                                                 plot_data)
        except FileNotFoundError:
            update_session_data_with_default_values(session_key)
        else:
            try:
                plot_distance(session_data, sim_obj)
            except (TypeError, ZeroDivisionError):
                messages.error(request, ERROR_MESSAGES['plot_parameters'])
                session_data.plot_div = None
                session_data.save()

        context = get_context_from_db(session_key)
        return render(request, 'recan.html', context=context)

# COMMENT THIS PATH IF UPLOAD ON PYTHONANYWHERE
#PATH_TO_MEDIA_DIR = './media/'

# UNCOMMENT THIS PATH IF UPLOAD ON PYTHONANYWHERE:
# PATH_TO_MEDIA_DIR = '/home/yuriyb/prj_recan_gui/media/'
SEQUENCE_LIMIT_IN_INPUT_FILE = 3
VALID_FASTA_EXTENSIONS = ['fa', 'fas', 'fasta']
SESSION_DATA_DEFAULT_VALUES = {
    'alignment': None,
    'alignment_with_key': None,
    'pot_rec_id': None,
    'pot_rec_index': 0,
    'plot_div': None,
    'window_size': 50,
    'window_shift': 25,
    'align_len': None,
    'region_start': 0,
    'region_end': None,
    'dist_method': 'pdist',
}

ERROR_MESSAGES = {'wrong_file_extension': "check file extension",
                  'less_than_3_seq': "file contains less than three sequences",
                  'plot_parameters': (
                      "distance can't by calculated "
                      "with chosen plot parameters."
                      "Try to enlarge window size, window shift or both. "
                      "If it doesn't help, change distance calculation method.")}



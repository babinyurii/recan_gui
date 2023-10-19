from django.test import TestCase, Client
from django.urls import reverse
from app_recan_gui.models import SessionData
import os
from app_recan_gui.models import SessionData
from app_recan_gui.views import ERROR_MESSAGES


VALID_INPUT_FILE = os.path.join(os.path.dirname(__file__), 'hiv.fasta')
INVALID_INPUT_FILE_TWO_SEQ = os.path.join(os.path.dirname(__file__), 'hiv_two_seq.fasta')
INVALID_INPUT_FILE_WRONG_EXTENSION = os.path.join(os.path.dirname(__file__), 'hiv_wrong_ext.txt')

class TestFileUploadAndPlotCreation(TestCase):


    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        #cls.session = cls.client.session
        #cls.session.save()

    def upload_file(self, test_file):
        self.client.session.session_key # when you access session key, it works in the test, otherwise doesn't
        url = reverse('recan_view')
        with open(test_file) as f:
            post_data = {'alignment_file': f, 'btn_submit_alignment':[]}
            response = self.client.post(url, post_data)
        return response

    def test_get_recan_session_data_created(self):
        response = self.client.get(reverse('recan_view'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(SessionData.objects.count(), 1)

        # TODO check here default values in session data table

    
    def test_valid_file_upload_and_start_data_session_values_after_upload(self):
             
        response = self.upload_file(VALID_INPUT_FILE)
        self.assertEqual(response.status_code, 200) 

        self.assertEqual(SessionData.objects.count(), 1)
        self.assertContains(response, 'AF193276.1_KAL153_rec')

        # check start values in the SessionData table after file is uploaded
        session_data_record = SessionData.objects.get(session_key=self.client.session.session_key)
        self.assertEqual(session_data_record.alignment, 'hiv.fasta')
        self.assertEqual(session_data_record.align_len, 3135)
        self.assertEqual(session_data_record.pot_rec_id, 'AF193276.1_KAL153_rec')
        self.assertEqual(session_data_record.pot_rec_index, 0)
        self.assertEqual(session_data_record.region_end, 3135)
        self.assertEqual(session_data_record.region_start, 0)
        self.assertEqual(session_data_record.plot_div, None)
        self.assertEqual(session_data_record.window_shift, 25)
        self.assertEqual(session_data_record.window_size, 50)
        self.assertEqual(session_data_record.dist_method, 'pdist')
        self.assertEqual(session_data_record.alignment_with_key, 'hiv' '_' + self.client.session.session_key + '.fasta')

    def test_upload_invalid_file_with_less_than_three_sequences(self):
        response = self.upload_file(test_file=INVALID_INPUT_FILE_TWO_SEQ)
        self.assertEqual(response.status_code, 200) 
        self.assertContains(response, ERROR_MESSAGES['less_than_3_seq'])
        session_data_record = SessionData.objects.get(session_key=self.client.session.session_key)
        self.assertEqual(session_data_record.alignment, None)
        self.assertEqual(session_data_record.alignment_with_key, None)


    def test_upload_invalid_file_with_wrong_extension(self):
            response = self.upload_file(INVALID_INPUT_FILE_WRONG_EXTENSION)
            self.assertEqual(response.status_code, 200) 
            self.assertContains(response, ERROR_MESSAGES['wrong_file_extension'])
            session_data_record = SessionData.objects.get(session_key=self.client.session.session_key)
            self.assertEqual(session_data_record.alignment, None)
            self.assertEqual(session_data_record.alignment_with_key, None)


    def test_plot_with_default_input_params(self):
        url = reverse('recan_view')
        
        response = self.upload_file(VALID_INPUT_FILE)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(SessionData.objects.count(), 1)

        # TODO here make method to send plot data and plot if needed
        post_data = {'window_size': ['50'], 'window_shift': ['25'], 'region_start': ['0'], 'region_end': ['3135'], 
        'calc_plot_form': [''], 'dist_method': ['pdist'], 'pot_rec': ['AF193276.1_KAL153_rec']}
        response = self.client.post(url, post_data)
        ################################################
        self.assertEqual(SessionData.objects.count(), 1)
        self.assertEqual(response.status_code, 200)
        returned_basic_input_params = ['file: hiv.fasta', 'alignment length: 3135', 'recombinant chosen: AF193276.1_KAL153_rec', ]
        for i in returned_basic_input_params:
            self.assertContains(response, i)
        session_data_record = SessionData.objects.get(session_key=self.client.session.session_key)
        self.assertNotEqual(session_data_record.plot_div, None)


    def test_plot_with_custom_input_params(self):
        url = reverse('recan_view')
        self.upload_file(VALID_INPUT_FILE)
        post_data = {'window_size': ['100'], 'window_shift': ['50'], 'region_start': ['500'], 'region_end': ['2500'], 
        'calc_plot_form': [''], 'dist_method': ['jcd'], 'pot_rec': ['AF193275.1_97BL006_min']}
        response = self.client.post(url, post_data)
        self.assertEqual(SessionData.objects.count(), 1)
        self.assertEqual(response.status_code, 200)
        returned_basic_input_params = ['file: hiv.fasta', 'alignment length: 3135', 'recombinant chosen: AF193275.1_97BL006_min', ]
        for i in returned_basic_input_params:
            self.assertContains(response, i)
        session_data_record = SessionData.objects.get(session_key=self.client.session.session_key)
        
        self.assertEqual(session_data_record.alignment, 'hiv.fasta')
        self.assertEqual(session_data_record.align_len, 3135)
        self.assertEqual(session_data_record.pot_rec_id, 'AF193275.1_97BL006_min')
        self.assertEqual(session_data_record.pot_rec_index, 1)
        self.assertEqual(session_data_record.region_end, 2500)
        self.assertEqual(session_data_record.region_start, 500)
        self.assertNotEqual(session_data_record.plot_div, None)
        self.assertEqual(session_data_record.window_shift, 50)
        self.assertEqual(session_data_record.window_size, 100)
        self.assertEqual(session_data_record.dist_method, 'jcd')
        self.assertEqual(session_data_record.alignment_with_key, 'hiv' '_' + self.client.session.session_key + '.fasta')

    



        




        
        


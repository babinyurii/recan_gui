from django.test import TestCase
from django.urls import reverse
from app_recan_gui.models import SessionData
 

class SessionDataTest(TestCase):

    def make_session(self):
        session = self.client.session
        session.save()
        return session

    def test_alignment_len_max_len_value(self):
        s = self.make_session()
        session_data = SessionData.objects.get(session_key_id=s.session_key)
        max_length = session_data._meta.get_field('alignment').max_length
        self.assertEqual(max_length, 100)

    def test_alignment_with_key_len_value(self):
        s = self.make_session()
        session_data = SessionData.objects.get(session_key_id=s.session_key)
        max_len = session_data._meta.get_field('alignment_with_key').max_length
        self.assertEqual(max_len, 132)

    def test_default_region_start_value(self):
        s = self.make_session()
        session_data = SessionData.objects.get(session_key_id=s.session_key)
        region_start = session_data._meta.get_field('region_start').default
        self.assertEqual(region_start, 0)

    def test_pot_rec_id_max_len_value(self):
        s = self.make_session()
        session_data = SessionData.objects.get(session_key_id=s.session_key)
        pot_rec_id_max_len = session_data._meta.get_field('pot_rec_id').max_length
        self.assertEqual(pot_rec_id_max_len, 100)

    def test_pot_rec_index_default_value(self):
        s = self.make_session()
        session_data = SessionData.objects.get(session_key_id=s.session_key)
        pot_rec_id_max_len = session_data._meta.get_field('pot_rec_index').default
        self.assertEqual(pot_rec_id_max_len, 0)

    def test_default_window_size_value(self):
        s = self.make_session()
        session_data = SessionData.objects.get(session_key_id=s.session_key)
        window_size_def = session_data._meta.get_field('window_size').default
        self.assertEqual(window_size_def, 50)

    def test_default_window_shift_value(self):
        s = self.make_session()
        session_data = SessionData.objects.get(session_key_id=s.session_key)
        window_size_def = session_data._meta.get_field('window_shift').default
        self.assertEqual(window_size_def, 25)

    def test_plot_div_default_value(self):
        s = self.make_session()
        session_data = SessionData.objects.get(session_key_id=s.session_key)
        plot_div_def = session_data._meta.get_field('plot_div').default
        self.assertEqual(plot_div_def, "")

    def test_dist_method_default_value(self):
        s = self.make_session()
        session_data = SessionData.objects.get(session_key_id=s.session_key)
        dist_method_def = session_data._meta.get_field('dist_method').default
        self.assertEqual(dist_method_def, 'pdist')

    def test_dist_method_max_len_value(self):
        s = self.make_session()
        session_data = SessionData.objects.get(session_key_id=s.session_key)
        dist_method_max_len = session_data._meta.get_field('dist_method').max_length
        self.assertEqual(dist_method_max_len, 5)

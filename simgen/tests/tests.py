from Bio import AlignIO
from simgen.calc_pairwise_distance import p_distance, estimate_nucleotide_frequencies
from simgen.rolling_window import RollingWindowOnAlignment
import unittest
import os


INPUT_FILE_P_DIST = os.path.join(os.path.dirname(__file__), './fasta_files/test_p_dist.fasta')
INPUT_FILE_NUC_FREQ = os.path.join(os.path.dirname(__file__), './fasta_files/test_nuc_freq.fasta')
INPUT_FILE_HBV_C_Bj_Ba = os.path.join(os.path.dirname(__file__), './fasta_files/hbv_C_Bj_Ba.fasta')


class SimgenTest(unittest.TestCase):

    def test_p_distance(self):
        
        align = AlignIO.read(INPUT_FILE_P_DIST, "fasta")
        """
        >s1_ref
        ATGCATGCAT
        >s2_dist_0
        ATGCATGCAT
        >s3_dist_10
        TTGCATGCAT
        >s4_dist_50
        GGCGGTGCAT
        >s5_dist_90
        GGCGGGGGGG
        >s5_dist_100
        GGCGGGCGGG
        """
        ref_seq = align[0]
        seq_0 = align[1]
        seq_10 = align[2]
        seq_50 = align[3]
        seq_90 = align[4]
        seq_100 = align[5]
        
        self.assertEqual(p_distance(ref_seq, seq_0), 0.0)
        self.assertEqual(p_distance(ref_seq, seq_10), 0.1)
        self.assertEqual(p_distance(ref_seq, seq_50), 0.5)
        self.assertEqual(p_distance(ref_seq, seq_90), 0.9)
        self.assertEqual(p_distance(ref_seq, seq_100), 1.0)
        

    def test_estimate_nuc_frequency(self):
        align = AlignIO.read(INPUT_FILE_NUC_FREQ, "fasta")
        
        """ sequences in the file 'test_nuc_freq.fastq":
        >s1_A_10
        ATGCCTGCTT
        >s2_G_50
        AGCGTGCGTG
        >s3_C_90
        CCCCACCCCC
        >s4_T_30
        TAGCTAGCTA
        >s5_A_0
        TGCTTGCTTG
        >s5_G_100
        GGGGGGGGGG
        """
        # return [ x / length for x in [A, C ,G, T] ]
        
        # seq to get Seq obj out of SeqRecord obj
        self.assertEqual(estimate_nucleotide_frequencies(align[0].seq)[0], 0.1)
        self.assertEqual(estimate_nucleotide_frequencies(align[1].seq)[2], 0.5)
        self.assertEqual(estimate_nucleotide_frequencies(align[2].seq)[1], 0.9)
        self.assertEqual(estimate_nucleotide_frequencies(align[3].seq)[3], 0.3)
        self.assertEqual(estimate_nucleotide_frequencies(align[4].seq)[0], 0.0)
        self.assertEqual(estimate_nucleotide_frequencies(align[5].seq)[2], 1.0)
        

    def test_sliced_alignment_slices_on_whole_alignment(self):
        
        align = RollingWindowOnAlignment(INPUT_FILE_HBV_C_Bj_Ba)
        sliced_align = align.roll_window_along_alignment(window_len=500, window_step=500)
        self.assertEqual(len(sliced_align), 7)     
        sliced_align = align.roll_window_along_alignment(window_len=1000, window_step=500)
        self.assertEqual(len(sliced_align), 7)    
        sliced_align = align.roll_window_along_alignment(window_len=1, window_step=1)
        self.assertEqual(len(sliced_align), 3215)    
        sliced_align = align.roll_window_along_alignment(window_len=3215, window_step=3215)
        self.assertEqual(len(sliced_align), 1)
        

    def test_sliced_alignment_slices_on_alignment_region(self):
        
        align = RollingWindowOnAlignment(INPUT_FILE_HBV_C_Bj_Ba)    
        sliced_align = align.roll_window_along_alignment_region(window_len=500, window_step=500, region=(0, 1000))
        self.assertEqual(len(sliced_align), 2)
        sliced_align = align.roll_window_along_alignment_region(window_len=500, window_step=250, region=(0, 1000))
        self.assertEqual(len(sliced_align), 4)
        sliced_align = align.roll_window_along_alignment_region(window_len=500, window_step=250, region=(0, 3215))
        self.assertEqual(len(sliced_align), 13)
        
        
    def test_sliced_alignment_window_borders_whole_alignment(self):
        
        align = RollingWindowOnAlignment(INPUT_FILE_HBV_C_Bj_Ba)
        sliced_align = align.roll_window_along_alignment(window_len=500, window_step=500)
        check_window_coords = [[0, 500], [500, 1000], [1000, 1500], [1500, 2000],
                        [2000, 2500], [2500, 3000], [3000, 3215]]
        
        counter = 0
        for window_coords in sliced_align.keys():
            self.assertEqual(window_coords[0], check_window_coords[counter][0])
            self.assertEqual(window_coords[1], check_window_coords[counter][1])
            counter += 1
            

    
    def test_sliced_alignment_window_borders_alignment_region(self):
        
        align = RollingWindowOnAlignment(INPUT_FILE_HBV_C_Bj_Ba)
        sliced_align = align.roll_window_along_alignment_region(window_len=500, window_step=250, region=(0, 1000))
        check_window_coords = [[0, 500], [250, 750], [500, 1000], [750, 1000]]
        
        counter = 0
        for window_coords in sliced_align.keys():   
            self.assertEqual(window_coords[0], check_window_coords[counter][0])
            self.assertEqual(window_coords[1], check_window_coords[counter][1])
            counter += 1
            
       
    
    
    
    
    
    
    


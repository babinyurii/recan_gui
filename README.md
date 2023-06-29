# recan_gui
Recan_gui is a Django-based web version of recan. It allows to analyze recombination events in viral genomes using genetic distance plotting. The tool is currently available at http://yuriyb.pythonanywhere.com.
# Guide
## Input files
Input files should be multiple sequence alignments in fasta format (with extenstions: `fasta`, `fas` or `fa`).
To upload an alignment click: `choose file` button and then `upload your alignment` button. After alignment is uploaded, the list of sequences it contains will appear on the left. 

## Distance plot settings
- `potential recombinant`. It's chosen from the list of sequences. All the distances will be plotted relatively to this sequence.
- `window size`. Sliding window size in nucleotides. It determines the 'sequence slice' which we take to calculate genetic distance.
- `window shift`. Sliding window shift in nucleotides. It determines how fast we move the window along the array of sequences. It must be less than window size. The smaller is the shift the more detailed is the plot. 
- `region start` and `region end`. If you need to examine a particular genomic region more closely, you can adjust these values. Window will roll along the alignment from `region start` to `region end`. In this case only data from the given region will be plotted. 
When you're happy with your settings hit `plot` button.

## Plot configuration
When the plot is constructed, hover your mouse over the top-right corner of the plot, and the plot control menu will appear. It allows to drag, resize and download the screenshot. The sequences with their color traces are shown above the plot. You can click on any them to hide or show it. You can also double click on any sequnce legend to isolate the single trace or return all the traces to the plot.   

## Example datasets
If you didn't use the distance method for virus recombination study before, you can download example datasets and play with them first. Each dataset contains sequences of a particular virus (HBV, HIB, HCV, LSDV, norovirus). Among the other sequences there is a recombinant virus and its major and minor parents in these alignments (except for the file hbv_C_Bj_Ba.fasta, it contains only recombinant and its parents). Minor parents have 'min' ending in their sequence name. Major parents have 'maj' ending. Recombinant sequences are designated with 'rec' ending. All the recombinant viruses included in the articles are described in the articles (see references below). 



## References
1. Hepatitis B Virus of Genotype B with or without Recombination with Genotype C over the Precore Region plus the Core Gene. Fuminaka Sugauchi et al. JOURNAL OF VIROLOGY, June 2002, p. 5985–5992. 10.1128/JVI.76.12.5985-5992.2002 https://jvi.asm.org/content/76/12/5985
2. Sprygin A, Babin Y, Pestova Y, Kononova S, Wallace DB, Van Schalkwyk A, et al. (2018) Analysis and insights into recombination signals in lumpy skin disease virus recovered in the field. PLoS ONE 13(12): e0207480. https://doi.org/ 10.1371/journal.pone.0207480
3. Liitsola, K., Holm K., Bobkov, A., Pokrovsky, V., Smolskaya,T., Leinikki,P., Osmanov,S. and Salminen,M. (2000) An AB recombinant and its parental HIV type 1 strains in the area of the former Soviet Union: low requirements for sequence identity in recombination. UNAIDS Virus Isolation Network. AIDS Res. Hum. Retroviruses, 16, 1047–1053.
4. Smith, D. B., Bukh, J., Kuiken, C., Muerhoff, A. S., Rice, C. M., Stapleton, J. T., & Simmonds, P. (2014). Expanded classification of hepatitis C virus into 7 genotypes and 67 subtypes: Updated criteria and genotype assignment web resource. Hepatology, 59(1), 318–327. https://doi.org/10.1002/hep.26744
5. Jiang,X., Espul,C., Zhong,W.M., Cuello,H. and Matson,D.O. (1999) Characterization of a novel human calicivirus that may be a naturally occurring recombinant. Arch. Virol., 144, 2377–2387







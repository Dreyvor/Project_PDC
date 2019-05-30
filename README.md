# Project_PDC

We implemented a 2-PAM.

As a basis we used an addition of 4 root-raised-cosine, with parameters B=1/2 and T=1/600, modulated at 2kHz, 4kHz, 6kHz and 8kHz respectively. The length of the basis is 133 samples.

A character will first be encoded into its ascii representation. Then we used the following map : 1 -> -1, 0 -> 1. So a character will be represented by a serie of {+-1} and for each of these representation, we will multiply its value by our basis to construct a waveform. We use 8 bits/symbol, so a symbol is represented by 8 * 133 = 1064 samples -> 1064 samples/symbol.

For symbol synchronization, we added at the beginning and at the end of the encoded sequence, already in passband, 2 different random sequences of {+-1}. These two sequences have the same length as the basis (133 samples).

To decode, we first compute an estimation of the parameters, check that the returned length is a multiple of our samples per symbol (here 1064). If not, we choose the closest multiple of 1064. Then we decode using the following decision rule : if the decoded value is greater than 0 we choose 1, else we choose -1. And then go back to ascii and find the corresponding character.

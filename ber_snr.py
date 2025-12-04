import numpy as np
import matplotlib.pyplot as plt
from core import canal_awgn, mod_bpsk, mod_qam, encode_differential, encode_manchester, calc_ber, decode_differential, decode_manchester, demod_bpsk, demod_qam 

def executar_simulacao_grafica():    
    n_bits = 50000 
    bits_tx = np.random.randint(0, 2, n_bits)
    snr_range = np.arange(-4, 14, 1)    

    ber_diff_bpsk, ber_diff_qam = [], []
    ber_manch_bpsk, ber_manch_qam = [], []

    for snr in snr_range:
        # 1°: Diferencial + BPSK
        rx = canal_awgn(mod_bpsk(encode_differential(bits_tx)), snr)
        ber_diff_bpsk.append(calc_ber(bits_tx, decode_differential(demod_bpsk(rx))))
        
        # 2°: Diferencial + QAM
        rx = canal_awgn(mod_qam(encode_differential(bits_tx)), snr)
        ber_diff_qam.append(calc_ber(bits_tx, decode_differential(demod_qam(rx))))
        
        # 3°: Manchester + BPSK
        rx = canal_awgn(mod_bpsk(encode_manchester(bits_tx)), snr)
        ber_manch_bpsk.append(calc_ber(bits_tx, decode_manchester(demod_bpsk(rx))))
        
        # 4°: Manchester + QAM
        # Aqui, QAM reduz pela metade e Manchester dobra. Tamanho de símbolo = tamanho original.
        rx = canal_awgn(mod_qam(encode_manchester(bits_tx)), snr)
        ber_manch_qam.append(calc_ber(bits_tx, decode_manchester(demod_qam(rx))))

    # Plotagem dos gráficos
    plt.figure(figsize=(10, 8))
    plt.semilogy(snr_range, ber_diff_bpsk, 'b-o', label='Diferencial + BPSK')
    plt.semilogy(snr_range, ber_diff_qam,  'r-s', label='Diferencial + 4-QAM')
    plt.semilogy(snr_range, ber_manch_bpsk, 'c--^', label='Manchester + BPSK')
    plt.semilogy(snr_range, ber_manch_qam,  'm--v', label='Manchester + 4-QAM')
    
    plt.title('Performance cruzada: codificação de linha + modulação')
    plt.xlabel('SNR (dB)'); plt.ylabel('BER')
    plt.legend(); plt.grid(True, which='both', alpha=0.4)
    plt.ylim(1e-5, 1)
    plt.show()
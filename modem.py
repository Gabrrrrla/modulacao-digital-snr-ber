import numpy as np

class DigitalModulator:
    """
    Responsável pela modulação (bits -> símbolos), simulação do canal (ruído)
    e demodulação (símbolos -> bits).
    """

    @staticmethod
    def modulate(bits, scheme='BPSK'):
        """
        Mapeia bits (0, 1) para símbolos complexos.
        """
        if scheme == 'BPSK':
            # 0 -> -1, 1 -> +1
            return 2 * bits.astype(float) - 1

        elif scheme == 'QPSK':
            # Garante número par de bits (padding)
            padded_bits = bits.copy()
            if len(bits) % 2 != 0:
                padded_bits = np.append(bits, 0)
            
            # Agrupa bits em pares: (I, Q)
            bits_reshaped = padded_bits.reshape(-1, 2)

            i_comp = 2 * bits_reshaped[:, 0].astype(float) - 1
            q_comp = 2 * bits_reshaped[:, 1].astype(float) - 1
            
            # Normalização
            return (i_comp + 1j * q_comp) / np.sqrt(2)
        
        else:
            raise ValueError(f"Esquema {scheme} não implementado.")

    @staticmethod
    def add_awgn_noise(symbols, snr_db):
        """
        Adiciona ruído gaussiano branco (AWGN) ao sinal com base na SNR desejada.
        """
        # Potência do sinal (assumindo normalização unitária na modulação)
        sig_power = 1.0
        
        # Conversão dB para linear: SNR = 10 * log10(Ps/Pn) -> Pn = Ps / 10^(SNR/10)
        noise_power = sig_power / (10 ** (snr_db / 10))
        
        # O ruído complexo divide a potência entre parte Real e Imag
        noise_std = np.sqrt(noise_power / 2)
        
        noise = (np.random.normal(0, noise_std, symbols.shape) + 
                 1j * np.random.normal(0, noise_std, symbols.shape))
        
        return symbols + noise

    @staticmethod
    def demodulate(received_symbols, scheme='BPSK', original_length=None):
        """
        Decide qual bit foi enviado baseado no símbolo ruidoso recebido.
        """
        if scheme == 'BPSK':
            # Se Real > 0 -> 1, senão -> 0
            decisions = (received_symbols.real > 0).astype(np.uint8)
            return decisions

        elif scheme == 'QPSK':
            # Analisa parte Real e Imaginária separadamente
            # Normalização não afeta o sinal (apenas a magnitude), o sinal basta
            bits_i = (received_symbols.real > 0).astype(np.uint8)
            bits_q = (received_symbols.imag > 0).astype(np.uint8)
            
            # Intercala os bits de volta: [i0, q0, i1, q1...]
            demodulated = np.column_stack((bits_i, bits_q)).flatten()
            
            # Corta padding se necessário (simples)
            if original_length and len(demodulated) > original_length:
                demodulated = demodulated[:original_length]
            
            return demodulated
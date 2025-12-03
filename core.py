import numpy as np
import matplotlib.pyplot as plt

def texto_para_bits(texto):
    """Converte string ASCII para array de bits."""
    bits = []
    for char in texto:
        bin_val = bin(ord(char))[2:].zfill(8)
        bits.extend([int(b) for b in bin_val])
    return np.array(bits)

def bits_para_texto(bits):
    """Converte array de bits para string ASCII."""
    chars = []
    for b in range(0, len(bits), 8):
        byte = bits[b:b+8]
        if len(byte) == 8:
            s_byte = ''.join(str(x) for x in byte)
            try:
                chars.append(chr(int(s_byte, 2)))
            except:
                chars.append('?') # Caractere inválido se houver muito erro
    return "".join(chars)

# --- 1.2 Codificadores de Linha ---
def encode_differential(bits):
    """NRZ-I: Inverte estado se 1, mantem se 0."""
    encoded = []
    state = 0
    for b in bits:
        if b == 1: state = 1 - state
        encoded.append(state)
    return np.array(encoded)

def decode_differential(bits):
    decoded = []
    last_state = 0
    for b in bits:
        decoded.append(1 if b != last_state else 0)
        last_state = b
    return np.array(decoded)

def encode_manchester(bits):
    """0 -> [0, 1], 1 -> [1, 0]"""
    encoded = []
    for b in bits:
        encoded.extend([0, 1] if b == 0 else [1, 0])
    return np.array(encoded)

def decode_manchester(bits):
    decoded = []
    for i in range(0, len(bits), 2):
        pair = bits[i:i+2]
        if np.array_equal(pair, [0, 1]): decoded.append(0)
        elif np.array_equal(pair, [1, 0]): decoded.append(1)
        else: decoded.append(0) # Erro de violação
    return np.array(decoded)

# --- 1.3 Moduladores Digitais ---
def mod_bpsk(bits):
    return 2 * bits - 1

def demod_bpsk(sinal):
    return (sinal.real > 0).astype(int)

def mod_qam(bits):
    if len(bits) % 2 != 0: bits = np.append(bits, 0) # Padding
    symbols = []
    for i in range(0, len(bits), 2):
        r = 1 if bits[i] == 0 else -1
        i_comp = 1 if bits[i+1] == 0 else -1
        symbols.append(r + 1j*i_comp)
    return np.array(symbols) / np.sqrt(2)

def demod_qam(sinal):
    bits = []
    sinal = sinal * np.sqrt(2)
    for s in sinal:
        bits.append(0 if s.real > 0 else 1)
        bits.append(0 if s.imag > 0 else 1)
    return np.array(bits)

# --- 1.4 Canal (Ruído) e Métricas ---
def canal_awgn(sinal, snr_db):
    potencia_sinal = np.mean(np.abs(sinal)**2)
    snr_lin = 10**(snr_db/10)
    potencia_ruido = potencia_sinal / snr_lin
    
    if np.iscomplexobj(sinal):
        noise = (np.random.normal(0, np.sqrt(potencia_ruido/2), sinal.shape) + 
                 1j*np.random.normal(0, np.sqrt(potencia_ruido/2), sinal.shape))
    else:
        noise = np.random.normal(0, np.sqrt(potencia_ruido), sinal.shape)
    return sinal + noise

def calc_ber(orig, rec):
    L = min(len(orig), len(rec))
    return np.sum(orig[:L] != rec[:L]) / L
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc

# ==========================================
# 1. FUNÇÕES DE UTILIDADE (ASCII <-> BIN)
# ==========================================

def text_to_bits(text):
    """Converte string ASCII para lista de bits."""
    bits = []
    for char in text:
        # Converte char para binário de 8 bits
        bin_val = bin(ord(char))[2:].zfill(8)
        bits.extend([int(b) for b in bin_val])
    return np.array(bits)

def bits_to_text(bits):
    """Converte lista de bits para string ASCII."""
    chars = []
    # Processa blocos de 8 bits
    for b in range(0, len(bits), 8):
        byte = bits[b:b+8]
        if len(byte) == 8: # Garante byte completo
            s_byte = ''.join(str(x) for x in byte)
            chars.append(chr(int(s_byte, 2)))
    return "".join(chars)

# ==========================================
# 2. CODIFICAÇÃO DE LINHA (Visualização)
# ==========================================

def line_code_manchester(bits):
    """Codificação Manchester: 0 -> [1, -1], 1 -> [-1, 1]"""
    signal = []
    for b in bits:
        if b == 0:
            signal.extend([1, -1])
        else:
            signal.extend([-1, 1])
    return np.array(signal)

def line_code_ami(bits):
    """Codificação AMI Bipolar: 0 -> 0, 1 -> Alterna +1/-1"""
    signal = []
    last_voltage = -1 # Começa assumindo que o anterior foi -1 para o primeiro ser +1
    for b in bits:
        if b == 0:
            signal.append(0)
        else:
            last_voltage *= -1
            signal.append(last_voltage)
    return np.array(signal)

# ==========================================
# 3. MODULAÇÃO DIGITAL E CANAL
# ==========================================

def modulate_bpsk(bits):
    """BPSK: 0 -> -1, 1 -> +1"""
    return 2 * bits - 1

def demodulate_bpsk(symbols):
    """Decisor BPSK simples"""
    return (symbols.real > 0).astype(int)

def modulate_4qam(bits):
    """4-QAM (similar a QPSK): Mapeia 2 bits por símbolo"""
    # Garante que o número de bits é par
    if len(bits) % 2 != 0:
        bits = np.append(bits, 0)
    
    symbols = []
    for i in range(0, len(bits), 2):
        # Mapeamento Gray simples
        # 00 -> -1-1j, 01 -> -1+1j, 10 -> 1-1j, 11 -> 1+1j
        real = 1 if bits[i] == 1 else -1
        imag = 1 if bits[i+1] == 1 else -1
        symbols.append(real + 1j*imag)
    
    # Normaliza a energia média para 1
    return np.array(symbols) / np.sqrt(2)

def demodulate_4qam(symbols):
    """Demodulador 4-QAM"""
    bits = []
    # Desnormaliza
    symbols = symbols * np.sqrt(2)
    for s in symbols:
        b1 = 1 if s.real > 0 else 0
        b2 = 1 if s.imag > 0 else 0
        bits.extend([b1, b2])
    return np.array(bits)

def add_awgn_noise(signal, snr_db):
    """Adiciona ruído Gaussiano Branco (AWGN) baseado na SNR em dB"""
    # Potência do sinal
    sig_power = np.mean(np.abs(signal)**2)
    
    # Converte SNR dB para linear
    snr_linear = 10**(snr_db / 10.0)
    
    # Potência do ruído requerida
    noise_power = sig_power / snr_linear
    
    # Gera ruído complexo se o sinal for complexo, real se for real
    if np.iscomplexobj(signal):
        noise = (np.random.normal(0, np.sqrt(noise_power/2), signal.shape) + 
                 1j*np.random.normal(0, np.sqrt(noise_power/2), signal.shape))
    else:
        noise = np.random.normal(0, np.sqrt(noise_power), signal.shape)
        
    return signal + noise

def calculate_ber(sent, received):
    # Ajusta comprimentos caso haja padding
    length = min(len(sent), len(received))
    errors = np.sum(sent[:length] != received[:length])
    return errors / length

# ==========================================
# 4. EXECUÇÃO PRINCIPAL
# ==========================================

# --- CONFIGURAÇÃO ---
mensagem_texto = "Engenharia"
snr_range = np.arange(-5, 12, 1) # De -5dB a 12dB

print(f"--- Sistema de Comunicação Digital ---")
print(f"Mensagem Original: {mensagem_texto}")

# 1. Conversão para Binário
bits_msg = text_to_bits(mensagem_texto)
print(f"Bits Totais: {len(bits_msg)}")
print(f"Primeiros 16 bits: {bits_msg[:16]}...")

# 2. Visualização de Codificação de Linha (Apenas um trecho)
trecho_bits = bits_msg[:16] # Pega 2 bytes para visualizar
sinal_ami = line_code_ami(trecho_bits)
sinal_manchester = line_code_manchester(trecho_bits)

plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.title("Codificação de Linha: AMI Bipolar")
plt.step(range(len(sinal_ami)), sinal_ami, where='post', color='blue', linewidth=2)
plt.grid(True); plt.ylim(-1.5, 1.5)

plt.subplot(2, 1, 2)
plt.title("Codificação de Linha: Manchester")
# Manchester tem 2x mais amostras, ajustamos o eixo X
plt.step(np.linspace(0, len(trecho_bits), len(sinal_manchester)), sinal_manchester, where='post', color='green', linewidth=2)
plt.grid(True); plt.ylim(-1.5, 1.5)
plt.tight_layout()
plt.show()

# 3. Simulação de BER vs SNR (Modulação Digital)
print("\nIniciando Simulação de BER (Monte Carlo)...")

ber_bpsk = []
ber_qam = []

# Geramos muitos bits aleatórios para ter uma curva BER suave (Monte Carlo)
# Usar apenas a mensagem curta "Engenharia" daria curvas "quadradas"
bits_simulacao = np.random.randint(0, 2, 100000) 

for snr in snr_range:
    # --- BPSK ---
    tx_bpsk = modulate_bpsk(bits_simulacao)
    rx_bpsk = add_awgn_noise(tx_bpsk, snr)
    bits_rx_bpsk = demodulate_bpsk(rx_bpsk)
    ber_bpsk.append(calculate_ber(bits_simulacao, bits_rx_bpsk))
    
    # --- 4-QAM ---
    tx_qam = modulate_4qam(bits_simulacao)
    rx_qam = add_awgn_noise(tx_qam, snr)
    bits_rx_qam = demodulate_4qam(rx_qam)
    ber_qam.append(calculate_ber(bits_simulacao, bits_rx_qam))

# 4. Plotagem BER vs SNR
plt.figure(figsize=(10, 6))
plt.semilogy(snr_range, ber_bpsk, 'b-o', label='BPSK')
plt.semilogy(snr_range, ber_qam, 'r-s', label='4-QAM (QPSK)')

# Teórico BPSK/QPSK (aproximação para comparação)
# Pb = 0.5 * erfc(sqrt(Eb/N0)) -> Eb/N0 linear aprox SNR linear

snr_lin = 10**(snr_range/10)
ber_theory = 0.5 * erfc(np.sqrt(snr_lin))
plt.semilogy(snr_range, ber_theory, 'k--', label='Teórico BPSK/QPSK', alpha=0.5)

plt.title('Desempenho BER vs SNR (Canal AWGN)')
plt.xlabel('SNR (dB)')
plt.ylabel('Taxa de Erro de Bit (BER)')
plt.grid(True, which="both", ls="-")
plt.legend()
plt.ylim(0.00001, 1)
plt.show()

# 5. Demonstração de Decodificação (Exemplo com SNR alto)
print("\n--- Teste de Recuperação da Mensagem (SNR = 10dB) ---")
# Usando BPSK no texto original
tx_demo = modulate_bpsk(bits_msg)
rx_demo = add_awgn_noise(tx_demo, 10) # Baixo ruído
bits_recuperados = demodulate_bpsk(rx_demo)
texto_final = bits_to_text(bits_recuperados)

print(f"Texto Enviado:    {mensagem_texto}")
print(f"Texto Recuperado: {texto_final}")
erros = calculate_ber(bits_msg, bits_recuperados)
print(f"BER na mensagem:  {erros:.4f}")
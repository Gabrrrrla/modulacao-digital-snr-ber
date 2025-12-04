import numpy as np
import matplotlib.pyplot as plt
from core import bits_para_texto, calc_ber, canal_awgn, texto_para_bits, encode_differential, mod_bpsk, demod_bpsk, decode_differential, mod_qam, demod_qam, encode_manchester, decode_manchester
from ber_snr import executar_simulacao_grafica

def plotar_cenario(ax_const, ax_time, tx_sinal, rx_sinal, nome, ber):
    """Função auxiliar para desenhar os gráficos de cada linha"""
    
    # --- GRÁFICO 1: Constelação  ---
    # Mostra todos os pontos recebidos no plano complexo
    ax_const.scatter(rx_sinal.real, rx_sinal.imag, color='red', alpha=0.5, s=10, label='Rx (Ruidoso)')
    # Mostra os pontos ideais (Tx) apenas para referência (primeiros 50 para não poluir)
    ax_const.scatter(tx_sinal.real[:50], tx_sinal.imag[:50], color='blue', marker='x', s=30, label='Tx (Ideal)')
    
    ax_const.set_title(f"{nome} | BER: {ber:.4f}", fontsize=10, fontweight='bold')
    ax_const.set_xlabel("In-Phase (I)")
    ax_const.set_ylabel("Quadrature (Q)")
    ax_const.grid(True, alpha=0.3)
    ax_const.axhline(0, color='black', lw=0.5)
    ax_const.axvline(0, color='black', lw=0.5)
    # Limita o zoom para focar na constelação padrão
    ax_const.set_xlim(-2.5, 2.5); ax_const.set_ylim(-2.5, 2.5)

    # --- GRÁFICO 2: Domínio do tempo (apenas um trecho) ---
    # Mostra apenas os primeiros 40 símbolos para ficar legível
    zoom = 40
    if len(tx_sinal) < zoom: zoom = len(tx_sinal)
    
    # Plotamos apenas a parte real para simplificar visualização 2D
    ax_time.plot(rx_sinal.real[:zoom], 'r-', alpha=0.6, label='Rx Real')
    ax_time.step(range(zoom), tx_sinal.real[:zoom], 'b--', where='mid', alpha=0.4, label='Tx Real')
    
    ax_time.set_title("Forma de onda (parte real - zoom)", fontsize=9)
    ax_time.grid(True, alpha=0.3)
    ax_time.set_ylim(-2.5, 2.5)

def processar_e_plotar(nome, bits_in, func_cod, func_mod, func_demod, func_decod, snr, axes_row):
    """Executa a cadeia completa e chama a função de plotagem"""
    
    # 1. Processamento
    cod = func_cod(bits_in)          # Codificação de linha
    tx_sinal = func_mod(cod)         # Modulação
    rx_sinal = canal_awgn(tx_sinal, snr) # Canal
    demod = func_demod(rx_sinal)     # Demodulação
    bits_out = func_decod(demod)     # Decodificação de linha
    
    # 2. Métricas
    L = min(len(bits_in), len(bits_out))
    ber = calc_ber(bits_in, bits_out[:L])
    texto_rec = bits_para_texto(bits_out[:L])
    
    # 3. Print no console
    print(f"[{nome}]")
    print(f"   -> BER: {ber:.4f}")
    print(f"   -> Texto: {texto_rec}")
    
    # 4. Plotagem nos eixos passados
    # axes_row[0] é a Constelação, axes_row[1] é o Tempo
    plotar_cenario(axes_row[0], axes_row[1], tx_sinal, rx_sinal, nome, ber)


def executar_teste_usuario():
    print("\n--- TESTE INTERATIVO COM GRÁFICOS ---")
    texto = input("Digite a frase para transmitir: ")
    try:
        snr_input = input("Digite o nível de SNR em dB (ex: 5 para ruim, 12 para bom): ")
        snr = float(snr_input)
    except ValueError:
        print("SNR inválido. Usando padrão 10dB.")
        snr = 10.0

    bits_originais = texto_para_bits(texto)
    print(f"\nTexto original: '{texto}' | SNR: {snr}dB")
    print("-" * 60)

    # Configura a figura (4 linhas, 2 colunas)
    fig, axs = plt.subplots(4, 2, figsize=(12, 16))
    plt.subplots_adjust(hspace=0.4)
    fig.suptitle(f"Análise de Sinais: Entrada '{texto}' @ SNR {snr}dB", fontsize=16)

    # --- CENÁRIO 1: Diferencial + BPSK ---
    processar_e_plotar("1. Diferencial + BPSK", bits_originais, 
                       encode_differential, mod_bpsk, demod_bpsk, decode_differential, snr, axs[0])
    
    # --- CENÁRIO 2: Diferencial + 4-QAM ---
    processar_e_plotar("2. Diferencial + 4-QAM", bits_originais, 
                       encode_differential, mod_qam, demod_qam, decode_differential, snr, axs[1])
    
    # --- CENÁRIO 3: Manchester + BPSK ---
    processar_e_plotar("3. Manchester + BPSK", bits_originais, 
                       encode_manchester, mod_bpsk, demod_bpsk, decode_manchester, snr, axs[2])
    
    # --- CENÁRIO 4: Manchester + 4-QAM ---
    processar_e_plotar("4. Manchester + 4-QAM", bits_originais, 
                       encode_manchester, mod_qam, demod_qam, decode_manchester, snr, axs[3])

    print("-" * 60)
    print("Gerando gráficos")
    plt.show()

if __name__ == "__main__":
    while True:
        print("\n=== SISTEMA DE COMUNICAÇÃO DIGITAL ===")
        print("1. Gerar gráfico de desempenho global")
        print("2. Testar frase (com gráficos de sinal)")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            executar_simulacao_grafica()
        elif opcao == '2':
            executar_teste_usuario()
        elif opcao == '0':
            break
        else:
            print("Opção inválida.")
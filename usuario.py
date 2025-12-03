import numpy as np
import matplotlib.pyplot as plt
from core import bits_para_texto, calc_ber, canal_awgn, texto_para_bits, encode_differential, mod_bpsk, demod_bpsk, decode_differential, mod_qam, demod_qam, encode_manchester, decode_manchester
from ber_snr import executar_simulacao_grafica

def processar_cadeia(nome, bits_in, func_cod, func_mod, func_demod, func_decod, snr):
    # 1. Codificação de linha
    cod = func_cod(bits_in)
    # 2. Modulação
    mod = func_mod(cod)
    # 3. Ruído
    rx_sinal = canal_awgn(mod, snr)
    # 4. Demodulação
    demod = func_demod(rx_sinal)
    # 5. Decodificação de linha
    bits_out = func_decod(demod)
    
    # Ajuste de tamanho e conversão para texto
    L = min(len(bits_in), len(bits_out))
    texto_rec = bits_para_texto(bits_out[:L])
    ber = calc_ber(bits_in, bits_out[:L])
    
    print(f"[{nome}]")
    print(f"   -> BER: {ber:.4f}")
    print(f"   -> Texto recebido: {texto_rec}\n")

def executar_teste_usuario():
    texto = input("Digite a frase a ser transmitida: ")
    try:
        snr = float(input("Digite o nível de SNR em dB (ex: 5 para ruído médio, 12 para limpo): "))
    except ValueError:
        print("SNR inválido. Usando padrão 10dB.")
        snr = 10.0

    bits_originais = texto_para_bits(texto)
    print(f"\nTexto original: '{texto}'")
    print(f"Total de bits: {len(bits_originais)}")
    print("-" * 50)

    # Executa as 4 combinações
    processar_cadeia("1°: Diferencial + BPSK", bits_originais, 
                     encode_differential, mod_bpsk, demod_bpsk, decode_differential, snr)
    
    processar_cadeia("2°: Diferencial + 4-QAM", bits_originais, 
                     encode_differential, mod_qam, demod_qam, decode_differential, snr)
    
    processar_cadeia("3°: Manchester + BPSK", bits_originais, 
                     encode_manchester, mod_bpsk, demod_bpsk, decode_manchester, snr)
    
    processar_cadeia("4°: Manchester + 4-QAM", bits_originais, 
                     encode_manchester, mod_qam, demod_qam, decode_manchester, snr)


if __name__ == "__main__":
    while True:
        print("1. Transmitir uma frase")
        print("2. Gerar gráficos")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            executar_teste_usuario()
        elif opcao == '2':
            executar_simulacao_grafica()
        elif opcao == '0':
            break
        else:
            print("Opção inválida.")
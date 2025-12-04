# Trabalho GB - Redes de Computadores: Internetworking, Roteamento e Transmissão

Este projeto implementa uma simulação completa de um sistema de comunicação digital em Python. 
A ideia é percorrer todas as etapas essenciais da camada física, como a codificação de linha até a modulação, transmissão em canal ruidoso (AWGN), demodulação e decodificação, para no fim analisarmos como diferentes técnicas se comportam diante do ruído.

Alunos: Gabriela Bley Rodrigues, Luisa Becker dos Santos e Pedro Lucas Erig Gerhardt.

Professor: Cristiano Bonato Both.

Ciências da Computação - UNISINOS

## 1. Funcionalidades

O simulador oferece duas formas de interação:
1.  **Simulação de gráfica:** Gera curvas de BER vs SNR para análise.
2.  **Transmissão de texto:** permite enviar mensagens reais e observar como o ruído afeta a recepção.

### Tecnologias Implementadas
* **Codificação de linha:**
    * *Diferencial (NRZ-I):* mudança de nível ocorre apenas quando o bit é 1.
    * *Manchester:* transição no meio do intervalo de bit, garantindo sincronismo de clock.
* **Modulação digital:**
    * *BPSK (Binary Phase Shift Keying):* fases opostas representam 0 e 1.
    * *4-QAM (Quadrature Amplitude Modulation):* símbolos em quadratura transmitindo 2 bits por vez.
* **Canal:**
    * *AWGN:* modelo clássico de ruído branco gaussiano aditivo.

---

## 2. Como executar

Certifique-se de ter o Python instalado e a biblioteca necessária:

```bash
  pip install numpy matplotlib
  python usuario.py
```
---

## 3. Testes
<img width="527" height="359" alt="image" src="https://github.com/user-attachments/assets/49133f81-a4ac-4fe2-a6c2-8b9af7e611b8" /> 

Acima estão os resultados práticos da transmissão da frase de teste.

Frase utilizada: "Trabalho de redes" - ruído limpo (SNR = 12dB)

* Nesse caso, todas as modulações conseguem reconstruir o texto corretamente.

---

<img width="537" height="366" alt="image" src="https://github.com/user-attachments/assets/578354f0-c1e2-437e-bebb-c7610bf12420" /> 

Acima estão os resultados práticos da transmissão da frase de teste.

Frase utilizada: "Trabalho de redes" - ruído médio (SNR = 5dB)

* Aqui, o impacto do ruído já é perceptível e a mensagem sofre degradações.

---

<img width="896" height="733" alt="image" src="https://github.com/user-attachments/assets/00e03d59-cf46-41dd-9530-36d77128b49e" /> 

Nesta seção, apresentamos a curva de desempenho BER vs SNR. O gráfico compara as 4 cadeias de transmissão implementadas.
O gráfico mostra o desempenho das quatro cadeias de transmissão. Para isso, geramos 50 mil bits aleatórios usando `np.random.randint(0, 2)`.
Isso garante uma sequência imprevisível (probabilidades iguais de 0 e 1) e evita vieses do padrão de dados. É importante usar muitos bits porque:
* Taxas de erro pequenas só aparecem com grandes volumes de dados;
* Com poucos bits, um único erro aleatório distorce o resultado.


### 1°: Manchester + BPSK
A combinação nos mostra uma boa performance de erro (curva de BER baixa), mas possui um custo significativo:
* O código Manchester dobra o número de bits (para garantir transição de clock).
* O BPSK modula 1 símbolo por bit.
* Esta combinação exige o dobro da frequência (largura de banda) comparada a um sistema BPSK puro sem codificação de linha.

### 2°: Manchester + 4-QAM
Aqui acontece um cancelamento matemático entre o codificador e o modulador, porque:
* Manchester dobra a taxa de bits.
* 4-QAM compacta os bits em pares, dividindo a taxa de símbolos por 2.

> **Análise:** Na prática, o aumento causado pela codificação é compensado pela eficiência espectral da modulação.
O resultado é uma taxa de símbolos igual à taxa original de bits, mantendo o sincronismo do Manchester sem estourar a banda.
>
### 3°: Diferencial vs. Manchester
Observando o gráfico, as técnicas com Manchester apresentam um deslocamento aproximado de 3 dB em relação à codificação diferencial. 
* Manchester usa duas transições por bit, ou seja, dobra a largura de banda.
* Isso dobra a largura de banda necessária. Ao dobrar a banda, o receptor acaba captando o dobro de ruído. Por fim, se perde eficiência energética.

Por outro lado, a codificação diferencial aparece como a mais eficiente energeticamente (mais à esquerda no gráfico), mas tem um ponto de atenção:
* O bit atual depende do estado anterior. Se o ruído causa erro em 1 bit, a referência para o próximo é perdida.
* Isso causa propagação de erro (1 erro de canal vira 2 erros no final).

---




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

<img width="1599" height="905" alt="image" src="https://github.com/user-attachments/assets/b2c82aea-3d12-4969-9f25-78bab8fe117b" />

#### 1. Diferencial + BPSK (BER: 0.0571)

Neste primeiro cenário, observamos uma taxa de erro de bit de aproximadamente 5,71%. O gráfico de constelação à esquerda exibe dois agrupamentos de símbolos (um positivo e um negativo), característicos da modulação binária. No entanto, devido ao SNR baixo (5dB), as "nuvens" de pontos vermelhos estão bastante dispersas, aproximando-se perigosamente da linha central de decisão. A alta taxa de erro, apesar da robustez natural do BPSK, deve-se principalmente à propagação de erro inerente ao codificador Diferencial: quando o ruído faz o receptor errar a detecção de uma fase, essa falha corrompe a referência para o próximo bit, resultando frequentemente em pares de erros consecutivos. No domínio do tempo (lado direito), nota-se que a onda recebida (linha vermelha) frequentemente não alcança a amplitude total esperada, flutuando em zonas de incerteza.

#### 2. Diferencial + 4-QAM (BER: 0.0643)

Este cenário apresentou o pior desempenho do conjunto, com uma taxa de erro de 6,43%. A análise do diagrama de constelação revela o motivo: ao utilizar 4-QAM, dividimos a energia do sinal em quatro quadrantes. Com a presença de ruído intenso, a distância de segurança entre os símbolos diminui drasticamente em comparação ao BPSK. Visualmente, vemos pontos vermelhos invadindo quadrantes vizinhos, o que significa que o receptor confundiu não apenas a fase, mas também a quadratura do sinal. Somando a fragilidade do QAM em baixa potência com a propagação de erros do codificador Diferencial, a integridade da mensagem "Trabalho de Redes..." foi severamente comprometida, resultando na maior perda de informação entre os testes.

#### 3. Manchester + BPSK (BER: 0.0250)

Aqui observamos um salto qualitativo significativo, com a taxa de erro caindo para 2,50% (menos da metade do cenário 1). O gráfico no domínio do tempo à direita revela a característica fundamental desta melhoria: a densidade de transições duplicou. O código Manchester utiliza dois "chips" de sinal para representar um único bit de informação. Isso confere ao sistema um ganho de processamento estatístico, pois o receptor tem mais "sinal" para integrar e tomar uma decisão. Mesmo sob o mesmo ruído de 5dB, a estrutura do Manchester permitiu filtrar melhor as incertezas, provando ser muito mais resiliente que a codificação Diferencial para proteger a transmissão.

#### 4. Manchester + 4-QAM (BER: 0.0179)

Surpreendentemente, este foi o cenário com o melhor desempenho nesta amostra específica, atingindo uma taxa de erro de apenas 1,79%. O gráfico de constelação mostra que, embora os pontos estejam dispersos como no cenário 2, a lógica de decodificação do Manchester conseguiu corrigir a maioria das ambiguidades. Este resultado ilustra um "trade-off" (compromisso) interessante de engenharia: ao combinar o Manchester (que dobra a largura de banda necessária) com o 4-QAM (que reduz a largura de banda pela metade), o sistema operou na mesma velocidade de transmissão efetiva do cenário 1, mas com uma robustez muito superior. O código conseguiu limpar os erros que a modulação QAM normalmente cometeria sozinha, preservando quase totalmente a integridade da string "Trabalho de Redes...".

---

<img width="896" height="733" alt="image" src="https://github.com/user-attachments/assets/00e03d59-cf46-41dd-9530-36d77128b49e" /> 

Nesta seção, apresentamos a curva de desempenho BER vs SNR. O gráfico compara as 4 cadeias de transmissão implementadas.
Para isso, geramos 50 mil bits aleatórios usando `np.random.randint(0, 2)`.
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

## Vídeo com Demonstração da Aplicação

https://github.com/user-attachments/assets/6f01c3ad-6a61-40ae-8f9f-e6d72920dfb9

import numpy as np
class Hamming74Codec:
    """
    Implementação vetorizada do Codec Hamming(7,4) Sistemático.
    """
    def __init__(self):
        # Definição da Matriz Geradora
        self.G = np.array([
            [1, 0, 0, 0, 0, 1, 1],
            [0, 1, 0, 0, 1, 0, 1],
            [0, 0, 1, 0, 1, 1, 0],
            [0, 0, 0, 1, 1, 1, 1],], 
            dtype=np.uint8)
        
        # Definição da Matriz de Verificação de Paridade
        self.H = np.array([
            [0, 1, 1, 1, 1, 0, 0],
            [1, 0, 1, 1, 0, 1, 0],
            [1, 1, 0, 1, 0, 0, 1]], 
            dtype=np.uint8)
        
        # Construção do mapa de síndromes para correção rápida
        self.syndrome_map = self._build_syndrome_map()

    def _build_syndrome_map(self):
        """
        Dicionário mapeando cada vetor de síndrome possível ao índice 
        do bit correspondente que contém o erro.
        """
        s_map = {}
        rows, cols = self.H.shape
        for i in range(cols):
            syndrome = tuple(self.H[:, i])
            s_map[syndrome] = i
        return s_map

    def encode(self, data_bits):
        """
        Codifica um fluxo de bits de dados usando Hamming(7,4).
        """
        n_k = 4 
        remainder = len(data_bits) % n_k
        if remainder!= 0:
            pad_len = n_k - remainder
            data_bits = np.append(data_bits, np.zeros(pad_len, dtype=np.uint8))

        n_blocks = len(data_bits) // n_k
        msg_matrix = data_bits.reshape((n_blocks, n_k))
        
        coded_matrix = np.dot(msg_matrix, self.G) % 2
        
        return coded_matrix.flatten().astype(np.uint8)

    def decode(self, received_bits):
        """
        Decodifica um fluxo de bits recebido, aplicando correção de erros baseada em síndrome.
        """
        n_n = 7 
        n_k = 4 
        
        if len(received_bits) % n_n!= 0:
            cutoff = len(received_bits) - (len(received_bits) % n_n)
            received_bits = received_bits[:cutoff]
            
        n_blocks = len(received_bits) // n_n
        rx_matrix = received_bits.reshape((n_blocks, n_n))
        
        syndromes = np.dot(rx_matrix, self.H.T) % 2
        
        corrected_matrix = rx_matrix.copy()
        
        for i, s in enumerate(syndromes):
            if np.any(s):
                s_tuple = tuple(s)
                if s_tuple in self.syndrome_map:
                    error_idx = self.syndrome_map[s_tuple]
                    corrected_matrix[i, error_idx] ^= 1
        
        decoded_data = corrected_matrix[:, :n_k]
        
        return decoded_data.flatten().astype(np.uint8)
import unittest
import numpy as np
from message_source import MessageSource
from bit_converter import BitConverter
from hamming_codec import Hamming74Codec
from modem import DigitalModulator


class TestCommunicationBlocks(unittest.TestCase):
    """
    Suíte de testes para validação unitária dos blocos de comunicação.
    """
    
    def setUp(self):
        """Configuração executada antes de cada teste."""
        self.source = MessageSource(source_type='fixed', fixed_message="Test")
        self.converter = BitConverter()
        self.codec = Hamming74Codec()

    def test_01_conversao_texto_bits_reversibilidade(self):
        """
        Valida se a conversão de texto para bits e de volta para texto é perfeita.
        """
        msg_original = "Engenharia 2025!"
        bits = self.converter.text_to_bits(msg_original)
        msg_recuperada = self.converter.bits_to_text(bits)
        
        self.assertEqual(msg_original, msg_recuperada, 
                         "Falha: O texto recuperado diverge do original.")
        self.assertEqual(len(bits), len(msg_original) * 8, 
                         "Falha: Número de bits incorreto para a string fornecida.")

    def test_02_validacao_matriz_geradora(self):
        """
        Verifica matematicamente se a codificação segue a matriz G definida.
        """
        input_nibble = np.array([1, 0, 1, 0], dtype=np.uint8)
        expected_code = np.array([1, 0, 1, 0, 1, 0, 1], dtype=np.uint8)
        
        encoded = self.codec.encode(input_nibble)
        
        np.testing.assert_array_equal(encoded, expected_code, 
                                      "Falha: A codificação não produziu o vetor esperado.")

    def test_03_capacidade_correcao_erro_unico(self):
        data = np.array([1, 0, 1, 0], dtype=np.uint8)
        encoded_ref = self.codec.encode(data) 
        
        decoded_clean = self.codec.decode(encoded_ref)
        np.testing.assert_array_equal(decoded_clean, data, "Falha na decodificação sem ruído.")
        
        for i in range(7):
            noisy_encoded = encoded_ref.copy()
            
            noisy_encoded[i] ^= 1 
            
            decoded_noisy = self.codec.decode(noisy_encoded)
            
            np.testing.assert_array_equal(decoded_noisy, data, 
                f"Falha Crítica: O codec não corrigiu um erro na posição de bit {i}.")

    def test_04_integracao_cadeia_completa(self):
        msg = "Teste Integração"
        
        bits_src = self.converter.text_to_bits(msg)
        
        bits_encoded = self.codec.encode(bits_src)
        
        if len(bits_encoded) > 10:
            # Inverte apenas o bit na posição 5 (ou qualquer outra posição válida)
            bits_encoded[5] ^= 1
        
        bits_decoded = self.codec.decode(bits_encoded)
        
        msg_final = self.converter.bits_to_text(bits_decoded)
        
        self.assertEqual(msg, msg_final, "Falha na integração da cadeia completa com injeção de erro.")

class TestModulation(unittest.TestCase):
    
    def setUp(self):
        self.modem = DigitalModulator()

    def test_bpsk_integrity(self):
        """Verifica se BPSK modula e demodula perfeitamente sem ruído."""
        bits_in = np.array([0, 1, 1, 0, 1, 0, 0, 1], dtype=np.uint8)
        
        # Modula
        symbols = self.modem.modulate(bits_in, scheme='BPSK')
        # Demodula (sem adicionar ruído)
        bits_out = self.modem.demodulate(symbols, scheme='BPSK')
        
        np.testing.assert_array_equal(bits_in, bits_out, 
            "Falha: BPSK sem ruído deveria retornar bits idênticos.")

    def test_qpsk_integrity_even(self):
        """Verifica QPSK com número PAR de bits."""
        bits_in = np.array([0, 0, 0, 1, 1, 0, 1, 1], dtype=np.uint8) # 8 bits (4 símbolos)
        
        symbols = self.modem.modulate(bits_in, scheme='QPSK')
        
        # Verifica se gerou 4 símbolos
        self.assertEqual(len(symbols), 4, "QPSK deveria gerar N/2 símbolos.")
        
        bits_out = self.modem.demodulate(symbols, scheme='QPSK')
        np.testing.assert_array_equal(bits_in, bits_out, "Falha: QPSK (par) corrompido.")

    def test_qpsk_integrity_odd(self):
        """Verifica QPSK com número ÍMPAR de bits (teste de padding)."""
        bits_in = np.array([1, 0, 1], dtype=np.uint8) # 3 bits -> precisa de padding para 4
        
        symbols = self.modem.modulate(bits_in, scheme='QPSK')
        
        # Devemos informar o tamanho original para cortar o padding na volta
        bits_out = self.modem.demodulate(symbols, scheme='QPSK', original_length=len(bits_in))
        
        np.testing.assert_array_equal(bits_in, bits_out, 
            "Falha: QPSK com bits ímpares (padding) não retornou corretamente.")

    def test_noise_impact(self):
        """Verifica se o ruído está realmente alterando os símbolos."""
        bits = np.array([0, 1]*100, dtype=np.uint8)
        symbols_clean = self.modem.modulate(bits, scheme='BPSK')
        
        # Adiciona ruído muito alto (SNR baixo)
        symbols_noisy = self.modem.add_awgn_noise(symbols_clean, snr_db=0)
        
        # Verifica se os arrays são diferentes
        are_equal = np.allclose(symbols_clean, symbols_noisy)
        self.assertFalse(are_equal, "Falha: A função de ruído não alterou os símbolos.")
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
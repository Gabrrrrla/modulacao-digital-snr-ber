class BitConverter:
    """
    Converte entre representações de texto e bits vetorizados (NumPy Arrays).
    """
    
    @staticmethod
    def text_to_bits(text):
        """
        Converte uma string de texto em um fluxo contínuo de bits.
        """
        # 1. Conversão direta da memória da string para bytes
        byte_data = np.frombuffer(text.encode('utf-8'), dtype=np.uint8)
        
        # 2. Desempacotamento de bits (Bit Unpacking)
        bit_array = np.unpackbits(byte_data)
        
        return bit_array

    @staticmethod
    def bits_to_text(bit_array):
        """
        Reconstitui a string de texto a partir de um fluxo de bits.
        Assume alinhamento de bytes (comprimento múltiplo de 8).
        """
        if len(bit_array) % 8!= 0:
            raise ValueError("O fluxo de bits deve ter comprimento múltiplo de 8 para conversão ASCII.")
        byte_data = np.packbits(bit_array)
        return byte_data.tobytes().decode('utf-8', errors='replace')
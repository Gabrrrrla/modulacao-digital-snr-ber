import numpy as np
import random
import string

class MessageSource:
    """
    Geração da informação original do sistema.
    """
    def __init__(self, source_type='random', fixed_message=None, seed=None):
        """
        Inicializa a fonte de dados.
        """
        self.source_type = source_type
        self.fixed_message = fixed_message
        if seed is not None:
            random.seed(seed)

    def get_message(self, length=100):
        """
        Gera ou recupera a mensagem de dados.
        """
        if self.source_type == 'fixed':
            if self.fixed_message is None:
                raise ValueError("Mensagem fixa não definida na inicialização.")
            return self.fixed_message
        
        elif self.source_type == 'random':
            # Seleciona caracteres do conjunto imprimível ASCII para facilitar visualização
            # Inclui letras, dígitos e pontuação.
            chars = string.ascii_letters + string.digits + string.punctuation + " "
            return ''.join(random.choice(chars) for _ in range(length))
        
        else:
            raise ValueError(f"Tipo de fonte '{self.source_type}' desconhecido.")
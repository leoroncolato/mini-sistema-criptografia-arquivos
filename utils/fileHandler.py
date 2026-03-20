import os

class FileHandler:
    """Utilitário para leitura e gravação de arquivos em modo binário."""
    
    @staticmethod
    def read_file(filepath: str) -> bytes:
        """Lê um arquivo do disco e retorna seus bytes."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Arquivo não encontrado no caminho: {filepath}")
        
        with open(filepath, 'rb') as file:
            return file.read()

    @staticmethod
    def write_file(filepath: str, data: bytes) -> None:
        """Grava bytes diretamente em um arquivo no disco."""
        # Cria os diretórios caso não existam (ex: pasta 'data/')
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'wb') as file:
            file.write(data)
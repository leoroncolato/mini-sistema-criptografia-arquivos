import logging
import os
from datetime import datetime

class CryptoLogger:
    """Configura e gerencia os logs de execução do sistema."""
    
    @staticmethod
    def setup_logger(name: str):
        # Garante que a pasta logs existe
        os.makedirs("logs", exist_ok=True)
        
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        
        # Evita duplicar handlers se o logger já foi configurado
        if not logger.handlers:
            # Formato da mensagem: Data - Nome - Nível - Mensagem
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            
            # Handler para arquivo
            file_handler = logging.FileHandler(f"logs/execucao_{datetime.now().strftime('%Y%m%d')}.log")
            file_handler.setFormatter(formatter)
            
            # Handler para console (terminal)
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)
            
        return logger
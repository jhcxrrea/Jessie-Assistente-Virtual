# modules/get_env.py
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

def print_env(variables):
    env_vars = {}
    for var in variables:
        value = os.getenv(var)
        if value is None:
            raise ValueError(f"Variável de ambiente '{var}' não encontrada.")
        env_vars[var] = value
    return env_vars

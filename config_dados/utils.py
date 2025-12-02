# utils.py - Funções Auxiliares
import re
from .config import (
    USUARIOS,
    IDADE_MIN,
    IDADE_MAX,
    NOME_MIN_CARACTERES,
    TELEFONE_PADROES,
)

def validar_telefone(telefone):
    """Valida telefone contra múltiplos padrões"""
    return any(re.match(padrao, telefone) for padrao in TELEFONE_PADROES)

def validar_nome(nome):
    """Valida nome: apenas letras, espaços e acentos"""
    return bool(re.match(r'^[a-zA-ZáéíóúãõçÁÉÍÓÚÃÕÇ\s]+$', nome)) and len(nome) >= NOME_MIN_CARACTERES

def validar_idade(idade):
    """Valida idade: número entre IDADE_MIN e IDADE_MAX"""
    try:
        idade_int = int(idade)
        return IDADE_MIN < idade_int <= IDADE_MAX
    except ValueError:
        return False

def validar_credenciais(usuario, senha):
    """Verifica se credenciais estão corretas"""
    return usuario in USUARIOS and USUARIOS[usuario] == senha

def formatar_telefone(telefone):
    """Remove caracteres especiais do telefone"""
    return ''.join(filter(str.isdigit, telefone))

def limpar_tela():
    """Limpa a tela do console"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def separador(char="=", tamanho=50):
    """Cria um separador visual"""
    return char * tamanho

def exibir_titulo(titulo):
    """Exibe título formatado"""
    print(f"{separador()}")
    print(f"--- {titulo} ---")
    print(f"{separador()}")

def exibir_sucesso(mensagem):
    """Exibe mensagem de sucesso"""
    print(f"✓ {mensagem}")

def exibir_erro(mensagem):
    """Exibe mensagem de erro"""
    print(f"✗ {mensagem}")

def exibir_info(mensagem):
    """Exibe mensagem de informação"""
    print(f"ℹ {mensagem}")

def pausar():
    """Pausa a execução para o usuário ler"""
    input("\nPressione ENTER para continuar...")

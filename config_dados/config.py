# config.py - Configurações do Sistema

# USUÁRIOS E SENHAS
USUARIOS = {
    "admin": "12345",
    "recepcionista": "54321",
    "medico": "senha_medico"
}

# VALIDAÇÕES
IDADE_MIN = 1
IDADE_MAX = 120
NOME_MIN_CARACTERES = 3

# FORMATOS DE TELEFONE (REGEX)
TELEFONE_PADROES = [
    r'^\(\d{2}\) \d{4,5}-\d{4}$',      # (11) 9999-9999
    r'^\d{2} \d{4,5}-\d{4}$',          # 11 9999-9999
    r'^\+55 \d{2} \d{4,5}-\d{4}$',     # +55 11 9999-9999
    r'^\d{10,11}$',                    # 1199999999
    r'^\+?[\d\s-]{10,}$'               # Genérico
]

# ARQUIVO DE BACKUP
ARQUIVO_BACKUP = "backup_pacientes.json"

# MENSAGENS
MSG_SUCESSO = "✓ Operação realizada com sucesso!"
MSG_ERRO = "✗ Erro ao realizar operação!"
MSG_NAO_ENCONTRADO = "✗ Nenhum registro encontrado!"
MSG_ACESSO_NEGADO = "✗ Acesso negado!"

# INTERFACE
JANELA_LARGURA = 800
JANELA_ALTURA = 500
JANELA_TITULO = "Clínica Vida+ - Sistema de Gestão de Pacientes"

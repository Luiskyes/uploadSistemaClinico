# Passo 4: Fila de Atendimento - Clínica Vida+
# Estrutura de Dados: Queue (FIFO - First In First Out)
# ✅ APENAS PACIENTES CADASTRADOS

from collections import deque
from datetime import datetime


class PacienteNaFila:
    """Representa um paciente na fila de atendimento"""

    def __init__(self, nome, cpf):
        self.nome = nome
        self.cpf = cpf
        self.data_entrada = datetime.now()
        self.numero_fila = None

    def __str__(self):
        return f"{self.numero_fila:03d} - {self.nome} ({self.cpf})"

    def __repr__(self):
        return f"PacienteNaFila(nome='{self.nome}', cpf='{self.cpf}')"


class FilaAtendimento:
    """Gerencia a fila de atendimento usando Queue (FIFO)

    ✅ Validação: Apenas pacientes cadastrados podem entrar
    ✅ Máximo: 3 pacientes na fila
    ✅ Estrutura: FIFO (First In First Out)
    """

    def __init__(self):
        self.fila = deque()
        self.proximo_numero = 1000
        self.historico_atendidos = []
        self.pacientes_cadastrados = []  # Lista de pacientes válidos

    def registrar_pacientes_sistema(self, clinica):
        """Registra lista de pacientes cadastrados no sistema"""
        self.pacientes_cadastrados = clinica.listar_pacientes()

    def validar_paciente_cadastrado(self, nome):
        """Valida se paciente está cadastrado no sistema

        Args:
            nome (str): Nome do paciente

        Returns:
            tuple: (bool, paciente_encontrado ou None)
        """
        for paciente in self.pacientes_cadastrados:
            if paciente.nome.lower() == nome.lower():
                return True, paciente

        return False, None

    def inserir_paciente(self, nome, cpf=None):
        """Insere paciente na fila com validação

        ✅ VERIFICA SE ESTÁ CADASTRADO
        ✅ MÁXIMO DE 3 PACIENTES

        Args:
            nome (str): Nome do paciente
            cpf (str): CPF do paciente (opcional)

        Returns:
            tuple: (sucesso, mensagem)
        """
        # Validar se está cadastrado
        validado, paciente_obj = self.validar_paciente_cadastrado(nome)

        if not validado:
            return False, f"❌ Erro: '{nome}' NÃO está cadastrado no sistema!"

        # Verificar fila cheia
        if len(self.fila) >= 3:
            return False, "❌ Fila cheia! Máximo de 3 pacientes."

        # Verificar duplicata
        for p in self.fila:
            if p.nome.lower() == nome.lower():
                return False, f"❌ '{nome}' já está na fila!"

        # Usar CPF do paciente cadastrado se não informado
        cpf_usar = cpf if cpf else paciente_obj.telefone

        # Inserir paciente
        paciente = PacienteNaFila(nome, cpf_usar)
        paciente.numero_fila = self.proximo_numero
        self.proximo_numero += 1

        self.fila.append(paciente)
        return True, f"✓ Paciente '{nome}' adicionado à fila (Nº {paciente.numero_fila})"

    def remover_proximo(self):
        """Remove o primeiro paciente da fila para atendimento (FIFO)

        Returns:
            tuple: (paciente, mensagem)
        """
        if len(self.fila) == 0:
            return None, "❌ Fila vazia! Nenhum paciente para atender."

        paciente = self.fila.popleft()
        self.historico_atendidos.append({
            'paciente': paciente,
            'hora_atendimento': datetime.now()
        })

        return paciente, f"✓ Chamando {paciente.nome} para atendimento!"

    def ver_proximos(self):
        """Mostra quem está na fila após o primeiro atendimento

        Returns:
            tuple: (lista_pacientes, mensagem)
        """
        if len(self.fila) == 0:
            return [], "Fila vazia após o atendimento."

        proximos = list(self.fila)
        return proximos, f"{len(proximos)} paciente(s) na fila"

    def listar_fila_completa(self):
        """Lista todos os pacientes na fila

        Returns:
            str: Representação formatada da fila
        """
        if len(self.fila) == 0:
            return "Fila vazia"

        resultado = "\n┌─ FILA DE ATENDIMENTO (FIFO) ──────────────────────┐\n"
        resultado += "│ Posição | Número | Nome              | Telefone     │\n"
        resultado += "├─────────┼────────┼───────────────────┼──────────────┤\n"

        for i, paciente in enumerate(self.fila, 1):
            resultado += f"│ {i}       │ {paciente.numero_fila} │ {paciente.nome:17} │ {paciente.cpf:12} │\n"

        resultado += "└─────────┴────────┴───────────────────┴──────────────┘"
        return resultado

    def tamanho_fila(self):
        """Retorna tamanho da fila

        Returns:
            int: Quantidade de pacientes na fila
        """
        return len(self.fila)

    def fila_cheia(self):
        """Verifica se fila está cheia

        Returns:
            bool: True se cheia (3 pacientes)
        """
        return len(self.fila) >= 3

    def fila_vazia(self):
        """Verifica se fila está vazia

        Returns:
            bool: True se vazia
        """
        return len(self.fila) == 0

    def listar_pacientes_disponiveis(self):
        """Lista pacientes cadastrados disponíveis para entrar na fila

        Returns:
            list: Lista de pacientes cadastrados
        """
        return self.pacientes_cadastrados


# Exemplos de uso
if __name__ == "__main__":
    print("Módulo passo4_fila_atendimento.py importado com sucesso!")
    print("\nClasse FilaAtendimento disponível para uso.")
    print("\n✅ VALIDAÇÃO IMPLEMENTADA:")
    print("   • Apenas pacientes cadastrados")
    print("   • Máximo de 3 na fila")
    print("   • Estrutura: FIFO (First In First Out)")
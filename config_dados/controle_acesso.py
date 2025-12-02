# Sistema de Controle de Acesso - Clínica Vida+
# Passo 3: Verificação de múltiplas condições

class ControladorAcesso:
    """Controlador de acesso para atendimento de pacientes"""

    def __init__(self):
        self.pacientes_ativos = {}

    def adicionar_paciente(self, nome, agendamento=False, documentos_ok=False, 
                           medico_disponivel=False, pagamentos_ok=False, tipo_atendimento="normal"):
        """
        Adiciona paciente com suas condições

        Args:
            nome (str): Nome do paciente
            agendamento (bool): A - Tem agendamento marcado
            documentos_ok (bool): B - Documentos em dia (RG/CPF válidos)
            medico_disponivel (bool): C - Há médico disponível no horário
            pagamentos_ok (bool): D - Está em dia com pagamentos
            tipo_atendimento (str): "normal" ou "emergencia"
        """
        self.pacientes_ativos[nome] = {
            'A': agendamento,
            'B': documentos_ok,
            'C': medico_disponivel,
            'D': pagamentos_ok,
            'tipo': tipo_atendimento
        }

    def pode_ser_atendido(self, nome):
        """
        Verifica se paciente pode ser atendido

        Regras:
        - CONSULTA NORMAL: (A E B E C) OU (B E C E D)
        - EMERGÊNCIA: (C) E (B OU D)

        Returns:
            tuple: (pode_atender: bool, motivo: str, condicoes: dict)
        """

        if nome not in self.pacientes_ativos:
            return False, "Paciente não encontrado no sistema.", {}

        paciente = self.pacientes_ativos[nome]
        A = paciente['A']  # Agendamento
        B = paciente['B']  # Documentos OK
        C = paciente['C']  # Médico disponível
        D = paciente['D']  # Pagamentos em dia
        tipo = paciente['tipo']

        # Mostrar condições
        condicoes = {
            'A - Agendamento': A,
            'B - Documentos (RG/CPF)': B,
            'C - Médico disponível': C,
            'D - Pagamentos em dia': D,
            'Tipo': tipo
        }

        # LÓGICA PARA CONSULTA NORMAL
        if tipo == "normal":
            # (A E B E C) OU (B E C E D)
            condicao1 = A and B and C  # Tem agendamento E documentos E médico
            condicao2 = B and C and D  # Tem documentos E médico E pagamentos

            pode_atender = condicao1 or condicao2

            if pode_atender:
                if condicao1:
                    motivo = "✓ CONSULTAAPROVADA (Agendamento + Documentos + Médico disponível)"
                else:
                    motivo = "✓ CONSULTA APROVADA (Documentos + Médico disponível + Pagamentos em dia)"
            else:
                motivo = "✗ CONSULTA NEGADA - Faltam condições necessárias"

        # LÓGICA PARA EMERGÊNCIA
        elif tipo == "emergencia":
            # (C) E (B OU D)
            condicao_base = C  # Há médico disponível
            condicao_docs_ou_pagto = B or D  # Documentos OU Pagamentos

            pode_atender = condicao_base and condicao_docs_ou_pagto

            if pode_atender:
                motivo = "✓ EMERGÊNCIA APROVADA (Médico disponível + Documentos/Pagamentos)"
            else:
                motivo = "✗ EMERGÊNCIA NEGADA - Médico indisponível ou sem documentos e pagamentos"

        else:
            pode_atender = False
            motivo = "✗ Tipo de atendimento inválido"

        return pode_atender, motivo, condicoes

    def relatorio_detalhado(self, nome):
        """Gera relatório detalhado de análise"""
        pode_atender, motivo, condicoes = self.pode_ser_atendido(nome)

        print("\n" + "="*70)
        print(f"RELATÓRIO DE ACESSO - {nome}")
        print("="*70)

        print("\n📋 CONDIÇÕES VERIFICADAS:")
        for condicao, valor in condicoes.items():
            if condicao != 'Tipo':
                status = "✓ SIM" if valor else "✗ NÃO"
                print(f"   {condicao}: {status}")

        print(f"\n🏥 Tipo de Atendimento: {condicoes['Tipo'].upper()}")

        print(f"\n🔍 RESULTADO: {motivo}")

        print("\n" + "="*70 + "\n")

        return pode_atender


class AnalisadorLogica:
    """Analisador de lógica booleana"""

    @staticmethod
    def analise_consulta_normal():
        """Mostra análise da lógica para consulta normal"""
        texto = """
╔════════════════════════════════════════════════════════════════════════════╗
║              ANÁLISE - CONSULTA NORMAL (LÓGICA BOOLEANA)                   ║
╚════════════════════════════════════════════════════════════════════════════╝

REGRA: (A E B E C) OU (B E C E D)

Onde:
  A = Paciente tem agendamento marcado
  B = Paciente tem documentos OK (RG/CPF válidos)
  C = Há médico disponível no horário
  D = Paciente está em dia com pagamentos

EXPRESSÃO LÓGICA:
  (A ∧ B ∧ C) ∨ (B ∧ C ∧ D)

INTERPRETAÇÃO:
  Paciente será atendido SE:
    • Tem agendamento E tem documentos E há médico
    OU
    • Tem documentos E há médico E pagamentos ok


EXEMPLOS:

┌─────────────────────────────────────────────────────────────┐
│ Exemplo 1: APROVADO (Primeira condição verdadeira)         │
├─────────────────────────────────────────────────────────────┤
│ A (Agendamento)      = V ✓                                  │
│ B (Documentos)       = V ✓                                  │
│ C (Médico)           = V ✓                                  │
│ D (Pagamentos)       = F ✗                                  │
│                                                             │
│ (V ∧ V ∧ V) ∨ (V ∧ V ∧ F)                                  │
│    V        ∨       F                                       │
│              V → APROVADO ✓                                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Exemplo 2: APROVADO (Segunda condição verdadeira)          │
├─────────────────────────────────────────────────────────────┤
│ A (Agendamento)      = F ✗                                  │
│ B (Documentos)       = V ✓                                  │
│ C (Médico)           = V ✓                                  │
│ D (Pagamentos)       = V ✓                                  │
│                                                             │
│ (F ∧ V ∧ V) ∨ (V ∧ V ∧ V)                                  │
│    F        ∨       V                                       │
│              V → APROVADO ✓                                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Exemplo 3: NEGADO (Ambas condições falsas)                 │
├─────────────────────────────────────────────────────────────┤
│ A (Agendamento)      = F ✗                                  │
│ B (Documentos)       = F ✗                                  │
│ C (Médico)           = V ✓                                  │
│ D (Pagamentos)       = V ✓                                  │
│                                                             │
│ (F ∧ F ∧ V) ∨ (F ∧ V ∧ V)                                  │
│    F        ∨       F                                       │
│              F → NEGADO ✗                                   │
└─────────────────────────────────────────────────────────────┘
        """
        print(texto)

    @staticmethod
    def analise_emergencia():
        """Mostra análise da lógica para emergência"""
        texto = """
╔════════════════════════════════════════════════════════════════════════════╗
║                ANÁLISE - EMERGÊNCIA (LÓGICA BOOLEANA)                      ║
╚════════════════════════════════════════════════════════════════════════════╝

REGRA: (C) E (B OU D)

Onde:
  B = Paciente tem documentos OK (RG/CPF válidos)
  C = Há médico disponível no horário
  D = Paciente está em dia com pagamentos

EXPRESSÃO LÓGICA:
  C ∧ (B ∨ D)

INTERPRETAÇÃO:
  Paciente será atendido em emergência SE:
    • Há médico disponível
    E
    • Tem documentos OU está em dia com pagamentos


EXEMPLOS:

┌─────────────────────────────────────────────────────────────┐
│ Exemplo 1: APROVADO (Médico + Documentos)                  │
├─────────────────────────────────────────────────────────────┤
│ B (Documentos)       = V ✓                                  │
│ C (Médico)           = V ✓                                  │
│ D (Pagamentos)       = F ✗                                  │
│                                                             │
│ C ∧ (B ∨ D)                                                 │
│ V ∧ (V ∨ F)                                                 │
│ V ∧  V                                                      │
│  V → APROVADO ✓                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Exemplo 2: APROVADO (Médico + Pagamentos)                  │
├─────────────────────────────────────────────────────────────┤
│ B (Documentos)       = F ✗                                  │
│ C (Médico)           = V ✓                                  │
│ D (Pagamentos)       = V ✓                                  │
│                                                             │
│ C ∧ (B ∨ D)                                                 │
│ V ∧ (F ∨ V)                                                 │
│ V ∧  V                                                      │
│  V → APROVADO ✓                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Exemplo 3: NEGADO (Sem médico)                             │
├─────────────────────────────────────────────────────────────┤
│ B (Documentos)       = V ✓                                  │
│ C (Médico)           = F ✗                                  │
│ D (Pagamentos)       = V ✓                                  │
│                                                             │
│ C ∧ (B ∨ D)                                                 │
│ F ∧ (V ∨ V)                                                 │
│ F ∧  V                                                      │
│  F → NEGADO ✗                                               │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Exemplo 4: NEGADO (Sem documentos e pagamentos)            │
├─────────────────────────────────────────────────────────────┤
│ B (Documentos)       = F ✗                                  │
│ C (Médico)           = V ✓                                  │
│ D (Pagamentos)       = F ✗                                  │
│                                                             │
│ C ∧ (B ∨ D)                                                 │
│ V ∧ (F ∨ F)                                                 │
│ V ∧  F                                                      │
│  F → NEGADO ✗                                               │
└─────────────────────────────────────────────────────────────┘
        """
        print(texto)


# Exemplos de uso
if __name__ == "__main__":
    controlador = ControladorAcesso()
    analisador = AnalisadorLogica()

    # Mostrar análises
    print("\n")
    analisador.analise_consulta_normal()
    input("Pressione ENTER para ver análise de emergência...")
    print("\n")
    analisador.analise_emergencia()

    # Exemplos práticos
    input("\nPressione ENTER para ver exemplos práticos...")
    print("\n\n")

    # Exemplo 1: Consulta Normal - Aprovada
    print("EXEMPLO 1: Consulta Normal - Cenário APROVADO")
    controlador.adicionar_paciente("João Silva", agendamento=True, documentos_ok=True, 
                                   medico_disponivel=True, pagamentos_ok=False, tipo_atendimento="normal")
    controlador.relatorio_detalhado("João Silva")

    # Exemplo 2: Consulta Normal - Negada
    print("EXEMPLO 2: Consulta Normal - Cenário NEGADO")
    controlador.adicionar_paciente("Maria Santos", agendamento=False, documentos_ok=False, 
                                   medico_disponivel=True, pagamentos_ok=True, tipo_atendimento="normal")
    controlador.relatorio_detalhado("Maria Santos")

    # Exemplo 3: Emergência - Aprovada
    print("EXEMPLO 3: Emergência - Cenário APROVADO")
    controlador.adicionar_paciente("Pedro Costa", agendamento=False, documentos_ok=True, 
                                   medico_disponivel=True, pagamentos_ok=False, tipo_atendimento="emergencia")
    controlador.relatorio_detalhado("Pedro Costa")

    # Exemplo 4: Emergência - Negada
    print("EXEMPLO 4: Emergência - Cenário NEGADO")
    controlador.adicionar_paciente("Ana Paula", agendamento=False, documentos_ok=False, 
                                   medico_disponivel=False, pagamentos_ok=False, tipo_atendimento="emergencia")
    controlador.relatorio_detalhado("Ana Paula")

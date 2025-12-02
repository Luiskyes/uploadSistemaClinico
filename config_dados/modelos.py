# modelos.py - Modelos de Dados

from datetime import datetime

class Paciente:
    """Classe que representa um paciente"""

    def __init__(self, nome, idade, telefone):
        self.nome = nome
        self.idade = idade
        self.telefone = telefone
        self.data_cadastro = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.historico = []

    def para_dicionario(self):
        """Converte paciente para dicionário"""
        return {
            'nome': self.nome,
            'idade': self.idade,
            'telefone': self.telefone,
            'data_cadastro': self.data_cadastro,
            'historico': self.historico
        }

    @staticmethod
    def de_dicionario(dados):
        """Cria paciente a partir de dicionário"""
        paciente = Paciente(dados['nome'], dados['idade'], dados['telefone'])
        paciente.data_cadastro = dados.get('data_cadastro', paciente.data_cadastro)
        paciente.historico = dados.get('historico', [])
        return paciente

    def editar(self, campo, novo_valor):
        """Edita um campo do paciente"""
        if campo == 'nome':
            self.nome = novo_valor
        elif campo == 'idade':
            self.idade = int(novo_valor)
        elif campo == 'telefone':
            self.telefone = novo_valor

        # Registra a alteração no histórico
        self.historico.append({
            'data': datetime.now().strftime("%d/%m/%Y %H:%M"),
            'tipo': 'edicao',
            'campo': campo,
            'novo_valor': novo_valor
        })

    def adicionar_historico(self, tipo, descricao):
        """Adiciona evento ao histórico"""
        self.historico.append({
            'data': datetime.now().strftime("%d/%m/%Y %H:%M"),
            'tipo': tipo,
            'descricao': descricao
        })

    def __str__(self):
        return f"{self.nome} ({self.idade} anos) - {self.telefone}"

    def __repr__(self):
        return f"Paciente(nome='{self.nome}', idade={self.idade}, telefone='{self.telefone}')"


class Clinica:
    """Classe que gerencia a clínica e seus pacientes"""

    def __init__(self, nome="Clínica Vida+"):
        self.nome = nome
        self.pacientes = []
        self.usuario_logado = None

    def adicionar_paciente(self, paciente):
        """Adiciona um paciente à clínica"""
        self.pacientes.append(paciente)
        return True

    def remover_paciente(self, nome):
        """Remove um paciente pelo nome"""
        for i, p in enumerate(self.pacientes):
            if p.nome.lower() == nome.lower():
                self.pacientes.pop(i)
                return True
        return False

    def buscar_paciente(self, nome):
        """Busca paciente(s) pelo nome"""
        encontrados = [p for p in self.pacientes if nome.lower() in p.nome.lower()]
        return encontrados

    def buscar_paciente_exato(self, nome):
        """Busca um paciente exato pelo nome"""
        for p in self.pacientes:
            if p.nome.lower() == nome.lower():
                return p
        return None

    def listar_pacientes(self):
        """Retorna lista de todos os pacientes"""
        return self.pacientes.copy()

    def total_pacientes(self):
        """Retorna total de pacientes"""
        return len(self.pacientes)

    def idade_media(self):
        """Calcula idade média"""
        if not self.pacientes:
            return 0
        return sum(p.idade for p in self.pacientes) / len(self.pacientes)

    def paciente_mais_novo(self):
        """Retorna paciente mais novo"""
        if not self.pacientes:
            return None
        return min(self.pacientes, key=lambda p: p.idade)

    def paciente_mais_velho(self):
        """Retorna paciente mais velho"""
        if not self.pacientes:
            return None
        return max(self.pacientes, key=lambda p: p.idade)

    def gerar_relatorio_estatisticas(self):
        """Gera relatório de estatísticas"""
        if not self.pacientes:
            return {}

        idades = [p.idade for p in self.pacientes]
        return {
            'total_pacientes': len(self.pacientes),
            'idade_media': self.idade_media(),
            'idade_minima': min(idades),
            'idade_maxima': max(idades),
            'paciente_mais_novo': self.paciente_mais_novo(),
            'paciente_mais_velho': self.paciente_mais_velho()
        }

# persistencia.py - Gerenciamento de Dados
# persistencia.py - Gerenciamento de Dados

import json
import os
from datetime import datetime

from .modelos import Paciente, Clinica
from .config import ARQUIVO_BACKUP

class GerenciadorBackup:
    """Gerencia backup e persistência de dados"""

    @staticmethod
    def fazer_backup(clinica, arquivo=ARQUIVO_BACKUP):
        """Salva dados em arquivo JSON"""
        try:
            dados = {
                'data_backup': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                'total_pacientes': clinica.total_pacientes(),
                'pacientes': [p.para_dicionario() for p in clinica.pacientes]
            }

            with open(arquivo, 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)

            return True, f"Backup realizado com sucesso!"
        except Exception as e:
            return False, f"Erro ao fazer backup: {e}"

    @staticmethod
    def carregar_backup(clinica, arquivo=ARQUIVO_BACKUP):
        """Carrega dados de arquivo JSON"""
        try:
            if not os.path.exists(arquivo):
                return False, "Nenhum backup encontrado."

            with open(arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)

            # Limpa pacientes atuais
            clinica.pacientes = []

            # Carrega novos pacientes
            for p_data in dados.get('pacientes', []):
                p = Paciente.de_dicionario(p_data)
                clinica.adicionar_paciente(p)

            return True, f"{clinica.total_pacientes()} pacientes carregados."

        except json.JSONDecodeError:
            return False, "Erro ao decodificar arquivo de backup."
        except Exception as e:
            return False, f"Erro ao carregar backup: {e}"

    @staticmethod
    def restaurar_backup(clinica, arquivo):
        """Restaura de um arquivo de backup específico"""
        return GerenciadorBackup.carregar_backup(clinica, arquivo)

    @staticmethod
    def listar_backups(diretorio='.'):
        """Lista todos os arquivos de backup disponíveis"""
        backups = []
        try:
            for arquivo in os.listdir(diretorio):
                if 'backup' in arquivo and arquivo.endswith('.json'):
                    caminho_completo = os.path.join(diretorio, arquivo)
                    tamanho = os.path.getsize(caminho_completo)
                    data_mod = datetime.fromtimestamp(os.path.getmtime(caminho_completo))
                    backups.append({
                        'arquivo': arquivo,
                        'tamanho': tamanho,
                        'data_modificacao': data_mod.strftime("%d/%m/%Y %H:%M")
                    })
        except Exception as e:
            pass

        return backups


class SerializadorJSON:
    """Serializa/desserializa dados para/de JSON"""

    @staticmethod
    def serializar_clinica(clinica):
        """Converte clínica para JSON"""
        return json.dumps({
            'nome': clinica.nome,
            'pacientes': [p.para_dicionario() for p in clinica.pacientes],
            'usuario_logado': clinica.usuario_logado
        }, ensure_ascii=False, indent=2)

    @staticmethod
    def desserializar_clinica(dados_json):
        """Cria clínica a partir de JSON"""
        dados = json.loads(dados_json)
        clinica = Clinica(dados['nome'])

        for p_data in dados.get('pacientes', []):
            p = Paciente.de_dicionario(p_data)
            clinica.adicionar_paciente(p)

        return clinica

# sistema_clinica_vida_simplificado.py
# Sistema de Gestão de Pacientes - Clínica Vida+
# Versão Completa: Passo 2 + Passo 3 + Passo 4 + GUI CORRIGIDA

from config_dados.config import USUARIOS, ARQUIVO_BACKUP
from config_dados.utils import (
    validar_nome, validar_idade, validar_telefone,
    validar_credenciais, exibir_sucesso, exibir_erro,
    exibir_titulo, exibir_info, pausar, limpar_tela,
)
from config_dados.modelos import Paciente, Clinica
from config_dados.persistencia import GerenciadorBackup
from config_dados.controle_acesso import ControladorAcesso
from config_dados.fila_atendimento import FilaAtendimento

from interface.interface_gui_melhorada import InterfaceGraficaMelhorada

from datetime import datetime


# ════════════════════════════════════════════════════════════════════════════
# IMPORTAR INTERFACE GRÁFICA MELHORADA
# ════════════════════════════════════════════════════════════════════════════

TKINTER_DISPONIVEL = False
try:
    from interface.interface_gui_melhorada import InterfaceGraficaMelhorada
    TKINTER_DISPONIVEL = True
except ImportError as e:
    print(f"⚠️ Aviso: Interface gráfica não disponível ({e})")
    TKINTER_DISPONIVEL = False



# ════════════════════════════════════════════════════════════════════════════
# AUTENTICAÇÃO - LOGIN OBRIGATÓRIO
# ════════════════════════════════════════════════════════════════════════════

class SistemaAutenticacao:
    """Gerencia autenticação do sistema"""

    def __init__(self):
        self.usuario_logado = None
        self.tentativas = 0
        self.max_tentativas = 3

    def fazer_login(self):
        """Realiza login obrigatório"""
        limpar_tela()

        print("\n" + "="*60)
        print("       CLÍNICA VIDA+ - SISTEMA DE GESTÃO DE PACIENTES")
        print("="*60)
        print("\n⚠️  LOGIN OBRIGATÓRIO\n")

        while self.tentativas < self.max_tentativas:
            try:
                usuario = input("👤 Usuário: ").strip()
                senha = input("🔐 Senha: ").strip()

                if not usuario or not senha:
                    exibir_erro("Usuário e senha não podem estar vazios!")
                    self.tentativas += 1
                    print(f"Tentativas restantes: {self.max_tentativas - self.tentativas}\n")
                    continue

                if validar_credenciais(usuario, senha):
                    self.usuario_logado = usuario
                    limpar_tela()
                    print("\n✓ Login realizado com sucesso!")
                    print(f"✓ Bem-vindo(a), {usuario}!\n")
                    pausar()
                    return True
                else:
                    self.tentativas += 1
                    tentativas_restantes = self.max_tentativas - self.tentativas
                    exibir_erro("Usuário ou senha incorretos!")
                    print(f"Tentativas restantes: {tentativas_restantes}\n")

                    if tentativas_restantes == 0:
                        break

            except KeyboardInterrupt:
                print("\n\n✗ Login cancelado pelo usuário.")
                return False
            except Exception as e:
                exibir_erro(f"Erro ao fazer login: {e}")
                self.tentativas += 1

        # Limite de tentativas excedido
        limpar_tela()
        print("\n" + "="*60)
        print("❌ LIMITE DE TENTATIVAS EXCEDIDO")
        print("="*60)
        print("\n✗ Você excedeu o limite de tentativas de login.")
        print("✗ O sistema será encerrado.")
        print("\nTente novamente mais tarde.\n")
        print("="*60 + "\n")

        return False


# ════════════════════════════════════════════════════════════════════════════
# MENU CONSOLE - COM INTEGRAÇÃO DOS PASSOS
# ════════════════════════════════════════════════════════════════════════════

class MenuConsole:
    """Menu do console com todos os passos integrados"""

    def __init__(self, clinica, usuario):
        self.clinica = clinica
        self.usuario = usuario
        self.controlador_acesso = ControladorAcesso()
        self.fila_atendimento = FilaAtendimento()

        # Registrar pacientes cadastrados na fila
        try:
            self.fila_atendimento.registrar_pacientes_sistema(self.clinica)
        except Exception as e:
            print(f"Aviso ao registrar pacientes na fila: {e}")

    def exibir_menu(self):
        """Exibe menu principal atualizado"""
        limpar_tela()
        exibir_titulo(f"CLÍNICA VIDA+ - Usuário: {self.usuario}")

        print("╔════════════════════════════════════════════════════════════╗")
        print("║                      MENU PRINCIPAL                        ║")
        print("╠════════════════════════════════════════════════════════════╣")
        print("║                      - Gestão -                            ║")
        print("║  1. Cadastrar paciente                                     ║")
        print("║  2. Ver estatísticas                                       ║")
        print("║  3. Buscar paciente                                        ║")
        print("║  4. Listar pacientes                                       ║")
        print("║  5. Editar paciente                                        ║")
        print("║  6. Remover paciente                                       ║")
        print("║  7. Interface gráfica                                      ║")
        print("║  8. Verificar acesso (Controle de Acesso)                  ║")
        print("║                                                            ║")
        print("║                      - Fila -                              ║")
        print("║  9. Gerenciar fila de atendimento                          ║")
        print("║                                                            ║")
        print("║                      - Gerais -                            ║")
        print("║  10. Fazer backup                                          ║")
        print("║  11. Restaurar backup                                      ║")
        print("║  12. Sair                                                  ║")
        print("╚════════════════════════════════════════════════════════════╝\n")

    # ────────────────────────────────────────────────────────────────────────
    # PASSO 2 - CRUD PACIENTES
    # ────────────────────────────────────────────────────────────────────────

    def cadastrar_paciente(self):
        """Cadastra novo paciente"""
        exibir_titulo("Cadastro de Paciente")

        while True:
            nome = input("Nome: ").strip()
            if validar_nome(nome):
                break
            exibir_erro("Nome inválido! Use apenas letras (mínimo 3 caracteres).")

        while True:
            try:
                idade = input("Idade: ").strip()
                if validar_idade(idade):
                    break
                exibir_erro("Idade inválida! Use um número entre 1 e 120.")
            except ValueError:
                exibir_erro("Idade inválida!")

        while True:
            telefone = input("Telefone: ").strip()
            if validar_telefone(telefone):
                break
            exibir_erro("Telefone inválido! Use formatos como (11) 98765-4321")

        paciente = Paciente(nome, int(idade), telefone)
        self.clinica.adicionar_paciente(paciente)
        GerenciadorBackup.fazer_backup(self.clinica)

        # Atualizar lista de pacientes na fila
        self.fila_atendimento.registrar_pacientes_sistema(self.clinica)

        exibir_sucesso(f"Paciente {nome} cadastrado com sucesso!")
        pausar()

    def ver_estatisticas(self):
        """Exibe estatísticas"""
        exibir_titulo("Estatísticas")

        if self.clinica.total_pacientes() == 0:
            exibir_info("Nenhum paciente cadastrado.")
            pausar()
            return

        stats = self.clinica.gerar_relatorio_estatisticas()

        print(f"Total de pacientes: {stats['total_pacientes']}")
        print(f"Idade média: {stats['idade_media']:.1f} anos")
        print(f"Idade mínima: {stats['idade_minima']} anos")
        print(f"Idade máxima: {stats['idade_maxima']} anos")
        print(f"Paciente mais novo: {stats['paciente_mais_novo'].nome} ({stats['paciente_mais_novo'].idade} anos)")
        print(f"Paciente mais velho: {stats['paciente_mais_velho'].nome} ({stats['paciente_mais_velho'].idade} anos)\n")

        pausar()

    def buscar_paciente(self):
        """Busca paciente"""
        exibir_titulo("Busca de Paciente")

        nome = input("Nome (parcial): ").strip()
        encontrados = self.clinica.buscar_paciente(nome)

        if not encontrados:
            exibir_erro("Nenhum paciente encontrado.")
        else:
            print(f"\n{len(encontrados)} paciente(s) encontrado(s):\n")
            for i, p in enumerate(encontrados, 1):
                print(f"{i}. Nome: {p.nome} | Idade: {p.idade} | Tel: {p.telefone}")
                print(f"   Cadastro: {p.data_cadastro}\n")

        pausar()

    def listar_pacientes(self):
        """Lista todos os pacientes"""
        exibir_titulo("Lista de Pacientes")

        pacientes = self.clinica.listar_pacientes()

        if not pacientes:
            exibir_info("Nenhum paciente cadastrado.")
            pausar()
            return

        print(f"\nTotal: {len(pacientes)} paciente(s)\n")

        for i, p in enumerate(pacientes, 1):
            print(f"{i}. {p.nome:30} | {p.idade:3} anos | {p.telefone}")

        print()
        pausar()

    def editar_paciente(self):
        """Edita paciente"""
        exibir_titulo("Edição de Paciente")

        nome = input("Nome do paciente: ").strip()
        paciente = self.clinica.buscar_paciente_exato(nome)

        if not paciente:
            exibir_erro("Paciente não encontrado.")
            pausar()
            return

        print(f"\nDados atuais:\n")
        print(f"Nome: {paciente.nome}")
        print(f"Idade: {paciente.idade}")
        print(f"Telefone: {paciente.telefone}\n")

        print("O que deseja editar?\n")
        print("1. Nome")
        print("2. Idade")
        print("3. Telefone\n")

        opcao = input("Opção: ").strip()

        if opcao == "1":
            novo_nome = input("Novo nome: ").strip()
            if validar_nome(novo_nome):
                paciente.editar("nome", novo_nome)
                exibir_sucesso("Nome atualizado!")
            else:
                exibir_erro("Nome inválido!")

        elif opcao == "2":
            nova_idade = input("Nova idade: ").strip()
            if validar_idade(nova_idade):
                paciente.editar("idade", nova_idade)
                exibir_sucesso("Idade atualizada!")
            else:
                exibir_erro("Idade inválida!")

        elif opcao == "3":
            novo_tel = input("Novo telefone: ").strip()
            if validar_telefone(novo_tel):
                paciente.editar("telefone", novo_tel)
                exibir_sucesso("Telefone atualizado!")
            else:
                exibir_erro("Telefone inválido!")

        GerenciadorBackup.fazer_backup(self.clinica)
        self.fila_atendimento.registrar_pacientes_sistema(self.clinica)
        pausar()

    def remover_paciente(self):
        """Remove paciente"""
        exibir_titulo("Remoção de Paciente")

        nome = input("Nome do paciente: ").strip()

        if not self.clinica.buscar_paciente_exato(nome):
            exibir_erro("Paciente não encontrado.")
            pausar()
            return

        confirmacao = input(f"\nTem certeza que deseja remover {nome}? (s/n): ").strip().lower()

        if confirmacao == "s":
            self.clinica.remover_paciente(nome)
            GerenciadorBackup.fazer_backup(self.clinica)
            self.fila_atendimento.registrar_pacientes_sistema(self.clinica)
            exibir_sucesso(f"Paciente {nome} removido!")
        else:
            exibir_info("Operação cancelada.")

        pausar()

    def interface_grafica(self):
        """Abre interface gráfica melhorada CORRIGIDA"""
        if not TKINTER_DISPONIVEL:
            exibir_erro("Interface gráfica não está disponível!")
            print("\n⚠️  Certifique-se de que:")
            print("   • Tkinter está instalado")
            print("   • interface_gui_melhorada.py existe no diretório")
            print()
            pausar()
            return

        try:
            print("\n📊 Abrindo interface gráfica...")
            print("Isso pode levar alguns segundos...\n")

            gui = InterfaceGraficaMelhorada(self.clinica, self.usuario)
            gui.iniciar()

        except Exception as e:
            exibir_erro(f"Erro ao abrir interface gráfica: {e}")
            print(f"\nDetalhes do erro: {type(e).__name__}")
            print("\nTente novamente ou use o menu console.")
            pausar()

    # ────────────────────────────────────────────────────────────────────────
    # PASSO 3 - CONTROLE DE ACESSO
    # ────────────────────────────────────────────────────────────────────────

    def verificar_acesso_paciente(self):
        """Menu para verificar acesso (Passo 3)"""
        exibir_titulo("Verificação de Acesso - Passo 3")

        print("\n📋 Escolha uma opção:\n")
        print("1. Verificar acesso de paciente existente")
        print("2. Testar novo paciente (simulação)")
        print("3. Voltar ao menu\n")

        opcao = input("Opção: ").strip()

        if opcao == "1":
            self.verificar_acesso_existente()
        elif opcao == "2":
            self.testar_acesso_novo()
        elif opcao == "3":
            return
        else:
            exibir_erro("Opção inválida!")

        pausar()

    def verificar_acesso_existente(self):
        """Verifica acesso de paciente existente"""
        print("\nPacientes cadastrados:\n")

        pacientes = self.clinica.listar_pacientes()
        if not pacientes:
            exibir_info("Nenhum paciente cadastrado.")
            return

        for i, p in enumerate(pacientes, 1):
            print(f"{i}. {p.nome}")

        print()
        opcao = input("Escolha um paciente (número): ").strip()

        try:
            idx = int(opcao) - 1
            if 0 <= idx < len(pacientes):
                paciente = pacientes[idx]
                self.realizar_verificacao_acesso(paciente.nome)
            else:
                exibir_erro("Opção inválida!")
        except ValueError:
            exibir_erro("Digite um número válido!")

    def testar_acesso_novo(self):
        """Testa acesso com novo paciente (simulação)"""
        exibir_titulo("Teste de Acesso - Novo Paciente")

        nome = input("Nome do paciente: ").strip()

        print("\nCondições (SIM/NÃO):")

        agendamento = input("A - Tem agendamento? (s/n): ").strip().lower() == "s"
        documentos = input("B - Documentos OK? (s/n): ").strip().lower() == "s"
        medico = input("C - Médico disponível? (s/n): ").strip().lower() == "s"
        pagamentos = input("D - Pagamentos em dia? (s/n): ").strip().lower() == "s"

        print("\nTipo de atendimento:")
        print("1. Normal")
        print("2. Emergência\n")

        tipo_opcao = input("Opção (1/2): ").strip()
        tipo = "emergencia" if tipo_opcao == "2" else "normal"

        self.controlador_acesso.adicionar_paciente(
            nome, agendamento, documentos, medico, pagamentos, tipo
        )

        self.controlador_acesso.relatorio_detalhado(nome)

    def realizar_verificacao_acesso(self, nome_paciente):
        """Realiza verificação de acesso"""
        print(f"\nVerificando acesso para: {nome_paciente}\n")
        print("Informações do paciente:")

        agendamento = input("A - Tem agendamento? (s/n): ").strip().lower() == "s"
        documentos = input("B - Documentos OK? (s/n): ").strip().lower() == "s"
        medico = input("C - Médico disponível? (s/n): ").strip().lower() == "s"
        pagamentos = input("D - Pagamentos em dia? (s/n): ").strip().lower() == "s"

        print("\nTipo de atendimento:")
        print("1. Normal")
        print("2. Emergência\n")

        tipo_opcao = input("Opção (1/2): ").strip()
        tipo = "emergencia" if tipo_opcao == "2" else "normal"

        self.controlador_acesso.adicionar_paciente(
            nome_paciente, agendamento, documentos, medico, pagamentos, tipo
        )

        self.controlador_acesso.relatorio_detalhado(nome_paciente)

    # ────────────────────────────────────────────────────────────────────────
    # PASSO 4 - FILA DE ATENDIMENTO
    # ────────────────────────────────────────────────────────────────────────

    def gerenciar_fila(self):
        """Menu para gerenciar fila de atendimento com VALIDAÇÃO"""
        exibir_titulo("Gerenciar Fila de Atendimento - Passo 4")

        while True:
            print("\n📋 Fila de Atendimento (FIFO):")
            print(f"Pacientes na fila: {self.fila_atendimento.tamanho_fila()}/3\n")

            print("1. Inserir paciente na fila (APENAS CADASTRADOS)")
            print("2. Chamar próximo paciente")
            print("3. Ver fila completa")
            print("4. Ver histórico de atendidos")
            print("5. Listar pacientes disponíveis")
            print("6. Voltar ao menu\n")

            opcao = input("Opção: ").strip()

            if opcao == "1":
                self.inserir_na_fila()
            elif opcao == "2":
                self.chamar_proximo_fila()
            elif opcao == "3":
                self.ver_fila_completa()
            elif opcao == "4":
                self.ver_historico_fila()
            elif opcao == "5":
                self.listar_pacientes_disponiveis()
            elif opcao == "6":
                break
            else:
                exibir_erro("Opção inválida!")

            pausar()

    def inserir_na_fila(self):
        """Insere paciente na fila com VALIDAÇÃO"""
        print("\n✅ INSERÇÃO COM VALIDAÇÃO DE CADASTRO")
        print("="*50)

        pacientes_disponiveis = self.fila_atendimento.listar_pacientes_disponiveis()

        if not pacientes_disponiveis:
            exibir_erro("Nenhum paciente cadastrado no sistema!")
            return

        print("\nPacientes cadastrados disponíveis:\n")
        for i, p in enumerate(pacientes_disponiveis, 1):
            print(f"{i}. {p.nome:30} - Telefone: {p.telefone}")

        print()
        opcao = input("Escolha um paciente (número) ou nome: ").strip()

        try:
            idx = int(opcao) - 1
            if 0 <= idx < len(pacientes_disponiveis):
                nome = pacientes_disponiveis[idx].nome
            else:
                exibir_erro("Opção inválida!")
                return
        except ValueError:
            nome = opcao

        sucesso, msg = self.fila_atendimento.inserir_paciente(nome)

        if sucesso:
            exibir_sucesso(msg)
        else:
            exibir_erro(msg)

    def chamar_proximo_fila(self):
        """Chama próximo paciente da fila"""
        paciente, msg = self.fila_atendimento.remover_proximo()

        if paciente:
            print(f"\n✓ {msg}")
            print(f"Paciente: {paciente.nome}")
            print(f"Telefone: {paciente.cpf}")
            print(f"Número da chamada: {paciente.numero_fila}")
        else:
            exibir_erro(msg)

    def ver_fila_completa(self):
        """Ver fila completa"""
        print("\n")
        print(self.fila_atendimento.listar_fila_completa())
        print(f"\nTotal na fila: {self.fila_atendimento.tamanho_fila()} pacientes")

    def ver_historico_fila(self):
        """Ver histórico de pacientes atendidos"""
        print("\n📊 Histórico de Atendidos:\n")

        if not self.fila_atendimento.historico_atendidos:
            exibir_info("Nenhum paciente atendido ainda.")
            return

        for i, atend in enumerate(self.fila_atendimento.historico_atendidos, 1):
            pac = atend['paciente']
            hora = atend['hora_atendimento'].strftime("%H:%M:%S")
            print(f"{i}. {pac.numero_fila} - {pac.nome}")
            print(f"   Telefone: {pac.cpf}")
            print(f"   Atendido em: {hora}\n")

    def listar_pacientes_disponiveis(self):
        """Lista pacientes disponíveis para entrar na fila"""
        exibir_titulo("Pacientes Disponíveis")

        pacientes = self.fila_atendimento.listar_pacientes_disponiveis()

        if not pacientes:
            exibir_info("Nenhum paciente cadastrado.")
            pausar()
            return

        print(f"\nTotal: {len(pacientes)} paciente(s) cadastrado(s)\n")

        for i, p in enumerate(pacientes, 1):
            print(f"{i}. {p.nome:30} | {p.idade:3} anos | {p.telefone}")

        print()

    # ────────────────────────────────────────────────────────────────────────
    # GERAIS
    # ────────────────────────────────────────────────────────────────────────

    def fazer_backup(self):
        """Faz backup manual"""
        exibir_titulo("Backup Manual")

        sucesso, mensagem = GerenciadorBackup.fazer_backup(self.clinica)

        if sucesso:
            exibir_sucesso(mensagem)
        else:
            exibir_erro(mensagem)

        pausar()

    def restaurar_backup(self):
        """Restaura backup"""
        exibir_titulo("Restauração de Backup")

        backups = GerenciadorBackup.listar_backups()

        if not backups:
            exibir_erro("Nenhum backup encontrado.")
            pausar()
            return

        print("\nBackups disponíveis:\n")
        for i, b in enumerate(backups, 1):
            print(f"{i}. {b['arquivo']} - {b['data_modificacao']}")

        print()
        opcao = input("Qual backup deseja restaurar? (número): ").strip()

        try:
            idx = int(opcao) - 1
            if 0 <= idx < len(backups):
                arquivo = backups[idx]['arquivo']
                sucesso, msg = GerenciadorBackup.restaurar_backup(self.clinica, arquivo)
                if sucesso:
                    exibir_sucesso(msg)
                    self.fila_atendimento.registrar_pacientes_sistema(self.clinica)
                else:
                    exibir_erro(msg)
            else:
                exibir_erro("Opção inválida!")
        except ValueError:
            exibir_erro("Opção inválida!")

        pausar()

    def executar(self):
        """Executa menu principal"""
        while True:
            self.exibir_menu()

            opcao = input("Escolha uma opção (1-12): ").strip()

            if opcao == "1":
                self.cadastrar_paciente()
            elif opcao == "2":
                self.ver_estatisticas()
            elif opcao == "3":
                self.buscar_paciente()
            elif opcao == "4":
                self.listar_pacientes()
            elif opcao == "5":
                self.editar_paciente()
            elif opcao == "6":
                self.remover_paciente()
            elif opcao == "7":
                self.interface_grafica()
            elif opcao == "8":
                self.verificar_acesso_paciente()
            elif opcao == "9":
                self.gerenciar_fila()
            elif opcao == "10":
                self.fazer_backup()
            elif opcao == "11":
                self.restaurar_backup()
            elif opcao == "12":
                limpar_tela()
                print("\n" + "="*60)
                print("Obrigado por usar Clínica Vida+!")
                print(f"Usuário: {self.usuario}")
                print(f"Data/Hora de saída: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
                print("="*60 + "\n")
                break
            else:
                exibir_erro("Opção inválida!")
                pausar()


# ════════════════════════════════════════════════════════════════════════════
# PROGRAMA PRINCIPAL
# ════════════════════════════════════════════════════════════════════════════

def main():
    """Função principal"""

    # LOGIN OBRIGATÓRIO
    autenticacao = SistemaAutenticacao()

    if not autenticacao.fazer_login():
        # Falha no login - fecha o sistema
        print("\n❌ ACESSO NEGADO - Sistema encerrado.")
        print("="*60 + "\n")
        return False

    # Login bem-sucedido - carrega dados e inicia menu
    clinica = Clinica("Clínica Vida+")
    GerenciadorBackup.carregar_backup(clinica)

    menu = MenuConsole(clinica, autenticacao.usuario_logado)
    menu.executar()

    return True


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✗ Programa interrompido pelo usuário.")
    except Exception as e:
        print(f"\n✗ Erro fatal: {e}")

# interface_gui_melhorada.py
# Interface Gráfica Profissional com Integração Completa - Clínica Vida+
# Todos os 4 Passos Integrados - VERSÃO CORRIGIDA FINAL

from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog

try:
    from config_dados.utils import validar_nome, validar_idade, validar_telefone
    from config_dados.modelos import Paciente
    from config_dados.persistencia import GerenciadorBackup
    from config_dados.controle_acesso import ControladorAcesso
    from config_dados.fila_atendimento import FilaAtendimento
except ImportError as e:
    print(f"Aviso: Alguns módulos não foram importados: {e}")



class InterfaceGraficaMelhorada:
    """Interface gráfica profissional com design moderno"""

    def __init__(self, clinica, usuario):
        self.clinica = clinica
        self.usuario = usuario
        self.paciente_selecionado = None

        # Módulos dos passos
        self.controlador_acesso = ControladorAcesso()
        self.fila_atendimento = FilaAtendimento()

        # Registrar pacientes na fila
        try:
            self.fila_atendimento.registrar_pacientes_sistema(self.clinica)
        except Exception as e:
            print(f"Aviso ao registrar pacientes na fila: {e}")

        # Configurar janela
        self.janela = tk.Tk()
        self.janela.title("🏥 Clínica Vida+ - Sistema Integrado de Gestão")
        self.janela.geometry("1400x800")
        self.janela.minsize(1200, 700)

        # Tema - Design System Moderno
        self.tema = {
            'primaria': '#1f6f78',      # Teal escuro
            'secundaria': '#2a9d8f',    # Teal médio
            'sucesso': '#06a77d',       # Verde
            'erro': '#d62828',          # Vermelho
            'aviso': '#f77f00',         # Laranja
            'info': '#457b9d',          # Azul
            'fundo': '#f8f9fa',         # Branco sujo
            'fundo_dark': '#1a1a1a',    # Preto
            'texto': '#2c3e50',         # Cinza escuro
            'texto_claro': '#ecf0f1',   # Branco
            'borda': '#e0e0e0',         # Cinza claro
        }

        # Estilo visual
        self.janela.configure(bg=self.tema['fundo'])
        self.configurar_estilos()
        self.criar_interface()

    def configurar_estilos(self):
        """Configura estilos globais do ttk"""
        style = ttk.Style()
        style.theme_use('clam')

        # Estilo para Treeview
        style.configure('Treeview',
                       rowheight=28,
                       font=('Segoe UI', 10),
                       background='white',
                       foreground=self.tema['texto'])
        style.configure('Treeview.Heading',
                       font=('Segoe UI', 11, 'bold'),
                       foreground=self.tema['primaria'])
        style.map('Treeview', background=[('selected', self.tema['secundaria'])])

        # Estilo para Notebook (abas)
        style.configure('TNotebook',
                       background=self.tema['fundo'],
                       borderwidth=0)
        style.configure('TNotebook.Tab',
                       font=('Segoe UI', 10),
                       padding=[15, 10])
        style.map('TNotebook.Tab',
                 background=[('selected', self.tema['primaria'])],
                 foreground=[('selected', 'white')])

    def criar_interface(self):
        """Cria layout principal com abas"""

        # CABEÇALHO
        frame_header = tk.Frame(self.janela, bg=self.tema['primaria'], height=80)
        frame_header.pack(fill=tk.X, side=tk.TOP)
        frame_header.pack_propagate(False)

        # Logo e título
        frame_titulo = tk.Frame(frame_header, bg=self.tema['primaria'])
        frame_titulo.pack(side=tk.LEFT, padx=20, pady=15)

        tk.Label(frame_titulo, text="🏥 CLÍNICA VIDA+",
                font=('Segoe UI', 24, 'bold'),
                fg='white', bg=self.tema['primaria']).pack()

        # Info do usuário
        frame_user = tk.Frame(frame_header, bg=self.tema['primaria'])
        frame_user.pack(side=tk.RIGHT, padx=20, pady=15)

        tk.Label(frame_user, text=f"👤 {self.usuario}",
                font=('Segoe UI', 10),
                fg='white', bg=self.tema['primaria']).pack()

        tk.Label(frame_user, 
                text=f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}",
                font=('Segoe UI', 9),
                fg=self.tema['fundo'], bg=self.tema['primaria']).pack()

        # ABAS PRINCIPAIS
        self.notebook = ttk.Notebook(self.janela)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Aba 1: Gestão de Pacientes
        self.criar_aba_gestao()

        # Aba 2: Controle de Acesso
        self.criar_aba_acesso()

        # Aba 3: Fila de Atendimento
        self.criar_aba_fila()

        # Aba 4: Ferramentas
        self.criar_aba_ferramentas()

        # RODAPÉ
        frame_footer = tk.Frame(self.janela, bg=self.tema['borda'], height=40)
        frame_footer.pack(fill=tk.X, side=tk.BOTTOM)
        frame_footer.pack_propagate(False)

        self.label_status = tk.Label(frame_footer,
                                     text="✓ Sistema pronto",
                                     font=('Segoe UI', 9),
                                     fg=self.tema['texto'],
                                     bg=self.tema['borda'])
        self.label_status.pack(pady=8)

        self.atualizar_status()

    # ════════════════════════════════════════════════════════════════════════
    # ABA 1: GESTÃO DE PACIENTES (PASSO 2)
    # ════════════════════════════════════════════════════════════════════════

    def criar_aba_gestao(self):
        """Cria aba de gestão de pacientes"""

        frame_gestao = ttk.Frame(self.notebook)
        self.notebook.add(frame_gestao, text="📋 Gestão de Pacientes")

        # Painel de ferramentas
        frame_toolbar = tk.Frame(frame_gestao, bg=self.tema['fundo'], height=60)
        frame_toolbar.pack(fill=tk.X, padx=10, pady=10)
        frame_toolbar.pack_propagate(False)

        btn_novo = tk.Button(frame_toolbar, text="➕ Novo Paciente",
                            command=self.novo_paciente,
                            bg=self.tema['sucesso'], fg='white',
                            font=('Segoe UI', 10, 'bold'),
                            padx=15, pady=10, relief=tk.FLAT, cursor='hand2')
        btn_novo.pack(side=tk.LEFT, padx=5)

        btn_atualizar = tk.Button(frame_toolbar, text="🔄 Atualizar",
                                 command=self.atualizar_tabela,
                                 bg=self.tema['info'], fg='white',
                                 font=('Segoe UI', 10, 'bold'),
                                 padx=15, pady=10, relief=tk.FLAT, cursor='hand2')
        btn_atualizar.pack(side=tk.LEFT, padx=5)

        # Frame principal
        frame_main = tk.Frame(frame_gestao, bg=self.tema['fundo'])
        frame_main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Tabela
        frame_tabela = tk.Frame(frame_main, bg='white', relief=tk.FLAT, bd=1)
        frame_tabela.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        scrollbar = ttk.Scrollbar(frame_tabela)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(frame_tabela,
                                columns=('Nome', 'Idade', 'Telefone', 'Cadastro'),
                                height=20,
                                yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)

        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('Nome', anchor=tk.W, width=250)
        self.tree.column('Idade', anchor=tk.CENTER, width=80)
        self.tree.column('Telefone', anchor=tk.W, width=150)
        self.tree.column('Cadastro', anchor=tk.CENTER, width=150)

        self.tree.heading('#0', text='')
        self.tree.heading('Nome', text='👤 Nome')
        self.tree.heading('Idade', text='📅 Idade')
        self.tree.heading('Telefone', text='📞 Telefone')
        self.tree.heading('Cadastro', text='📋 Data Cadastro')

        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<ButtonRelease-1>', self.ao_clicar_paciente)

        # Painel lateral
        frame_lateral = tk.Frame(frame_main, bg='white', width=300, relief=tk.FLAT, bd=1)
        frame_lateral.pack(fill=tk.BOTH, side=tk.RIGHT, padx=(10, 0))
        frame_lateral.pack_propagate(False)

        tk.Label(frame_lateral, text='⚙️ Ações',
                font=('Segoe UI', 12, 'bold'),
                bg='white', fg=self.tema['primaria']).pack(pady=10)

        ttk.Separator(frame_lateral, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=10)

        self.btn_editar = tk.Button(frame_lateral, text='✏️ Editar',
                                    command=self.editar_paciente,
                                    bg=self.tema['aviso'], fg='white',
                                    font=('Segoe UI', 10, 'bold'),
                                    padx=15, pady=12, relief=tk.FLAT,
                                    state=tk.DISABLED, cursor='hand2')
        self.btn_editar.pack(fill=tk.X, padx=10, pady=8)

        self.btn_visualizar = tk.Button(frame_lateral, text='👁️ Visualizar',
                                        command=self.visualizar_paciente,
                                        bg=self.tema['info'], fg='white',
                                        font=('Segoe UI', 10, 'bold'),
                                        padx=15, pady=12, relief=tk.FLAT,
                                        state=tk.DISABLED, cursor='hand2')
        self.btn_visualizar.pack(fill=tk.X, padx=10, pady=8)

        self.btn_remover = tk.Button(frame_lateral, text='🗑️ Remover',
                                     command=self.remover_paciente,
                                     bg=self.tema['erro'], fg='white',
                                     font=('Segoe UI', 10, 'bold'),
                                     padx=15, pady=12, relief=tk.FLAT,
                                     state=tk.DISABLED, cursor='hand2')
        self.btn_remover.pack(fill=tk.X, padx=10, pady=8)

        ttk.Separator(frame_lateral, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=10, pady=10)

        tk.Label(frame_lateral, text='📊 Estatísticas',
                font=('Segoe UI', 11, 'bold'),
                bg='white', fg=self.tema['primaria']).pack(pady=10)

        self.label_total = tk.Label(frame_lateral, text='Total: 0',
                                    font=('Segoe UI', 9),
                                    bg='white', fg=self.tema['texto'])
        self.label_total.pack(pady=3)

        self.label_media_idade = tk.Label(frame_lateral, text='Idade Média: --',
                                          font=('Segoe UI', 9),
                                          bg='white', fg=self.tema['texto'])
        self.label_media_idade.pack(pady=3)

        self.atualizar_tabela()

    def novo_paciente(self):
        """Abre diálogo para novo paciente"""

        janela_novo = tk.Toplevel(self.janela)
        janela_novo.title("Novo Paciente")
        janela_novo.geometry("450x400")
        janela_novo.resizable(False, False)
        janela_novo.transient(self.janela)
        janela_novo.grab_set()
        janela_novo.configure(bg=self.tema['fundo'])

        frame_main = tk.Frame(janela_novo, bg='white')
        frame_main.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(frame_main, text="📝 Cadastro de Novo Paciente",
                font=('Segoe UI', 14, 'bold'),
                bg='white', fg=self.tema['primaria']).pack(pady=15)

        ttk.Separator(frame_main, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        tk.Label(frame_main, text="Nome *",
                font=('Segoe UI', 10, 'bold'),
                bg='white', fg=self.tema['texto']).pack(anchor=tk.W, pady=(15, 5))

        entry_nome = tk.Entry(frame_main, font=('Segoe UI', 10), width=40)
        entry_nome.pack(fill=tk.X, pady=5)
        entry_nome.focus()

        tk.Label(frame_main, text="Idade *",
                font=('Segoe UI', 10, 'bold'),
                bg='white', fg=self.tema['texto']).pack(anchor=tk.W, pady=(15, 5))

        entry_idade = tk.Entry(frame_main, font=('Segoe UI', 10), width=40)
        entry_idade.pack(fill=tk.X, pady=5)

        tk.Label(frame_main, text="Telefone *",
                font=('Segoe UI', 10, 'bold'),
                bg='white', fg=self.tema['texto']).pack(anchor=tk.W, pady=(15, 5))

        entry_telefone = tk.Entry(frame_main, font=('Segoe UI', 10), width=40)
        entry_telefone.pack(fill=tk.X, pady=5)

        def salvar():
            nome = entry_nome.get().strip()
            idade = entry_idade.get().strip()
            telefone = entry_telefone.get().strip()

            if not validar_nome(nome):
                messagebox.showerror("Erro", "Nome inválido! Mínimo 3 caracteres.")
                return

            if not validar_idade(idade):
                messagebox.showerror("Erro", "Idade inválida! (1-120)")
                return

            if not validar_telefone(telefone):
                messagebox.showerror("Erro", "Telefone inválido!")
                return

            try:
                paciente = Paciente(nome, int(idade), telefone)
                self.clinica.adicionar_paciente(paciente)
                GerenciadorBackup.fazer_backup(self.clinica)

                # Atualizar fila
                self.fila_atendimento.registrar_pacientes_sistema(self.clinica)

                messagebox.showinfo("Sucesso", f"✓ Paciente {nome} cadastrado!")
                self.atualizar_tabela()
                janela_novo.destroy()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao cadastrar: {e}")

        frame_botoes = tk.Frame(frame_main, bg='white')
        frame_botoes.pack(pady=20, fill=tk.X)

        tk.Button(frame_botoes, text="✓ Salvar",
                 command=salvar,
                 bg=self.tema['sucesso'], fg='white',
                 font=('Segoe UI', 10, 'bold'),
                 padx=30, pady=10, relief=tk.FLAT,
                 cursor='hand2').pack(side=tk.LEFT, padx=5)

        tk.Button(frame_botoes, text="✗ Cancelar",
                 command=janela_novo.destroy,
                 bg='#999', fg='white',
                 font=('Segoe UI', 10, 'bold'),
                 padx=30, pady=10, relief=tk.FLAT,
                 cursor='hand2').pack(side=tk.LEFT, padx=5)

    def ao_clicar_paciente(self, event):
        """Ao selecionar um paciente na tabela"""
        try:
            selecionado = self.tree.selection()

            if selecionado:
                item = selecionado[0]
                valores = self.tree.item(item)['values']
                self.paciente_selecionado = valores[0]

                self.btn_editar.config(state=tk.NORMAL)
                self.btn_visualizar.config(state=tk.NORMAL)
                self.btn_remover.config(state=tk.NORMAL)

                self.label_status.config(text=f"✓ Paciente selecionado: {self.paciente_selecionado}")
            else:
                self.paciente_selecionado = None
                self.btn_editar.config(state=tk.DISABLED)
                self.btn_visualizar.config(state=tk.DISABLED)
                self.btn_remover.config(state=tk.DISABLED)
        except Exception as e:
            print(f"Erro ao clicar: {e}")

    def editar_paciente(self):
        """Edita paciente selecionado"""

        if not self.paciente_selecionado:
            messagebox.showwarning("Aviso", "Selecione um paciente!")
            return

        try:
            paciente = self.clinica.buscar_paciente_exato(self.paciente_selecionado)
            if not paciente:
                messagebox.showerror("Erro", "Paciente não encontrado!")
                return

            janela_editar = tk.Toplevel(self.janela)
            janela_editar.title(f"Editar - {paciente.nome}")
            janela_editar.geometry("450x400")
            janela_editar.resizable(False, False)
            janela_editar.transient(self.janela)
            janela_editar.grab_set()
            janela_editar.configure(bg=self.tema['fundo'])

            frame_main = tk.Frame(janela_editar, bg='white')
            frame_main.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

            tk.Label(frame_main, text=f"✏️ Editando: {paciente.nome}",
                    font=('Segoe UI', 14, 'bold'),
                    bg='white', fg=self.tema['primaria']).pack(pady=15)

            ttk.Separator(frame_main, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

            tk.Label(frame_main, text="Nome",
                    font=('Segoe UI', 10, 'bold'),
                    bg='white').pack(anchor=tk.W, pady=(15, 5))

            entry_nome = tk.Entry(frame_main, font=('Segoe UI', 10))
            entry_nome.insert(0, paciente.nome)
            entry_nome.pack(fill=tk.X, pady=5)

            tk.Label(frame_main, text="Idade",
                    font=('Segoe UI', 10, 'bold'),
                    bg='white').pack(anchor=tk.W, pady=(15, 5))

            entry_idade = tk.Entry(frame_main, font=('Segoe UI', 10))
            entry_idade.insert(0, str(paciente.idade))
            entry_idade.pack(fill=tk.X, pady=5)

            tk.Label(frame_main, text="Telefone",
                    font=('Segoe UI', 10, 'bold'),
                    bg='white').pack(anchor=tk.W, pady=(15, 5))

            entry_telefone = tk.Entry(frame_main, font=('Segoe UI', 10))
            entry_telefone.insert(0, paciente.telefone)
            entry_telefone.pack(fill=tk.X, pady=5)

            def salvar():
                nome = entry_nome.get().strip()
                idade = entry_idade.get().strip()
                telefone = entry_telefone.get().strip()

                if not validar_nome(nome):
                    messagebox.showerror("Erro", "Nome inválido!")
                    return
                if not validar_idade(idade):
                    messagebox.showerror("Erro", "Idade inválida!")
                    return
                if not validar_telefone(telefone):
                    messagebox.showerror("Erro", "Telefone inválido!")
                    return

                try:
                    paciente.editar("nome", nome)
                    paciente.editar("idade", idade)
                    paciente.editar("telefone", telefone)
                    GerenciadorBackup.fazer_backup(self.clinica)
                    self.fila_atendimento.registrar_pacientes_sistema(self.clinica)

                    messagebox.showinfo("Sucesso", "✓ Paciente atualizado!")
                    self.atualizar_tabela()
                    janela_editar.destroy()
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao editar: {e}")

            frame_botoes = tk.Frame(frame_main, bg='white')
            frame_botoes.pack(pady=20, fill=tk.X)

            tk.Button(frame_botoes, text="✓ Salvar",
                     command=salvar,
                     bg=self.tema['sucesso'], fg='white',
                     font=('Segoe UI', 10, 'bold'),
                     padx=30, pady=10, relief=tk.FLAT).pack(side=tk.LEFT, padx=5)

            tk.Button(frame_botoes, text="✗ Cancelar",
                     command=janela_editar.destroy,
                     bg='#999', fg='white',
                     font=('Segoe UI', 10, 'bold'),
                     padx=30, pady=10, relief=tk.FLAT).pack(side=tk.LEFT, padx=5)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao editar paciente: {e}")

    def visualizar_paciente(self):
        """Visualiza detalhes do paciente"""

        if not self.paciente_selecionado:
            messagebox.showwarning("Aviso", "Selecione um paciente!")
            return

        try:
            paciente = self.clinica.buscar_paciente_exato(self.paciente_selecionado)
            if not paciente:
                messagebox.showerror("Erro", "Paciente não encontrado!")
                return

            janela_vis = tk.Toplevel(self.janela)
            janela_vis.title(f"Detalhes - {paciente.nome}")
            janela_vis.geometry("500x450")
            janela_vis.resizable(False, False)
            janela_vis.transient(self.janela)
            janela_vis.grab_set()
            janela_vis.configure(bg=self.tema['fundo'])

            frame_main = tk.Frame(janela_vis, bg='white')
            frame_main.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

            info_text = f"""INFORMAÇÕES DO PACIENTE

Nome:
{paciente.nome}

Idade:
{paciente.idade} anos

Telefone:
{paciente.telefone}

Data de Cadastro:
{paciente.data_cadastro}
"""

            text_widget = tk.Text(frame_main, font=('Courier', 10),
                                 bg=self.tema['fundo'], fg=self.tema['texto'],
                                 relief=tk.FLAT, bd=0, height=15, width=50)
            text_widget.pack(fill=tk.BOTH, expand=True, pady=10)
            text_widget.insert(tk.END, info_text)
            text_widget.config(state=tk.DISABLED)

            tk.Button(janela_vis, text="Fechar",
                     command=janela_vis.destroy,
                     bg=self.tema['primaria'], fg='white',
                     font=('Segoe UI', 10, 'bold'),
                     padx=30, pady=10, relief=tk.FLAT).pack(pady=15)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao visualizar: {e}")

    def remover_paciente(self):
        """Remove paciente com confirmação"""

        if not self.paciente_selecionado:
            messagebox.showwarning("Aviso", "Selecione um paciente!")
            return

        try:
            if messagebox.askyesno("Confirmar Remoção",
                                  f"Remover {self.paciente_selecionado}?\n\nEsta ação não pode ser desfeita!"):
                self.clinica.remover_paciente(self.paciente_selecionado)
                GerenciadorBackup.fazer_backup(self.clinica)
                self.fila_atendimento.registrar_pacientes_sistema(self.clinica)
                messagebox.showinfo("Sucesso", "✓ Paciente removido!")
                self.atualizar_tabela()
                self.paciente_selecionado = None
                self.btn_editar.config(state=tk.DISABLED)
                self.btn_visualizar.config(state=tk.DISABLED)
                self.btn_remover.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao remover: {e}")

    def atualizar_tabela(self):
        """Atualiza tabela de pacientes"""
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)

            pacientes = self.clinica.listar_pacientes()
            for paciente in pacientes:
                self.tree.insert('', tk.END,
                               values=(paciente.nome, paciente.idade,
                                     paciente.telefone, paciente.data_cadastro))

            self.atualizar_status()
        except Exception as e:
            print(f"Erro ao atualizar tabela: {e}")

    # ════════════════════════════════════════════════════════════════════════
    # ABA 2: CONTROLE DE ACESSO (PASSO 3)
    # ════════════════════════════════════════════════════════════════════════

    def criar_aba_acesso(self):
        """Cria aba de controle de acesso"""

        frame_acesso = ttk.Frame(self.notebook)
        self.notebook.add(frame_acesso, text="🔐 Controle de Acesso")

        frame_main = tk.Frame(frame_acesso, bg=self.tema['fundo'])
        frame_main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        frame_instrucoes = tk.Frame(frame_main, bg='white', relief=tk.FLAT, bd=1)
        frame_instrucoes.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(frame_instrucoes, 
                text="🔐 Verificação de Acesso - Lógica Booleana (A, B, C, D)",
                font=('Segoe UI', 12, 'bold'),
                bg='white', fg=self.tema['primaria']).pack(pady=10)

        instrucoes_text = """A = Paciente tem agendamento marcado
B = Paciente tem documentos OK (RG/CPF válidos)
C = Há médico disponível no horário
D = Paciente está em dia com pagamentos

CONSULTA NORMAL: (A ∧ B ∧ C) ∨ (B ∧ C ∧ D)
EMERGÊNCIA: C ∧ (B ∨ D)"""

        tk.Label(frame_instrucoes, text=instrucoes_text,
                font=('Courier', 9),
                bg='white', fg=self.tema['texto'],
                justify=tk.LEFT).pack(padx=10, pady=10)

        ttk.Separator(frame_main, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        frame_entrada = tk.Frame(frame_main, bg='white', relief=tk.FLAT, bd=1)
        frame_entrada.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(frame_entrada, text="📝 Inserir Dados do Paciente",
                font=('Segoe UI', 11, 'bold'),
                bg='white', fg=self.tema['primaria']).pack(pady=10)

        frame_campos = tk.Frame(frame_entrada, bg='white')
        frame_campos.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(frame_campos, text="Nome:", font=('Segoe UI', 10), bg='white').pack(anchor=tk.W)
        entry_nome_acesso = tk.Entry(frame_campos, font=('Segoe UI', 10), width=40)
        entry_nome_acesso.pack(fill=tk.X, pady=5)

        frame_condicoes = tk.Frame(frame_entrada, bg='white')
        frame_condicoes.pack(fill=tk.X, padx=15, pady=10)

        var_A = tk.BooleanVar()
        var_B = tk.BooleanVar()
        var_C = tk.BooleanVar()
        var_D = tk.BooleanVar()

        tk.Checkbutton(frame_condicoes, text="A - Tem agendamento", variable=var_A,
                      font=('Segoe UI', 10), bg='white').pack(anchor=tk.W, pady=5)
        tk.Checkbutton(frame_condicoes, text="B - Documentos OK", variable=var_B,
                      font=('Segoe UI', 10), bg='white').pack(anchor=tk.W, pady=5)
        tk.Checkbutton(frame_condicoes, text="C - Médico disponível", variable=var_C,
                      font=('Segoe UI', 10), bg='white').pack(anchor=tk.W, pady=5)
        tk.Checkbutton(frame_condicoes, text="D - Pagamentos em dia", variable=var_D,
                      font=('Segoe UI', 10), bg='white').pack(anchor=tk.W, pady=5)

        frame_tipo = tk.Frame(frame_entrada, bg='white')
        frame_tipo.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(frame_tipo, text="Tipo de Atendimento:", font=('Segoe UI', 10), bg='white').pack(anchor=tk.W)

        var_tipo = tk.StringVar(value="normal")
        tk.Radiobutton(frame_tipo, text="Normal", variable=var_tipo, value="normal",
                      font=('Segoe UI', 10), bg='white').pack(anchor=tk.W, pady=3)
        tk.Radiobutton(frame_tipo, text="Emergência", variable=var_tipo, value="emergencia",
                      font=('Segoe UI', 10), bg='white').pack(anchor=tk.W, pady=3)

        frame_resultado = tk.Frame(frame_entrada, bg=self.tema['fundo'], relief=tk.FLAT, bd=1)
        frame_resultado.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        text_resultado = tk.Text(frame_resultado, font=('Courier', 9),
                                height=10, width=60, bg=self.tema['fundo'],
                                fg=self.tema['texto'], relief=tk.FLAT, bd=0)
        text_resultado.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        def verificar_acesso():
            try:
                nome = entry_nome_acesso.get().strip()

                if not nome:
                    messagebox.showwarning("Aviso", "Digite o nome do paciente!")
                    return

                self.controlador_acesso.adicionar_paciente(
                    nome,
                    var_A.get(),
                    var_B.get(),
                    var_C.get(),
                    var_D.get(),
                    var_tipo.get()
                )

                pode_atender, motivo, condicoes = self.controlador_acesso.pode_ser_atendido(nome)

                resultado = f"""RESULTADO DA VERIFICAÇÃO

Paciente: {nome}
Tipo: {var_tipo.get().upper()}

CONDIÇÕES:
  A (Agendamento): {"SIM" if var_A.get() else "NÃO"}
  B (Documentos): {"SIM" if var_B.get() else "NÃO"}
  C (Médico): {"SIM" if var_C.get() else "NÃO"}
  D (Pagamentos): {"SIM" if var_D.get() else "NÃO"}

DECISÃO: {"✓ APROVADO" if pode_atender else "✗ NEGADO"}"""

                text_resultado.config(state=tk.NORMAL)
                text_resultado.delete('1.0', tk.END)
                text_resultado.insert(tk.END, resultado)
                text_resultado.config(state=tk.DISABLED)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao verificar: {e}")

        frame_botoes = tk.Frame(frame_entrada, bg='white')
        frame_botoes.pack(fill=tk.X, padx=15, pady=10)

        tk.Button(frame_botoes, text="✓ Verificar Acesso",
                 command=verificar_acesso,
                 bg=self.tema['sucesso'], fg='white',
                 font=('Segoe UI', 10, 'bold'),
                 padx=20, pady=10, relief=tk.FLAT,
                 cursor='hand2').pack(side=tk.LEFT, padx=5)

    # ════════════════════════════════════════════════════════════════════════
    # ABA 3: FILA DE ATENDIMENTO (PASSO 4)
    # ════════════════════════════════════════════════════════════════════════

    def criar_aba_fila(self):
        """Cria aba de fila de atendimento"""

        frame_fila = ttk.Frame(self.notebook)
        self.notebook.add(frame_fila, text="📋 Fila de Atendimento")

        frame_main = tk.Frame(frame_fila, bg=self.tema['fundo'])
        frame_main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        frame_inserir = tk.Frame(frame_main, bg='white', relief=tk.FLAT, bd=1)
        frame_inserir.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        tk.Label(frame_inserir, text="➕ Inserir Paciente na Fila",
                font=('Segoe UI', 11, 'bold'),
                bg='white', fg=self.tema['primaria']).pack(pady=10)

        frame_campos_fila = tk.Frame(frame_inserir, bg='white')
        frame_campos_fila.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(frame_campos_fila, text="Selecione Paciente Cadastrado *:",
                font=('Segoe UI', 10, 'bold'), bg='white').pack(anchor=tk.W, pady=5)

        try:
            pacientes_nomes = [p.nome for p in self.clinica.listar_pacientes()]
        except:
            pacientes_nomes = []

        combo_pacientes = ttk.Combobox(frame_campos_fila, values=pacientes_nomes,
                                       font=('Segoe UI', 10), state='readonly', width=30)
        combo_pacientes.pack(fill=tk.X, pady=5)

        frame_fila_visual = tk.Frame(frame_inserir, bg=self.tema['fundo'], height=200)
        frame_fila_visual.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        tk.Label(frame_fila_visual, text="📊 Fila Atual (FIFO)",
                font=('Segoe UI', 10, 'bold'),
                bg=self.tema['fundo'], fg=self.tema['texto']).pack()

        self.text_fila_visual = tk.Text(frame_fila_visual, font=('Courier', 9),
                                      height=10, width=40, bg=self.tema['fundo'],
                                      fg=self.tema['texto'], relief=tk.FLAT, bd=0)
        self.text_fila_visual.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.text_fila_visual.insert(tk.END, "Fila vazia")
        self.text_fila_visual.config(state=tk.DISABLED)

        def inserir_fila():
            try:
                nome_selecionado = combo_pacientes.get()

                if not nome_selecionado:
                    messagebox.showwarning("Aviso", "Selecione um paciente cadastrado!")
                    return

                paciente = self.clinica.buscar_paciente_exato(nome_selecionado)
                if not paciente:
                    messagebox.showerror("Erro", "Paciente não encontrado!")
                    return

                sucesso, msg = self.fila_atendimento.inserir_paciente(nome_selecionado, paciente.telefone)

                if sucesso:
                    messagebox.showinfo("Sucesso", msg)
                    combo_pacientes.set('')
                    self.atualizar_fila_visual(self.text_fila_visual)
                else:
                    messagebox.showerror("Erro", msg)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao inserir na fila: {e}")

        def chamar_proximo():
            try:
                paciente, msg = self.fila_atendimento.remover_proximo()

                if paciente:
                    messagebox.showinfo("Chamada", f"{msg}{paciente.nome}Telefone: {paciente.cpf}")
                    self.atualizar_fila_visual(self.text_fila_visual)
                else:
                    messagebox.showerror("Erro", msg)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao chamar próximo: {e}")

        frame_botoes_fila = tk.Frame(frame_inserir, bg='white')
        frame_botoes_fila.pack(fill=tk.X, padx=15, pady=10)

        tk.Button(frame_botoes_fila, text="➕ Inserir",
                 command=inserir_fila,
                 bg=self.tema['sucesso'], fg='white',
                 font=('Segoe UI', 10, 'bold'),
                 padx=15, pady=10, relief=tk.FLAT,
                 cursor='hand2').pack(fill=tk.X, pady=5)

        tk.Button(frame_botoes_fila, text="📢 Chamar Próximo",
                 command=chamar_proximo,
                 bg=self.tema['info'], fg='white',
                 font=('Segoe UI', 10, 'bold'),
                 padx=15, pady=10, relief=tk.FLAT,
                 cursor='hand2').pack(fill=tk.X, pady=5)

        frame_info_fila = tk.Frame(frame_main, bg='white', relief=tk.FLAT, bd=1, width=300)
        frame_info_fila.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(5, 0))
        frame_info_fila.pack_propagate(False)

        tk.Label(frame_info_fila, text="ℹ️ Informações",
                font=('Segoe UI', 11, 'bold'),
                bg='white', fg=self.tema['primaria']).pack(pady=10)

        text_info_fila = tk.Text(frame_info_fila, font=('Segoe UI', 9),
                                height=25, width=35, bg=self.tema['fundo'],
                                fg=self.tema['texto'], relief=tk.FLAT, bd=0)
        text_info_fila.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_info_fila.insert(tk.END, """FILA DE ATENDIMENTO (FIFO)

Estrutura: Queue
First In First Out

✓ Apenas pacientes cadastrados
✓ Máximo 3 pacientes
✓ Sem duplicatas
✓ Histórico mantido

Operações:
• Inserir: O(1)
• Remover: O(1)
• Visualizar: O(n)

Fluxo:
1. Selecione paciente
2. Clique em Inserir
3. Paciente entra na fila
4. Chame próximo (FIFO)
5. Histórico registra""")
        text_info_fila.config(state=tk.DISABLED)

        self.atualizar_fila_visual(self.text_fila_visual)

    def atualizar_fila_visual(self, text_widget):
        """Atualiza visualização da fila"""
        try:
            text_widget.config(state=tk.NORMAL)
            text_widget.delete('1.0', tk.END)

            if self.fila_atendimento.fila_vazia():
                text_widget.insert(tk.END, "Fila vazia")
            else:
                text_widget.insert(tk.END, f"Pacientes na fila: {self.fila_atendimento.tamanho_fila()}/3")
                text_widget.insert(tk.END, "Posição | Nome")
                text_widget.insert(tk.END, "─────────────────────")

                for i, paciente in enumerate(self.fila_atendimento.fila, 1):
                    text_widget.insert(tk.END, f"{i}      | {paciente.nome}")

            text_widget.config(state=tk.DISABLED)
        except Exception as e:
            print(f"Erro ao atualizar fila visual: {e}")

    # ════════════════════════════════════════════════════════════════════════
    # ABA 4: FERRAMENTAS
    # ════════════════════════════════════════════════════════════════════════

    def criar_aba_ferramentas(self):
        """Cria aba de ferramentas"""

        frame_ferramentas = ttk.Frame(self.notebook)
        self.notebook.add(frame_ferramentas, text="🛠️ Ferramentas")

        frame_main = tk.Frame(frame_ferramentas, bg=self.tema['fundo'])
        frame_main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        frame_backup = tk.Frame(frame_main, bg='white', relief=tk.FLAT, bd=1)
        frame_backup.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(frame_backup, text="💾 Backup e Restauração",
                font=('Segoe UI', 12, 'bold'),
                bg='white', fg=self.tema['primaria']).pack(pady=10)

        frame_botoes_backup = tk.Frame(frame_backup, bg='white')
        frame_botoes_backup.pack(fill=tk.X, padx=15, pady=10)

        def fazer_backup():
            try:
                sucesso, msg = GerenciadorBackup.fazer_backup(self.clinica)
                if sucesso:
                    messagebox.showinfo("Sucesso", msg)
                else:
                    messagebox.showerror("Erro", msg)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao fazer backup: {e}")

        def restaurar_backup():
            try:
                backups = GerenciadorBackup.listar_backups()
                if not backups:
                    messagebox.showerror("Erro", "Nenhum backup encontrado!")
                    return

                if backups:
                    sucesso, msg = GerenciadorBackup.restaurar_backup(self.clinica, backups[0]['arquivo'])
                    if sucesso:
                        messagebox.showinfo("Sucesso", msg)
                        self.fila_atendimento.registrar_pacientes_sistema(self.clinica)
                        self.atualizar_tabela()
                    else:
                        messagebox.showerror("Erro", msg)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao restaurar: {e}")

        tk.Button(frame_botoes_backup, text="💾 Fazer Backup",
                 command=fazer_backup,
                 bg=self.tema['info'], fg='white',
                 font=('Segoe UI', 10, 'bold'),
                 padx=20, pady=10, relief=tk.FLAT,
                 cursor='hand2').pack(side=tk.LEFT, padx=5)

        tk.Button(frame_botoes_backup, text="📂 Restaurar",
                 command=restaurar_backup,
                 bg=self.tema['aviso'], fg='white',
                 font=('Segoe UI', 10, 'bold'),
                 padx=20, pady=10, relief=tk.FLAT,
                 cursor='hand2').pack(side=tk.LEFT, padx=5)

        frame_info_sistema = tk.Frame(frame_main, bg='white', relief=tk.FLAT, bd=1)
        frame_info_sistema.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(frame_info_sistema, text="ℹ️ Informações do Sistema",
                font=('Segoe UI', 12, 'bold'),
                bg='white', fg=self.tema['primaria']).pack(pady=10)

        try:
            total = self.clinica.total_pacientes()
            info_sistema = f"""INFORMAÇÕES DO SISTEMA

Usuário Logado: {self.usuario}

Estatísticas:
  • Total de Pacientes: {total}
  • Pacientes na Fila: {self.fila_atendimento.tamanho_fila()}/3

Versão: 1.0.0 Completa
Passos Implementados: 4/5
  ✓ Autenticação
  ✓ CRUD Pacientes
  ✓ Controle de Acesso
  ✓ Fila de Atendimento

Integrações:
  ✓ Interface GUI Moderna
  ✓ Backup/Restauração
  ✓ Validações Completas
  ✓ Design System Profissional

Desenvolvido para: Clínica Vida+
Status: Produção"""
        except:
            info_sistema = "Erro ao carregar informações do sistema"

        text_info = tk.Text(frame_info_sistema, font=('Courier', 9),
                           bg=self.tema['fundo'], fg=self.tema['texto'],
                           height=20, width=60, relief=tk.FLAT, bd=0)
        text_info.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        text_info.insert(tk.END, info_sistema)
        text_info.config(state=tk.DISABLED)

    def atualizar_status(self):
        """Atualiza status bar"""
        try:
            total = self.clinica.total_pacientes()

            if total > 0:
                stats = self.clinica.gerar_relatorio_estatisticas()
                self.label_status.config(
                    text=f"✓ Sistema pronto | {total} pacientes | Idade média: {stats['idade_media']:.1f} anos"
                )

                if hasattr(self, 'label_total'):
                    self.label_total.config(text=f"Total: {total}")
                if hasattr(self, 'label_media_idade'):
                    self.label_media_idade.config(
                        text=f"Idade Média: {stats['idade_media']:.1f}"
                    )
            else:
                self.label_status.config(
                    text="✓ Sistema pronto | Nenhum paciente cadastrado"
                )
        except Exception as e:
            print(f"Erro ao atualizar status: {e}")

    def iniciar(self):
        """Inicia a interface gráfica"""
        self.janela.mainloop()
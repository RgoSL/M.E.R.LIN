# Classe de Controle da Palheta de Cores Exclusiva Para os Elementos Pós Configurações

from customtkinter import get_appearance_mode

class CoresTema:
    
    # Nossas Cores Tradicionais
    ROXO_PRINCIPAL = "#654E82"
    ROXO_HOVER = "#56397C"
    ROXO_ESCURO = "#432D5D"
    ROXO_BORDA = "#644C81"
    ROXO_MAIS_ESCURO = "#3A205A"
    ROXO_PROFUNDO = "#200B3A"
    
    DOURADO = "#F9B14F"
    DOURADO_HOVER = "#CE8E34"
    
    LILAS_CLARO = "#E6C8FA"
    LILAS_MEDIO = "#C58ADE"
    LILAS_BORDA = "#CB91E4"
    
    # Método Para Descobrir o Tema Atual e Retornar os Dicionários com as Cores do Tema
    @staticmethod
    def obter_cores():
        modo = get_appearance_mode()
        
        if modo == "Light": # Dicionário do Tema Claro
            return {
                # Fundos
                "fundo_principal": "#F5F5F5",      # Cinza Claro
                "fundo_secundario": "#FFFFFF",     # Branco
                "fundo_frame": "#E8E8E8",          # Cinza Mais Claro
                "fundo_card": "#FAFAFA",           # Branco OffWhite
                
                # Bordas
                "borda_principal": CoresTema.LILAS_MEDIO,
                "borda_destaque": CoresTema.DOURADO,
                "borda_sutil": "#D0D0D0",
                
                # Textos
                "texto_principal": "#2B2B2B",      # Preto
                "texto_secundario": "#666666",     # Cinza 
                "texto_destaque": CoresTema.ROXO_PRINCIPAL,
                "texto_botao": "#FFFFFF",        
                
                # Botões
                "botao_normal": CoresTema.LILAS_MEDIO,
                "botao_hover": CoresTema.ROXO_PRINCIPAL,
                "botao_secundario": "#D0D0D0",
                "botao_secundario_hover": "#B0B0B0",
                
                # Efeitos
                "selecionado": CoresTema.LILAS_CLARO,
                "hover": CoresTema.LILAS_MEDIO,
                "destaque": CoresTema.DOURADO,
                
                # Scrollbar
                "scrollbar": CoresTema.LILAS_MEDIO,
                "scrollbar_hover": CoresTema.ROXO_PRINCIPAL,
                
                # Transparência
                "transparente": "#654E82",
            }
        else: # Dicionário do Tema Escuro
            return {
                # Fundos
                "fundo_principal": "#2B2B2B",    
                "fundo_secundario": "#1E1E1E",     
                "fundo_frame": CoresTema.ROXO_BORDA,
                "fundo_card": CoresTema.ROXO_MAIS_ESCURO,
                
                # Bordas
                "borda_principal": CoresTema.DOURADO,
                "borda_destaque": CoresTema.DOURADO,
                "borda_sutil": CoresTema.ROXO_ESCURO,
                
                # Textos
                "texto_principal": "#E6C8FA",     
                "texto_secundario": "#D9D9D9",     
                "texto_destaque": CoresTema.DOURADO,
                "texto_botao": "#E6C8FA",
                
                # Botões
                "botao_normal": CoresTema.ROXO_ESCURO,
                "botao_hover": CoresTema.LILAS_MEDIO,
                "botao_secundario": CoresTema.ROXO_BORDA,
                "botao_secundario_hover": CoresTema.ROXO_HOVER,
                
                # Efeitos
                "selecionado": CoresTema.ROXO_HOVER,
                "hover": CoresTema.LILAS_MEDIO,
                "destaque": CoresTema.DOURADO,
                
                # Scrollbar
                "scrollbar": CoresTema.DOURADO,
                "scrollbar_hover": CoresTema.DOURADO_HOVER,
                
                # Transparência
                "transparente": "#654E82",
            }

def cores():
    return CoresTema.obter_cores()

# Cores Constantes Dos 2 Temas
ROXO = CoresTema.ROXO_PRINCIPAL
DOURADO = CoresTema.DOURADO
LILAS = CoresTema.LILAS_CLARO
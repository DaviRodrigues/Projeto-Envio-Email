"""
-Paleta de cores utilizada-

#000000 - Preto
#1693A5 - Azul Escuro
#D8D8C0 - Cinza Esverdeado
#F0F0D8 - Bege Claro
#FFFFFF - Branco
#F5F5F5 - Cinza Claro
#333333 - Cinza Escuro
#D1D1D1 - Cinza
#8ECDDD - Azul Claro
#B3B3B3 - Cinza Médio
#000 - Preto (abreviação padrão)

-- Caso for adicionar ou tirar alguma lembre-se de mexer aqui

"""

# Cores do CSS
cor_preta = "#000000"
cor_azul_escuro = "#1693A5"
cor_cinza_esverdeado = "#D8D8C0"
cor_bege_claro = "#F0F0D8"
cor_branco = "#FFFFFF"
cor_cinza_claro = "#F5F5F5"
cor_cinza_escuro = "#333333"
cor_cinza = "#D1D1D1"
cor_azul_claro = "#8ECDDD"
cor_cinza_medio = "#D6D6D6"
cor_vermelho_escuro = "#BD2626"

# Estilo da página principal
styleMain = f"""
        QWidget {{
            color: {cor_preta};
            background-color: {cor_bege_claro};
        }}

        QLabel {{
            background: transparent;
            font-weight: 400;
            font-size: 12px;
        }}

        QLineEdit {{
            color: {cor_preta};
            border-radius: 8px;
            border: 2px outset {cor_cinza_esverdeado};
            padding: 5px;
            background: {cor_branco};
        }}

        QPushButton {{
            background-color: {cor_cinza_escuro};
            color: #fff;
            font-weight: 500;
            border-radius: 8px;
            padding: 10px 20px;
            margin-top: 10px;
            outline: 0px;
            font-size: 11px;
        }}

        QPushButton:hover {{
            border: 1px inset {cor_cinza_esverdeado};
        }}

        QTextEdit {{
            border: 2px outset {cor_cinza_esverdeado};
            color: {cor_preta};
            background-color: {cor_branco};
            border-radius: 8px;
        }}

        """
import math
import tkinter as tk

from TabelaTransformador import TabelaTransformador

def divide(a, b):
    return round(a / b,1)

def calcula_densidade(potencia_secundaria):
    if potencia_secundaria <= 500:
        return 3
    elif potencia_secundaria <= 1000:
        return 2.5
    else:
        return 2

def calcula_lado_a_lamina_padronizada(secao_magnetica_nucleo):
    if secao_magnetica_nucleo >= 18.8:
        return 5,1880,0.095
    elif secao_magnetica_nucleo >= 12:
        return 4,1200,0.17
    elif secao_magnetica_nucleo >= 9:
        return 3.5,900,0.273
    elif secao_magnetica_nucleo >= 6.75:
        return 3,675,0.38
    elif secao_magnetica_nucleo >= 4.68:
        return 2.5,468,0.516
    elif secao_magnetica_nucleo >= 3:
        return 2,300,0.674
    else:
        return 1.5,168,1.053

def calcula_lado_a_lamina_comprida(secao_magnetica_nucleo):
    if secao_magnetica_nucleo >= 24:
        return 5,3750,1
    else:
        return 4,2400,1.58
    
def calcula_constante_espiras(frequencia):
    if frequencia == 60:
        return 33.5
    elif frequencia == 50:
        return 40
    else:
        return 0
    
def calcula_dados_transformador(frequencia=60,potencia_secundaria = 1000,tensao_primaria = 220,tensao_secundaria = 24):
    try:
        frequencia = float(frequencia)
        potencia_secundaria = float(potencia_secundaria)
        tensao_primaria = float(tensao_primaria)
        tensao_secundaria = float(tensao_secundaria)
    except ValueError:
        # Exibir mensagem de erro para o usuário
        print("Valor inválido detectado. Insira números de ponto flutuante.")

    potencia_primaria = potencia_secundaria * 1.1

    corrente_primaria = divide(potencia_primaria,tensao_primaria)
    corrente_secundaria = divide(potencia_secundaria,tensao_secundaria)

    # Calculo Bitola

    densidade = calcula_densidade(potencia_secundaria)

    secao_condutor_primario = divide(corrente_primaria,densidade)
    secao_condutor_secundario = divide(corrente_secundaria,densidade)

    # Calculo densidades

    densidade_corrente_primaria = divide(corrente_primaria,secao_condutor_primario)
    densidade_corrente_secundaria = divide(corrente_secundaria,secao_condutor_secundario)

    media_densidades = round( (densidade_corrente_primaria + densidade_corrente_secundaria) / 2 ,1 )

    # Calculo laminas
    
    secao_magnetica_nucleo = round(7.5 * math.sqrt(divide(potencia_secundaria, frequencia)), 1)
    
    secao_geometrica_nucleo = round(secao_magnetica_nucleo * 1.1,1);

    lado_a,secao_janela,peso_nucleo = calcula_lado_a_lamina_padronizada(secao_magnetica_nucleo)
    lado_b = round(secao_geometrica_nucleo/lado_a,1)
    
    # Calculo espiras

    constante_espiras = calcula_constante_espiras(frequencia)

    espiras_volt = divide(constante_espiras,secao_magnetica_nucleo)

    numero_espiras_primario = round(tensao_primaria * espiras_volt)
    numero_espiras_secundario = round(tensao_secundaria * espiras_volt * 1.1)

    # Possibilidade execucao

    secao_cobre_enrolado = numero_espiras_primario * secao_condutor_primario + numero_espiras_secundario * secao_condutor_secundario

    possibilidade_execucao = secao_janela / secao_cobre_enrolado

    tipo_lamina = "Padronizada"

    if possibilidade_execucao < 3:
        tipo_lamina = "Comprida"

        # solucao laminas compridas

        # Calculo laminas

        secao_magnetica_nucleo = round(6.5 * math.sqrt(divide(potencia_secundaria, frequencia)), 1)
    
        secao_geometrica_nucleo = round(secao_magnetica_nucleo * 1.1,1);

        lado_a,secao_janela,peso_nucleo = calcula_lado_a_lamina_comprida(secao_magnetica_nucleo)
        lado_b = round(secao_geometrica_nucleo/lado_a,1)

        # Calculo espiras

        constante_espiras = calcula_constante_espiras(frequencia)

        espiras_volt = divide(constante_espiras,secao_magnetica_nucleo)

        numero_espiras_primario = round(tensao_primaria * espiras_volt)
        numero_espiras_secundario = round(tensao_secundaria * espiras_volt * 1.1)

        secao_cobre_enrolado = numero_espiras_primario * secao_condutor_primario + numero_espiras_secundario * secao_condutor_secundario

        possibilidade_execucao = secao_janela / secao_cobre_enrolado

    # Calculo peso
        
    peso_ferro = round(lado_b * peso_nucleo)
        
    comprimento_espira_media = 2 * lado_a + 2 * lado_b + 0.5 * lado_a * 3.14;

    peso_cobre_g = round(divide(secao_cobre_enrolado,100) * comprimento_espira_media * 9,1)

    peso_cobre_kg = divide(peso_cobre_g,1000)

    # Calculo perdas 

    # Perdas do ferro

    coeficiente_material_correntes_parasitas = 4.8
    coeficiente_material_histerese_magnetica = 2.4
    espessura_laminas = 0.5

    coeficiente_perda_especifica = round(coeficiente_material_correntes_parasitas * ((espessura_laminas * frequencia / 50) ** 2) + coeficiente_material_histerese_magnetica * frequencia / 50,1)

    inducao_maxima = 11300

    perda_ferro = round(coeficiente_perda_especifica * ((inducao_maxima / 10000) ** 2),1)
    
    # Perdas do cobre

    perda_cobre = round(2.43 * (media_densidades ** 2) * peso_cobre_kg,1)
    
    # Perdas totais

    perda_total = perda_ferro + perda_cobre

    # Total rendimento

    rendimento = round(potencia_secundaria / (potencia_secundaria + perda_total),2)
    
    dados = dict()
    dados['numero_espiras_primario'] = numero_espiras_primario
    dados['numero_espiras_secundario'] = numero_espiras_secundario
    dados['secao_condutor_primario'] = secao_condutor_primario
    dados['secao_condutor_secundario'] = secao_condutor_secundario
    dados['tipo_lamina'] = tipo_lamina
    dados['qtd_lamina'] = secao_janela
    dados['dimensoes_transformador'] = f"{lado_a} x {lado_b}"
    dados['secao_magnetica_nucleo'] = secao_magnetica_nucleo
    dados['secao_geometrica_nucleo'] = secao_geometrica_nucleo
    dados['peso_ferro'] = peso_ferro
    dados['peso_cobre'] = peso_cobre_kg
    dados['perda_ferro'] = perda_ferro
    dados['perda_cobre'] = perda_cobre
    dados['rendimento'] = rendimento

    return dados   

def mostrar_tabela(root,frequencia,potencia_secundaria,tensao_primaria,tensao_secundaria):
    dados = calcula_dados_transformador(frequencia,potencia_secundaria,tensao_primaria,tensao_secundaria)
    tabela = TabelaTransformador(root,dados)
    tabela.pack()

def main():
    root = tk.Tk()

    root.title("Calculos de transformadores monofasicos")

    input_frame = tk.Frame(root)

    entry_1 = tk.Entry(input_frame)
    entry_2 = tk.Entry(input_frame)
    entry_3 = tk.Entry(input_frame)
    entry_4 = tk.Entry(input_frame)

    tk.Label(input_frame, text="Frequencia (Hz)").grid(column=0, row=0, padx=10, pady=10)

    entry_1.grid(column=1, row=0, padx=10, pady=10)

    tk.Label(input_frame, text="Potencia secundaria (VA)").grid(column=0, row=1, padx=10, pady=10)

    entry_2.grid(column=1, row=1, padx=10, pady=10)

    tk.Label(input_frame, text="Tensao primaria (v)").grid(column=0, row=2, padx=10, pady=10)

    entry_3.grid(column=1, row=2, padx=10, pady=10)

    tk.Label(input_frame, text="Tensao secundaria (v)").grid(column=0, row=3, padx=10, pady=10)

    entry_4.grid(column=1, row=3, padx=10, pady=10)

    button_frame = tk.Frame(root)

    button = tk.Button(button_frame, text="Calcular dados transformador", command=lambda:mostrar_tabela(root,entry_1.get(),entry_2.get(),entry_3.get(),entry_4.get()))

    button.grid(columnspan=2, padx=10, pady=10)
    
    input_frame.pack()
    button_frame.pack()

    # Inicia o loop principal da janela
    root.mainloop()
if __name__ == "__main__":
    main()
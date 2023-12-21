import math

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

    if possibilidade_execucao < 3:
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
    
    print("secao_condutor_primario | corrente_primaria",secao_condutor_primario,corrente_primaria)
    print("secao_condutor_secundario | corrente_secundaria",secao_condutor_secundario,corrente_secundaria)
    print("densidade_corrente_primaria | densidade_corrente_secundaria",densidade_corrente_primaria,densidade_corrente_secundaria)
    print("media_densidades",media_densidades)
    print("secao_magnetica_nucleo",secao_magnetica_nucleo)
    print("secao_geometrica_nucleo",secao_geometrica_nucleo)
    print("lado_a",lado_a)
    print("lado_b",lado_b)
    print("constante_espiras",constante_espiras)
    print("espiras_volt",espiras_volt)
    print("numero_espiras_primario",numero_espiras_primario)
    print("numero_espiras_secundario",numero_espiras_secundario)
    print("secao_cobre_enrolado",secao_cobre_enrolado)
    print("possibilidade_execucao",possibilidade_execucao)
    print("peso_nucleo",peso_nucleo)
    print("peso_ferro",peso_ferro)
    print("peso_cobre",peso_cobre_g)
    print("peso_cobre",peso_cobre_kg)
    print("perda_cobre",perda_cobre)
    print("coeficiente_perda_especifica",coeficiente_perda_especifica)
    print("perda_ferro",perda_ferro)
def main():
    calcula_dados_transformador()
if __name__ == "__main__":
    main()
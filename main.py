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

def calcula_lado_a_lamina(secao_magnetica_nucleo):
    if secao_magnetica_nucleo >= 18.8:
        return 5
    elif secao_magnetica_nucleo >= 12:
        return 4
    elif secao_magnetica_nucleo >= 9:
        return 3.5
    elif secao_magnetica_nucleo >= 6.75:
        return 3
    elif secao_magnetica_nucleo >= 4.68:
        return 2.5
    elif secao_magnetica_nucleo >= 3:
        return 2
    else:
        return 1.5
    
def main():
    frequencia = 60 # Hz
    potencia_secundaria = 1000 # VA
    tensao_primaria = 220 # V
    tensao_secundaria = 24 # V

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

    lado_a = calcula_lado_a_lamina(secao_magnetica_nucleo)
    lado_b = round(secao_geometrica_nucleo/lado_a,1)
    
    print(secao_condutor_primario,corrente_primaria)
    print(secao_condutor_secundario,corrente_secundaria)
    print(densidade_corrente_primaria,densidade_corrente_secundaria)
    print(media_densidades)
    print(secao_magnetica_nucleo)
    print(secao_geometrica_nucleo)
    print(lado_a)
    print(lado_b)

if __name__ == "__main__":
    main()
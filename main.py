import math

def divide(a, b):
    return round(a / b,2)

def calcula_densidade(potencia_secundaria):
    if potencia_secundaria <= 500:
        return 3
    elif potencia_secundaria <= 1000:
        return 2.5
    else:
        return 2

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

    media_densidades = round( (densidade_corrente_primaria + densidade_corrente_secundaria) / 2 ,2 )

    secao_magnetica_nucleo = round(7.5 * math.sqrt(divide(potencia_secundaria, frequencia)), 2)

    secao_geometrica_nucleo = secao_magnetica_nucleo * 1.1;

    print(secao_condutor_primario,corrente_primaria)
    print(secao_condutor_secundario,corrente_secundaria)
    print(densidade_corrente_primaria,densidade_corrente_secundaria)
    print(media_densidades)
    print(secao_magnetica_nucleo)
    print(secao_geometrica_nucleo)

if __name__ == "__main__":
    main()
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
import tkinter.ttk as ttk

class PlotCorrenteMagnetizacao(tk.Frame):

    def __init__(self, master=None, frequencia=60, potencia_secundaria=1000, tensao_primaria=220, tensao_secundaria=24, dados=None):
        super().__init__(master)
        try:
            frequencia = float(frequencia)
            potencia_secundaria = float(potencia_secundaria)
            tensao_primaria = float(tensao_primaria)
            tensao_secundaria = float(tensao_secundaria)
        except ValueError:
            # Exibir mensagem de erro para o usuário
            print("Valor inválido detectado. Insira números de ponto flutuante.")

        self.dados = dados
        self.frequencia = frequencia
        self.potencia_secundaria = potencia_secundaria
        self.tensao_primaria = tensao_primaria
        self.tensao_secundaria = tensao_secundaria
        self.plot_corrente_magnetizacao()

    def plot_corrente_magnetizacao(self):

        # Parâmetros do transformador

        Vp = self.tensao_primaria  # Tensão Primária em Volts
        Vs = self.tensao_secundaria   # Tensão Secundária em Volts
        Potencia = self.potencia_secundaria  # Potência da carga em VA

        # Número de espiras do enrolamento primário
        Np = self.dados['Número de Espiras do Enrolamento Primário']

        # Número de espiras do enrolamento secundário
        #Ns = (Vs/Vp) * Np
        Ns = self.dados['Número de Espiras do Enrolamento Secundário']

        # Resistência do enrolamento primário (calculada com base na potência)
        Rp = Vp**2 / Potencia

        # Frequência
        f = self.frequencia  # Hz

        # Período
        T = 1/f

        # Tempo de simulação
        tempo_simulacao = np.arange(0, 0.34, 1/3000.0)

        # Corrente de magnetização considerando a resistência e relação de transformação
        corrente_magnetizacao = (Ns/Np) * (1/Rp) * np.sin(2 * np.pi * f * tempo_simulacao)

        # Plotando a corrente de magnetização
        plt.plot(tempo_simulacao, corrente_magnetizacao)
        plt.title('Corrente de Magnetização ao longo do tempo')
        plt.xlabel('Tempo (s)')
        plt.ylabel('Corrente (A)')
        plt.grid(True)
        plt.show()

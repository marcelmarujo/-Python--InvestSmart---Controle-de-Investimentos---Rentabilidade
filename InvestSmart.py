import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.table import Table


class Investimento:
    def __init__(self, valor_inicial, taxa_juros_anual, contribuicao_mensal, anos):
        self.valor_inicial = valor_inicial
        self.taxa_juros_anual = taxa_juros_anual
        self.contribuicao_mensal = contribuicao_mensal
        self.anos = anos

    def calcular_valor_futuro(self):
        valor = self.valor_inicial
        taxa_juros_mensal = self.taxa_juros_anual / 12 / 100
        meses = self.anos * 12

        for mes in range(meses):
            valor = valor * (1 + taxa_juros_mensal) + self.contribuicao_mensal

        return valor

    def projetar_crescimento(self):
        valores = [self.valor_inicial]
        valor = self.valor_inicial
        taxa_juros_mensal = self.taxa_juros_anual / 12 / 100
        meses = self.anos * 12

        for mes in range(meses):
            valor = valor * (1 + taxa_juros_mensal) + self.contribuicao_mensal
            valores.append(valor)

        return valores

    def mostrar_detalhes(self):
        valor_final = self.calcular_valor_futuro()
        valor_investido = self.valor_inicial + \
            (self.contribuicao_mensal * self.anos * 12)
        rendimentos = valor_final - valor_investido
        rentabilidade_acumulada = ((valor_final / valor_investido) - 1) * 100
        rentabilidade_media_anual = rendimentos / self.anos

        detalhes = {
            "Meu Patrimônio Total no Futuro": f"R$ {valor_final:,.0f}",
            "Tempo total do investimento": f"{self.anos} anos",
            "Rentabilidade total acumulada": f"{rentabilidade_acumulada:.2f}%",
            "Valor investido total": f"R$ {valor_investido:,.0f}",
            "Valor de rendimentos total": f"R$ {rendimentos:,.0f}",
            "Rentabilidade média anual": f"R$ {rentabilidade_media_anual:,.0f}"
        }

        print("Detalhes do Investimento:")
        for chave, valor in detalhes.items():
            print(f"{chave}: {valor}")

        return detalhes

    @staticmethod
    def formatar_valores(valor):
        if valor >= 1_000_000:
            return f'R$ {valor / 1_000_000:.2f} Milhão'
        elif valor >= 1_000:
            return f'R$ {valor / 1_000:.0f} Mil'
        else:
            return f'R$ {valor:.0f}'

    @staticmethod
    def comparar_investimentos(investimentos, MeuInvestimento=None):
        fig, ax = plt.subplots(figsize=(12, 8))

        if MeuInvestimento:
            crescimento_normal = MeuInvestimento.projetar_crescimento()
            anos = range(MeuInvestimento.anos + 1)
            ax.plot(anos, crescimento_normal[::12],
                    linewidth=2.5, label='Meu Investimento')
            ax.text(MeuInvestimento.anos, crescimento_normal[-1], Investimento.formatar_valores(
                crescimento_normal[-1]), fontsize=9, verticalalignment='bottom')

        for investimento in investimentos:
            crescimento = investimento.projetar_crescimento()
            label = 'Investimento Conservador' if investimento.taxa_juros_anual == 5 else 'Investimento Arrojado'
            ax.plot(range(investimento.anos + 1),
                    crescimento[::12], label=label)
            ax.text(investimento.anos, crescimento[-1], Investimento.formatar_valores(
                crescimento[-1]), fontsize=9, verticalalignment='bottom')

        ax.set_title('Comparação de Crescimento de Investimentos')
        ax.set_xlabel('Anos')
        ax.set_ylabel('Valor do Investimento')
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(
            lambda x, _: Investimento.formatar_valores(x)))
        ax.legend()
        ax.grid(True)

        # Adicionar tabela com detalhes
        detalhes = MeuInvestimento.mostrar_detalhes()
        col_labels = list(detalhes.keys())
        table_data = [[value] for value in detalhes.values()]
        table = Table(ax, bbox=[0, -0.4, 1, 0.3])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1.5)

        # Adicionar as células da tabela
        for i, (label, data) in enumerate(zip(col_labels, table_data)):
            table.add_cell(i, 0, width=0.5, height=0.1, text=label,
                           loc='right', edgecolor='none', facecolor='none')
            table.add_cell(i, 1, width=0.5, height=0.1,
                           text=data[0], loc='left', edgecolor='none', facecolor='none')

        ax.add_table(table)

        plt.subplots_adjust(top=0.85, bottom=0.3)
        plt.show()


# Parâmetros do investimento
valor_inicial = 100000
taxa_juros_anual = 10
contribuicao_mensal = 3000
anos = 10

# Criação do objeto de investimento
MeuInvestimento = Investimento(
    valor_inicial, taxa_juros_anual, contribuicao_mensal, anos)

# Mostrar detalhes do investimento normal
detalhes_investimento = MeuInvestimento.mostrar_detalhes()

# Comparação de diferentes cenários de investimento
investimentoConservador = Investimento(100000, 7, 3000, 10)
investimentoArrojado = Investimento(100000, 12, 3000, 10)

Investimento.comparar_investimentos(
    [investimentoConservador, investimentoArrojado], MeuInvestimento)
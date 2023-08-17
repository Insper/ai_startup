import tabulate
import pandas as pd

t1 = pd.read_excel('plano-de-aulas.xlsx')
#t1['Data'] = t1['Data'].apply(lambda x: x.strftime('%d/%m'))

with open('docs/_snippets/plano_aula.md', 'w') as f:
    tabela_str = tabulate.tabulate(t1[['Data', 'Questão/Problema/Desafio',
'Fundamentos / Conteúdo', 'Evidências de Aprendizado', 'Programação/Atividades']], headers=['Data', 'Questão',
'Conteúdo', 'Evidências de Aprendizado', 'Atividades'], tablefmt='pipe', showindex=False)
    f.write(tabela_str)

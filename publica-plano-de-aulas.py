# import tabulate
# import pandas as pd

# t1 = pd.read_excel('plano-de-aulas.xlsx')
# #t1['Data'] = t1['Data'].apply(lambda x: x.strftime('%d/%m'))

# with open('docs/_snippets/plano_aula.md', 'w') as f:
#     tabela_str = tabulate.tabulate(t1[['Data', 'Questão/Problema/Desafio',
# 'Fundamentos / Conteúdo', 'Evidências de Aprendizado', 'Programação/Atividades']], headers=['Data', 'Questão',
# 'Conteúdo', 'Evidências de Aprendizado', 'Atividades'], tablefmt='html', showindex=False)
#     f.write(tabela_str)

import pandas as pd
from pretty_html_table import build_table

df = pd.read_excel('plano-de-aulas.xlsx')
html_table_blue_light = build_table(df[[
    'Data', 'Questão',
    'Conteúdo', 'Evidências de Aprendizado', 'Atividades']], 
    color='blue_light')

html_table_blue_light = html_table_blue_light.replace('&lt;strong&gt;','<strong>')
html_table_blue_light = html_table_blue_light.replace('&lt;/strong&gt;','</strong>')

# Save to html file
with open('docs/_snippets/plano_aula.md', 'w') as f:
    f.write(html_table_blue_light)

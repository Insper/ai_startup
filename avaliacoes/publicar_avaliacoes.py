import pandas as pd
from enviar_email import Email

def texto_diferenca(nota, media):

    diff = media - nota
    if diff < -1:
        return('muito inferior. É imperativo conversar com os outros membros para entender o que está acontecendo.')
    elif diff < -0.5:
        return('inferior. Recomendo que você converse com os outros membros para saber mais detalhes.')
    elif diff <= -0.01:
        return('um pouco inferior. Não muito, mas vale a pena refletir, pois é possível que você tenha superestimado seu nível.')
    elif diff < 0.01:
        return('igual. Sua percepção parece correta, mas também é possível que os outros membros tenham avaliado todos da mesma maneira, sem refletir muito.')
    elif diff > 1:
        return('muito superior. É possível que os outros membros tenham avaliado todos da mesma maneira, mas o tamanho da diferença indica que você provavelmente subestimou seu nível.')
    elif diff > 0.5:
        return('superior. Você parece ter subestimado seu nível, mas também é possível que os outros membros tenham avaliado todos da mesma maneira, sem refletir muito.')
    else:
        return('um pouco superior. Não muito, mas vale a pena refletir, pois é possível que você tenha subestimado seu nível.')


def cria_mensagem(
        nome, produtividade, produtividade_media, 
        proatividade, proatividade_media,
        transparencia, transparencia_media):
    
    SPRINT = '1'

    TEMPLATE = f'''
    Olá {nome},

    Segue abaixo seu feedback de pares da Sprint {SPRINT}.

    Produtividade
    -------------

    Lembrete: níveis 1 e 2 são negativos, níveis 3 e 4 são positivos e nível 5 é positivo mas indesejado.

    A diferença entre 3 e 4, sozinha, não faz diferença para aprovação. O nível 4 deve ser usado para reconhecer o esforço de membros específicos.

    Nível que você atribuiu a si mesmo: {produtividade}

    Média dos níveis que os colegas atribuíram a você: {produtividade_media}

    Diferença: {produtividade_media - produtividade}

    Ou seja, a visão dos colegas sobre você foi {texto_diferenca(produtividade, produtividade_media)}


    Proatividade
    ------------

    Lembrete: níveis 1, 2 e 5 são negativos e níveis 3 e 4 são positivos.

    A diferença entre 3 e 4, sozinha, não faz diferença para aprovação. O nível 4 deve ser usado para reconhecer o esforço de membros específicos.

    Nível que você atribuiu a si mesmo: {proatividade}

    Média dos níveis que os colegas atribuíram a você: {proatividade_media}

    Diferença: {proatividade_media - proatividade}

    Ou seja, a visão dos colegas sobre você foi {texto_diferenca(proatividade, proatividade_media)}


    Transparência
    -------------

    Lembrete: níveis 1 e 2 são negativos, níveis 3 e 4 são positivos e nível 5 é positivo mas indesejado.

    A diferença entre 3 e 4, sozinha, não faz diferença para aprovação. O nível 4 deve ser usado para reconhecer o esforço de membros específicos.

    Nível que você atribuiu a si mesmo: {transparencia}

    Média dos níveis que os colegas atribuíram a você: {transparencia_media}

    Diferença: {transparencia_media-transparencia}

    Ou seja, a visão dos colegas sobre você foi {texto_diferenca(transparencia, transparencia_media)}

    Esteja à vontade para perguntar em caso de quaisquer dúvidas.

    []'s
    Barth e Nakagawa
    '''
    return TEMPLATE

df = pd.read_excel('avaliacoes.xlsx', sheet_name='resumo_individual')

e = Email()

for index, row in df.iterrows():
    mensagem = cria_mensagem(
        row['Nome'], 
        row['Produtividade'], 
        row['Produtividade - média'], 
        row['Proatividade'], 
        row['Proatividade - média'], 
        row['Transparência'], row['Transparência - média'])
    
    with open('emails/'+row['Email']+'.txt', 'w') as file:
        file.write(mensagem)

    e.enviar(row['Email'], '[AI Startup] Feedback de pares', 'emails/'+row['Email']+'.txt')
    
    



import os

from statistics import mean

from fidibequi import Loader, Sender


SPRINT = '4'

TEMPLATE = '''
Olá {},

Segue abaixo seu feedback de pares da Sprint {}.


Produtividade
-------------

Lembrete: níveis 1 e 2 são negativos, níveis 3 e 4 são positivos e nível 5 é positivo mas indesejado.

A diferença entre 3 e 4, sozinha, não faz diferença para aprovação. O nível 4 deve ser usado para reconhecer o esforço de membros específicos.

Nível que você atribuiu a si mesmo: {}

Média dos níveis que os colegas atribuíram a você: {}

Diferença: {}{}

Ou seja, a visão dos colegas sobre você foi {}


Proatividade
------------

Lembrete: níveis 1, 2 e 5 são negativos e níveis 3 e 4 são positivos.

A diferença entre 3 e 4, sozinha, não faz diferença para aprovação. O nível 4 deve ser usado para reconhecer o esforço de membros específicos.

Nível que você atribuiu a si mesmo: {}

Média dos níveis que os colegas atribuíram a você: {}

Diferença: {}{}

Ou seja, a visão dos colegas sobre você foi {}


Transparência
-------------

Lembrete: níveis 1 e 2 são negativos, níveis 3 e 4 são positivos e nível 5 é positivo mas indesejado.

A diferença entre 3 e 4, sozinha, não faz diferença para aprovação. O nível 4 deve ser usado para reconhecer o esforço de membros específicos.

Nível que você atribuiu a si mesmo: {}

Média dos níveis que os colegas atribuíram a você: {}

Diferença: {}{}

Ou seja, a visão dos colegas sobre você foi {}


Esteja à vontade para perguntar em caso de quaisquer dúvidas.

[]'s
Hashi
'''


def main():
    names = {}
    codes = {}
    egos = {}
    alters = {}
    loader = Loader('input')
    sheet = loader.load('Presenca')
    for row in sheet[1:]:
        nick = row[0]
        names[nick] = row[3]
        codes[nick] = row[1]
        alters[nick] = {
            'prod': [],
            'proa': [],
            'tran': [],
        }

    loader = Loader('pares')
    sheet = loader.load(SPRINT)
    sender = Sender(
        'Fabricio Barth',
        'fabricio.barth@gmail.com',
        'fabriciojb@insper.edu.br',
    )

    for row in sheet[1:]:
        nick = row[0]
        if nick in names:
            egos[nick] = {
                'prod': int(row[5]),
                'proa': int(row[10]),
                'tran': int(row[15]),
            }
            for i in range(1, 6):
                nick = row[i]
                if nick in names:
                    alters[nick]['prod'].append(int(row[5 + i]))
                    alters[nick]['proa'].append(int(row[10 + i]))
                    alters[nick]['tran'].append(int(row[15 + i]))

    with open(os.path.join('pares', f'{SPRINT}.txt'), 'w') as file:
        for nick in egos:
            file.write(nick + '\n')
            args = [names[nick], SPRINT]
            total = 0
            for key in ['prod', 'proa', 'tran']:
                ego = egos[nick][key]
                alter = round(mean(alters[nick][key]), 2)
                diff = round(alter - ego, 2)
                args.append(ego)
                args.append(alter)
                args.append('+' if diff > 0 else '')
                args.append(diff)
                if diff < -1:
                    args.append('muito inferior. É imperativo conversar com os outros membros para entender o que está acontecendo.')
                elif diff < -0.5:
                    args.append('inferior. Recomendo que você converse com os outros membros para saber mais detalhes.')
                elif diff <= -0.01:
                    args.append('um pouco inferior. Não muito, mas vale a pena refletir, pois é possível que você tenha superestimado seu nível.')
                elif diff < 0.01:
                    args.append('igual. Sua percepção parece correta, mas também é possível que os outros membros tenham avaliado todos da mesma maneira, sem refletir muito.')
                elif diff > 1:
                    args.append(
                        'muito superior. É possível que os outros membros tenham avaliado todos da mesma maneira, mas o tamanho da diferença indica que você provavelmente subestimou seu nível.')
                elif diff > 0.5:
                    args.append(
                        'superior. Você parece ter subestimado seu nível, mas também é possível que os outros membros tenham avaliado todos da mesma maneira, sem refletir muito.')
                else:
                    args.append('um pouco superior. Não muito, mas vale a pena refletir, pois é possível que você tenha subestimado seu nível.')
                suffix = ''
                if key == 'proa':
                    if alter < 2:
                        suffix = ' --'
                    elif alter < 3 or alter > 4:
                        suffix = ' -'
                    elif alter > 3:
                        suffix = ' +'
                    if alter > 4:
                        total += 4 - alter
                    else:
                        total += alter - 3
                else:
                    if alter < 2:
                        suffix = ' --'
                    elif alter < 3:
                        suffix = ' -'
                    elif alter > 4:
                        suffix = ' ++'
                    elif alter > 3:
                        suffix = ' +'
                    total += alter - 3
                file.write('{}{}\n'.format(alter, suffix))
            file.write('{}\n'.format(total / 3))
            file.write('\n')
            sender.send(
                # 'marcelo.hashimoto@insper.edu.br',
                nick + '@al.insper.edu.br',
                'Feedback de Pares da Sprint {}'.format(SPRINT),
                TEMPLATE.format(*args),
                None,
            )
            print(nick)


if __name__ == '__main__':
    main()

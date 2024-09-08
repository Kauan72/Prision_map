Para que o mapa seja compartilhado, adicionar a pasta prison_map para a workspace. Não selecionar a game e a map_creator separadamente pois 
compartilham o arquivo do mapa.

Para iniciar o game, executar a classe game.py.
	para alterar a velocidade do rick,  alterar a variável intervalo_mover_rick na linha 254 da classe game.py

Para modificar o mapa do game, executar a classe map_creator.py.
	após modificar o mapa, selecionar a opção salvar para que o mapa seja atualizado no game.


OBS:
O caminho é calculado antes do game iniciar, caso seja impossível encontrar um caminho ou seja muito complexo, a interface do game 
não irá abrir, ou demorará para abrir.

A heuristica utilizada para decidir a ordem de busca dos personagens e a distância estimada de rick de um personagem foi a distância manhattan, logo, 
se o terreno for modificado de forma extrema, é possível que não encontremos a solução ótima.

Score conta o custo para chegar na posição atual.
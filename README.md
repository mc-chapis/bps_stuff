# bps_stuff
scripts para serem usados no BrasilPlayShox, servidor de SA:MP (San Andreas Multiplayer)

## auto_adv.py
script de automatizar atividade de advogado
* requer Python 3, dependências estão listadas no começo do arquivo
* vc provavelmente precisará mudar a linha 38 (que cropa o print da lista de presos), pois ela é feita para meu monitor, que é ultra wide
  * possivelmente mudar pra ```im = im.crop((750, 0, 1208, h))``` deve fazer funcionar em um monitor 1080p, mas precisa testar antes
* para parar o script basta jogar o mouse pra um dos cantos da tela (ativando o failsafe do PyAutoGUI)

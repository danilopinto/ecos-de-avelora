# Ecos de Avelora

> **Autor:** Danilo Pinto · [danilo.pinto1@gmail.com](mailto:danilo.pinto1@gmail.com) · [GitHub](https://github.com/danilopinto/)

Jogo de aventura 2D em Pixel Art para navegador.

## Visão geral

Ecos de Avelora é uma aventura de exploração top-down sobre ruínas antigas e as memórias de uma civilização desaparecida. Um artefato permite ao protagonista revelar fragmentos do passado, compreender enigmas e reconstruir caminhos.

## Objetivo atual

Desenvolver um MVP jogável com uma única fase, do início ao fim. A primeira entrega deve validar exploração, interação, alternância entre passado e presente, um enigma e uma conclusão narrativa.

O planejamento considera dez fases para o jogo completo, mas as fases 2 a 10 ficam fora da implementação do MVP.

## Requisitos principais

- Plataforma inicial: navegadores modernos para desktop.
- Genero: aventura e exploracao narrativa.
- Perspectiva: top-down.
- Direção visual: Pixel Art, com resolução-base proposta de 320 x 180.
- Narrativa principal linear.
- Controles iniciais por teclado; mouse para elementos de interface quando necessario.
- Salvamento local no navegador.

## Documentacao

- [Visão do jogo](docs/01-visao-do-jogo.md)
- [Narrativa e fases](docs/02-narrativa-e-fases.md)
- [Especificação do MVP](docs/03-especificacao-do-mvp.md)
- [Arquitetura técnica](docs/04-arquitetura-tecnica.md)
- [Plano de desenvolvimento](docs/05-plano-de-desenvolvimento.md)
- [Plano técnico de desenvolvimento](docs/06-plano-tecnico-de-desenvolvimento.md)
- [Portal HTML](index.html)
- [Jogar o MVP](jogo.html)
- [Plano e implementação V2](V2/README.md)

## Referências visuais

O portal apresenta sete imagens de referência recuperadas da conversa compartilhada. Elas ficam em `assets/images/`, com créditos e links para as fontes no próprio HTML. São referências de terceiros, não assets originais do jogo; valide as licenças antes de reutilizá-las na distribuição do jogo.

## Tecnologias propostas

- Phaser para o jogo 2D.
- TypeScript para a logica.
- Vite para desenvolvimento e build.
- Tiled para edicao de mapas.
- Aseprite ou ferramenta equivalente para Pixel Art.

As tecnologias são uma proposta inicial, ainda sujeita a validação durante a prototipagem.

## Limites do MVP

Não fazem parte da primeira entrega: fases 2 a 10, combate, multiplayer, contas de usuário, backend, salvamento em nuvem ou finais alternativos.

## Como jogar

Abra `jogo.html` em um navegador moderno. Não é necessário instalar dependências nem iniciar um servidor.

- **W/A/S/D** ou setas: movimentar.
- **E** ou **Espaço**: ler, interagir e avançar diálogos.
- **Q**: alternar entre passado e presente após despertar o artefato.
- **Esc**: pausar.

Leia a inscrição, desperte o cristal, atravesse a ponte no passado, encontre a memória e repita a sequência **Sol → Lua → Ondas** diante do santuário. O progresso é local neste navegador.

## Definicao de sucesso

O jogador consegue iniciar a partida, explorar a floresta, usar a mecânica temporal, resolver o enigma principal e concluir a fase sem bloqueios impeditivos.

## Status

Primeira versão jogável da Fase 1 disponível em `jogo.html`. É um protótipo independente em HTML5 Canvas e JavaScript, sem bibliotecas externas: pode ser aberto diretamente no navegador e o jogador não precisa instalar nada. Inclui movimentação e colisões, inscrição e artefato, alternância temporal, memória com pista, enigma dos três símbolos, encerramento e salvamento local validado.

A jornada visual foi refeita em **High Detail Pixel Art**: renderização 3x sobre coordenadas de jogo 320 x 180, terreno com grão fino, trilha composta de pedras irregulares e facetadas, margens sinuosas, portal de ruínas, ponte restaurada no passado e santuário com alvenaria, musgo, gravações e entrada em arco. A floresta combina copas em camadas, folhagem variada, arbustos, samambaias, musgo, cogumelos, folhas caídas e cristais decorativos esparsos. O cristal central, as runas, as tochas e a lanterna têm iluminação localizada; o personagem tem roupa, mochila, botas, lanterna e animação de caminhada. A stack Phaser/TypeScript permanece como proposta a avaliar; esta implementação inicial prioriza um ciclo jogável imediato no ambiente disponível.

O fluxo jogável — inscrição, artefato, alternância temporal, ponte, memória, sequência dos símbolos e encerramento — foi percorrido em Chrome. Também foram verificados o carregamento de progresso válido e a recuperação de um salvamento corrompido. O jogo ainda precisa de validação manual em outros navegadores e iteração de arte, mapa e dificuldade. Estimativas e metas registradas nos documentos são hipóteses de planejamento, não resultados medidos.

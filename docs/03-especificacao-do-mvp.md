# Ecos de Avelora — Especificacao do MVP

> **Autor:** Danilo Pinto · [danilo.pinto1@gmail.com](mailto:danilo.pinto1@gmail.com) · [GitHub](https://github.com/danilopinto/)

## Objetivo

Entregar uma única fase de aventura em Pixel Art, executável no navegador e concluível do início ao fim. O MVP deve provar que movimentação, exploração, mecânica temporal, enigma e narrativa funcionam como uma experiência integrada.

## Limites do escopo

### Incluido

- Menu inicial simples.
- Uma fase: A Floresta Esquecida.
- Personagem controlável, movimento em oito direções, colisões e câmera.
- Interação com inscrições e artefatos, com diálogos curtos.
- Alternancia entre passado e presente.
- Um enigma principal com três símbolos e desbloqueio da câmara final.
- Cena de encerramento, salvamento local e opção de pausa ou reinício.
- Interface e efeitos visuais básicos.

### Fora do escopo

Fases 2 a 10, combate, chefes, inventário complexo, fabricação, habilidades, missões secundárias, diálogos ramificados, múltiplos finais, multiplayer, contas, salvamento em nuvem e controles por toque como requisito.

## Duração estimada

A primeira partida é estimada em 10 a 15 minutos. A duração deve ser validada com testes reais e pode variar conforme a familiaridade do jogador.

## Fluxo da fase

1. Iniciar uma partida e receber uma breve introducao ao sinal misterioso.
2. Explorar a floresta e encontrar uma inscrição.
3. Aprender a interagir e descobrir o artefato temporal.
4. Alternar entre presente e passado para investigar a ruína.
5. Resolver o enigma dos três símbolos.
6. Abrir a câmara final, assistir à memória e concluir a fase.

## Mecânicas funcionais

### Movimento e camera

- Movimento em oito direcoes, com velocidade consistente.
- Colisões com paredes, árvores, obstáculos e limites do mapa.
- Animações básicas de repouso e caminhada.
- Camera acompanha o personagem sem tremores e respeita os limites da fase.

### Interacao

- Interagir com objetos próximos e indicar quando a ação está disponível.
- Avançar textos por uma tecla.
- Impedir ativações repetidas indevidas em objetos importantes.

### Alternancia temporal

O artefato alterna entre dois estados:

- **Presente:** vegetação crescida, ruínas danificadas e caminhos bloqueados.
- **Passado:** estruturas preservadas, inscrições visíveis e pistas para o enigma.

A posição do jogador é preservada. Antes de concluir a transição, o jogo valida se a posição é segura no estado de destino; a alternância não pode prender o jogador nem permitir atravessar paredes.

### Enigma e progressao

- Três símbolos devem ser ativados na ordem indicada por uma memória.
- Uma tentativa incorreta fornece feedback claro e não bloqueia o progresso.
- A sequência pode ser reiniciada de forma previsível.
- O jogo acompanha inscrição encontrada, artefato despertado, memória observada, enigma resolvido e câmara alcançada.
- Os objetivos são atualizados conforme a progressão.

### Salvamento

Registrar progresso mínimo para continuar a partida, distinguindo novo jogo de jogo em andamento. Validar dados restaurados; se o salvamento for inválido, permitir reiniciar sem travar. O armazenamento local não é um backup garantido.

## Controles iniciais

| Entrada | Ação |
|---|---|
| W, A, S, D ou setas | Movimentar personagem |
| E ou Espaco | Interagir e avançar diálogos |
| Q | Alternar entre passado e presente |
| Esc | Pausar ou abrir o menu |

Os controles devem aparecer no início e permanecer acessíveis durante a partida.

## Interface

Menu inicial com iniciar/continuar, objetivo atual, mensagem contextual, caixa de diálogo, indicador do estado temporal, pausa com continuar/reiniciar e tela final com retorno ao menu.

## Criterios de aceite

1. O jogo abre em um navegador suportado.
2. O personagem se movimenta e respeita colisões e limites.
3. O visual apresenta Pixel Art consistente.
4. Interações e diálogos principais funcionam.
5. A alternância temporal altera corretamente o cenário e preserva uma posição válida.
6. O enigma pode ser resolvido com as pistas disponíveis; uma tentativa errada não bloqueia.
7. A passagem final abre após a solução e a narrativa chega ao encerramento.
8. O progresso pode ser salvo e restaurado localmente.
9. A fase pode ser reiniciada e concluída sem erros impeditivos.

## Principios de qualidade

Evitar bloqueios de progressão, objetos obrigatórios inacessíveis e transições temporais que prendam o jogador. Manter textos legíveis, controles consistentes, feedback visual e reinício confiável.

## Metrica proposta

Usar a taxa de conclusão em testes de jogo como métrica principal. Meta inicial proposta: pelo menos 80% de participantes de um pequeno teste concluem a fase sem intervenção externa. É uma meta ainda não medida, não um resultado garantido. Registrar também pontos de confusão, erros no enigma e dificuldades para compreender a mecânica temporal.

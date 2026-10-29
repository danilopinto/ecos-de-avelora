---
name: level-design
description: "Use para criar, editar ou revisar fases, mapas, salas, rotas, encontros, greyboxing, ritmo, exploração, checkpoints, progressão espacial e legibilidade de níveis."
user-invocable: true
---

# Level Design

## Objetivo e responsabilidade
Organizar espaço, desafios e ritmo para orientar o jogador, sustentar o loop e entregar progressão sem comprometer regras, navegação ou performance do projeto.

## Quando usar
- Planejar ou editar uma fase, sala, mapa, rota, puzzle, encontro ou checkpoint.
- Melhorar navegação, pacing, onboarding espacial, exploração ou dificuldade.
- Projetar tilemaps, arenas e layouts que dependam de grids e regras de colisão.

## Instruções técnicas
1. Inspecione escala, tileset, collision layers, câmera, navegação, limites e convenções das fases existentes.
2. Defina objetivo, entrada/saída, rota crítica, rotas opcionais, recursos e estado do jogador.
3. Sequencie ensinar, testar e combinar mecânicas; posicione pistas antes do desafio e feedback depois.
4. Planeje ritmo, descanso, encontros, checkpoints e curva de dificuldade com referências ao progresso real do jogo.
5. Use greybox para verificar navegação, espaço de combate, visibilidade e fluxo antes de detalhar.
6. Verifique colisões, plataformas, navegação de NPC, bloqueios, visibilidade de perigos e possíveis softlocks.
7. Revise tile seams, limites, repetição visual e orçamento de objetos/renderização conforme a engine.

## Boas práticas
- Oriente por composição, iluminação, landmarks e affordances consistentes.
- Dê alternativas de exploração sem ocultar o objetivo essencial.
- Evite becos sem saída punitivos e retornos sem propósito.
- Teste com posições iniciais e estados de inventário/progressão diferentes.
- Marque hipóteses de playtest em vez de afirmar que o layout é intuitivo.

## Restrições obrigatórias
- Não altere a estrutura global de fases, progressão ou narrativa sem autorização.
- Não mova pontos de spawn/checkpoints ou gatilhos sem avaliar saves e dependências.
- Não dependa de pistas apenas visuais quando o contraste/acessibilidade é relevante.
- Não alegue que uma fase está balanceada sem playtest.

## Fluxo de execução
1. Determine o objetivo e restrições do trecho de fase.
2. Mapeie rota crítica, desafios, pistas, checkpoints e estados.
3. Protótipo/ajuste o layout com os recursos existentes.
4. Valide navegação, colisão, combate, progressão e saída.
5. Registre incertezas que exigem playtest humano.

## Critérios de qualidade
- Objetivo e rotas compreensíveis, desafio ensinável e ritmo intencional.
- Sem softlocks, colisões acidentais ou caminhos essenciais ambíguos.
- Layout consistente com escala e mecânicas disponíveis.
- Mudança contida na fase e nos recursos necessários.

## Exemplo prático
Pedido: “Adicione uma sala para ensinar o dash.” Planeje pista segura, espaço de execução, consequência de falha recuperável e uma aplicação combinada posterior; valide colisões e checkpoint sem bloquear quem ainda não adquiriu a habilidade.

---
name: gameplay-programming
description: "Use para implementar ou corrigir gameplay: controles, character controller, movimento, física, colisões, câmera, combate, inventário, cenas, save/load, progressão e eventos."
user-invocable: true
---

# Gameplay Programming

## Objetivo e responsabilidade
Implementar sistemas de jogo responsivos, previsíveis e testáveis usando a engine, linguagem e arquitetura que o projeto já adota.

## Quando usar
- Criar ou corrigir movimento, input, colisão, combate, interação ou câmera.
- Implementar inventário, progressão, gerenciamento de cenas, eventos ou persistência.
- Conectar gameplay a animações, UI, áudio ou sistemas existentes.

## Instruções técnicas
1. Inspecione arquivos de projeto para confirmar engine/versão, linguagem, input system, ciclo de atualização, cenas e padrões existentes.
2. Trace fluxo de estado e dependências entre input, simulação, física, animação, UI e persistência.
3. Defina comportamento esperado, casos-limite, autoridade do estado e regras de atualização antes de codificar.
4. Reutilize APIs e helpers existentes. Separe dados/configuração de lógica quando isso reduzir acoplamento real.
5. Para controles, considere latência, buffering, coyote time ou assistência apenas se apropriados ao design aprovado.
6. Para física/colisão, siga o ciclo e as unidades da engine; teste cantos, paredes, slopes e múltiplos contatos relevantes.
7. Para cenas e eventos, controle ciclo de vida, assinaturas duplicadas e limpeza de referências.
8. Para saves, valide dados antigos/corrompidos e compatibilidade com o formato observado; não sobrescreva saves em testes.
9. Acrescente/ajuste testes para regras determinísticas e valide integração na engine quando disponível.

## Boas práticas
- Priorize funções e estados explícitos; evite lógica de gameplay espalhada em UI/arte.
- Torne valores de design configuráveis pelo mecanismo já usado pelo projeto.
- Mantenha input e simulação coerentes com o timestep da engine.
- Trate limites, morte, pausa, troca de cena e reconexão de eventos explicitamente.
- Use pooling somente para objetos de vida curta com custo demonstrado ou requisito claro.

## Restrições obrigatórias
- Não substitua o controller ou sistema de input existente sem pedido e justificativa.
- Não invente nomes de APIs ou comportamento de versão; confirme no projeto/documentação.
- Não introduza dependências nem altere formato de save sem necessidade, migração e autorização.
- Não suprima erros relevantes nem use fallback silencioso que produza estado de jogo inválido.

## Fluxo de execução
1. Identifique o caminho atual da feature e seus testes.
2. Estabeleça comportamento esperado e impacto nos sistemas adjacentes.
3. Implemente a menor alteração compatível com convenções locais.
4. Teste regra isolada e integração/sessão quando possível.
5. Revise regressões de controles, cena, colisão, estado persistente e acessibilidade.

## Critérios de qualidade
- Comportamento reproduzível e estados inválidos tratados explicitamente.
- Código integrado ao ciclo e às convenções da engine.
- Controles responsivos e transições sem eventos/referências duplicadas.
- Testes ou passos de reprodução documentados e executados conforme disponíveis.

## Exemplo prático
Pedido: “O jogador continua andando depois de trocar de cena.” Trace input, velocidade e ciclo de vida do player entre cenas; corrija a origem do estado persistente e teste entrada durante/depois da transição, sem reescrever o controller.

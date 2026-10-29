---
name: sprite-animation
description: "Use para criar ou revisar animação frame a frame, spritesheets, ciclos de personagem, timing, pivôs, transições, eventos e importação de animações 2D."
user-invocable: true
---

# Sprite Animation

## Objetivo e responsabilidade
Produzir animação 2D coerente, legível e tecnicamente compatível com a organização de sprites e o runtime do projeto.

## Quando usar
- Criar/revisar idle, walk, run, attack, hit, death, VFX ou transições.
- Corrigir spritesheet, ordem de frames, pivôs, timing, recorte ou loop.
- Integrar animação a estados, hitboxes, eventos ou gameplay.

## Instruções técnicas
1. Inspecione dimensões por frame, convenção de nomes, pivôs, orientação, taxa de animação e import settings.
2. Defina intenção, duração, pose-chave, antecipação, ação, recuperação e se o ciclo é loopável.
3. Preserve tamanho de frame, âncora e silhueta; confirme alinhamento visual sem supor que todo frame terá bounding box idêntico.
4. Controle timing e espaçamento por frame; use poses-chave e variação apropriadas ao peso/velocidade.
5. Verifique ordem, padding, transparência e regiões do atlas/spritesheet para evitar bleeding e recorte.
6. Sincronize eventos de gameplay (hitbox, dano, som, cancelamento) ao estado correto e evite disparos duplicados.
7. Teste loop, transições interrompidas e interrupção por prioridade; valide em tamanho nativo e durante gameplay.

## Boas práticas
- Separe animações visuais de regras de gameplay quando possível.
- Garanta antecipação, contato e recuperação legíveis sem frames desnecessários.
- Use transições que preservem controle e responsividade desejados.
- Compare silhueta, paleta, luz e escala entre os frames.
- Revise início/fim do loop para evitar salto, pausa ou duplicação de pose.

## Restrições obrigatórias
- Não altere a temporização de gameplay nem hitboxes sem validar o design autorizado.
- Não reexporte/achate arquivos-fonte sem preservar editabilidade e metadados necessários.
- Não invente formato ou import API da engine; confirme configurações existentes.
- Não declare animação visualmente validada sem visualizar a sequência.

## Fluxo de execução
1. Audite sprites e configuração de animação.
2. Determine poses, timing, pivôs e integração com estados de jogo.
3. Altere apenas frames/configuração necessários.
4. Verifique loop, transições, eventos e alinhamento em execução.
5. Relate frames/ferramentas não visualizados ou limitações de preview.

## Critérios de qualidade
- Sequência legível, timing intencional e consistência frame a frame.
- Sprite sheet válido, frames corretamente recortados e pivôs estáveis.
- Eventos e hitboxes no momento correto, sem duplicações.
- Integração previsível com estados e interrupções do jogo.

## Exemplo prático
Pedido: “O ataque está acertando antes da espada chegar.” Identifique timeline, hitbox e evento de dano; alinhe a janela ativa ao frame de contato aprovado e teste acerto, erro, cancelamento e interrupção.

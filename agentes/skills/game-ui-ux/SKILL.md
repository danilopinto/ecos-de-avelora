---
name: game-ui-ux
description: "Use para projetar ou implementar HUD, menus, inventários, diálogos, navegação, feedback visual, tipografia, legibilidade, acessibilidade e experiência do jogador."
user-invocable: true
---

# Game UI/UX

## Objetivo e responsabilidade
Fazer a interface comunicar estado e opções do jogo com hierarquia, consistência, acessibilidade e resposta adequada a input e plataforma; preservar ou estabelecer um design system proporcional ao projeto.

## Quando usar
- Criar ou alterar HUD, menu, inventário, mapa, diálogo, configurações ou onboarding.
- Melhorar legibilidade, navegação, feedback, layout responsivo ou controles de acessibilidade.
- Revisar consistência visual entre interface e mundo do jogo.

## Instruções técnicas
1. Inspecione resolução/viewport, estilo visual, fluxo de telas, input (teclado, mouse, controle, toque) e localização existentes.
2. Identifique tarefa do jogador, informação prioritária, estados, ações disponíveis e feedback necessário.
3. Organize hierarquia, navegação e foco; reutilize tokens e componentes de um design system existente, garantindo que o jogador saiba onde está, o que pode fazer e o resultado da ação.
4. Use texto, ícones e cores redundantes para comunicar estados importantes; valide contraste e tamanho em resolução real.
5. Considere safe areas, escalas, proporções, localização, leitura de fontes pixel e consistência de grid.
6. Modele estados vazio, carregando, indisponível, selecionado, erro, confirmação e retorno, quando aplicável.
7. Preserve bindings de input e preferências; valide teclado/controle e remapeamento quando suportado.
8. Teste fluxo ponta a ponta, inclusive cancelar/voltar, foco, pause e transição de cena.

## Boas práticas
- Priorize informação acionável e evite sobrecarregar HUD.
- Mantenha padrões de rótulos, foco, margens, ícones e feedback entre telas.
- Não dependa exclusivamente de cor para indicar perigo, raridade ou seleção.
- Considere opção de reduzir flashes/movimento, legendas e controles de volume quando coerentes com o produto.
- Use protótipo com conteúdo realista e tamanhos finais para verificar legibilidade.

## Restrições obrigatórias
- Não reorganize toda a interface ou identidade visual fora do pedido.
- Não presuma plataforma, tamanho de fonte ou requisitos de acessibilidade não informados.
- Não esconda ações destrutivas nem altere preferências sem consentimento.
- Não declare acessibilidade validada sem verificar os requisitos e o fluxo correspondente.

## Fluxo de execução
1. Mapeie telas, tarefas, estados e modos de input envolvidos.
2. Defina hierarquia e critérios de legibilidade/navegação.
3. Implemente mudanças localizadas, reutilizando tokens/componentes existentes.
4. Verifique escalas, foco, input, estados vazios/erro e retorno.
5. Registre limitações de ferramentas ou dispositivos não disponíveis.

## Critérios de qualidade
- Informação crítica legível na escala e plataforma-alvo.
- Navegação consistente por inputs suportados e feedback compreensível.
- Estados e ações cobertos sem regressão no fluxo do jogo.
- Identidade visual e acessibilidade relevantes preservadas.

## Exemplo prático
Pedido: “O inventário precisa funcionar com controle.” Siga o fluxo de foco atual, acrescente seleção/confirmar/voltar e estados visuais, teste abertura, navegação, uso de item e fechamento sem mouse.

# Ecos de Avelora — Arquitetura Tecnica

> **Autor:** Danilo Pinto · [danilo.pinto1@gmail.com](mailto:danilo.pinto1@gmail.com) · [GitHub](https://github.com/danilopinto/)

## Objetivo técnico

Construir uma base simples e extensível para um jogo 2D no navegador. A arquitetura deve suportar uma fase no MVP sem impedir a expansão planejada para dez fases.

## Stack proposta

- **Phaser:** renderização 2D, cenas, entrada, animações, câmera e integração de física/colisões.
- **TypeScript:** lógica do jogo, entidades, estados temporais, interações, enigmas e salvamento.
- **Vite:** servidor de desenvolvimento e build de produção.
- **Tiled:** edição de mapas, tilesets, camadas e objetos interativos.
- **Aseprite ou equivalente:** sprites, tilesets, animações e efeitos em Pixel Art.

Esta stack é uma proposta, não uma decisão já implementada.

### Implementação inicial do MVP

A primeira versão jogável foi iniciada como um arquivo HTML independente usando Canvas 2D e JavaScript nativo, sem dependências externas. Isso permite abrir a fase diretamente em um navegador, sem instalação de ferramentas para o jogador. A proposta Phaser/TypeScript/Vite permanece como opção para uma estrutura de produção; decidir uma migração somente se o protótipo demonstrar necessidade concreta.

## Requisitos de execucao

- Navegadores modernos com suporte a HTML5 Canvas.
- Execução sem instalação de aplicativo.
- Renderização pixel-perfect e teclado como entrada principal.
- Mouse para elementos de interface quando necessário.
- Assets locais junto à aplicação.
- Salvamento local com `localStorage`.
- Distribuicao por hospedagem de arquivos estaticos.

## Configuração visual

Resolução-base proposta: 320 x 180 pixels. Usar escalonamento sem suavização para evitar borramento e adaptar o canvas à janela sem distorcer a proporção. A interface deve permanecer legível em janelas menores.

## Estrutura de diretórios sugerida

```text
ecos-de-avelora/
├── public/
│   ├── assets/
│   │   ├── sprites/
│   │   ├── tilesets/
│   │   ├── backgrounds/
│   │   ├── audio/
│   │   └── ui/
│   └── maps/fase-01/
├── src/
│   ├── scenes/
│   │   ├── BootScene.ts
│   │   ├── MenuScene.ts
│   │   ├── ExplorationScene.ts
│   │   └── EndingScene.ts
│   ├── entities/Player.ts
│   ├── systems/
│   │   ├── InteractionSystem.ts
│   │   ├── DialogueSystem.ts
│   │   ├── MemorySystem.ts
│   │   ├── PuzzleSystem.ts
│   │   └── SaveSystem.ts
│   ├── data/
│   │   ├── story.ts
│   │   └── levels.ts
│   └── main.ts
├── index.html
├── package.json
├── tsconfig.json
└── README.md
```

Esta estrutura é uma referência inicial. Módulos podem ser divididos ou combinados desde que suas responsabilidades permaneçam claras.

## Responsabilidades

- **BootScene:** carregar recursos essenciais e preparar configurações.
- **MenuScene:** iniciar, continuar ou retornar ao menu.
- **ExplorationScene:** executar exploração, movimento, câmera e integração dos sistemas.
- **EndingScene:** exibir a conclusão narrativa.
- **Player:** controlar movimento, animação, colisões e estado do personagem.
- **InteractionSystem / DialogueSystem:** detectar interações e apresentar diálogos.
- **MemorySystem:** controlar estados temporais e validar transições.
- **PuzzleSystem:** validar símbolos e comunicar a solução à progressão.
- **SaveSystem:** salvar e restaurar o estado mínimo.
- **Story/Level data:** manter textos, eventos, mapas e metadados separados da apresentação.

## Estados do jogo

Controlar separadamente:

- Estado da aplicação: menu, jogando, pausado ou concluído.
- Estado temporal: presente ou passado.
- Estado da missão: etapas concluídas.
- Estado do enigma: não iniciado, em andamento ou resolvido.
- Estado de salvamento: novo jogo ou progresso restaurável.

Essa separação reduz o risco de uma mudança temporal reiniciar diálogos ou permitir resolver o enigma antes da hora.

## Regras da mecânica temporal

- Preservar a posição lógica do jogador durante a alternância.
- Variar elementos visuais conforme o estado temporal.
- Validar colisão e passagem antes de finalizar uma transição.
- Recusar a mudança ou aplicar regra segura se a posição no estado de destino for inválida.
- Definir explicitamente disponibilidade de objetos e pistas por estado.
- Fazer o enigma depender de condições explícitas, não apenas de efeitos visuais.

## Persistencia local

Registrar identificador da versão do formato, fase atual, etapas principais, estado do enigma e último ponto seguro. Validar os dados carregados e oferecer reinício se forem inválidos. O armazenamento local não deve ser tratado como backup garantido.

## Expansão para dez fases

Reutilizar movimentação, interação, diálogos, memória e salvamento. Fases futuras fornecem mapas, objetos, eventos e regras por dados/configurações. A progressão principal controla o acesso em ordem. Não é necessário implementar carregamento dinâmico complexo no MVP.

## Publicação e requisitos não funcionais

Fluxo esperado: desenvolver e testar localmente, gerar build, publicar arquivos estáticos e validar carregamento de recursos, controles e salvamento no endereço publicado.

Requisitos: carregamento sem erros impeditivos, controles responsivos, pixels nítidos, código organizado e tipado, ausência de servidor obrigatório, salvamento resiliente a dados inválidos e desempenho estável em navegadores modernos.

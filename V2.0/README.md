# Ecos de Avelora — V2

> **Autor:** Danilo Pinto · [danilo.pinto1@gmail.com](mailto:danilo.pinto1@gmail.com) · [GitHub](https://github.com/danilopinto/)

Versão separada da V1, estruturada com Phaser, TypeScript e Vite. O protótipo inicial desta pasta implementa a fatia jogável da Fase 1 com viewport lógico 640×360, tiles 32×32 e renderização pixelada.

## Requisitos

- Node.js 20.x, 22.x ou 24+ e npm.
- Navegador moderno com Canvas/WebGL e armazenamento local.
- O Tiled é opcional para abrir/editar `public/maps/fase-01/forest.json`.
- A arte atual é exportada em PNG. Uma ferramenta como Aseprite é opcional para edição posterior dos arquivos-fonte.

## Instalação e execução

No terminal, dentro de `V2/`:

```sh
npm install
npm run dev
```

Abra o endereço local que o Vite imprimir. Para validar build e testes:

```sh
npm test
npm run build
npm run preview
```

A V2 precisa ser servida via Vite ou hospedagem estática; não foi projetada para abrir `index.html` via `file://`. O jogo em execução não chama APIs remotas e o progresso fica em `localStorage` sob a chave `ecos-de-avelora-v2`.

## Controles

- **W/A/S/D** ou **setas:** movimentar.
- **E**, **Espaço** ou **Enter:** interagir/avançar diálogo.
- **Q:** alternar presente/passado após despertar o cristal.
- **Esc:** abrir pausa; use os botões da interface para continuar ou reiniciar.

## Organização

- `src/scenes/ExplorationScene.ts`: renderização Phaser, câmera, input e integração de sistemas.
- `src/data/phase.ts`: viewport, dimensões do mundo e ponto inicial.
- `src/systems/progression.ts`: estado tipado, puzzle e validação do save.
- `src/systems/save.ts`: persistência local isolada para a V2.
- `public/maps/fase-01/forest.json`: mapa Tiled JSON com chão, detalhes, água, caminho, arquitetura e objetos.
- `public/maps/fase-01/decor.json`: posicionamento da decoração (frame, posição, colisão e luz), gerado por `tools/gen_world.py`.
- `public/assets/`: atlas de tiles (`tiles/`), atlas de decoração `decor.png/json`, `player.png` e `light.png` (`sprites/`).
- `tools/`: geradores Python (Pillow) reprodutíveis da arte e do mundo; veja "Regenerar a arte".
- `tests/`: testes de regras de progressão e validação do save.

## Renderização

O renderer lógico trabalha em 640×360; em uma área de 1280×720, isso resulta em escala 2×. `pixelArt`, `roundPixels`, `antialias: false` e CSS `image-rendering: pixelated` ajudam a preservar bordas. Phaser `FIT` mantém a proporção 16:9 durante resize; a escala pode ser fracionária em tamanhos de tela que não sejam múltiplos inteiros, então inspecione a nitidez em cada browser/tamanho suportado.

### Iluminação

O cenário é escuro por padrão: um `RenderTexture` 640×360 (depth 2500, abaixo da HUD) é preenchido a cada frame e "apagado" com a textura `light.png` em cada fonte de luz (lanterna do jogador, tochas, cristais, runas acesas, núcleo e eco). Sprites aditivos dão o brilho colorido. No passado o ambiente fica mais claro e esverdeado. A câmera é posicionada em pixels inteiros após a física (`POST_UPDATE`) para a luz não tremer em relação ao jogador.

### Arte

O jogador usa 4 direções × 4 frames de 32×48 (`frame = direção*4 + passo`; 0 baixo, 1 direita, 2 esquerda, 3 cima). A esquerda é o espelho exato da direita, em perfil 3/4 com os dois olhos visíveis, mochila e passada alternada. Árvores, rochas, ruínas, cristais, tochas e runas vêm do atlas `decor` (cinco variações de copa com tons verde/azulado/amarelado/outonal e troncos de cascas diferentes).

### Regenerar a arte

Requer Python 3 com Pillow. A partir de `V2/tools`:

```bash
python3 gen_tiles.py ../public/assets/tiles/avelora-tiles.png
python3 gen_decor.py     # decor.png + decor.json
python3 gen_player.py    # player.png
python3 gen_light.py     # light.png
python3 gen_world.py     # camadas do mapa + decor.json de posicionamento (idempotente, seed fixa)
```

Os PNGs são gerados proceduralmente e não substituem fontes Aseprite/PSD; preserve fontes editáveis quando a produção de arte final começar.

## Estado e limitações

- A estrutura, o mapa, os sprites iniciais e os sistemas de gameplay estão implementados; build e testes automatizados devem ser executados antes de cada entrega.
- A V1 permanece intacta em `../V1/`.
- A V2 não importa saves V1; usa outra chave de armazenamento.
- Phaser e Vite são dependências locais. É necessário instalar pacotes antes de executar build/testes.
- A geração inicial dos PNGs e do mapa estabelece uma base jogável; precisa de revisão visual/QA em runtime, playtest e iteração de arte.
- Os testes automatizados cobrem regras de progressão e validação, não substituem playtest, testes de browser ou análise de performance.
- Tiled, Aseprite, browsers alvo e ferramentas de profiling devem ser confirmados conforme o ambiente de produção.

# Ecos de Avelora V2 — Plano de Implementação

> **Autor:** Danilo Pinto · [danilo.pinto1@gmail.com](mailto:danilo.pinto1@gmail.com) · [GitHub](https://github.com/danilopinto/)

## 1. Objetivo

Construir uma segunda versão do MVP de **A Floresta Esquecida**, preservando o ciclo narrativo e os sistemas funcionais da V1, mas adotando uma base de projeto organizada e aproximando a apresentação da referência `../assets/images/ImagemGerada.png`.

A V2 deve combinar:

- jogo 2D top-down para navegadores desktop;
- Pixel Art de alta densidade, com texturas orgânicas e iluminação atmosférica;
- resolução lógica de **640 × 360 px**;
- exibição de referência de **1280 × 720 px**, com ampliação 2×;
- tiles de **32 × 32 px**;
- personagens com frames-base de **32 × 48 px** ou **48 × 64 px**, conforme personagem e legibilidade;
- renderização por **Nearest Neighbor**, sem suavização da arte-fonte.

O estado real de implementação, recursos existentes e validações pendentes é registrado no [README da V2](./README.md); o plano não deve ser interpretado como confirmação de que todas as fases foram concluídas.

## 2. Referências e diagnóstico inicial

- A imagem [ImagemGerada.png](../assets/images/ImagemGerada.png) mede aproximadamente **1672 × 941 px**, proporção próxima de 16:9. Ela serve como referência de composição, materiais, densidade visual, paleta e iluminação; seu tamanho não revela a resolução nativa dos sprites.
- A V1 está em `V1/jogo.html`, como aplicação independente em HTML, JavaScript e Canvas 2D. O canvas é exibido em 960 × 540 CSS pixels, enquanto o desenho usa coordenadas lógicas de 320 × 180 e escala 3×, com `imageSmoothingEnabled = false`.
- A V1 já contém exploração, colisões, câmera, interação, diálogo, alternância temporal, enigma, conclusão e salvamento local. Deve continuar disponível e sem alterações durante o desenvolvimento da V2.
- A documentação existente em `../docs/` propõe Phaser, TypeScript, Vite, Tiled e Aseprite ou equivalente. A V2 pode adotar essa stack como fundação, mas deve confirmar versões e APIs quando o projeto for inicializado.
- A resolução lógica maior permite representar mais detalhe-fonte e também mostra mais mundo ao mesmo tempo. Portanto, câmera, composição, mapa, escala do personagem e interface precisam ser reprojetados; trocar apenas o tamanho do canvas é insuficiente.

## 3. Escopo

### Incluído

- Nova aplicação isolada em `V2/`, sem substituir a V1.
- Uma fase verticalmente completa: **A Floresta Esquecida**.
- Fundação técnica, cenas, mapas, assets e build Web.
- Movimento, colisão, câmera, interação e diálogos.
- Presente/passado, ponte, memória, enigma dos símbolos e encerramento.
- Salvamento local versionado para a V2.
- Direção visual de alta densidade, assets de ambiente e iluminação.
- Testes automatizados e validação manual de browser, arte, gameplay e performance.

### Fora do escopo inicial

- Fases 2–10, combate, multiplayer, contas, backend, salvamento em nuvem, monetização e sistemas genéricos de plugins.
- Migração destrutiva, remoção ou alteração dos arquivos da V1.
- Conversão automática de todos os saves V1. Se a continuidade de saves for necessária, projetar importação segura como decisão separada.
- Reprodução pixel-a-pixel da imagem de referência. Usá-la para direção visual, sem copiar ou redistribuir assets de terceiros sem direitos.

## 4. Decisões técnicas propostas

| Área | Proposta V2 | Observação |
|---|---|---|
| Engine e renderização | Phaser 2D | Confirmar versão estável e configuração de pixel art no início do projeto. |
| Linguagem | TypeScript | Tipar estados, dados de fase, interações e formato de save. |
| Dev server e build | Vite | Distribuir build estático; desenvolvimento local usa servidor Vite. |
| Mapas | Tiled | Tile size de 32 × 32; exportação compatível com o loader escolhido para Phaser. |
| Arte | Aseprite ou ferramenta equivalente | Manter arquivos-fonte editáveis; PNG para exportação de sprites/tiles. |
| Viewport lógico | 640 × 360 | Representa 20 × 11,25 tiles de 32 px no enquadramento base. Rever enquadramento vertical e limites da câmera. |
| Escala de saída | 2× para referência de 1280 × 720 | Manter 16:9, sem distorção. Em telas menores, usar o maior fator inteiro que caiba quando possível; letterbox é preferível a blur. |
| Filtragem | Nearest Neighbor | Desabilitar suavização no renderer e manter o alinhamento ao grid. Verificar o comportamento do canvas e CSS em browsers suportados. |
| Física/colisão | Spike técnico antes de decidir | Comparar Arcade Physics com colisão simples baseada em mapa, levando em conta movimento top-down, obstáculos e precisão pixel. Escolher a opção mais simples que satisfaça o MVP. |
| Persistência | `localStorage` com chave V2 e formato versionado | Não sobrescrever save V1. Validar dados e oferecer nova partida se forem inválidos. |
| Alvo inicial | Navegadores desktop modernos | Registrar browsers e versões a suportar quando a equipe confirmar o ambiente de aceite. |

### Contrato de renderização

1. Coordenadas de gameplay e câmera são expressas no espaço lógico de 640 × 360, sem aplicar a escala de apresentação à física.
2. A imagem é renderizada no tamanho lógico e ampliada para a tela. Não desenhar UI ou efeitos em uma superfície borrada de alta resolução para depois reduzir a arte pixelada.
3. Sprites, tiles, câmera e pontos de origem permanecem alinhados a pixels inteiros; arredondar somente na fronteira de renderização quando necessário.
4. A escala visual 2× significa que um pixel lógico ocupa 2 × 2 pixels de saída em 1280 × 720. Dispositivos e tamanhos de janela diferentes podem exigir letterbox ou escala não inteira; validar a nitidez nesses casos.
5. Iluminação pode usar máscaras, sprites de luz ou camadas, desde que não suavize nem destrua os clusters da arte-fonte.
6. `32 × 32` é o tamanho do tile, não uma regra para toda imagem. Personagens, objetos grandes, UI e elementos modulares podem ocupar vários tiles.

## 5. Direção visual da V2

Usar a imagem de referência para orientar linguagem visual, não como mapa fechado:

- **Composição:** trilha sinuosa de pedra conduzindo o olhar até o santuário/cristal; vegetação enquadra o espaço e deixa rotas e pontos de interesse legíveis.
- **Pedra:** blocos irregulares, juntas, desgaste, pequenas rachaduras, variação de valor e musgo nos vãos. Evitar repetição óbvia de um único tile.
- **Vegetação:** copas e arbustos em camadas, folhas de diferentes tamanhos, samambaias, plantas de borda, sobreposição e variação tonal coerentes com o material.
- **Profundidade:** oclusão de contato, sombras nas bordas, sobreposição de planos e redução de contraste/detalhe em áreas de fundo.
- **Luz:** base ambiente escura, luz localizada quente em tochas/lanterna e luz fria/ciano em cristais ou ecos temporais. A luz deve ser controlada por clusters e não criar blur na fonte.
- **Paleta:** verdes profundos, oliva e musgo; pedra em cinzas quentes, marrons e ocres; ciano/azul para cristal e memória; âmbar para fontes quentes. Ajustar ramps aos assets e estados presente/passado.
- **Densidade:** detalhe fino nos materiais e pontos focais; áreas de descanso visual em caminhos, espaço ao redor do jogador e UI. Não adicionar ruído uniforme ou pixels isolados sem função.
- **Personagem:** escolher 32 × 48 ou 48 × 64 conforme teste no viewport, distância de câmera e legibilidade. Manter proporção, pivô, outline, paleta e leitura entre direções e animações.

Antes de produzir todos os assets, criar um pequeno **kit visual** com um tile de chão, dois ou três tiles de pedra, vegetação, um cristal, uma tocha e um frame de personagem. Aprovar leitura em 640 × 360 e em 1280 × 720; só então expandir para o mapa completo.

## 6. Arquitetura proposta

```text
V2/
├── public/
│   ├── assets/
│   │   ├── audio/
│   │   ├── sprites/
│   │   ├── tilesets/
│   │   ├── backgrounds/
│   │   └── ui/
│   └── maps/fase-01/
├── src/
│   ├── data/                 # narrativa, fase e configuração
│   ├── entities/              # jogador e entidades
│   ├── scenes/                # boot, menu, exploração e encerramento
│   ├── systems/               # interação, diálogo, tempo, enigma e save
│   ├── types/                 # tipos dos estados e dados persistidos
│   └── main.ts
├── tests/
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── README.md
```

A estrutura é uma referência inicial; criar módulos apenas quando houver responsabilidade real.

### Responsabilidades e limites

- **Boot/Preload:** inicializar renderer, viewport e carregar recursos; erros de asset devem ser reportados explicitamente.
- **Menu/Exploração/Encerramento:** coordenar o fluxo de telas sem concentrar as regras de todos os sistemas.
- **Player:** input, movimento, animação e colisão; não controla narrativa ou persistência diretamente.
- **Interaction/Dialogue:** alvo próximo, contexto, sequência e feedback de interação.
- **Memory/Time:** estado presente/passado e validação de posição antes da transição.
- **Puzzle/Progression:** sequência do enigma e condições explícitas de progressão, testáveis sem renderização.
- **Save:** serializar, validar, versionar e restaurar o estado mínimo. Capturar erros com mensagem/log apropriado; não simular sucesso.
- **Dados da fase:** objetos, diálogos, pistas, layers e metadados. Manter dados de narrativa fora do renderer quando isso facilitar revisão e teste.
- **Mapa/colisão:** Tiled deve separar visual, obstáculos, objetos de interação e elementos que passam na frente do jogador.
- **UI:** manter controles e textos DOM acessíveis quando adequado; alinhar o espaço da HUD ao viewport lógico e testar legibilidade após o upscale.

### Layers de mapa sugeridas

1. `Ground`: chão base.
2. `GroundDetails`: textura, pequenas variações e detalhes que não ocultam gameplay.
3. `Water`: rio e suas bordas/animação controlada.
4. `PathAndArchitecture`: trilha, ruínas, ponte e santuário.
5. `Collision`: obstáculos e limites não necessariamente visíveis.
6. `Objects`: inscrição, cristal, memória, runas, pontos de interação e spawns.
7. `AbovePlayer`: copas, arcos e elementos que devem sobrepor o personagem.
8. `Lighting`: fontes e máscaras de luz, caso a solução escolhida exija layer dedicada.

O presente e o passado podem compartilhar o mapa-base e ativar camadas/tiles/objetos por estado. Evitar duplicar todo o mapa se diferenças localizadas resolverem a mecânica temporal.

## 7. Fases de implementação

### Fase 0 — Baseline, escopo e ambiente

**Atividades**
- Tratar `V1/` como baseline somente leitura; conferir que a V2 será iniciada em pasta separada.
- Registrar critérios de aceite da fase e comportamentos da V1 que precisam ser preservados.
- Instalar/configurar a stack escolhida em `V2/`, confirmar versões, scripts e browsers disponíveis.
- Fazer spike de renderer/viewport, filtro nearest-neighbor, resize, escala e física/colisão.

**Entrega:** projeto mínimo inicializável e decisões técnicas registradas.

**Gate:** viewport 640 × 360 e apresentação 1280 × 720 demonstradas sem distorção; caminho de build estático conhecido.

### Fase 1 — Fundação e fatia visual

**Atividades**
- Configurar TypeScript, Phaser, Vite, preload de assets e cenas vazias.
- Implementar redimensionamento com proporção preservada, escala 2× de referência, fallback para viewport menor e letterbox quando necessário.
- Criar grid de 32 px, tileset de teste, câmera, personagem placeholder e controle de nearest-neighbor.
- Construir o kit visual de aprovação antes de ampliar o conteúdo.

**Entrega:** cena pequena executável, com teste de nitidez em tamanho nativo e final.

**Gate:** pixels sem blur, personagem legível, tile seams ausentes e layout utilizável no tamanho mínimo acordado.

### Fase 2 — Mapa e linguagem visual

**Atividades**
- Montar no Tiled um greybox da fase 1, com caminho, rio, ponte, ruína, santuário, limites e objetos de jogo.
- Implementar layers de renderização, colisão e elementos acima do jogador.
- Produzir tileset inicial e atlas de peças de borda/canto para reduzir repetição.
- Criar fontes editáveis e exportações PNG com transparência; registrar nomes, dimensões, pivôs e frames.
- Compor variação de materiais, musgo, sombras e pontos de luz sem ocultar rotas ou objetos.

**Entrega:** mapa jogável greybox com kit de arte integrado.

**Gate:** rota principal compreensível, colisões coerentes e leitura dos pontos de interesse preservada.

### Fase 3 — Gameplay principal

**Atividades**
- Implementar movimento em oito direções, aceleração/velocidade segundo comportamento aprovado, colisões e limites.
- Implementar câmera estável e limites de mundo para viewport lógico maior.
- Implementar interação, diálogos, estado de aplicação e pausa.
- Implementar presente/passado com validação de posição e atualização de visibilidade, colisão e pistas.

**Entrega:** exploração funcional com alternância temporal.

**Gate:** sem jitter de câmera ou personagem, sem atravessar obstáculos e sem troca temporal que prenda o jogador.

### Fase 4 — Enigma, progressão e salvamento

**Atividades**
- Portar inscription, artefato, memória, sequência Sol → Lua → Ondas, abertura e encerramento.
- Manter regras em sistemas testáveis e separar texto/configuração do desenho da cena.
- Definir save V2 versionado, novo jogo, continuar, reiniciar e recuperação de dados inválidos.
- Usar chave de armazenamento diferente da V1. Se importar saves V1 for requisito, desenhar e testar conversão antes; caso contrário, não migrar.

**Entrega:** jogo completo do menu ao encerramento.

**Gate:** progressão correta, erro de enigma recuperável, save inválido não bloqueia e fluxo inteiro concluível.

### Fase 5 — Arte final e polimento

**Atividades**
- Expandir tileset e sprites a partir do kit visual aprovado.
- Criar animações de idle/caminhada/interação e estados temporais coerentes.
- Refinar textura orgânica por material, contraste, iluminação localizada e variações de vegetação.
- Ajustar HUD, menus e diálogos ao viewport de 640 × 360 e à escala de apresentação.
- Otimizar somente gargalos observados; controlar tamanho de atlas/assets e custo de luz.

**Entrega:** primeira versão visualmente completa da V2.

**Gate:** legibilidade nativa e em execução, consistência entre assets/estados e performance validada no ambiente-alvo.

### Fase 6 — QA, release e comparação

**Atividades**
- Automatizar regras de progressão, interação, save e transição temporal onde viável.
- Testar dimensões/janelas, telas 1280 × 720 e menores, entrada de teclado, foco e menus.
- Testar browsers acordados e a build publicada, não apenas o servidor de desenvolvimento.
- Fazer playtest sem instrução do desenvolvedor e registrar pontos de confusão e bloqueios.
- Comparar capturas com a referência em composição, densidade de detalhe, material, paleta e iluminação; evitar alegar equivalência exata.
- Registrar riscos, defeitos conhecidos e procedimento de rollback para a V1.

**Entrega:** build V2 candidata a MVP e relatório de aceite.

**Gate:** critérios de aceite abaixo aprovados; V1 continua acessível independentemente da V2.

## 8. Critérios de aceite da V2

### Técnica e apresentação

- [ ] Projeto instala dependências declaradas, inicia em desenvolvimento e gera build estático reproduzível.
- [ ] Viewport lógico é 640 × 360; a escala de referência 2× resulta em 1280 × 720.
- [ ] O aspecto 16:9 é preservado em resize; não há distorção e o fallback de janela menor está documentado/testado.
- [ ] Sprites e tiles são desenhados sem suavização; posições não produzem jitter perceptível.
- [ ] Tiles de 32 × 32 e dimensões de personagem escolhidas são consistentes com grid, pivôs e animação.
- [ ] Build publicado carrega assets locais sem erros impeditivos.

### Jogo

- [ ] Início, exploração, inscrição, artefato, alternância temporal, ponte, memória, enigma e encerramento funcionam de ponta a ponta.
- [ ] Colisões e limites funcionam nos dois estados temporais; transições não permitem softlock.
- [ ] Enigma incorreto fornece feedback e não impede reinício/tentativa correta.
- [ ] Save V2 pode continuar, reiniciar e recuperar dados inválidos sem danificar o save V1.
- [ ] A fase pode ser concluída sem intervenção do desenvolvedor.

### Arte e experiência

- [ ] Pedra, vegetação, água, cristais, luz e sombras têm tratamento coerente por material, sem ruído genérico.
- [ ] Densidade de detalhes não reduz leitura de personagem, caminho, perigos, interações ou UI.
- [ ] A imagem é inspecionada em 640 × 360 e 1280 × 720; compatibilidade de nearest-neighbor verificada em browsers-alvo.
- [ ] Playtest documenta problemas de orientação, interação, enigma e visibilidade; metas quantitativas são definidas antes do teste, não inventadas após ele.

### Performance

- [ ] Medições são feitas em build de produção e dispositivo/browser de referência registrados.
- [ ] Frame time, picos, carregamento e consumo observável são revistos com a ferramenta disponível.
- [ ] Qualquer meta de FPS ou orçamento de memória é definida com o ambiente-alvo antes do aceite; não alegar ganho sem baseline comparável.

## 9. Estratégia de testes

- **Unitários:** progressão, sequência do enigma, validação de save e regras de transição.
- **Integração:** carregamento do mapa/tileset, colisões, objetos, cenas e armazenamento.
- **Gameplay manual:** fluxo completo, mudanças de estado temporal, posições perto de obstáculos e reinício.
- **Visual:** escala 1× e 2×, viewport menor, alinhamento de grid, seams, pivôs, paleta, contraste e luz.
- **Browser:** navegadores desktop acordados, resize, teclado, foco em controles DOM e build publicado.
- **Performance:** mesma build/cena/dispositivo antes e depois de qualquer otimização.
- **Playtest:** observar entendimento de controles, descoberta da mecânica temporal, pistas e resolução do enigma.

Toda validação deve reportar comando/ferramenta, ambiente, resultado e limitações reais. Validação automática não substitui inspeção de arte ou playtest.

## 10. Riscos e mitigação

| Risco | Mitigação |
|---|---|
| A resolução lógica maior altera demais o enquadramento | Prototipar câmera e composição na fatia visual antes de desenhar o mapa completo. |
| Mais detalhe vira ruído visual | Definir hierarquia focal, áreas de descanso e orçamento de detalhe no kit visual. |
| Reuso direto do desenho procedural da V1 limita arte | Tratar V1 como referência funcional, migrar regras e substituir apresentação em etapas; não transcrever tudo sem necessidade. |
| Phaser/Tiled aumenta custo inicial frente ao HTML independente | Manter MVP em uma fase e validar benefício da stack no spike; evitar sistemas genéricos. |
| Escala responsiva não inteira suaviza ou varia a largura dos pixels | Preferir fator inteiro/letterbox quando possível; testar browsers e tamanhos acordados. |
| Estados temporais duplicam mapa e lógica | Reutilizar base de mapa e variar somente layers, tiles, objetos e colisões que mudam. |
| Save V1 incompatível | Chave V2 isolada por padrão; importação somente com requisito e migração validada. |
| Asset de referência tem direitos de terceiros | Usar como inspiração interna; verificar licença antes de reutilizar imagens ou elementos derivados. |

## 11. Dependências e pré-requisitos

- Node.js e gerenciador de pacotes compatíveis com Vite/TypeScript/Phaser, versões a confirmar no setup.
- Editor de código e browser desktop para desenvolvimento.
- Tiled e ferramenta de pixel art, como Aseprite ou equivalente, se disponíveis; formatos e licença devem ser verificados.
- Assets-fonte editáveis e permissões de uso dos materiais incluídos na distribuição.
- Critérios acordados de browser, janela mínima, dispositivos de performance e publicação.

Ferramentas de arte, profiling e browser automatizado são dependências do processo de validação, não assumidas como já instaladas.

## 12. Ordem de execução recomendada

1. Aprovar viewport, escala, stack e browsers-alvo após spike curto.
2. Criar a fatia visual com viewport, câmera, um tile, um cristal e o jogador.
3. Aprovar legibilidade e densidade em 640 × 360 e 1280 × 720.
4. Greybox de fase e colisão antes da arte completa.
5. Implementar e validar o loop jogável completo.
6. Produzir arte final e iluminação sobre o layout aprovado.
7. Rodar testes, playtest, medição e build publicada.

Evitar estimar datas definitivas até confirmar experiência da equipe, disponibilidade de arte e stack instalada.

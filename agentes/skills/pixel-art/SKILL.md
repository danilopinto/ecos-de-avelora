---
name: pixel-art
description: "Use ao criar, editar, especificar ou revisar Pixel Art para jogos, especialmente arte detalhada com pixels artísticos menores, alta densidade, texturas orgânicas, transições tonais, sombras graduais, iluminação atmosférica, sprites, personagens, tilesets e fidelidade visual."
user-invocable: true
---

# Pixel Art

## Objetivo e responsabilidade
Criar, editar ou avaliar arte pixelada legível e coerente com o estilo do jogo, incluindo direção de alta densidade de detalhes quando solicitada: pixels artísticos visualmente menores, texturas orgânicas, variações tonais, sombras elaboradas e luz atmosférica sem perder a nitidez ou a leitura em jogo.

## Quando usar
- Produzir ou revisar personagens, props, cenários, tilesets e ícones pixelados.
- Definir paleta, materiais, shading, iluminação, dithering ou regras de estilo.
- Integrar uma imagem de referência em um projeto sem perder a identidade visual.
- Aproximar-se da direção de Pixel Art detalhada da referência compartilhada: vegetação variada, pedra irregular, mais detalhe por asset e iluminação localizada.

## Instruções técnicas
1. Inspecione arte existente, resolução nativa, escala de sprites, perspectiva, outline, paleta e convenções de importação.
2. Defina finalidade, tamanho nativo do asset, escala de exibição, distância de leitura e orçamento de detalhe. Pixels artísticos menores significam mais unidades de detalhe no asset-fonte, não blur ou upscale artificial.
3. Componha para guiar o olhar e construa do maior para o menor: silhueta/planos, massas de cor, luz e sombra, textura por material, detalhes e acentos.
4. Para alta densidade, introduza irregularidades controladas: pedra com contorno/juntas e variação de valor; vegetação com clusters sobrepostos e múltiplas formas; sombras e pequenas variações cromáticas nas bordas. Faça cada marca descrever forma, material, luz ou profundidade.
5. Crie ramps tonais coerentes entre luz e sombra. Combine iluminação ambiente e fontes localizadas para dar atmosfera e separar planos, respeitando uma direção de luz legível e as cores do projeto.
6. Preserve a hierarquia visual: detalhe a silhueta e os pontos focais primeiro; reduza contraste e frequência de textura em fundos quando competirem com gameplay.
7. Limite cores por material ou iluminação quando apropriado; preserve contraste entre figura e fundo e não imponha paleta, resolução ou tile size arbitrários.
8. Use clusters intencionais e de escala coerente; revise pixels soltos, tangências, outlines inconsistentes, rampas, padrões de textura repetidos e ruído.
9. Harmonize luz, perspectiva, escala, densidade de detalhe e contorno entre assets que aparecerão juntos.
10. Verifique transparência, margens, recortes, dimensões, seams e leitura em tamanho nativo e na escala final.

## Boas práticas
- Leia primeiro em silhueta e em tamanho real de jogo; use zoom apenas para inspeção.
- Use rampas de cor controladas e mudanças de valor que expliquem volume e material.
- Varie frequência, direção e escala da textura de acordo com o material; pedra, folhas, madeira e solo não devem compartilhar o mesmo padrão de ruído.
- Combine sombras graduais, oclusão de contato e luz localizada em clusters discretos; se a engine aplicar luz dinâmica, confirme que o resultado não borra nem destrói o pixel grid da arte.
- Use detalhe para sugerir profundidade e material, mas mantenha áreas de descanso visual e contraste maior no foco/interação.
- Empregue dithering seletivamente para textura/transição, não como substituto automático de shading.
- Evite blur e antialiasing acidental; confirme o método de filtragem no pipeline.
- Preserve perspectiva e direção de luz entre frames, tiles e objetos próximos.
- Para parallax scrolling, agrupe camadas por profundidade e contraste, mantendo velocidade relativa, repetição e alinhamento de pixels coerentes com a câmera.
- Considere contraste, daltonismo e leitura sobre fundos variados quando a arte comunica estados ou perigos.

## Restrições obrigatórias
- Não redesenhe assets existentes nem mude o estilo global sem autorização.
- Não invente resolução, paleta, ferramenta ou recurso do engine; verifique arquivos e opções disponíveis.
- Não presuma que resolução de saída alta, escala 2×, tiles 32×32 ou qualquer tamanho específico são necessários; parâmetros exemplificados numa referência são pontos de partida, nunca medições do projeto.
- Não aumente detalhe de fundo a ponto de ocultar personagens, ameaças, pickups, caminhos, colisões ou informação de UI.
- Não adicione ruído, pixels isolados ou dithering indiscriminado como substituto de textura/material bem desenhados.
- Não afirme que um asset foi gerado, exportado ou visualmente validado se isso não ocorreu.
- Não descarte a fonte editável ou altere formatos em massa sem solicitação.

## Fluxo de execução
1. Recolha referência e regras artísticas observadas.
2. Defina dimensões nativas, escala, paleta, direção de luz, perspectiva e prioridade de detalhe a partir do projeto e do pedido.
3. Produza primeiro forma e planos; acrescente textura orgânica, variação tonal, sombras e luz por material, do foco principal para o fundo.
4. Crie a menor alteração que satisfaça o pedido e compare densidade, paleta, contornos e iluminação com assets relacionados.
5. Valide resolução-fonte, transparência, nitidez, seams e legibilidade em tamanho nativo e no jogo; relate limitações de ferramenta.

## Critérios de qualidade
- Silhueta reconhecível na escala nativa e função visual clara, inclusive quando há alta densidade de detalhes.
- Texturas complexas e orgânicas descrevem materiais por variações intencionais, sem ruído ou padrões genéricos.
- Transições tonais, sombras e iluminação local criam profundidade sem borrar a grade ou destruir contraste de gameplay.
- Clusters limpos, paleta consistente, luz/perspectiva e densidade de detalhe coerentes com os assets adjacentes.
- Dimensões, bordas e transparência adequadas à importação.
- Fidelidade ao estilo existente sem introduzir alterações fora do escopo.

## Exemplo prático
Pedido: “Crie um trecho de ruínas com a riqueza visual da imagem de referência.” Inspecione os tiles e a resolução-fonte do projeto; defina a silhueta do caminho e dos blocos antes de detalhar; varie juntas, rachaduras e valores das pedras, sobreponha clusters de musgo/folhas de escalas diferentes e acrescente sombras nas bordas e luz localizada. Preserve áreas de leitura para o jogador e valide seams, nitidez e contraste na escala real. Não force 32×32 ou outra dimensão sugerida pela referência se os tiles existentes usam outra grade.

---
name: pixel-perfect
description: "Use para diagnosticar ou implementar nitidez Pixel Perfect: resolução interna, escala, grid, alinhamento de sprites e câmeras, filtering, subpixel e seams de tiles."
user-invocable: true
---

# Pixel Perfect

## Objetivo e responsabilidade
Manter pixels nítidos e alinhados em renderização, movimento e composição, respeitando a resolução interna e o pipeline reais do projeto.

## Quando usar
- Imagem borrada, shimmering, jitter, seams ou sprites desalinhados.
- Configuração de resolução, viewport, câmera, escala, filtros ou pixel snapping.
- Importação de tiles/sprites com tamanhos incompatíveis.

## Instruções técnicas
1. Identifique resolução-fonte, resolução interna, viewport, escala de apresentação, proporção, câmera e filtros atuais.
2. Separe resolução de renderização da resolução física da janela/tela; escolha escala inteira quando viável para preservar pixels.
3. Mapeie coordenadas de sprites, tiles, câmera e UI para a mesma unidade/grid; verifique posições fracionárias e origem dos sprites.
4. Avalie o trade-off de letterboxing/cropping ao manter proporção; não distorça para preencher sem requisito.
5. Revise import settings e sampling na engine para nearest-neighbor quando adequado; confirme mipmaps, compressão e filtragem conforme plataforma e uso.
6. Teste movimento de câmera em velocidades e direções diferentes; pixel snapping pode reduzir jitter, mas também causar movimento irregular.
7. Verifique bordas compartilhadas, padding e atlas para evitar bleeding e seams.
8. Valide captura da cena em resolução nativa e escalas de tela previstas.

## Boas práticas
- Mantenha tiles e sprites em dimensões compatíveis com o tile size estabelecido.
- Use coordenadas e pivôs consistentes; alinhe câmera e UI às regras do projeto.
- Prefira mudanças específicas a mudar globalmente importações ou renderização.
- Avalie arte estática e animação: uma configuração nítida em repouso pode tremer em movimento.

## Restrições obrigatórias
- Não imponha uma resolução universal nem escala inteira quando isso quebrar o requisito de plataforma.
- Não altere globalmente filtros, viewport ou câmera sem verificar impacto em outros assets.
- Não afirme correção de blur sem comparar saída renderizada.
- Não confunda resolução do asset, resolução interna e resolução física.

## Fluxo de execução
1. Reproduza/identifique o artefato e os parâmetros que o geram.
2. Determine quais coordenadas e filtros divergem da grade desejada.
3. Faça uma alteração localizada e documente trade-offs visuais.
4. Capture ou inspecione a saída em várias posições e escalas, se ferramentas permitirem.
5. Verifique que nitidez foi melhorada sem introduzir jitter, cortes ou distorção.

## Critérios de qualidade
- Bordas e clusters nítidos sem interpolação inesperada.
- Posição estável durante movimento, sem seams ou recortes novos.
- Aspect ratio e composição preservados ou trade-off explicitamente solicitado.
- Mudança limitada aos recursos que precisavam de correção.

## Exemplo prático
Pedido: “O cenário fica borrado em fullscreen.” Inspecione resolução interna, stretch, escala, filtro e proporção; teste nearest-neighbor e escala inteira se compatíveis com o projeto e compare screenshot fullscreen e janela nativa.

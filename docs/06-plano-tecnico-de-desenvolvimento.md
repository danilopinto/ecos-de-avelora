# Ecos de Avelora — Plano Técnico de Desenvolvimento

> **Autor:** Danilo Pinto · [danilo.pinto1@gmail.com](mailto:danilo.pinto1@gmail.com) · [GitHub](https://github.com/danilopinto/)

## 1. Objetivo e escopo

Este plano transforma a proposta do MVP em uma sequência de implementação e validação técnica. O alvo é entregar **A Floresta Esquecida**, uma fase de navegador concluível do início ao fim, sem backend. A primeira versão jogável está em `jogo.html` e usa Canvas 2D/JavaScript nativos para evitar dependências no runtime e permitir abrir o protótipo diretamente no navegador. A stack Phaser/TypeScript/Vite permanece uma opção arquitetural, não um pré-requisito para testar essa fatia vertical.

O plano original propunha Phaser, TypeScript e Vite; mapas editados no Tiled; arte em Pixel Art. A implementação inicial usa Canvas 2D nativo e arte procedural em um arquivo autônomo. Antes de expandir a base ou produzir conteúdo extenso, avaliar se migrar para Phaser/TypeScript traz benefício concreto frente à simplicidade e execução sem instalação do protótipo.

### Incluído no MVP

- Aplicação Web inicializável e build estático.
- Menu simples, uma fase, uma cena de encerramento e opções de pausa/reinício.
- Movimento, colisões, câmera, interação e diálogos curtos.
- Alternância entre presente e passado com validação de posição.
- Enigma dos três símbolos e progressão até a conclusão.
- Salvamento local versionado e recuperação segura de dados inválidos.
- Testes automatizados dos sistemas lógicos e testes manuais do jogo no navegador.

### Fora do escopo técnico

Backend, contas, multiplayer, salvamento em nuvem, combate, fases 2 a 10, sistema genérico de plugins ou carregamento dinâmico de fases. Os sistemas devem permitir expansão razoável, sem implementar antecipadamente necessidades futuras.

## 2. Princípios e decisões iniciais

1. **Uma fatia vertical antes de conteúdo extenso:** colocar uma área pequena, o jogador, uma colisão e uma interação a funcionar antes de montar a fase inteira.
2. **Dados separados da apresentação:** manter textos da história, configuração do mapa e condições de progressão fora do código de renderização sempre que isso simplificar revisão e testes.
3. **Estados explícitos:** não inferir progressão a partir de efeitos visuais ou da cena atualmente aberta.
4. **Persistência tolerante a falhas:** validar todo dado vindo do `localStorage`; falha de leitura ou formato incompatível nunca deve impedir uma nova partida.
5. **Segurança nas transições:** testar posição e colisões no estado temporal de destino antes de confirmar a troca.
6. **Sem serviço remoto obrigatório:** o jogo deve funcionar como conjunto de arquivos estáticos, sem credenciais ou API de terceiros em runtime.

### Decisões a confirmar na prototipagem

- Versões compatíveis de Phaser, TypeScript e Vite.
- Dimensões finais do mapa, tamanho de tile e política de escalonamento. A proposta de resolução-base é 320 × 180; testar legibilidade em telas menores.
- Uso de Arcade Physics ou colisões implementadas sobre os dados do mapa. Escolher após comparar o protótipo com o movimento e as colisões requeridos.
- Navegadores e sistema de hospedagem estática usados para a validação final.

Registrar essas decisões no README e na documentação de arquitetura quando forem tomadas.

## 3. Organização técnica proposta

```text
ecos-de-avelora/
├── public/
│   ├── assets/
│   │   ├── audio/
│   │   ├── sprites/
│   │   ├── tilesets/
│   │   └── ui/
│   └── maps/fase-01/
├── src/
│   ├── data/                 # textos e configuração da fase
│   ├── entities/             # jogador e entidades do jogo
│   ├── scenes/               # inicialização, menu, exploração e encerramento
│   ├── systems/              # interação, diálogo, tempo, enigma e salvamento
│   ├── types/                # estados e formatos persistidos
│   └── main.ts
├── tests/                    # testes de lógica independentes do navegador
├── index.html
├── package.json
├── tsconfig.json
└── README.md
```

A árvore é uma referência; manter módulos pequenos e coesos, sem criar camadas que não tenham uma responsabilidade real.

### Responsabilidades

| Área | Responsabilidade | Limite principal |
|---|---|---|
| Inicialização | Criar o jogo, carregar recursos e selecionar a primeira cena | Reportar falhas de carregamento; não iniciar uma partida em estado parcial |
| Cenas | Menu, exploração, pausa e encerramento | Coordenar sistemas; não concentrar regras de todos os subsistemas |
| Jogador | Entrada, movimento, animação e colisão | Não controlar a narrativa nem gravar diretamente no armazenamento |
| Interação/diálogo | Encontrar alvos próximos, apresentar e avançar mensagens | Uma interação por vez; estado de diálogo explícito |
| Memória temporal | Trocar estado visual e validar a transição | Não mover o jogador através de colisões inválidas |
| Enigma/progressão | Validar símbolos e liberar a passagem | Regras determinísticas e cobertas por testes |
| Salvamento | Serializar, validar, gravar e restaurar progresso | Formato versionado; falha recuperável |
| Dados da fase | Definir objetos, objetivos, textos e metadados | Dados validados antes de serem consumidos pelos sistemas |

## 4. Modelo mínimo de estado

Manter um estado de partida central tipado, atualizado por ações explícitas. Exemplo conceitual, sujeito à implementação:

```ts
type TimeState = "present" | "past";
type AppState = "menu" | "playing" | "paused" | "completed";

interface GameProgress {
  version: 1;
  currentPhase: "forest-01";
  timeState: TimeState;
  position: { x: number; y: number };
  milestones: {
    inscriptionFound: boolean;
    artifactAwakened: boolean;
    memoryObserved: boolean;
    puzzleSolved: boolean;
    endingReached: boolean;
  };
}
```

O exemplo não determina o formato final de coordenadas nem exige persistir todos os campos. Persistir apenas o que for necessário para retomar a partida com coerência. O estado de interface (por exemplo, pausa ou diálogo aberto) não deve ser restaurado como progresso seguro, a menos que um teste justifique essa decisão.

### Fluxo principal de dados

1. A inicialização carrega recursos e tenta restaurar um progresso validado.
2. Sem progresso válido, oferece iniciar uma partida nova.
3. A cena de exploração envia ações aos sistemas e atualiza o estado de partida.
4. A mecânica temporal verifica colisões do destino antes de alterar o estado.
5. O enigma altera a progressão apenas após validar uma sequência correta.
6. O salvamento grava um snapshot versionado em momentos seguros, como checkpoints ou mudanças importantes.
7. A conclusão da fase registra o marco final e abre a cena de encerramento.

## 5. Plano de implementação por etapas

As semanas são uma ordem de referência compatível com a estimativa inicial de 4 a 6 semanas. Reordenar por dependências reais; não reduzir qualidade para cumprir uma data hipotética.

### Etapa 0 — Fundação e protótipo técnico (semana 1)

**Tarefas**

- Criar projeto TypeScript/Vite e integrar Phaser.
- Configurar verificações de tipos, lint e comandos de desenvolvimento/build.
- Criar cena inicial, canvas responsivo e escalonamento sem suavização.
- Adicionar uma área temporária, jogador provisório, teclado e limites.
- Verificar o fluxo de carregamento e mensagens de erro.

**Saída:** aplicação executável localmente e protótipo de movimentação.

**Condição para avançar:** build de produção gerado; jogador move-se nos eixos e diagonais; a proporção visual é preservada; erros de carregamento são visíveis.

### Etapa 1 — Mapa, movimento e colisões (semana 1–2)

**Tarefas**

- Definir tamanho do tile e mapa inicial com assets provisórios.
- Importar o mapa da fase 1 e identificar camadas de chão, decoração, colisão e objetos.
- Implementar velocidade diagonal normalizada, limites e colisões.
- Configurar câmera seguindo o jogador e limitada ao mapa.
- Testar paredes, obstáculos, cantos e transições de borda.

**Saída:** área explorável sem atravessar obstáculos nem sair dos limites.

**Condição para avançar:** teste manual repetido em todas as direções; colisões previsíveis; câmera estável durante movimento e nos limites.

### Etapa 2 — Interações e progressão da fase (semana 2–3)

**Tarefas**

- Criar identificadores e dados para objetos interativos.
- Detectar alvos próximos e apresentar indicação de interação.
- Implementar diálogos de uma sequência por vez, avanço e encerramento.
- Definir objetivos e marcos narrativos da fase em dados.
- Conectar a inscrição e o artefato à sequência de objetivos.

**Saída:** exploração com inscrição, artefato e feedback de objetivo.

**Condição para avançar:** objetos inacessíveis não são acionáveis; diálogo não duplica nem perde mensagens; marcos são atualizados apenas após ações válidas.

### Etapa 3 — Estados temporais e segurança (semana 3)

**Tarefas**

- Representar presente e passado como estados explícitos.
- Alternar camadas/objetos e apresentação visual por estado.
- Definir colisões e acessibilidade específicas de cada estado.
- Verificar o espaço de colisão do jogador no estado de destino antes de confirmar.
- Recusar a troca inválida com feedback claro, sem alterar parcialmente o estado.
- Incluir pistas visuais e instrução para a primeira utilização.

**Saída:** alternância temporal integrada ao mapa.

**Condição para avançar:** alternar em áreas livres; impedir troca quando o destino sobrepõe obstáculo; garantir que recusa não altera sprites, colisões ou estado do progresso.

### Etapa 4 — Enigma, encerramento e salvamento (semana 4)

**Tarefas**

- Implementar sequência de três símbolos como regra determinística.
- Fornecer feedback para acerto e erro, reiniciando a tentativa incorreta.
- Liberar a passagem e a câmara somente após a solução.
- Criar cena de encerramento que prepara a próxima fase sem implementá-la.
- Implementar formato versionado de salvamento e validação de dados.
- Oferecer continuar, nova partida e reinício da fase.

**Saída:** primeira versão da fase jogável do início ao fim e retomável.

**Condição para avançar:** sequência correta completa a fase; incorreta não bloqueia; dados inválidos ou corrompidos permitem iniciar novamente; carregar progresso não permite pular pré-requisitos narrativos.

### Etapa 5 — Arte, qualidade e publicação (semanas 5–6)

**Tarefas**

- Substituir placeholders prioritários por arte final ou aprovada para o MVP.
- Revisar escala, legibilidade, contraste e transições visuais.
- Executar testes automatizados, fluxo manual e validação em navegadores desktop.
- Testar janela redimensionada, carregamento dos assets e armazenamento local.
- Gerar build de produção e publicar em hospedagem estática escolhida.
- Fazer smoke test no endereço publicado e registrar problemas conhecidos.

**Saída:** MVP publicado e checklist de aceite preenchido.

**Condição de conclusão:** nenhum bloqueio conhecido impede terminar a fase; build publicado carrega sem erros impeditivos; dados locais podem ser restaurados ou reiniciados.

## 6. Estratégia de testes

### Testes unitários de lógica

Cobrir com a ferramenta de teste adotada no projeto:

- Normalização e limites do movimento.
- Transição temporal válida e recusada.
- Regras de colisão relevantes para mudança de estado.
- Validação de sequência do enigma, incluindo erros e reinício.
- Pré-condições de progressão e abertura da passagem.
- Serialização, versão, campos inválidos e fallback do salvamento.

Preferir funções de regra que não dependam de Phaser, DOM ou armazenamento real, para testar os casos sem renderizar o jogo.

### Testes de integração e manuais

- Inicialização, menu, nova partida, pausa, continuar e reiniciar.
- Fluxo completo desde a chegada à floresta até a cena final.
- Todas as direções, diagonais, limites de mapa e obstáculos.
- Alternância temporal em posições seguras e bloqueadas.
- Interação próxima/longe, mensagens e avanço de diálogos.
- Enigma errado, reiniciado e resolvido.
- Salvamento novo, restaurado, ausente e inválido.
- Navegadores modernos para desktop e diferentes tamanhos de janela.
- Build servido localmente e após a publicação.

### Verificações automatizadas do projeto

Manter scripts separados e executáveis localmente para:

- `typecheck`: checagem de tipos TypeScript.
- `lint`: regras de estilo e erros estáticos.
- `test`: testes unitários.
- `build`: geração do pacote estático.

Os nomes finais dos comandos serão definidos no `package.json` quando o projeto de jogo for criado.

## 7. Requisitos não funcionais e operação

- **Compatibilidade:** teclado como entrada principal; não depender de API experimental do navegador.
- **Renderização:** preservar proporção e pixels nítidos, com interface legível em tela menor.
- **Desempenho:** evitar alocação e reconstrução de objetos a cada quadro sem necessidade; medir em um computador de referência antes de definir metas numéricas.
- **Acessibilidade básica:** exibir controles, oferecer texto legível e comunicar estado temporal por mais de apenas mudança de cor.
- **Resiliência:** falha de asset essencial deve indicar erro; falha de salvamento deve notificar e oferecer nova partida, sem falsa confirmação de gravação.
- **Privacidade:** manter progresso apenas no dispositivo; não coletar nem enviar dados de jogador no MVP.
- **Publicação:** arquivos estáticos; validar caminhos relativos de assets e funcionamento em subdiretório caso a hospedagem escolhida o exija.

## 8. Riscos técnicos e resposta

| Risco | Resposta técnica |
|---|---|
| Alternância coloca o jogador dentro de obstáculo | Validar colisão no estado de destino antes de alterar qualquer estado |
| Mapa e código ficam acoplados | Usar IDs e propriedades do mapa com validação na carga |
| Salvamento antigo ou inválido bloqueia o jogo | Versionar formato, validar campos e permitir reinício explícito |
| Placeholder artístico atrasa a avaliação visual | Aprovar cedo paleta, tamanho de tile e escala de exibição |
| Cronograma cresce com escopo futuro | Manter uma fase e priorizar P0; não implementar backend ou sistemas das demais fases |
| Assets de referência têm restrições de uso | Usá-los apenas como referência; confirmar licença de cada asset antes de distribuí-lo no jogo |
| Build funciona apenas na raiz do domínio | Testar caminhos e base URL na hospedagem escolhida antes da publicação final |

## 9. Critérios técnicos de conclusão

- [ ] Projeto inicializa e gera build de produção reproduzível.
- [ ] Checagem de tipos, lint e testes automatizados passam.
- [ ] Jogador move-se em oito direções e respeita obstáculos e limites.
- [ ] A câmera acompanha o jogador sem sair da área jogável.
- [ ] Interações e diálogos não deixam a progressão em estado inconsistente.
- [ ] A alternância temporal não permite atravessar obstáculos nem prender o jogador.
- [ ] Sequências incorretas do enigma são recuperáveis; a correta libera a passagem.
- [ ] Salvamento válido restaura progresso; dado inválido permite reinício com erro visível.
- [ ] A fase é concluível do começo ao fim em teste manual.
- [ ] Build publicado carrega recursos e funciona no ambiente escolhido.

## 10. Dependências e pontos em aberto

- Assets finais ou licença aprovada para uso e distribuição.
- Decisão de versões da stack após o protótipo inicial.
- Navegadores e dispositivo de referência para validação.
- Hospedagem estática e configuração do endereço público.
- Decisão sobre checkpoints exatos e quais marcos podem ser restaurados.
- Definição final das pistas e da solução do enigma pela documentação narrativa.

Este documento descreve um plano, não uma implementação concluída. Estimativas, ferramentas e critérios devem ser revisados quando o protótipo e os primeiros testes fornecerem evidência real.

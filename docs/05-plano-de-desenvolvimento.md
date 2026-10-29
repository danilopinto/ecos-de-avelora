# Ecos de Avelora — Plano de Desenvolvimento do MVP

> **Autor:** Danilo Pinto · [danilo.pinto1@gmail.com](mailto:danilo.pinto1@gmail.com) · [GitHub](https://github.com/danilopinto/)

## Objetivo e estimativa

Desenvolver e publicar a primeira fase para validar a experiência central antes de iniciar as outras nove. Prazo inicial estimado: **4 a 6 semanas**, assumindo uma pessoa com conhecimentos básicos a intermediários de desenvolvimento Web e jogos 2D. O prazo depende da experiência, produção de assets, complexidade dos enigmas e disponibilidade; é uma estimativa, não uma garantia.

## Etapas propostas

### Semana 1 — Fundação técnica

Configurar Phaser, TypeScript e Vite; criar a aplicação; configurar canvas e escalonamento; implementar movimento, colisões e câmera; criar mapa temporário.

**Entrega:** personagem controlável em mapa simples. **Conclusão:** movimento consistente, colisões funcionais e câmera estável.

### Semana 2 — Arte e exploracao

Definir paleta, criar/integrar tileset, montar mapa inicial, posicionar ruínas e objetos e criar animações básicas.

**Entrega:** fase explorável com visual provisório ou inicial. **Conclusão:** jogador explora sem atravessar obstáculos nem sair da área.

### Semana 3 — Mecânica temporal

Criar presente e passado, alternância, elementos que mudam, validação de posição/colisões e pistas.

**Entrega:** mecânica temporal funcional. **Conclusão:** a alternância revela pistas e não prende o jogador.

### Semana 4 — Enigma e narrativa

Implementar diálogos, inscrição inicial, enigma dos três símbolos, liberação da câmara e cena de encerramento.

**Entrega:** primeira versão jogável do início ao fim. **Conclusão:** jogadores conseguem concluir a fase seguindo as pistas.

### Semanas 5 e 6 — Polimento e publicação

Testar fluxo completo, corrigir bugs, ajustar enigma e instruções, melhorar efeitos, implementar/testar salvamento, verificar navegadores e publicar.

**Entrega:** MVP acessível por endereço Web. **Conclusão:** critérios obrigatórios de aceite atendidos.

## Ordem de prioridade

### P0 — Obrigatório

Inicialização, movimento e colisões, mapa da fase 1, interações, alternância temporal, enigma, progressão narrativa, cena final e conclusão sem bloqueios.

### P1 — Entrega estavel

Salvamento local, menu, pausa/reinício, interface de objetivos, tratamento de erros de carregamento e testes de navegadores.

### P2 — Polimento

Música, efeitos sonoros, animações decorativas, segredos opcionais e efeitos adicionais na alternância. P2 não deve atrasar P0.

## Checklist de aceite

- [ ] O jogo abre em navegador suportado.
- [ ] Movimento em oito direções, colisões e limites funcionam.
- [ ] A câmera acompanha o jogador.
- [ ] O visual tem Pixel Art consistente.
- [ ] Inscrição, artefato e diálogos funcionam.
- [ ] Alternância temporal é consistente e mantém posição válida.
- [ ] O enigma tem pistas suficientes; erro não bloqueia o progresso.
- [ ] A solução abre a câmara e a cena final prepara a continuação.
- [ ] Progresso salva/restaura e a fase pode ser reiniciada.
- [ ] A versão publicada foi testada e não tem bloqueios conhecidos.

## Plano de testes

- **Movimento:** todas as direções, colisões, limites e transições.
- **Estados temporais:** alternância em locais permitidos e problemáticos; colisão em ambos os estados; posição válida.
- **Enigma:** sequência incorreta e correta, reinício, porta e impossibilidade de pular etapas.
- **Progressão:** nova partida, conclusão, reinício, continuação e dados de salvamento inválidos.
- **Navegadores:** pelo menos dois navegadores modernos para desktop, janelas de dimensoes diferentes e assets no build publicado.

## Validacao com jogadores

Testar com pessoas que não participaram do desenvolvimento. Observar se entendem movimentação, interações, artefato, enigma e conclusão.

Meta inicial proposta: pelo menos 80% concluem sem ajuda externa. É uma referência a validar, não um resultado garantido.

## Riscos e mitigacoes

- **Escopo excessivo:** priorizar P0 e manter as outras fases apenas na documentação.
- **Mecânica temporal confusa:** usar sinais visuais consistentes, instruções e pistas ambientais.
- **Bloqueios de progressão:** testar posições inválidas, oferecer saída segura e permitir reinício.
- **Produção artística demorada:** usar placeholders e substituir assets gradualmente.
- **Salvamento inconsistente:** versionar e validar o formato, oferecendo reinício se inválido.

## Entregaveis do MVP

Código-fonte, projeto configurado para desenvolvimento local, assets da fase, mapa da Floresta Esquecida, sistemas de interação/memória/enigma/salvamento, build Web, documentação, checklist de testes e endereço de publicação.

## Proxima etapa

Coletar feedback, corrigir usabilidade, ajustar ritmo/dificuldade, revisar o roteiro, planejar a fase 2 com base nos sistemas existentes e evitar duplicar a lógica principal.

## Regra de escopo

A primeira entrega deve ser uma fase pequena, completa e estável. O objetivo não é demonstrar dez fases incompletas, mas provar que a experiência central funciona e pode ser ampliada.

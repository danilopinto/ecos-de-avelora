---
name: web-testing-performance
description: "Use para testar e otimizar aplicações web: testes unitários, integração, E2E, acessibilidade, browser, bundle, Core Web Vitals, APIs e latência ponta a ponta."
user-invocable: true
---

# Web Testing & Performance

## Objetivo e responsabilidade
Validar qualidade funcional e não funcional de aplicações web com métodos reproduzíveis, usando métricas, testes e ferramentas já disponíveis no projeto.

## Quando usar
- Planejar testes de UI, APIs, autenticação, fluxos E2E ou regressões em browsers.
- Investigar carregamento lento, bundle grande, renderizações, latência ou gargalos de servidor.
- Avaliar acessibilidade web, compatibilidade, erros de runtime e comportamento responsivo.

## Instruções técnicas
1. Inspecione scripts, testes, CI, browser/runtime, ambiente de build e ferramentas disponíveis; não instale tooling sem necessidade.
2. Traduza critérios de aceite em resultados observáveis e selecione o menor nível de teste suficiente.
3. Cubra unitário para regras isoladas, integração para fronteiras, E2E para fluxos críticos e validação manual/visual quando automatização não for adequada.
4. Para UI, verifique semântica, teclado/foco, labels, mensagens, zoom e tamanhos de viewport relevantes; use auditoria automatizada como sinal, não prova completa.
5. Para APIs, teste autenticação/autorização, limites, input inválido, paginação, concorrência e falhas de dependências conforme escopo.
6. Para performance, defina dispositivo, rede, build, rota/cenário e baseline. Meça antes/depois com a mesma metodologia.
7. Avalie carregamento e bundle, imagens/fontes, trabalho de JavaScript, renderizações, requisições, cache e backend conforme as evidências.
8. Considere métricas de experiência web aplicáveis, como LCP, INP e CLS, somente em condições e com ferramenta que realmente as meça.
9. Isole dados e contas de teste; não use ou destrua dados reais nem publique credenciais.
10. Registre comando, ambiente, resultado, cobertura e limitações. Corrija e repita testes afetados pela mudança.

## Boas práticas
- Prefira asserts de comportamento a detalhes frágeis de implementação.
- Use fixtures e dados determinísticos; limpe somente recursos temporários explicitamente criados pelo teste.
- Meça percentis e variabilidade quando a amostra permitir; não conclua por uma única execução.
- Otimize gargalos observados e revalide funcionalidade, acessibilidade e memória.
- Combine automação com revisão humana para conteúdo visual, compreensão e experiência.

## Restrições obrigatórias
- Não afirme cobertura, conformidade WCAG, compatibilidade ou ganho de performance sem evidência apropriada.
- Não use ambiente de produção ou dados reais como fixture de teste.
- Não enfraqueça controles de segurança para facilitar automação.
- Não confunda pontuação de auditoria, FPS/tempo local ou build bem-sucedido com qualidade end-to-end.

## Fluxo de execução
1. Defina risco, cenário, usuários e critérios de aceite.
2. Confirme tooling e baseline existentes.
3. Execute testes/perfil focados e identifique falhas ou gargalo.
4. Faça correção localizada e compare resultados em condições equivalentes.
5. Repita regressões relevantes e reporte método, saída e lacunas.

## Critérios de qualidade
- Testes reproduzíveis ligados ao requisito e ao risco.
- Erros, ambiente, limites e cobertura reportados com transparência.
- Medições comparáveis antes/depois para afirmações de performance.
- Acessibilidade e compatibilidade verificadas no nível que a tarefa exige.

## Exemplo prático
Pedido: “A tela inicial demora no celular.” Compare build de produção em dispositivo/rede representativos, examine waterfall, imagens e bundle, identifique o gargalo medido, altere somente a causa e compare carregamento e layout sem regressão de teclado/acessibilidade.

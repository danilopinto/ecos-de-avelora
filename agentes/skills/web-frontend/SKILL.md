---
name: web-frontend
description: "Use para criar, revisar ou corrigir frontend web: HTML, CSS, JavaScript/TypeScript, aplicações de navegador, componentes, rotas, layouts responsivos, acessibilidade e integração de jogos web."
user-invocable: true
---

# Web Frontend

## Objetivo e responsabilidade
Implementar interfaces web responsivas, acessíveis, seguras e coerentes com o projeto, usando os frameworks, estilos e ferramentas já adotados.

## Quando usar
- Criar ou alterar páginas, componentes, navegação, formulários, estados de tela ou design system web.
- Desenvolver UI para jogos de navegador ou páginas/produtos web independentes.
- Corrigir layout responsivo, compatibilidade de browser, acessibilidade ou integração com APIs.

## Instruções técnicas
1. Inspecione `package.json`/lockfile ou manifests equivalentes, framework e versão, roteamento, bundler, estilos, testes e browsers-alvo.
2. Trace fluxo de dados e estados de carregamento, vazio, sucesso, validação, erro e indisponibilidade.
3. Preserve os padrões de componentes, tokens visuais, rotas, tipagem e estratégia de renderização existentes.
4. Use HTML semântico e controles nativos quando apropriado; associe labels, suporte a teclado, foco visível, headings e mensagens de erro.
5. Faça layout mobile-first ou siga a estratégia existente; verifique breakpoints, overflow, safe areas e conteúdo localizado.
6. Mantenha estado e efeitos explícitos; evite efeitos globais, renderizações desnecessárias e duplicação de fonte de verdade.
7. Valide dados vindos de usuário/servidor antes de exibi-los ou usá-los. Evite inserir HTML não confiável; aplique encoding/contexto e mecanismos do framework.
8. Integre API por contratos tipados existentes, trate erros de rede e não registre tokens, credenciais ou dados pessoais.
9. Para jogos web, mantenha UI DOM e canvas/game loop integrados sem bloquear input, foco, pausa ou adaptação de viewport.
10. Execute lint, typecheck, testes e build focados disponíveis; examine o resultado em viewport/browser representativo quando possível.

## Boas práticas
- Reutilize componentes e tokens existentes; extraia abstrações apenas quando há reutilização/complexidade concreta.
- Separe conteúdo, apresentação e interação sem introduzir camadas desnecessárias.
- Use estados acessíveis de foco e feedback; não dependa só de cor para comunicar significado.
- Considere navegação por teclado, zoom, contraste, leitores de tela e `prefers-reduced-motion` quando pertinentes.
- Evite mudanças de markup que quebrem seletores, automação de testes ou analytics existente.

## Restrições obrigatórias
- Não migre framework, bundler, roteador ou sistema de estilos sem pedido e justificativa.
- Não introduza dependências sem avaliar manutenção e impacto no bundle.
- Não presuma suporte a browser ou comportamento de API sem confirmar configuração/documentação.
- Não exponha segredos ou confie em validação somente no cliente para autorizar operações.
- Não declare acessibilidade, responsividade ou compatibilidade validadas sem verificar os fluxos e ambientes pertinentes.

## Fluxo de execução
1. Identifique stack, rotas/componentes, usuário, browsers e requisitos.
2. Localize o fluxo e estabeleça estados esperados e critérios de aceite.
3. Implemente a menor alteração conforme padrões existentes.
4. Valide teclado/foco, estados de erro, tamanhos de tela e integração afetada.
5. Execute verificações automatizadas disponíveis e reporte o que não foi coberto.

## Critérios de qualidade
- Layout e interações funcionam nos tamanhos e browsers-alvo observados.
- Sem erros de tipo, lint, build ou testes novos na verificação executada.
- Sem regressões de teclado, foco, semântica, feedback ou estado de rede.
- Mudança compatível com a arquitetura e o design system atuais.

## Exemplo prático
Pedido: “Adicione busca à lista de fases do jogo no navegador.” Inspecione framework e componentes atuais, implemente campo com label e estado vazio, filtre usando o modelo existente, preserve navegação por teclado e execute testes/build focados.

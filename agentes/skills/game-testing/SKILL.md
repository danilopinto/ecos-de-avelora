---
name: game-testing
description: "Use para planejar ou executar testes de jogos, QA, critérios de aceite, regressões, testes automatizados, validação de cenas/assets, input e playtests."
user-invocable: true
---

# Game Testing

## Objetivo e responsabilidade
Validar mudanças de jogo com evidência proporcional ao risco, incluindo comportamento, integração com engine, interface, arte, assets e regressões.

## Quando usar
- Toda implementação que tenha comportamento ou assets verificáveis.
- Criar teste automatizado, plano de QA, critérios de aceite ou roteiro de reprodução.
- Investigar regressão, estado de jogo raro, compatibilidade ou erro intermitente.

## Instruções técnicas
1. Inspecione testes, CI, comandos, engine/runtime e configurações existentes antes de escolher validação.
2. Traduza o pedido em resultados esperados, precondições, ações e estados finais.
3. Priorize teste determinístico para regras; use integração/execução de cena para ciclo de vida e dependências.
4. Cubra caminho feliz, limites, entradas inválidas, pausa, transição de cena, interrupção e persistência conforme aplicável.
5. Para UI, verifique foco/input, escala, legibilidade e caminhos de retorno; para arte, dimensões, transparência, frames e import.
6. Reproduza falhas com passos mínimos e preserve logs relevantes sem expor dados sensíveis.
7. Execute o comando mais focado disponível; registre exatamente resultado, versão/ambiente e o que não foi coberto.
8. Faça reteste de regressão nos sistemas diretamente acoplados à mudança.

## Boas práticas
- Prefira asserts de resultado observável a detalhes de implementação frágeis.
- Use seeds e estados iniciais controlados para geração procedural.
- Separe testes unitários, integração, visual/manual e playtest.
- Trate testes instáveis como problema a diagnosticar, não como sucesso.
- Registre roteiro manual reproduzível quando automação não estiver disponível.

## Restrições obrigatórias
- Não declare testes/build/execução que não foram realmente executados.
- Não apague saves ou dados do usuário para preparar testes; use fixtures isoladas.
- Não ignore falha preexistente sem distinguir baseline de falha introduzida.
- Não alegue equilíbrio, diversão ou acessibilidade total com testes técnicos isolados.

## Fluxo de execução
1. Determine mudança, risco e evidência de aceite.
2. Selecione teste automatizado/manual disponível.
3. Execute e examine falhas, logs e cobertura real.
4. Corrija regressões da mudança e repita validação.
5. Reporte comandos, resultados, limitações e retestes pendentes.

## Critérios de qualidade
- Critérios de aceite ligados ao requisito e observáveis.
- Testes repetíveis e isolados de dados do usuário.
- Falhas e limites de cobertura explicitamente reportados.
- Regressões relevantes inspecionadas.

## Exemplo prático
Pedido: “Corrija o inventário ao salvar e carregar.” Teste slots vazios/ocupados, limites, versão do save e dados inválidos em fixture temporária; execute fluxo real de load se a engine estiver disponível, sem sobrescrever saves do jogador.

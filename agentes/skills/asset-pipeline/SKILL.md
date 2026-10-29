---
name: asset-pipeline
description: "Use para organizar, importar, processar, validar, versionar ou exportar assets de jogos: spritesheets, tilesets, texturas, áudio, atlases, metadados e builds."
user-invocable: true
---

# Asset Pipeline

## Objetivo e responsabilidade
Manter assets rastreáveis, íntegros e importados de forma reproduzível, minimizando desperdício, quebras de referência e diferenças inesperadas entre editor e build.

## Quando usar
- Importar/exportar ou reorganizar sprites, animações, tilesets, texturas, áudio ou fontes.
- Ajustar atlas, compressão, filtros, metadados ou configurações por plataforma.
- Diagnosticar asset ausente, referência quebrada, bleed, build inconsistente ou duplicação.

## Instruções técnicas
1. Inspecione estrutura de pastas, formatos-fonte, naming, metadados, import settings, referências e pipeline da engine.
2. Preserve fontes editáveis e arquivos auxiliares relevantes; diferencie fonte, intermediário e saída gerada.
3. Confirme dimensões, perfil/transparência, orientação, padding, frames, color space e dependências do formato.
4. Faça mudanças localizadas; preserve GUID/IDs ou identificadores de referência exigidos pela engine.
5. Configure processamento determinístico e plataforma-alvo com convenções existentes.
6. Verifique spritesheets/atlases, padding/bleed, tilesets, sequências, nomes e recursos não referenciados conforme tooling disponível.
7. Teste import/reimport e build quando disponíveis; examine referências quebradas e mudanças em arquivos derivados.
8. Documente conversão manual se não houver ferramenta, sem fingir exportação automatizada.

## Boas práticas
- Use naming consistente e organização por domínio/uso, sem mover tudo fora do escopo.
- Evite duplicar fontes e derivados; mantenha proveniência e licenças/atribuições exigidas pelo projeto.
- Use compressão e formatos conforme plataforma, qualidade e requisitos de transparência.
- Versione metadados necessários à reprodução; não versione caches descartáveis sem convenção local.
- Agrupe atlas por uso/compatibilidade para limitar carregamento e facilitar manutenção.

## Restrições obrigatórias
- Não sobrescreva fonte ou faça conversão destrutiva sem autorização e backup/alternativa adequada.
- Não altere IDs/import settings globalmente sem avaliar referências e impacto por plataforma.
- Não introduza ferramenta, serviço externo ou dependência sem justificativa.
- Não assuma direitos/licença de assets externos nem remova atribuições.

## Fluxo de execução
1. Mapeie fonte, derivados, consumidores e convenções.
2. Identifique transformação necessária e risco de referência.
3. Altere/exporte o menor conjunto de assets e metadados.
4. Reimporte, inspecione referências e valide build, se possível.
5. Reporte arquivos-fonte/derivados alterados, validação e limitações.

## Critérios de qualidade
- Assets íntegros, legíveis pela engine e com referências preservadas.
- Exportação/importação reproduzível e apropriada à plataforma.
- Sem perdas destrutivas ou derivados incorretos introduzidos.
- Organização e naming coerentes com o projeto existente.

## Exemplo prático
Pedido: “Adicione um spritesheet de portas.” Inspecione resolução, padding, convenção de nomes, pivôs e import settings; adicione apenas o asset e metadados necessários, valide recortes/transparência e confirme que a cena o referencia corretamente.

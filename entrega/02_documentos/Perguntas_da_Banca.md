# Perguntas para preparar a defesa

Respostas de apoio à apresentação do AlertaCidadão. Dados e evidências atualizados em 19/11/2026. Usem as respostas para explicar o projeto com as próprias palavras e respeitem os limites observados.

## Já não existe alerta da Defesa Civil?

Sim. O projeto propõe uma jornada complementar de comunicação: relacionar o aviso ao local cadastrado, apresentar contexto e preferências, registrar a leitura e permitir acompanhamento pela organização. Não alegamos inventar o alerta por localidade ou substituir os canais oficiais. A necessidade dessa camada em uma administradora ainda deve ser validada com pessoas e compradores.

## Por que uma organização pagaria?

A hipótese é que ela pague pela operação e pela rastreabilidade da comunicação. O comprador inicial a testar é uma administradora de conjuntos residenciais; o morador teria acesso gratuito. Ainda não temos contratos nem disposição de pagamento comprovada. A proposta comercial deve ser confrontada com a rotina, as alternativas e o orçamento do comprador.

## Como chegaram a R$ 990 por mês?

É uma hipótese de oferta por organização, com até 500 cadastros e 2.000 mensagens externas em uma operação futura. A planilha separa as premissas de mensageria, infraestrutura, suporte, carga sobre a receita e custos fixos. No cenário-base, R$ 990 menos R$ 500 de variáveis e R$ 59,40 de carga hipotética de 6% deixam R$ 430,60 de contribuição por cliente. Para cobrir R$ 18.000 de fixos mensais assumidos, o ponto de equilíbrio é de 42 clientes, arredondado para cima.

Esses valores são premissas, não cotações de fornecedores ou resultados comerciais obtidos. Na sensibilidade com mensagem a R$ 0,30, a contribuição cai para R$ 130,60 e o equilíbrio sobe para 138 clientes. A oferta futura de mensagens externas não significa que o MVP já faça esses envios.

Fonte: [modelo financeiro](../05_modelo_financeiro/Modelo_Financeiro_AlertaCidadao.xlsx) e [auditoria dos cálculos](../05_modelo_financeiro/auditoria_calculos.json).

## O que funciona no site público?

O MVP publicado executa cadastro manual, extração textual de PDF, revisão dos campos, seleção por área, validade e preferências, notificação interna, confirmação de leitura, painel, exportação e isolamento entre visitantes. O processamento e o armazenamento funcionam com cenários sintéticos. A implementação pública usa JavaScript em Worker e banco D1 persistente.

As 36 de 36 verificações HTTP públicas aprovadas documentam essa implantação. A jornada cadastrou locais A e B, gerou uma notificação pertinente apenas para A, registrou a leitura e atualizou o painel. Repetir o cenário não criou uma notificação duplicada, e uma segunda sessão não acessou os registros da primeira. Os três PDFs sintéticos foram extraídos e comparados com seus gabaritos.

Fonte: [verificação pública](../04_evidencias/site_publico_verificado.json) e [método das evidências](../04_evidencias/LEIA_EVIDENCIAS.md).

## Qual é a diferença entre o site público e a versão Python?

O repositório contém as duas implementações: Python na raiz e Worker/D1 em `sites/`. A aplicação pública usa Worker/D1. A implementação Python/FastAPI foi testada com SQLite e PostgreSQL e inclui OCR de imagem com Tesseract. No site público, a extração demonstrada é de PDF textual, além da entrada manual; não apresentamos o OCR de imagem como recurso ativo nessa hospedagem.

As capturas e a demonstração técnica de 90 segundos registram a versão Python executada localmente em 17/11/2026. A base visual do pitch reutiliza essa jornada real. As verificações HTTP de 19/11/2026 documentam separadamente o resultado atual no endereço público.

Fonte: [repositório](https://github.com/jpczz/alertacidadao-bi) e [origem das evidências](../04_evidencias/LEIA_EVIDENCIAS.md).

## Os dados são falsos?

São dados sintéticos, identificados como tal. A entrada é controlada, enquanto o processamento, o armazenamento e a interface são executados de verdade. Isso permite reproduzir o fluxo e verificar seus estados sem apresentar um cenário acadêmico como emergência real. Esses resultados não representam uma amostra de moradores nem comprovam utilidade em campo.

## Por que não aparece uma mensagem recebida no WhatsApp?

O canal demonstrado é a central interna do aplicativo. A implementação Python possui testes de um adaptador HTTP de mensageria, mas nenhum envio real por WhatsApp/SMS foi executado. Uma operação externa exige configuração do provedor, destinatários optantes e verificação do recebimento. Não usamos imagens de conversas para simular uma integração inexistente.

## Como sabem que uma rua vai alagar?

O MVP não faz essa previsão. Ele trabalha com áreas fictícias e regras de correspondência entre local e aviso. Uma integração futura precisa respeitar a abrangência e o significado dos dados da fonte. Um aviso meteorológico não equivale a risco confirmado em cada imóvel, e o produto acadêmico não é um sistema de emergência.

## Qual é a validação do Canvas?

Temos evidências técnicas do fluxo e documentação da evolução do planejamento para a implementação local e a publicação. Dor, compreensão, utilidade percebida e preço continuam como hipóteses até serem avaliados em entrevistas e tarefas observadas. O protocolo de coleta está preparado, mas não existem entrevistas ou resultados humanos preenchidos. Não reconstruímos resultados de CP1 que não foram fornecidos.

Fonte: [dossiê](Dossie_AlertaCidadao_BI.pdf) e [protocolo de validação](../06_validacao/Protocolo_de_Validacao.pdf).

## Os 61 testes provam segurança ou impacto?

Não. São 61 casos únicos da implementação Python, repetidos em SQLite e PostgreSQL. Não são 122 casos diferentes. A implementação Worker tem 12 testes locais; a implantação pública passou em 36 verificações HTTP. Cada conjunto tem um escopo próprio e os números não devem ser somados como se representassem participantes ou resultados de impacto.

As execuções locais e públicas documentadas não equivalem a aprovação do CI remoto. Também não substituem uma auditoria completa, teste de carga, uso por moradores ou estudo de redução de danos. O relatório demonstra o comportamento testado, dentro das condições controladas.

Fonte: [relatório técnico](../04_evidencias/Relatorio_Ensaio_Controlado.pdf) e [método das evidências](../04_evidencias/LEIA_EVIDENCIAS.md).

## O painel com 100% significa que o alerta foi eficaz?

Na jornada sintética, 100% significa uma leitura registrada para uma notificação interna criada. O indicador deriva dos eventos daquela sessão. A confirmação é uma ação voluntária e não comprova compreensão, entrega em canal externo, mudança de comportamento ou proteção contra danos. Esses resultados exigem outras métricas e observação com pessoas reais.

## O que falta para um piloto real?

Validar o problema e o comprador, observar pessoas usando a solução, conectar fontes com condições claras, implementar identidade e permissões adequadas à operação comercial, revisar privacidade, verificar continuidade e custos e testar um canal externo. A publicação permite avaliar o fluxo, mas não transforma a demonstração em serviço de emergência. O plano de validação descreve uma próxima etapa, não uma atividade já realizada.

## O que ainda falta para entregar o trabalho?

O vídeo final foi fornecido pela equipe e está vinculado em [YouTube](https://youtu.be/RtqAPawx7h4). O dossiê já inclui esse endereço na Ficha Técnica. O passo acadêmico restante é conferir os links, a duração e a participação exigidas, anexar `Dossie_AlertaCidadao_Para_Submissao.pdf` no portal da disciplina e guardar o comprovante. A página 32 do enunciado exige PDF único; o link do GitHub organiza o projeto, mas não substitui esse arquivo.

O prazo informado é 19/11/2026 às 23h55; o grupo adota o horário de São Paulo. Os arquivos e os links precisam permanecer acessíveis durante a correção. O roteiro e a organização dos materiais apoiam a entrega; a avaliação cabe ao professor.

00  /  FIAP / GLOBAL SOLUTION 2026.2

# AlertaCidadão

Dossiê de produto e negócio

Do aviso à confirmação: uma jornada de comunicação climática para moradores e organizações.

Interface implementada, registrada na execução local. Cenários sintéticos, sem alertas reais ou envio externo.

Business Intelligence & Startup Development

Professor: Henio Luiz Scheidt

Global Solution CitizenTech | Engenharia de Software | 4ES

Equipe (5 integrantes):
RM 553282 — Kaio Vinicius Meireles Alves · RM 553956 — Lucas Alves de Souza
RM 554323 — Guilherme Fernandes de Freitas · RM 553172 — João Pedro Chizzolini de Freitas
RM 553945 — Henrique Rafael

Versão 3.1 | 19 de novembro de 2026. MVP e repositório públicos; vídeo-pitch da equipe vinculado à Ficha Técnica. Validação humana e comercial permanece como próxima etapa.

01  /  PRODUTO ENTREGUE

## Ficha técnica e leitura executiva

O AlertaCidadão demonstra uma operação completa: registrar um local, relacionar um aviso válido à área e às preferências, disponibilizar uma notificação e registrar a confirmação de leitura. O painel calcula seus indicadores a partir desses registros.

| Campo | Definição desta entrega |
| --- | --- |
| Cidadão e território | Moradores em contexto urbano. A execução usa Cidade Exemplo/SP e áreas fictícias TESTE-A, B e C, sem atribuir risco a bairros reais. |
| Problema investigado | Organizar e acompanhar comunicações climáticas pertinentes à localidade de interesse. |
| Proposta de valor | Contexto para o morador; rastreabilidade da comunicação para a organização. |
| Comprador proposto | Administradora de conjuntos residenciais. Hipótese comercial ainda não validada. |
| Componentes | Site público: HTML/CSS/JavaScript, API JavaScript em Cloudflare Worker e banco D1. Versão Python/FastAPI, com SQLite/PostgreSQL, também disponível no repositório. |
| Dados e inteligência | Cenários e PDFs sintéticos, extração textual e revisão humana. OCR de imagens apenas no Python. Sem modelo de IA preditiva ou generativa para risco climático. |
| Indicadores | Locais, notificações internas, leituras confirmadas, taxa de confirmação e histórico de eventos. |
| ODS | 11 e 13: contribuição pretendida à preparação urbana e conscientização climática; impacto social não medido. |

MVP público: [Abrir o AlertaCidadão](https://alertacidadao-bi-jpczz.est-dio-like-0113.chatgpt.site)

Repositório público: [github.com/jpczz/alertacidadao-bi](https://github.com/jpczz/alertacidadao-bi)

Vídeo-pitch da equipe: [https://youtu.be/RtqAPawx7h4](https://youtu.be/RtqAPawx7h4)

Requisitos do pitch: até cinco minutos e participação dos cinco integrantes. O vídeo técnico de 90 segundos é apenas material de apoio. Conferir acesso ao vídeo pelo link acima antes do envio. [F1]

02  /  CIDADÃO E CONTEXTO

## Problema de comunicação climática

### O que se sabe e o que ainda é hipótese

Os canais oficiais da Defesa Civil já oferecem comunicação de alertas. O projeto não reivindica a invenção de alertas por localidade nem substitui esses serviços. [R1]

O INMET distingue avisos meteorológicos de alertas da Defesa Civil. Uma previsão de fenômeno severo não comprova risco em um imóvel específico. O produto deve preservar fonte, abrangência, tipo e validade, sem inventar precisão por rua. [R2]

Hipótese central: algumas organizações precisam distribuir e acompanhar comunicações manualmente, sem um histórico estruturado. Essa dor precisa ser confirmada em entrevistas.

### Persona de trabalho Lúcia

Lúcia é uma personagem fictícia usada para projetar a jornada. Ela deseja acompanhar informações sobre o local onde mora, entender a vigência de uma comunicação e consultar sua origem. Não representa uma participante entrevistada nem um depoimento real.

| Ator | Trabalho que queremos facilitar | Evidência necessária |
| --- | --- | --- |
| Morador | Identificar evento, localidade, validade e próxima ação. | Tarefa observada e perguntas de compreensão. |
| Operador | Identificar destinatários e acompanhar confirmações. | Entrevista sobre a rotina atual e teste comparativo. |
| Comprador | Decidir se organização e rastreabilidade justificam o gasto. | Reação ao escopo/preço e compromisso verificável de piloto. |

Nenhuma entrevista, tamanho de mercado, taxa de perda ou melhoria percentual foi presumida. A evidência produzida nesta versão é de funcionamento do software, não de demanda comercial.

03  /  POSICIONAMENTO

## Posicionamento e comprador

| Alternativa | Papel na jornada | Nossa decisão |
| --- | --- | --- |
| Canais oficiais de alerta | Comunicam informações de emergência. São referência, não concorrentes a eliminar. [R1] | Recomendar seu uso. Não cobrar pela informação pública em si. |
| Portais meteorológicos | Permitem consultar avisos e sua origem. Um aviso tem semântica e abrangência próprias. [R2] | Preservar procedência. Não transformar aviso municipal em previsão individual. |
| Grupos e planilhas | São alternativas possíveis de comunicação. Não foram auditadas no contexto do comprador. | Testar se o registro estruturado e as confirmações reduzem trabalho manual. |

### Oferta de operação da comunicação

A oferta proposta é a operação de comunicação: cadastro voluntário, preferências, regras de pertinência, histórico e acompanhamento. A organização paga; o morador utiliza gratuitamente. Trata-se de uma tese B2B2C, ainda sem clientes contratados.

### Diferencial funcional e vantagem futura

Nesta versão, é possível demonstrar que um local não elegível deixa de receber a notificação e que uma leitura confirmada altera o painel. Esse conjunto funcional não prova exclusividade frente a todos os produtos existentes.

A vantagem competitiva desejada depende de aprendizagem com compradores, processos de implantação e integrações. OCR, dados públicos e um painel, isoladamente, não são barreiras de entrada.

Posicionamento: comunicação climática contextualizada e acompanhável. Nunca: previsão de enchente por imóvel, serviço oficial ou garantia de proteção.

04  /  NOVE BLOCOS / VERSÃO 3.0

## Lean Canvas consolidado

Desenho de negócio consolidado com hipóteses comerciais abertas e evidências técnicas identificadas. A evolução documentada é das versões v1 a v3; não há validação histórica de CP1 presumida.

### 1 / PROBLEMA

Comunicação possivelmente dispersa; dificuldade de contextualização; acompanhamento manual de respostas. Alternativas: serviços oficiais, portais e grupos. Dor ainda não validada com comprador.

### 2 / SEGMENTOS

Beneficiário: morador. Operador: responsável pela comunicação. Comprador inicial a testar: administradora de conjuntos residenciais. Primeiro adotante desejado: organização com rotina manual e disposição para piloto.

### 3 / PROPOSTA DE VALOR

Do aviso à confirmação: informação contextualizada para o morador e comunicação acompanhável para quem cuida da comunidade. Complementar, nunca substituir, os canais oficiais.

### 4 / SOLUÇÃO

Cadastro revisado; extração documental opcional; regras de área, validade e preferências; notificação interna; confirmação e painel. Fluxo implementado com cenários sintéticos. Integrações oficiais ainda não ativas.

### 5 / CANAIS

Prospecção direta de administradoras; diagnóstico da rotina; demonstração; piloto. Ativação do morador por convite da organização. Parcerias e conversões ainda não existem.

### 6 / RECEITA

Assinatura hipotética de R$ 990/mês por organização: até 500 cadastros e 2.000 mensagens externas. Morador gratuito. Implantação opcional R$ 1.500, fora do recorrente. Preço não validado.

### 7 / CUSTOS

Mensageria, infraestrutura, suporte e operação. Base hipotética: R$ 500 variáveis/cliente + 6% sobre receita; R$ 18.000 fixos/mês. Não são cotações nem enquadramento tributário.

### 8 / MÉTRICAS

Locais confirmados, notificações e confirmações: implementados. Compreensão, conversão de pilotos, retenção e receita: medir em campo. Entrega externa não é confundida com disponibilização interna.

### 9 / VANTAGEM

Ainda sem vantagem defensável comprovada. Hipótese: processos de implantação, aprendizagem operacional e integrações específicas. Diferencial funcional não equivale a exclusividade de mercado.

05  /  MODELO DE NEGÓCIO

## Uma oferta que pode ser testada

Morador: acesso gratuito. Organização: assinatura pelo fluxo e pela gestão da comunicação.

| Elemento | Hipótese comercial / condição |
| --- | --- |
| Plano institucional | R$ 990 por organização/mês, até 500 cadastros optantes e 2.000 mensagens externas. Dois operadores previstos na oferta comercial; autenticação por papéis ainda não implementada. |
| Implantação opcional | R$ 1.500 por contrato, para treinamento e configuração. Não incluída na receita recorrente do modelo. |
| Excedentes e continuidade | Não prometer mensagens ilimitadas. Definir preço de excedente e regras de aviso de consumo antes do piloto. Não bloquear canais oficiais nem vender garantia de emergência. |
| Escopo realmente entregue | Demonstração com dez locais por sessão, sem contas comerciais e sem envio externo pelo site. A oferta de 500 cadastros não é capacidade de produção certificada. |
| Decisão de preço | Apresentar escopo e custo ao comprador; registrar objeções, disposição de pagamento e condições de um piloto. Nenhum contrato fechado nesta versão. |

### Aquisição com um comprador específico

Começar pela administradora que já executa comunicação manual. O contato inicial investiga o último episódio, o responsável pela operação, o tempo empregado e o critério de sucesso. Só então apresentar a demonstração e o piloto.

Não expandir simultaneamente para governos, seguradoras e escolas antes de descobrir um primeiro contexto com necessidade e decisor. Essa escolha é de foco estratégico, não resultado de pesquisa de mercado.

06  /  ECONOMIA UNITÁRIA

## Economia unitária e cenários

A planilha do pacote reúne seis abas e 143 fórmulas verificadas na preparação. As entradas são hipóteses editáveis, não tarifas de provedores. Valores mensais em reais; implantação fora do recorrente.

| Indicador | Eficiente | Base | Pressionado |
| --- | --- | --- | --- |
| Preço / cliente | 990,00 | 990,00 | 990,00 |
| Custo / mensagem | 0,08 | 0,15 | 0,30 |
| Mensagens / cliente | 2.000 | 2.000 | 2.000 |
| Variáveis / cliente | 360,00 | 500,00 | 800,00 |
| Carga hipotética de 6% | 59,40 | 59,40 | 59,40 |
| Contribuição / cliente | 570,60 | 430,60 | 130,60 |
| Margem de contribuição | 57,6% | 43,5% | 13,2% |
| Equilíbrio comercial | 32 clientes | 42 clientes | 138 clientes |
| Resultado com 50 clientes | 10.530,00 | 3.530,00 | -11.470,00 |

### Memória de cálculo do cenário base

Variáveis = (2.000 × R$ 0,15) + R$ 80 de infraestrutura atribuída + R$ 120 de suporte = R$ 500. Carga assumida = R$ 990 × 6% = R$ 59,40. Contribuição = 990 - 500 - 59,40 = R$ 430,60.

Fixos assumidos = R$ 12.000 de engenharia/operação compartilhadas + R$ 3.000 de administração + R$ 3.000 de aquisição = R$ 18.000. Equilíbrio = teto(18.000 / 430,60) = 42 clientes.

Cenário não é tração: 50 clientes gerariam R$ 49.500 de receita e R$ 3.530 de resultado operacional hipotético. Hoje não há clientes contratados.

Não se trata de lucro líquido ou caixa. Investimentos iniciais, financiamento, depreciação e imprevistos não foram integralmente modelados. A carga de 6% não define regime tributário. O custo real de cada canal e a disposição de pagamento continuam abertos.

07  /  EVOLUÇÃO E INDICADORES

## Evolução documentada das versões

| Decisão | Versões anteriores | Versão 3 e motivo |
| --- | --- | --- |
| Economia | R$ 3.500 de fixos acadêmicos; carga sobre receita não incluída. | R$ 18.000 de fixos comerciais e carga hipotética de 6%. Evita apresentar trabalho não remunerado como viabilidade. |
| Produto | v1: telas especificadas. v2: aplicativo local. | MVP público com API Worker e D1. Fluxo e regras preservados; publicação sem depender do banco Render. |
| Mensageria | Integração prevista. | Site mantém central interna; adaptador Twilio fica na versão Python. Nenhuma entrega externa é declarada. |
| Validação | Hipóteses abertas. | Suítes Python e Worker documentadas. Hipóteses de compreensão, dor e pagamento permanecem abertas. |

### Métricas com denominadores claros

| Indicador | Como calcular | Interpretação |
| --- | --- | --- |
| Confirmação interna | Leituras confirmadas / notificações internas. | Confirmação voluntária, não compreensão. |
| Entrega externa | Delivered/read do provedor / tentativas externas. | Não medida. Queued não significa entregue. |
| Compreensão | Pessoas que identificam evento, área, validade e ação / participantes. | Coleta humana pendente; sem percentual presumido. |
| Conversão comercial | Contratos pagos / pilotos concluídos. | Sem dados de pilotos ou contratos. |
| Contribuição | Receita menos variáveis e carga assumida. | Cenário financeiro; não lucro líquido. |

O painel não apresenta números de moradores reais, receita ou vidas protegidas. Cada contador vem de eventos da sessão sintética. O arquivo de evidências exportado permite conferir o denominador.

08  /  MVP EXECUTADO

## Um fluxo de ponta a ponta

Cadastrar → revisar → relacionar aviso → notificar → confirmar leitura → atualizar o painel.

Interface da jornada controlada registrada localmente. No MVP público, o estado é consultado da API e persistido em D1.

No site público, o cadastro é manual ou por PDF sintético com texto, de até duas páginas e 2 MB. A extração preenche sugestões; o usuário revisa e confirma os campos. O arquivo não é armazenado. OCR de PNG/JPG com Tesseract pertence à versão Python do repositório.

O fluxo público inclui cadastro, locais, central de notificações, detalhe do aviso, painel, laboratório e transparência. As ações alteram registros reais da sessão de demonstração; a comunicação permanece interna.

A proposta futura inclui dados do INMET, Cemaden e Defesa Civil e canais WhatsApp/SMS. Esses conectores oficiais e a entrega externa não estão ativos nesta versão.

09  /  ENGENHARIA E LIMITES

## Arquitetura do MVP público

| Camada | Implementação | Responsabilidade |
| --- | --- | --- |
| Experiência | HTML, CSS e JavaScript. | Navegação responsiva, formulários, estados de erro, leitura e painel. |
| API | JavaScript em Cloudflare Worker. | Sessões, cadastros, cenários, extração de PDF, leitura e exportação. |
| Domínio | Funções de elegibilidade e versões. | Área + validade + preferências + consentimento. Duplicidade impedida. |
| Persistência | Cloudflare D1, com SQL parametrizado. | Sessões, locais, avisos, notificações e eventos, independentes dos arquivos estáticos. |
| Versão Python | FastAPI; SQLite/PostgreSQL; Tesseract. | Execução alternativa, OCR de imagens e adaptador externo em ensaio seco. |

### Proteções implementadas

A API pública usa cookie opaco com HttpOnly, SameSite=Strict e Secure em HTTPS; token anti-CSRF; validação de origem; SQL parametrizado; limites de corpo e arquivo; limitação de escrita por instância; e isolamento por sessão. O arquivo original do comprovante não é salvo.

A sessão expira em 24 horas. Ao iniciar ou recuperar uma sessão, o servidor remove as vencidas e seus registros vinculados. O reset afeta apenas a sessão atual. O site não coleta telefone nem envia WhatsApp/SMS.

### Limites da demonstração

Não há autenticação comercial por papéis, certificação de acessibilidade, geocodificação, integração meteorológica ao vivo ou operação de emergência. Morador e operador são visões da mesma sessão de demonstração.

A versão Python mantém FastAPI, SQLite/PostgreSQL e adaptador Twilio em ensaio seco. O Render não hospeda este MVP: a criação do banco gratuito exigiu cartão. O site usa Worker/D1. O workflow remoto não concluiu os jobs; não se declara CI aprovado.

10  /  TESTES EXECUTADOS

## Verificação técnica e rastreabilidade

Site público: 36 de 36 verificações HTTP aprovadas. Python: 61 casos únicos aprovados em SQLite e repetidos em PostgreSQL local. Worker: 12 testes locais aprovados. São evidências de software, sem validação humana ou CI remoto aprovado.

| Conjunto Python | Casos | O que cobre |
| --- | --- | --- |
| Regras de domínio | 12 | Área correta/incorreta, preferência, consentimento, janela temporal e cancelamento. |
| API e persistência | 36 | Jornada, duplicidade, atualizações, sessões, CSRF, exportações, tamanho de requisição e reabertura do banco. |
| Documentos | 7 | Três PDFs sintéticos, OCR de imagem, formatos/tamanho inválidos e endpoint de extração. |
| Adaptador externo | 6 | Contrato com HTTP simulado, validação e tratamento de falhas. Não houve envio ao provedor real. |

### Verificação pública e suíte do site

A rodada HTTP pública de 19/11/2026, 17h58–18h01 de Brasília, aprovou 36 de 36 verificações: acesso, extração dos três PDFs, cadastro A/B, pertinência, leitura, persistência, isolamento, CSRF/origem e exportação. O Worker também tem 12 testes locais aprovados com SQLite por um adaptador de D1.

O JSON público registra valores esperados e observados, sem cookies ou tokens. As capturas anteriores de desktop (1440 × 960) e celular (390 × 844) são da interface local. O OCR de imagem pertence à versão Python.

### Correções e alcance da verificação

A versão Python inclui correção da inicialização WAL e teste de reabertura do banco. O site tem testes próprios de domínio, API e persistência. Aprovação técnica não comprova compreensão, demanda comercial ou disponibilidade em produção.

Rastreabilidade: evidencias/site_publico_verificado.json e scripts/verificar_site_publico.py no GitHub registram a rodada pública. Os resultados locais do Worker estão em sites/tests/. O pacote reúne relatório e capturas em 04_evidencias.

11  /  RESULTADOS OBSERVADOS

## O valor que conseguimos demonstrar

| Ação observada | Resultado real no cenário | Benefício funcional |
| --- | --- | --- |
| Cadastrar TESTE-A e TESTE-B | 2 locais persistidos. | Endereços e preferências associados à sessão. |
| Processar chuva de TESTE-A | 1 notificação criada; TESTE-B excluído. | Comunicação pertinente ao critério territorial de teste. |
| Confirmar leitura | 1 confirmação registrada; painel atualizado. | Acompanhamento verificável do evento de leitura. |
| Repetir o mesmo aviso | Nenhuma notificação adicional. | Prevenção de repetição da mesma versão. |
| Aviso de TESTE-C | Nenhuma notificação para A/B. | Caso negativo processado sem simular destinatários. |

Painel da jornada controlada local. 100% corresponde a 1 confirmação em 1 notificação, sem participantes humanos.

O teste HTTP público confirmou estes resultados: a leitura passou de 0 para 1, com 2 locais e 1 notificação, e o estado persistiu em novo cliente com o mesmo cookie. Foram 36 de 36 verificações aprovadas. Não foram medidos compreensão, redução de prejuízos, economia de tempo ou entrega em telefone.

12  /  APRENDIZAGEM E EVIDÊNCIAS ABERTAS

## Hipóteses e aprendizagem documentada

O Canvas registra hipóteses comerciais e uma hipótese técnica testada. A evolução observada vai do plano v1 ao aplicativo v2 e à publicação v3. O histórico de CP1 e entrevistas não está documentado; não se presume validação dessas etapas. [F1]

| Hipótese | Experimento proposto | Situação |
| --- | --- | --- |
| H1: a mensagem é compreendida. | Cinco voluntários executam cadastro, localização de aviso e confirmação. Perguntar evento, área, validade e ação. | Não executado com pessoas. |
| H2: existe trabalho manual relevante. | Entrevistar um responsável por comunicação sobre seu último episódio, esforço e falhas. | Não entrevistado. |
| H3: há disposição de pagamento. | Mostrar escopo, limites e preço. Registrar objeções e compromisso concreto de piloto. | Preço não validado. |
| H4: a regra territorial funciona. | Conjunto automatizado e jornada observada com locais elegíveis e não elegíveis. | Comportamento verificado no conjunto de teste. |

### Próxima etapa de pesquisa

O kit propõe cinco voluntários e uma entrevista com comprador para a próxima etapa. A amostra é uma decisão do grupo, não exigência numérica da rubrica. Os CSVs permanecem vazios. Registrar conclusão, tempo, ajuda, erros e compreensão com identificadores P01 a P05 e dados fictícios.

Critério futuro de decisão: ao menos quatro de cinco pessoas concluírem a jornada sem ajuda e identificarem evento, área, validade e ação. É uma meta exploratória, não uma taxa observada. Compreensão e disposição de pagamento continuam abertas.

Leitura confirmada não significa mensagem compreendida. Teste técnico não substitui entrevista. Elogio não equivale a compra.

13  /  ODS 11 E 13

## Impacto pretendido e responsabilidade

| Conexão | Contribuição proposta | O que medir posteriormente |
| --- | --- | --- |
| ODS 11 / meta 11.5 | Apoiar preparação e acesso à informação em desastres urbanos. A meta oficial trata de pessoas afetadas e perdas; o MVP não mede essas reduções. [R4] | Cobertura do piloto, acesso à comunicação e barreiras de uso. |
| ODS 13 / meta 13.1 | Contribuir para capacidade de adaptação por comunicação contextualizada. Não afirmar resiliência comprovada. [R5] | Entendimento, decisões e acompanhamento de uso em contexto real. |
| ODS 13 / meta 13.3 | Apoiar conscientização e capacidade institucional de interpretar comunicações. [R5] | Compreensão correta de evento, abrangência, validade e ação. |

### Inclusão por projeto

O cadastro manual permanece disponível: um comprovante não é condição para consultar a demonstração. Os avisos combinam rótulos e ícones, sem depender apenas de cor. A interface foi verificada em tela pequena, mas acessibilidade completa ainda exige auditoria e testes assistivos.

### Salvaguardas de comunicação

Ausência de mensagem não significa região segura. Falha de coleta aparece como indisponibilidade, e não como ausência de risco. Toda tela identifica o caráter sintético; avisos antigos mantêm sua validade no histórico.

Não orientamos evacuação, tratamento médico ou decisão de emergência com base nos cenários. O produto remete aos canais oficiais para situações reais. Não existe parceria ou endosso dos órgãos citados.

14  /  RISCOS E PRÓXIMAS DECISÕES

## Da demonstração ao piloto

| Risco | Tratamento nesta versão | Porta de saída para piloto |
| --- | --- | --- |
| Falsa precisão territorial | Áreas fictícias explicitadas; sem geocodificação real. | Fonte documentada, resolução territorial correta e regras auditadas. |
| Falsa certeza de entrega | Central interna separada do canal externo. | Teste optante; evidência do provedor e recebimento no telefone. |
| Custo de mensagem elevado | Sensibilidade em três custos e franquia proposta. | Cotação, política de excedentes e validação comercial. |
| Exposição de dados | Apenas dados sintéticos, sessões isoladas e descarte do arquivo. | Revisão de privacidade e segurança; contas e permissões reais. |
| Persistência e continuidade | Site usa D1; a sessão expira por política em 24 horas. Código preparado para outra hospedagem. | Definir retenção, backups, disponibilidade e capacidade antes de um piloto comercial. |
| Demanda não comprovada | H1-H3 abertas, com protocolo de coleta. | Sinal verificável de necessidade e compromisso de piloto. |

### Marcos de continuidade

M1 | Finalização acadêmica: conferir o pitch dos cinco integrantes, seu link na Ficha Técnica e enviar o PDF único. M2 | Pesquisa: observar moradores, entrevistar comprador e revisar preço. M3 | Piloto: integrar fontes e canais após tratar consentimento, segurança e continuidade.

Pedido ao parceiro: acesso a uma rotina real de comunicação para um piloto avaliado. Critério de continuidade: utilidade observada, entendimento e capacidade de operação a custo sustentável. O projeto não solicita adoção como sistema oficial de emergência.

15  /  MATRIZ DE ATENDIMENTO

## Relação entre evidências e rubrica

A matriz relaciona os cinco critérios da página 33 do briefing aos entregáveis verificáveis. Os pesos somam 14 pontos; representam a rubrica, não notas atribuídas ao projeto. [F1]

| Critério / peso | Material produzido | Situação e alcance da evidência |
| --- | --- | --- |
| Lean Canvas / 2,0 | Nove blocos na p. 5; evolução na p. 8; hipóteses e plano de pesquisa na p. 13. | Desenho consolidado e regra territorial testada. CP1, compreensão, dor e preço sem validação humana comprovada. |
| Negócio / 2,5 | Proposta, comprador, preço, canais, métricas e cenários nas p. 6 a 8; planilha com fórmulas. | Contribuição de R$ 430,60 e equilíbrio de 42 clientes no cenário base. Premissas hipotéticas identificadas. |
| Narrativa / 2,5 | Apresentação, roteiro por integrante e teleprompter com duração planejada de 4min55s. | Vídeo da equipe: consultar link na Ficha Técnica. Conferir até cinco minutos e participação dos cinco integrantes. |
| Fluxo ponta a ponta / 3,5 | MVP e repositório públicos na p. 2; cadastro, regras, notificação, leitura e painel nas p. 9 a 12. | Aplicação publicada com Worker/D1: 36 de 36 verificações HTTP públicas aprovadas. Demonstração com dados sintéticos identificados. |
| Valor evidenciado / 3,5 | Ensaio controlado da p. 12: pertinência territorial, confirmação persistida e bloqueio de duplicatas. | Teste documentado evidencia benefício funcional. Não mede compreensão, redução de danos ou demanda comercial. |

MVP e repositório publicados. Vídeo da equipe: consultar link na Ficha Técnica. Conferir duração, participação e acesso antes de enviar o PDF único. Pesquisa com moradores e comprador é a próxima etapa do produto.

### Finalização do envio

Conferir o vídeo com todos os integrantes, até cinco minutos, e os três links da Ficha Técnica. Um integrante envia o PDF único no portal de BI. Manter aplicação, repositório e vídeo públicos durante a correção, até uma semana após o prazo. [F1]

Prazo do enunciado: 19/11/2026, às 23h55. Horário adotado pelo grupo: Brasília. A geração deste pacote não realiza o envio no portal da faculdade. [F1]

16  /  FONTES E NATUREZA DAS AFIRMAÇÕES

## Referências e rastreabilidade

Fatos externos se apoiam nas fontes abaixo. Produto, persona, preço, custos e critérios de piloto são propostas do projeto. Resultados técnicos se apoiam nos arquivos de evidência. Os órgãos citados não endossam a solução.

F1 | FIAP. Desafio FIAP: CitizenTech, GS 2026.2. Arquivo fornecido pelo grupo; p. 18, 20, 24 e 32-34.

R1 | Ministério da Integração e do Desenvolvimento Regional. Perguntas frequentes: alertas. [  Abrir fonte oficial](https://www.gov.br/mdr/pt-br/acesso-a-informacao/perguntas-frequentes/perguntas-frequentes-defesa-civil/alertas)

R2 | INMET. Aviso meteorológico e alerta: entenda a diferença. [  Abrir fonte oficial](https://portal.inmet.gov.br/noticias/aviso-meteorol%C3%B3gico-e-alerta-entenda-a-diferenca)

R3 | Twilio. Test WhatsApp messaging with the Sandbox. Restrições e condições de teste. [  Abrir fonte oficial](https://www.twilio.com/docs/whatsapp/sandbox)

R4 | Nações Unidas no Brasil. Objetivo de Desenvolvimento Sustentável 11. [  Abrir fonte oficial](https://brasil.un.org/pt-br/sdgs/11)

R5 | Nações Unidas no Brasil. Objetivo de Desenvolvimento Sustentável 13. [  Abrir fonte oficial](https://brasil.un.org/pt-br/sdgs/13)

R6 | Render. Persistent Disks: persistência e limitações de armazenamento. [  Abrir fonte oficial](https://render.com/docs/disks)

R7 | FastAPI. Deployment: Docker. Referência para empacotamento. [  Abrir fonte oficial](https://fastapi.tiangolo.com/deployment/docker/)

Fontes externas consultadas em 17/11/2026. Documentação de provedores pode mudar; confirmar condições e custos antes de contratar.

### Mapa do pacote

Materiais: dossiê, apresentação, evidências, modelo financeiro, protocolo e guias de gravação/publicação. Código atualizado no GitHub: aplicação Python na raiz; versão pública Worker/D1 na pasta sites. Roteiro e teleprompter também estão no portal de gravação.

A demonstração é acadêmica e usa dados sintéticos. Não é serviço de emergência.

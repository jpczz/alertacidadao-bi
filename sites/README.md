# AlertaCidadão — versão pública

MVP acadêmico de Business Intelligence & Startup Development, FIAP CitizenTech 2026.2. O site executa cadastro, pertinência territorial, notificação interna, confirmação de leitura e indicadores persistidos. Todos os endereços, documentos e cenários climáticos são sintéticos.

- Aplicação: https://alertacidadao-bi-jpczz.est-dio-like-0113.chatgpt.site
- Materiais de avaliação: https://alertacidadao-bi-jpczz.est-dio-like-0113.chatgpt.site/entrega
- Gerador do PDF após o vídeo: https://alertacidadao-bi-jpczz.est-dio-like-0113.chatgpt.site/finalizar
- Teleprompter da equipe: https://alertacidadao-bi-jpczz.est-dio-like-0113.chatgpt.site/gravacao
- Código das duas implementações: https://github.com/jpczz/alertacidadao-bi

## Arquitetura publicada

worker/index.js serve os arquivos e aplica os cabeçalhos de resposta; worker/api.js contém a API e as regras. O banco persistente Cloudflare D1 usa o binding DB, declarado em .openai/hosting.json, com esquema em drizzle/0000_init.sql. A interface é HTML, CSS e JavaScript. unpdf extrai a camada textual dos PDFs sintéticos; OCR de imagens existe somente na implementação Python da raiz do repositório principal.

Os dados de cada visitante ficam isolados por cookie opaco. A sessão dura 24 horas; as sessões vencidas são removidas quando /api/session é consultado. Persistência não implica retenção indefinida dos dados de demonstração. Não há SMS, WhatsApp, feed meteorológico ao vivo, conta comercial ou modelo de previsão de risco.

## Reproduzir build e testes

Use Node.js 22 ou superior, com node:sqlite disponível, e npm.

```sh
npm ci
npm test
npm run build
npm run validate
```

O build empacota os arquivos de public/ e gera dist/server/index.js. Os PDFs da entrega são distribuídos pela central pública e pelo pacote de materiais, sem cópia neste repositório. Para reproduzir também as páginas documentais e o gerador de PDF em outra hospedagem, acrescente os arquivos indicados em public/docs/README.md antes do build. A aplicação central e os testes de domínio não dependem desses PDFs de apresentação. Os arquivos gerados não são a fonte de edição. Os 12 testes de tests/worker-api.test.mjs chamam os handlers reais e usam SQLite por um adaptador da interface D1. São testes locais; não equivalem à verificação HTTP da implantação pública.

No repositório principal, scripts/verificar_site_publico.py executa uma jornada HTTP pública com duas sessões sintéticas próprias. O relatório em evidencias/site_publico_verificado.json registra expectativas, resultados e métricas, sem cookies ou tokens. O script não acessa dados de outras sessões nem envia mensagens externas.

## Conteúdo para gravação e avaliação

public/gravacao.html e public/static/teleprompter.js oferecem seis trechos, cinco integrantes e 4min55s planejados. O pitch final depende da gravação da equipe; esta demonstração não substitui a participação dos alunos. public/entrega.html reúne dossiê, apresentação e ensaio documentado.

## Finalização do PDF

A página /finalizar recebe a URL pública, a duração e a declaração de participação dos cinco integrantes. A edição é local no navegador, usando pdf-lib. O template sem o marcador e o mapa de coordenadas são vinculados por SHA-256. A ferramenta insere o hyperlink; não verifica a publicação do vídeo ou a veracidade das declarações.

## Limites da evidência

Os testes verificam funcionamento e consistência dos registros. Não comprovam compreensão dos moradores, disposição de pagamento, validação comercial ou redução de danos. Os números de preço, custos e equilíbrio são hipóteses declaradas no dossiê. O projeto complementa a discussão sobre comunicação climática e não é serviço de emergência.

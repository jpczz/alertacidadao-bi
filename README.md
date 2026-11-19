| RM | Integrante |
|---|---|
| **RM553282** | Kaio Vinicius Meireles Alves |
| **RM553956** | Lucas Alves de Souza |
| **RM554323** | Guilherme Fernandes de Freitas |
| **RM553172** | João Pedro Chizzolini de Freitas |
| **RM553945** | Henrique Rafael |

# AlertaCidadão

**FIAP · CitizenTech 2026.2 · Business Intelligence & Startup Development**

Comunicação por localidade, aviso interno, confirmação de leitura e indicadores em um MVP acadêmico funcional.

## Acesso para avaliação

| Material | Acesso |
|---|---|
| **Vídeo-pitch final** | **[Assistir no YouTube](https://youtu.be/RtqAPawx7h4)** — 4min09s, aproximadamente; arquivo enviado com 248,87 segundos |
| Cópia do vídeo | [Baixar MP4 no GitHub](video/AlertaCidadao_Pitch_Final.mp4?raw=1) — 1080p, comprimido e sem cortes |
| **PDF único de entrega** | **[Dossie_AlertaCidadao_Para_Submissao.pdf](docs/Dossie_AlertaCidadao_Para_Submissao.pdf)** — equipe, Lean Canvas, modelo de negócio, evidências e links de vídeo, MVP e repositório |
| **MVP funcionando** | **[Abrir o AlertaCidadão](https://alertacidadao-bi-jpczz.est-dio-like-0113.chatgpt.site)** |
| Materiais completos | [Pasta entrega/](entrega/) — documentos editáveis, apresentação, modelo financeiro, roteiro e evidências |
| Central online | [Abrir a central de materiais](https://alertacidadao-bi-jpczz.est-dio-like-0113.chatgpt.site/entrega) |
| Resultados técnicos | [Relatório do ensaio controlado](entrega/04_evidencias/Relatorio_Ensaio_Controlado.pdf) · [36 verificações do site público](evidencias/site_publico_verificado.json) |

O último slide do vídeo preserva texto da preparação; os links e os documentos desta entrega refletem o estado final publicado. O vídeo acima é a gravação final fornecida pela equipe; a base visual sem áudio continua arquivada somente como material de apoio.

Para a submissão acadêmica, use o PDF único indicado acima, conforme o enunciado. Este repositório reúne o código e todos os materiais de consulta. O envio ao portal da disciplina é uma etapa externa ao projeto.

## Ficha Técnica do MVP

| Campo | Conteúdo |
|---|---|
| Produto | AlertaCidadão - informação clara para agir a tempo |
| Cidadão / território | Moradores; execução com Cidade Exemplo/SP, TESTE-A/B/C e CEPs fictícios |
| Problema | Organizar e acompanhar comunicações pertinentes à localidade |
| Proposta de valor | Contexto para o morador; rastreabilidade para a organização |
| Arquitetura | Site público: JavaScript Worker + Cloudflare D1 + HTML/CSS/JS. Implementação Python adicional: FastAPI + SQLite/PostgreSQL. Ambas aplicam regras de elegibilidade e trilha de eventos |
| Dados | Cenários sintéticos; nenhum feed oficial conectado |
| Modelos de IA | Site: sem modelo de IA; extração textual de PDF com unpdf. Python: Tesseract para OCR de imagem. Sem previsão climática ou GenAI |
| URL do MVP | https://alertacidadao-bi-jpczz.est-dio-like-0113.chatgpt.site |
| Repositório | https://github.com/jpczz/alertacidadao-bi |
| Vídeo-pitch | https://youtu.be/RtqAPawx7h4 |
| PDF de entrega | [Dossiê final](docs/Dossie_AlertaCidadao_Para_Submissao.pdf) |
| Indicadores | Locais, notificações internas, confirmações e trilha de eventos |
| ODS | 11 e 13; contribuição pretendida, impacto ainda não medido |

**Demonstração acadêmica, não serviço de emergência. Não envie documentos pessoais reais.**

## Duas implementações identificadas

| Implementação | Local do código | Persistência | Extração |
|---|---|---|---|
| Publicada no endereço acima | sites/ | Cloudflare D1, sessões isoladas de 24h | PDF sintético com camada de texto, até 2 MB e 2 páginas |
| Python executável localmente e compatível com Docker | Raiz: app/, tests/ | SQLite local ou PostgreSQL via DATABASE_URL | PDF textual e OCR de PNG/JPG com Tesseract |

A tentativa de banco gratuito no Render exigiu cartão e não foi usada na publicação. A demonstração está hospedada em Sites com D1. Os relatórios distinguem testes da implementação Python, testes locais do Worker e verificação do endereço público.

## Início rápido da versão Python

Python 3.12+ recomendado. Windows: execute `INICIAR_WINDOWS.bat`. Linux/macOS: `sh iniciar.sh`.

Manual:

```sh
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 1
```
Abra `http://127.0.0.1:8000`. A interface precisa do servidor; não abra o HTML isoladamente. O banco local padrão fica em `data/alerta.db`.

O arquivo `.env.example` documenta variáveis; não é carregada automaticamente. Configure variáveis no terminal ou no painel da hospedagem. **Não publique credenciais.**

## Roteiro de demonstração

1. Cadastro: selecione `app/samples/comprovante_A.pdf`, clique em Ler documento, revise e confirme o caráter fictício. O texto do PDF é extraído; não o chamamos de OCR.
2. Cadastre o exemplo B. Agora existem dois locais sintéticos.
3. Laboratório: execute chuva para TESTE-A. Apenas A recebe a notificação.
4. Na central, abra as informações e confirme a leitura. No painel, a confirmação aparece.
5. Reexecute chuva: nenhuma duplicação. Execute TESTE-C: nenhum dos locais A/B recebe.
6. Explore calor, aviso expirado, futuro, cancelado, nova versão e falha de fonte. Alterar preferências afeta os próximos processamentos.
7. Exporte JSON/CSV. O reset apaga somente os dados da sessão atual.

## Extração e OCR na versão Python

PDF: até 2 páginas com camada textual; imagens em PDF sem texto não são convertidas automaticamente. Imagem: PNG/JPG, até 2 MB e 8 megapixels, com Tesseract e idioma `eng` no PATH. O gabarito usa campos sintéticos em letras latinas; isso não valida extração de contas reais de concessionárias.

O Dockerfile inclui Tesseract. Em instalação local sem esse programa, use o PDF ou entrada manual. O arquivo enviado é processado e descartado; não é persistido.

## Testes

```sh
python -m pip install -r requirements-dev.txt
python -m pytest -q --junitxml=test-results.xml
```
Em 19/11/2026, os mesmos 61 casos passaram com SQLite e com PostgreSQL 16.2 real, usando Tesseract e as versões exatas de requirements.txt. Sem ele, o teste de OCR pode ser ignorado explicitamente. 12 casos de domínio, 36 de API, 7 de documentos e 6 de contrato de mensageria. Os testes de mensageria usam HTTP simulado; nenhum SMS ou WhatsApp foi enviado.

`tests/browser_smoke.py` é o roteiro de navegador da implementação Python. A evidência local anterior está no pacote e em `evidencias/controlled_value_journey.json` (12 verificações). A versão Worker tem 12 testes locais próprios em `sites/tests/worker-api.test.mjs`.

**36 de 36 verificações HTTP do site público passaram no ensaio documentado de 19/11/2026.** Elas cobrem cadastro persistente, seleção por área, leitura, painel, isolamento entre visitantes e extração dos PDFs sintéticos. A verificação pública reproduzível está em `scripts/verificar_site_publico.py`, com relatório `evidencias/site_publico_verificado.json`. Execute `python scripts/verificar_site_publico.py --help` antes de repetir; o teste cria somente dados sintéticos em sessões próprias.

Os resultados locais aprovados não significam CI remoto aprovado. Na auditoria de 19/11, a execução GitHub Actions 44609914142 terminou sem iniciar os steps dos dois jobs; não foi possível determinar a causa pelo log disponível.

## API e dados

Na implementação Python, esquema OpenAPI em `/api/openapi.json`. Nas duas implementações, saúde em `/api/health`. Não há Swagger externo/CDN. Endpoints principais: `/api/session`, `/api/state`, `/api/places`, `/api/documents/extract`, `/api/scenarios/run`, `/api/notifications/{id}/confirm`, `/api/export` e `/api/reset`. Operações mutáveis exigem cookie da sessão e cabeçalho `X-CSRF-Token` recebido ao iniciar a sessão.

Persistência: `sessions` (expiração), `places` (local/preferências), `notices` (código/versão/payload), `notifications` (canal/leitura) e `events` (trilha). Unicidade impede notificação duplicada para o mesmo local e versão. Toda consulta de usuário é limitada à sessão.

## Segurança e limites

Os testes técnicos não representam entrevistas com moradores, validação comercial, clientes pagantes ou comprovação de redução de danos. Preços e custos do modelo financeiro são hipóteses explícitas.

Sessões opacas, HttpOnly/SameSite, CSRF, consultas parametrizadas, limite de upload e de escrita, CSP e isolamento. Configurar `COOKIE_SECURE=1` somente sob HTTPS. Sessão expira em 24h; remoção física de vencidas ocorre ao chamar `/api/session`. Dez locais por sessão. O limitador é por processo: uma instância/worker nesta arquitetura.

As visões morador/operador compartilham a sessão de teste; **não constituem RBAC comercial**. Sem dados pessoais de produção, sem autenticação de empresas e sem geocodificação. A oferta comercial de 500 cadastros ainda não é capacidade certificada.

## Hospedagem da versão Python

O `Dockerfile` inclui Tesseract e inicia a API com um worker na porta `PORT`. `docker compose up --build` usa SQLite com volume local. Na hospedagem, configure `DATABASE_URL` com a conexão PostgreSQL e `COOKIE_SECURE=1`. Não inclua a conexão no repositório. A construção Docker não foi validada por deploy nesta entrega. Nenhum recurso Render foi necessário para o site publicado. Para contratar hospedagem adicional, consultar as condições atuais do provedor. A demonstração acadêmica usa apenas dados sintéticos.

## Mensageria opcional

O site nunca dispara mensagens externas. O adaptador de teste fica em `scripts/notificar_teste.py` e inicia em ensaio seco. Exige credenciais por variável de ambiente, número optante e confirmação explícita de custo. `queued` não significa entregue. Detalhes no guia de mensageria do pacote.

## Fontes de contexto

- Defesa Civil: https://www.gov.br/mdr/pt-br/acesso-a-informacao/perguntas-frequentes/perguntas-frequentes-defesa-civil/alertas
- INMET: https://portal.inmet.gov.br/noticias/aviso-meteorol%C3%B3gico-e-alerta-entenda-a-diferenca
- Render: https://render.com/docs/disks
Nenhuma parceria ou integração ativa com os órgãos citados. Consulta em 17/11/2026.

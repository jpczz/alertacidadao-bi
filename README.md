# AlertaCidadão

## Ficha Técnica do MVP

| Campo | Conteúdo |
|---|---|
| Produto | AlertaCidadão - informação clara para agir a tempo |
| Cidadão / território | Moradores; execução com Cidade Exemplo/SP, TESTE-A/B/C e CEPs fictícios |
| Problema | Organizar e acompanhar comunicações pertinentes à localidade |
| Proposta de valor | Contexto para o morador; rastreabilidade para a organização |
| Arquitetura | FastAPI + HTML/CSS/JS + PostgreSQL na hospedagem (SQLite local) + regras de elegibilidade + trilha de eventos |
| Dados | Cenários sintéticos; nenhum feed oficial conectado |
| IA | Tesseract para OCR de imagem; sem modelo climático preditivo ou GenAI |
| URL do MVP | Aguardando publicação pelo grupo |
| Repositório | https://github.com/jpczz/alertacidadao-bi |
| Indicadores | Locais, notificações internas, confirmações e trilha de eventos |
| ODS | 11 e 13; contribuição pretendida, impacto ainda não medido |

**Demonstração acadêmica, não serviço de emergência. Não envie documentos pessoais reais.**

## Equipe

| Integrante | RM |
|---|---|
| Kaio Vinicius Meireles Alves | 553282 |
| Lucas Alves de Souza | 553956 |
| Guilherme Fernandes de Freitas | 554323 |
| João Pedro Chizzolini de Freitas | 553172 |
| Henrique Rafael | 553945 |

## Início rápido
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

## OCR
PDF: até 2 páginas com camada textual; imagens em PDF sem texto não são convertidas automaticamente. Imagem: PNG/JPG, até 2 MB e 8 megapixels, com Tesseract e idioma `eng` no PATH. O gabarito usa campos sintéticos em letras latinas; isso não valida extração de contas reais de concessionárias.

O Dockerfile inclui Tesseract. Em instalação local sem esse programa, use o PDF ou entrada manual. O arquivo enviado é processado e descartado; não é persistido.

## Testes
```sh
python -m pip install -r requirements-dev.txt
python -m pytest -q --junitxml=test-results.xml
```
Em 19/11/2026, os mesmos 61 casos passaram com SQLite e com PostgreSQL 16.2 real, usando Tesseract e as versões exatas de requirements.txt. Sem ele, o teste de OCR pode ser ignorado explicitamente. 12 casos de domínio, 36 de API, 7 de documentos e 6 de contrato de mensageria. Os testes de mensageria usam HTTP simulado; nenhum SMS ou WhatsApp foi enviado.

`tests/browser_smoke.py` executa uma jornada em uma URL por navegação normal. Requer Playwright e Chromium instalados (`python -m playwright install chromium`). As capturas anteriores constam no pacote. A rodada atual também executou 12 verificações HTTP da jornada sintética; os registros estão em `evidencias/`.

## API e dados
Esquema OpenAPI em `/api/openapi.json`; saúde em `/api/health`. Não há Swagger externo/CDN. Endpoints principais: `/api/session`, `/api/state`, `/api/places`, `/api/documents/extract`, `/api/scenarios/run`, `/api/notifications/{id}/confirm`, `/api/export` e `/api/reset`. Operações mutáveis exigem cookie da sessão e cabeçalho `X-CSRF-Token` recebido ao iniciar a sessão.

Persistência: `sessions` (expiração), `places` (local/preferências), `notices` (código/versão/payload), `notifications` (canal/leitura) e `events` (trilha). Unicidade impede notificação duplicada para o mesmo local e versão. Toda consulta de usuário é limitada à sessão.

## Segurança e limites
Sessões opacas, HttpOnly/SameSite, CSRF, consultas parametrizadas, limite de upload e de escrita, CSP e isolamento. Configurar `COOKIE_SECURE=1` somente sob HTTPS. Sessão expira em 24h; remoção física de vencidas ocorre ao chamar `/api/session`. Dez locais por sessão. O limitador é por processo: uma instância/worker nesta arquitetura.

As visões morador/operador compartilham a sessão de teste; **não constituem RBAC comercial**. Sem dados pessoais de produção, sem autenticação de empresas e sem geocodificação. A oferta comercial de 500 cadastros ainda não é capacidade certificada.

## Implantar
O `Dockerfile` inclui Tesseract e inicia a API com um worker na porta `PORT`. `docker compose up --build` usa SQLite com volume local. Na hospedagem, configure `DATABASE_URL` com a conexão PostgreSQL e `COOKIE_SECURE=1`. Não inclua a conexão no repositório. A construção será verificada no primeiro deploy. O plano gratuito do Render Postgres tem prazo de 30 dias e o serviço web pode ficar inativo até novo acesso; consultar https://render.com/docs/free. A demonstração acadêmica usa apenas dados sintéticos.

## Mensageria opcional
O site nunca dispara mensagens externas. O adaptador de teste fica em `scripts/notificar_teste.py` e inicia em ensaio seco. Exige credenciais por variável de ambiente, número optante e confirmação explícita de custo. `queued` não significa entregue. Detalhes no guia de mensageria do pacote.

## Fontes de contexto
- Defesa Civil: https://www.gov.br/mdr/pt-br/acesso-a-informacao/perguntas-frequentes/perguntas-frequentes-defesa-civil/alertas
- INMET: https://portal.inmet.gov.br/noticias/aviso-meteorol%C3%B3gico-e-alerta-entenda-a-diferenca
- Render: https://render.com/docs/disks
Nenhuma parceria ou integração ativa com os órgãos citados. Consulta em 17/11/2026.

# Roteiro de gravação do AlertaCidadão

Versão 3 · 19/11/2026 · 4min55s planejados · cinco integrantes e seis trechos.

Teleprompter: https://alertacidadao-bi-jpczz.est-dio-like-0113.chatgpt.site/gravacao
MVP: https://alertacidadao-bi-jpczz.est-dio-like-0113.chatgpt.site
Repositório: https://github.com/jpczz/alertacidadao-bi

## Ordem de gravação

| Trecho | Participante | RM | Duração | Arquivo |
|---|---|---|---|---|
| 0:00–0:45 | Kaio Vinicius Meireles Alves | RM553282 | 45 s | 01_problema.mp4 |
| 0:45–1:30 | Lucas Alves de Souza | RM553956 | 45 s | 02_solucao.mp4 |
| 1:30–3:00 | Guilherme Fernandes de Freitas | RM554323 | 90 s | 03_demo.mp4 |
| 3:00–4:00 | João Pedro Chizzolini de Freitas | RM553172 | 60 s | 04_negocio.mp4 |
| 4:00–4:30 | Henrique Rafael | RM553945 | 30 s | 05_impacto.mp4 |
| 4:30–4:55 | Henrique Rafael | RM553945 | 25 s | 06_time.mp4 |

Gravem na horizontal, em ambiente silencioso, no ritmo 1× do teleprompter. As indicações de cena não são faladas. A contagem de três segundos fica fora do trecho aproveitado. As falas reais devem caber nos blocos, sem aceleração artificial.

## 0:00–0:45 · Kaio Vinicius Meireles Alves · RM553282

Problema e cidadão · 1 e 2 · arquivo 01_problema.mp4

### 0:00 do trecho

Um aviso de chuva chega. Ele vale para a região onde eu moro? Até quando? E como a organização sabe se o morador confirmou a leitura?

### 0:14 do trecho

Essa é a jornada que o AlertaCidadão quer melhorar. Já existem canais oficiais de alerta. Nossa proposta é complementar essa estrutura, conectando moradores e administradoras de conjuntos residenciais. Organizamos o caminho entre o local cadastrado, a informação pertinente e a confirmação de leitura. Nossa hipótese é que comunicar com contexto e acompanhar a resposta pode reduzir o trabalho manual da organização.

## 0:45–1:30 · Lucas Alves de Souza · RM553956

Solução e proposta de valor · 3 · arquivo 02_solucao.mp4

### 0:00 do trecho

Para o morador, o AlertaCidadão reúne o aviso, sua abrangência, validade e origem. Para a organização, registra as notificações criadas e as leituras confirmadas.

### 0:15 do trecho

O endereço pode ser digitado ou preenchido com ajuda de um documento de teste. O cidadão sempre revisa e confirma. O sistema considera a área, as preferências e a validade do aviso.

### 0:31 do trecho

O MVP demonstra chuva e calor com cenários sintéticos. Ele já executa esse fluxo completo na central interna. A proposta de negócio é organizar e acompanhar a comunicação, com acesso gratuito para o morador.

## 1:30–3:00 · Guilherme Fernandes de Freitas · RM554323

Demonstração do MVP · Aplicação · trecho de demonstração · arquivo 03_demo.mp4

### 0:00 do trecho

Vamos executar a jornada no AlertaCidadão. Todos os dados são sintéticos.

Na tela: Mostrar início e rótulo de dados sintéticos.

### 0:06 do trecho

O PDF de teste preenche os campos. O usuário revisa o endereço e confirma o cadastro.

Na tela: Cadastrar local com comprovante_A.pdf, revisar e confirmar.

### 0:18 do trecho

Salvamos dois locais: um na área TESTE-A e outro na TESTE-B. Agora o sistema tem dois endereços para avaliar.

Na tela: Salvar TESTE-A e cadastrar o segundo local em TESTE-B.

### 0:31 do trecho

Processamos chuva para A. Só o local correspondente recebe a notificação.

Na tela: No laboratório, processar chuva para TESTE-A.

### 0:38 do trecho

A notificação mostra abrangência, validade e origem. Assim, o morador sabe a qual local a informação se refere.

Na tela: Abrir a notificação e mostrar origem, área e validade.

### 0:49 do trecho

Ao confirmar a leitura, essa ação fica registrada no banco.

Na tela: Clicar para confirmar a leitura.

### 0:55 do trecho

O painel já mostra uma notificação e uma leitura confirmada. Os indicadores vêm dessa interação.

Na tela: Abrir o painel e mostrar 1 notificação e 1 confirmação.

### 1:04 do trecho

Repetimos o mesmo aviso. Nenhuma nova mensagem é criada: o sistema evita duplicidade.

Na tela: Repetir o mesmo cenário e mostrar ausência de duplicidade.

### 1:12 do trecho

Um aviso da área C também não gera notificações para A ou B.

Na tela: Processar aviso da área TESTE-C.

### 1:19 do trecho

Esse fluxo funciona na central interna. WhatsApp, SMS e dados oficiais ao vivo são evoluções previstas, ainda não ativadas.

Na tela: Encerrar na tela do produto, mantendo o rótulo de demonstração.

## 3:00–4:00 · João Pedro Chizzolini de Freitas · RM553172

Modelo de negócio e viabilidade · 5 e 6 · arquivo 04_negocio.mp4

### 0:00 do trecho

O morador usa gratuitamente. Nossa primeira hipótese de comprador é a administradora de conjuntos residenciais. Propomos uma assinatura de novecentos e noventa reais mensais por organização, com até quinhentos cadastros e duas mil mensagens externas na futura oferta comercial.

### 0:20 do trecho

No cenário-base, assumimos quinhentos reais de custo variável por cliente. Com uma carga hipotética de seis por cento, sobram quatrocentos e trinta reais e sessenta centavos de contribuição.

### 0:36 do trecho

Para cobrir dezoito mil reais de custos fixos mensais, seriam necessários quarenta e dois clientes. A planilha também mostra como mensagens mais caras pressionam essa conta.

### 0:49 do trecho

Esses valores são hipóteses, ainda sem vendas ou validação de preço. O canal inicial é prospecção direta, seguida de diagnóstico, demonstração e piloto.

## 4:00–4:30 · Henrique Rafael · RM553945

Evidências, métricas e impacto · 7 · arquivo 05_impacto.mp4

### 0:00 do trecho

Os testes automatizados verificam as regras de processamento, o isolamento das sessões e a prevenção de duplicidade. A demonstração mostra o cadastro, a notificação e a confirmação atualizando o painel.

### 0:16 do trecho

A contribuição pretendida aos ODS onze e treze é apoiar preparação urbana e conscientização climática. Compreensão dos moradores, disposição de pagamento e redução de danos ainda precisam ser avaliadas.

## 4:30–4:55 · Henrique Rafael · RM553945

Equipe e próximo passo · 8 · arquivo 06_time.mp4

### 0:00 do trecho

Nossa equipe transformou a ideia em um MVP demonstrável, com modelo de negócio, indicadores e hipóteses explícitas. O próximo passo é um piloto observado com uma organização e seus moradores.

### 0:15 do trecho

Vamos medir compreensão, utilidade e compromisso de contratação. Os materiais estão na ficha técnica. AlertaCidadão: informação clara para uma comunidade que acompanha.

## Montagem

A base visual tem 295 segundos, sem voz. Insira as gravações reais da equipe. `ADICIONAR_NARRACOES.py` reúne o áudio, normaliza volumes e preenche o restante de cada bloco com silêncio. Não corta falas longas e não monta janelas de rosto.

Após gravar, revisar e publicar o vídeo, inserir seu link público no PDF único da disciplina. O vídeo-base sem participação da equipe não substitui esse item. Medir o resultado real para garantir no máximo 5min.

A apresentação possui 11 lâminas. As lâminas 9–11 são apêndices de apoio e não integram o pitch de 4min55s. A demonstração gravada preserva cenários sintéticos e processamento real. Nenhum relato de entrevistas, integração ao vivo ou entrega externa é afirmado.

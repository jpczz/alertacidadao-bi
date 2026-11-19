# Evidências do AlertaCidadão

## Verificação do site público em 19/11/2026

O arquivo site_publico_verificado.json registra 36 verificações HTTP aprovadas no domínio público, sem autenticação ou token de acesso especial. Foram usados somente cenários fictícios e duas sessões próprias do teste, limpas ao final.

O cadastro persistiu A e B; chuva gerou uma comunicação apenas para A; a confirmação levou o painel de 0 para 1 leitura; repetição não duplicou; outro visitante não acessou esses registros. Os três PDFs A/B/C foram extraídos pelo servidor e comparados com seus gabaritos.

As métricas antes/depois são da jornada sintética. 100% significa 1 leitura para 1 notificação, sem inferência sobre moradores reais, compreensão, entrega externa ou redução de danos. Nenhuma mensagem WhatsApp/SMS foi enviada.

## Implementação Python

Os relatórios tests_sqlite.xml e tests_postgresql.xml registram os mesmos 61 casos aprovados nas duas bases em 19/11/2026. Não são 122 casos distintos. controlled_value_journey.json contém 12 verificações da jornada HTTP local. Os resultados são de execução local; o CI remoto não foi declarado aprovado.

## Implementação Worker

worker-controlled-journey.json e evidence-worker-api.txt registram 12 testes locais do Worker com SQLite real por adaptador da interface D1. A jornada central contém 12 expectativas. Esses resultados locais são separados dos 36 checks HTTP públicos.

## Material visual anterior

As capturas e a demonstração de 90s documentam a implementação Python executada na rodada de 17/11/2026. A base visual do pitch reutiliza essa jornada real, com cenários sintéticos. O resultado atual em hospedagem pública é documentado pelo relatório HTTP acima. OCR de imagem mostrado em captura antiga pertence à implementação Python; o site público usa PDF textual ou cadastro manual.

O conjunto não contém entrevistas ou validação comercial. O protocolo em 06_validacao está disponível para coleta futura.

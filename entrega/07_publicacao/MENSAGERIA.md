# WhatsApp/SMS: teste opcional e controlado

**Nenhum envio real foi executado. O aplicativo web usa a central interna.** O adaptador Twilio é uma ferramenta separada para o operador, não uma integração de produção. Seus testes de contrato utilizam HTTP simulado.

## Pré-condições
Conta habilitada, origem autorizada, telefone de teste optante e aprovação de possíveis custos. No WhatsApp, a adesão ao ambiente de teste e as regras de janela/template devem ser cumpridas. O Sandbox é para teste, não produção. A documentação atual distingue o Sandbox na console legada e a experiência de teste da nova console: conferir a conta usada.

Fonte oficial: https://www.twilio.com/docs/whatsapp/sandbox (consulta 17/11/2026).

Configure no terminal/servidor, nunca no repositório ou em conversa:
`TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_FROM`, `TWILIO_TEST_TO` e, se necessário, `TWILIO_CONTENT_SID` de um template de teste compatível sem variáveis obrigatórias. Origem/destino WhatsApp usam o prefixo `whatsapp:` e formato internacional.

## Ensaio seco
Na raiz da implementação Python do repositório https://github.com/jpczz/alertacidadao-bi :
```sh
python scripts/notificar_teste.py
```
Não envia nada. Para enviar uma única mensagem ao destino configurado, após consentimento e aceite de custo:
```sh
python scripts/notificar_teste.py --send --acknowledge-costs --output prova_provedor.json
```
A mensagem deve continuar claramente acadêmica, sem risco real. Não usar template que sugira aviso oficial. Para consultar o resultado, usar o identificador realmente retornado pelo provedor:
```sh
python scripts/notificar_teste.py --poll IDENTIFICADOR_REAL_DA_MENSAGEM --output status_provedor.json
```

`queued`/`sent` não comprovam recebimento. Registrar status delivered/read quando disponível e captura no telefone optante, ocultando o número. O adaptador não atualiza automaticamente o painel da demonstração. Não alterar o contador de entregas externas manualmente para simular integração.

Sem configuração e teste real, manter no pitch: "O canal demonstrado é a central interna; entrega externa ainda não validada."

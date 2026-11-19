# Protocolo de validação | AlertaCidadão

## Estado
Nenhuma pessoa foi testada ou entrevistada nesta entrega. Os arquivos de coleta têm apenas cabeçalhos; não contêm respostas fabricadas. A amostra proposta de cinco voluntários é exploratória, não representativa.

## Abertura e consentimento verbal
"Estamos avaliando um aplicativo acadêmico com dados fictícios, não um serviço de emergência. Avaliamos o sistema, não você. A participação é voluntária; você pode parar a qualquer momento. Não use seu endereço, telefone ou conta de serviço real. Podemos anotar suas dificuldades e o tempo das tarefas sem registrar seu nome?"

Usar P01 a P05. Não registrar voz/rosto sem autorização específica. Não selecionar apenas pessoas que conhecem o projeto. Identificar se é colega do grupo; isso afeta a interpretação.

## Tarefas padronizadas
T1. Abra a URL e cadastre o local do documento sintético A; revise e salve. Começar o cronômetro após ler a tarefa, parar quando o local aparecer salvo. Registrar ajuda e erros.
T2. O moderador executa o cenário de chuva no laboratório. Peça à pessoa que encontre a comunicação e diga, com suas palavras, o tipo de evento, a área abrangida, a validade e a próxima ação da demonstração.
T3. Peça que confirme a leitura e mostre onde consegue saber que a ação foi registrada.
T4. Pergunte: "Ausência de notificação significa que o lugar está seguro?" A resposta esperada é não; não ensinar antes da resposta.

## Perguntas finais
O que esperava que acontecesse? Qual trecho foi confuso? A mensagem parecia real ou de teste? O que significa confirmar a leitura? Em qual situação usaria esse recurso? Que alternativa usaria hoje?

## Registro e análise
Usar `sessoes_cidadaos.csv`. Conclusão e compreensão são campos separados. Registrar tempos em segundos, número de intervenções e evidência de cada resposta. Para semântica, 1 significa correto e 0 incorreto; deixar vazio significa não observado. Nunca converter vazio em sucesso.

Meta proposta (ainda não resultado): pelo menos 4 de 5 concluindo sem ajuda e 4 de 5 identificando as quatro informações essenciais. Apresentar contagens, resultados individuais e mediana de tempos; explicar a amostra.

## Comparativo opcional antes/depois
Usar o mesmo número de avisos e a mesma complexidade na tarefa manual e no aplicativo. Alternar a ordem entre participantes. Registrar intervenções e erros. Só calcular melhoria percentual depois de medir ambas as condições. Não atribuir melhoria ao produto a partir de um cronômetro isolado.

## Entrevista de comprador
Conversar com um responsável real pela comunicação de moradores. Perguntar sobre o último aviso: quando ocorreu, quem atuou, quais ferramentas usou, como escolheu destinatários, quanto tempo gastou e o que não conseguiu acompanhar. Investigar quem decide e de qual orçamento sairia o gasto.

Somente depois mostrar a proposta de R$ 990/mês, limites e funcionalidades previstas. Perguntar que condições seriam necessárias para um piloto, quais objeções existem e qual próximo compromisso concreto faria sentido. Registrar em `entrevista_comprador.csv`. Uma resposta positiva ou elogio não é contrato.

## Atualizar o Canvas
Para cada hipótese, registrar evidência, limitação e decisão: manter, alterar ou rejeitar. Preservar a versão anterior. Não inventar histórico de CP1. Se o resultado contrariar a proposta, explicitar a mudança: isso mostra aprendizagem.

# Gravação do pitch — AlertaCidadão

O aplicativo, o repositório, os slides, o roteiro e a base visual estão preparados. A etapa pendente é gravar as vozes reais dos cinco integrantes, montar o resultado e publicar o vídeo final. A base entregue, sozinha e sem a participação da equipe, não atende ao vídeo-pitch da disciplina.

## Acessos

- [Teleprompter: escolha seu nome e trecho](https://alertacidadao-bi-jpczz.est-dio-like-0113.chatgpt.site/gravacao)
- [MVP público](https://alertacidadao-bi-jpczz.est-dio-like-0113.chatgpt.site)
- [Materiais da entrega](https://alertacidadao-bi-jpczz.est-dio-like-0113.chatgpt.site/entrega)
- [Repositório público](https://github.com/jpczz/alertacidadao-bi)

O roteiro completo, com falas literais, ações de tela e tempos da demonstração, está em `../02_documentos/Roteiro_Pitch_e_Gravacao.pdf`. O arquivo editável está ao lado, em DOCX. `KIT_GRAVACAO.json` e `roteiro_segmentos.json` reproduzem os seis blocos do teleprompter.

## Quem grava o quê

| No vídeo | Integrante | RM | Duração | Nome do arquivo |
|---|---|---|---|---|
| 0:00–0:45 | Kaio Vinicius Meireles Alves | 553282 | 45 s | `01_problema.mp4` |
| 0:45–1:30 | Lucas Alves de Souza | 553956 | 45 s | `02_solucao.mp4` |
| 1:30–3:00 | Guilherme Fernandes de Freitas | 554323 | 90 s | `03_demo.mp4` |
| 3:00–4:00 | João Pedro Chizzolini de Freitas | 553172 | 60 s | `04_negocio.mp4` |
| 4:00–4:30 | Henrique Rafael | 553945 | 30 s | `05_impacto.mp4` |
| 4:30–4:55 | Henrique Rafael | 553945 | 25 s | `06_time.mp4` |

São cinco pessoas e seis arquivos: Henrique grava dois trechos. Gravem na horizontal, com o microfone próximo e luz no rosto. Leiam no ritmo 1× do teleprompter. A contagem inicial não entra no clipe aproveitado. Deixem a fala caber no tempo sem acelerar a voz. As instruções de tela não são faladas.

## Base visual pronta

`Pitch_Base_Visual_4m55.mp4` tem **295 segundos, 1920 × 1080, 25 quadros/s e nenhuma faixa de áudio**. O vídeo contém os slides revisados e preserva a captura real da jornada de 90 segundos já produzida: cadastro, filtragem por área, notificação interna, leitura, painel e ausência de duplicidade. A captura usa cenários sintéticos; não apresenta um envio externo real nem uma integração meteorológica ao vivo.

| Momento | Conteúdo visual |
|---|---|
| 0:00–0:14 | Lâmina 1: abertura |
| 0:14–0:45 | Lâmina 2: problema |
| 0:45–1:30 | Lâmina 3: solução |
| 1:30–3:00 | Demonstração real gravada |
| 3:00–3:20 | Lâmina 5: cliente e receita |
| 3:20–4:00 | Lâmina 6: economia unitária |
| 4:00–4:30 | Lâmina 7: evidências e limites |
| 4:30–4:55 | Lâmina 8: equipe e próximo passo |

As lâminas 9–11 são apêndices para consulta e não entram nos cinco minutos. A lâmina 4 acompanha a demonstração no deck; a base em MP4 apresenta a jornada gravada nesse intervalo.

## Montagem com as seis vozes

Coloque os seis clipes em uma pasta, usando os nomes da tabela. Também são aceitos WAV, MP3, M4A e AAC com o mesmo nome-base. Cada arquivo deve conter áudio. O script já entregue normaliza os volumes, reúne as vozes na ordem correta e completa o restante do bloco com silêncio. Ele recusa uma fala maior que o bloco e não gera voz artificial.

Com Python e FFmpeg disponíveis, execute a partir desta pasta:

```bash
python ADICIONAR_NARRACOES.py --audio-dir PASTA_DAS_VOZES --output Pitch_Final_AlertaCidadao.mp4
```

Esse comando monta apenas o áudio sobre a base visual. Para mostrar o rosto dos integrantes, posicione os clipes em um editor de vídeo sem cobrir as informações do produto. O roteiro identifica os participantes e os nomes/RMs também aparecem na lâmina final.

## Antes da submissão

Assistam ao resultado completo. Confiram as cinco vozes, a sincronização da demo, o volume e a duração real de no máximo cinco minutos. Publiquem o vídeo com acesso sem login e insiram o endereço real no PDF único da disciplina, junto aos links do MVP e do repositório. Uma página com o aviso de vídeo pendente não substitui o vídeo.

O prazo informado no enunciado é 19/11/2026 às 23h55. Mantenham os materiais acessíveis durante a correção. Os testes técnicos não substituem entrevistas ou validação comercial; essas atividades não são afirmadas como realizadas.


## Gerar o PDF após publicar o vídeo

Abra https://alertacidadao-bi-jpczz.est-dio-like-0113.chatgpt.site/finalizar, cole a URL pública real, informe a duração final e confirme a participação dos cinco. O gerador produz o PDF único com o link clicável, sem precisar editar no Word. Confira o vídeo e o PDF antes de enviar no portal da disciplina.

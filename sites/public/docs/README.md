# Recursos documentais da entrega

O vídeo final fornecido pela equipe está em [YouTube](https://youtu.be/RtqAPawx7h4). O PDF único de submissão está em [docs/Dossie_AlertaCidadao_Para_Submissao.pdf](../../../docs/Dossie_AlertaCidadao_Para_Submissao.pdf) e os materiais completos estão em [entrega/](../../../entrega/).

Esta pasta contém os recursos usados pela central online e pelo utilitário de atualização do PDF:

- `Dossie_AlertaCidadao_BI.pdf` — versão final com o link do vídeo.
- `Dossie_AlertaCidadao_Modelo_Video.pdf` — template técnico com o campo do vídeo limpo, usado somente pelo utilitário `/finalizar`.
- `Pitch_AlertaCidadao.pdf`.
- `Roteiro_Pitch_e_Gravacao.pdf`.
- `Relatorio_Ensaio_Controlado.pdf`.
- `Guia_Publicacao.pdf`.
- `video-link-slot.json` — coordenadas e SHA-256 do template.

O template não substitui o dossiê final de submissão. Seu SHA-256 deve corresponder a `video-link-slot.json`; o gerador recusa versões diferentes. Ao atualizar o documento final, preserve esse par técnico até que ambos sejam regenerados juntos.

A central pública está em https://alertacidadao-bi-jpczz.est-dio-like-0113.chatgpt.site/entrega. O MVP central — cadastros, cenários, notificações, leituras, painel e extração dos comprovantes em `public/samples` — funciona independentemente dos documentos de apresentação.

import { PDFDocument, StandardFonts, PDFName, PDFString, rgb } from 'pdf-lib';

const PDF_PATH = '/docs/Dossie_AlertaCidadao_Modelo_Video.pdf';
const SLOT_PATH = '/docs/video-link-slot.json';
const DOWNLOAD_NAME = 'Dossie_AlertaCidadao_Para_Submissao.pdf';
const LINK_TEXT = 'Vídeo-pitch da equipe: assistir ao vídeo público';

class FinalizerError extends Error {
  constructor(message, fieldId = null) {
    super(message);
    this.name = 'FinalizerError';
    this.fieldId = fieldId;
  }
}

export function validateVideoUrl(value) {
  if (typeof value !== 'string' || /[\u0000-\u001f\u007f]/.test(value)) {
    throw new FinalizerError('O link contém caracteres de controle. Cole uma URL HTTPS em uma única linha.', 'video-url');
  }
  const text = value.trim();
  if (!text || text.length > 4096 || /\s/.test(text) || /%(?:0[0-9a-f]|1[0-9a-f]|7f)/i.test(text)) {
    throw new FinalizerError('Cole o link HTTPS completo do vídeo, sem espaços ou quebras de linha.', 'video-url');
  }
  let url;
  try { url = new URL(text); }
  catch { throw new FinalizerError('O link não é válido. Use uma URL completa começando com https://.', 'video-url'); }
  if (url.protocol !== 'https:' || !url.hostname) {
    throw new FinalizerError('O link do vídeo precisa começar com https://.', 'video-url');
  }
  if (url.username || url.password) {
    throw new FinalizerError('Use um link sem usuário ou senha incorporados à URL.', 'video-url');
  }
  return url.href;
}

export function validateDuration(value) {
  const seconds = Number(value);
  if (String(value).trim() === '' || !Number.isInteger(seconds) || seconds < 1 || seconds > 300) {
    throw new FinalizerError('Informe a duração em segundos inteiros, entre 1 e 300.', 'video-duration');
  }
  return seconds;
}

function durationText(seconds) {
  const minutes = Math.floor(seconds / 60);
  const remaining = seconds % 60;
  return minutes ? `${minutes}min${String(remaining).padStart(2, '0')}s` : `${remaining}s`;
}

function validateSlot(slot, doc) {
  if (!slot || !/^[a-f0-9]{64}$/i.test(slot.sha256 || '') ||
      !Number.isInteger(slot.page_index) || slot.page_index < 0 || slot.page_index >= doc.getPageCount() ||
      !Array.isArray(slot.rect) || slot.rect.length !== 4 || !slot.rect.every(Number.isFinite) ||
      !Number.isFinite(slot.page_height)) {
    throw new FinalizerError('A configuração do campo de vídeo está incompleta. Recarregue a página e tente novamente.');
  }
  const page = doc.getPage(slot.page_index);
  const [x0, y0, x1, y1] = slot.rect;
  const height = page.getHeight();
  const media = page.getMediaBox();
  if (Math.abs(height - slot.page_height) > 0.5 || page.getRotation().angle % 360 !== 0 ||
      Math.abs(media.x) > 0.01 || Math.abs(media.y) > 0.01 ||
      x0 < 0 || y0 < 0 || x1 > page.getWidth() || y1 > height || x1 <= x0 || y1 <= y0) {
    throw new FinalizerError('O campo de vídeo não corresponde ao formato deste PDF. Recarregue os materiais antes de continuar.');
  }
  return { page, x: x0, y: height - y1, width: x1 - x0, height: y1 - y0, top: height - y0 };
}

async function sha256(bytes) {
  const digest = await globalThis.crypto.subtle.digest('SHA-256', bytes);
  return Array.from(new Uint8Array(digest), byte => byte.toString(16).padStart(2, '0')).join('');
}

function fitFontSize(font, text, availableWidth, preferred, minimum) {
  const width = font.widthOfTextAtSize(text, preferred);
  const size = Math.min(preferred, preferred * availableWidth / width);
  return size >= minimum ? size : null;
}

/** Modify only the confirmed video slot; retain all original pages and annotations. */
export async function createSubmissionPdf(pdfBytes, slot, values) {
  const videoUrl = validateVideoUrl(values.videoUrl);
  const seconds = validateDuration(values.duration);
  if (values.teamConfirmed !== true) {
    throw new FinalizerError('Confirme a participação dos cinco integrantes no vídeo.', 'team-confirmed');
  }
  if (!slot || !/^[a-f0-9]{64}$/i.test(slot.sha256 || '')) {
    throw new FinalizerError('A identificação da versão do dossiê não está disponível. Tente novamente.');
  }
  if (!globalThis.crypto?.subtle) {
    throw new FinalizerError('Este navegador não disponibiliza a verificação do PDF. Abra esta página em um navegador atualizado, usando HTTPS.');
  }
  if (await sha256(pdfBytes) !== slot.sha256.toLowerCase()) {
    throw new FinalizerError('O dossiê foi atualizado e o campo de vídeo pertence a outra versão. Recarregue a página antes de gerar o PDF.');
  }

  const doc = await PDFDocument.load(pdfBytes, { updateMetadata: false });
  const box = validateSlot(slot, doc);
  const font = await doc.embedFont(StandardFonts.Helvetica);
  const padding = 3;
  const availableWidth = box.width - padding * 2;
  const linkSize = fitFontSize(font, LINK_TEXT, availableWidth, 10.5, 9);
  if (!linkSize || box.height < 18) {
    throw new FinalizerError('O espaço reservado ao vídeo está pequeno demais. O dossiê precisa de um campo de vídeo maior.');
  }
  const declaration = `Equipe declara: ${durationText(seconds)} de duração e participação dos 5 integrantes.`;
  const declarationSize = fitFontSize(font, declaration, availableWidth, 9, 8.5);
  const linkY = box.top - padding - linkSize;
  const declarationY = linkY - 13;
  const declarationIncluded = declarationSize !== null && declarationY >= box.y + padding + 1;

  // PyMuPDF's top-left rectangle becomes a bottom-left PDF rectangle here.
  box.page.drawRectangle({ x: box.x, y: box.y, width: box.width, height: box.height, color: rgb(1, 1, 1) });
  const linkX = box.x + padding;
  const linkWidth = font.widthOfTextAtSize(LINK_TEXT, linkSize);
  box.page.drawText(LINK_TEXT, { x: linkX, y: linkY, size: linkSize, font, color: rgb(0.07, 0.31, 0.32) });
  box.page.drawLine({ start: { x: linkX, y: linkY - 1.4 }, end: { x: linkX + linkWidth, y: linkY - 1.4 }, thickness: 0.55, color: rgb(0.07, 0.31, 0.32) });
  if (declarationIncluded) {
    box.page.drawText(declaration, { x: linkX, y: declarationY, size: declarationSize, font, color: rgb(0.26, 0.34, 0.35) });
  }

  const annotation = doc.context.obj({
    Type: PDFName.of('Annot'),
    Subtype: PDFName.of('Link'),
    Rect: [linkX, linkY - 3, linkX + linkWidth, linkY + linkSize],
    Border: [0, 0, 0],
    A: doc.context.obj({ Type: PDFName.of('Action'), S: PDFName.of('URI'), URI: PDFString.of(videoUrl) }),
  });
  box.page.node.addAnnot(doc.context.register(annotation));
  return { bytes: await doc.save(), declarationIncluded, pageNumber: slot.page_index + 1 };
}

async function readTemplate() {
  const options = { cache: 'no-store', credentials: 'omit', redirect: 'error' };
  const [pdfResponse, slotResponse] = await Promise.all([fetch(PDF_PATH, options), fetch(SLOT_PATH, options)]);
  if (!pdfResponse.ok || !slotResponse.ok) {
    throw new FinalizerError('Não foi possível carregar o dossiê e o campo de vídeo. Recarregue a página e tente novamente.');
  }
  const [bytes, slot] = await Promise.all([pdfResponse.arrayBuffer(), slotResponse.json()]);
  return { bytes, slot };
}

function bindPage() {
  const form = document.getElementById('finalizer-form');
  if (!form) return;
  const fields = document.getElementById('finalizer-fields');
  const button = document.getElementById('generate-pdf');
  const status = document.getElementById('status');
  const result = document.getElementById('download-result');
  const download = document.getElementById('download-pdf');
  let blobUrl = null;
  let running = false;

  const clearDownload = () => {
    if (blobUrl) URL.revokeObjectURL(blobUrl);
    blobUrl = null;
    download.removeAttribute('href');
    result.hidden = true;
  };
  const setStatus = (message, kind = 'info') => {
    status.dataset.kind = kind;
    status.textContent = message;
  };
  form.addEventListener('input', () => {
    if (!running && blobUrl) {
      clearDownload();
      setStatus('Os dados foram alterados. Gere o PDF novamente para incluir a versão atual.');
    }
  });
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (running) return;
    clearDownload();
    try {
      const values = {
        videoUrl: validateVideoUrl(document.getElementById('video-url').value),
        duration: validateDuration(document.getElementById('video-duration').value),
        teamConfirmed: document.getElementById('team-confirmed').checked,
      };
      if (!values.teamConfirmed) throw new FinalizerError('Confirme a participação dos cinco integrantes no vídeo.', 'team-confirmed');
      running = true;
      button.disabled = true;
      fields.disabled = true;
      setStatus('Carregando e conferindo a versão do dossiê…');
      const { bytes, slot } = await readTemplate();
      setStatus('Inserindo o link no PDF, neste navegador…');
      const generated = await createSubmissionPdf(bytes, slot, values);
      blobUrl = URL.createObjectURL(new Blob([generated.bytes], { type: 'application/pdf' }));
      download.href = blobUrl;
      download.download = DOWNLOAD_NAME;
      result.hidden = false;
      download.click();
      setStatus(`PDF gerado com o link na página ${generated.pageNumber}. Se o download não começou, use o botão abaixo. Abra o arquivo e confira o acesso ao vídeo antes de enviar.`, 'success');
    } catch (error) {
      const message = error instanceof FinalizerError ? error.message : 'Não foi possível gerar o PDF. Confira sua conexão, recarregue esta página e tente novamente.';
      setStatus(message, 'error');
      fields.disabled = false;
      if (error instanceof FinalizerError && error.fieldId) document.getElementById(error.fieldId)?.focus();
    } finally {
      running = false;
      fields.disabled = false;
      button.disabled = false;
    }
  });
  window.addEventListener('pagehide', clearDownload);
  fields.disabled = false;
  setStatus('Preencha os dados do vídeo final para gerar o PDF.');
}

if (typeof document !== 'undefined') bindPage();

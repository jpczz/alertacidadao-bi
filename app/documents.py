"""Extract synthetic document fields. Never store document bytes."""
import io, re, shutil, unicodedata
from PIL import Image, ImageOps
from pypdf import PdfReader

MAX_SIZE=2*1024*1024
Image.MAX_IMAGE_PIXELS=8_000_000

class DocumentError(ValueError): pass

def normalize(text):
    return ''.join(c for c in unicodedata.normalize('NFKD',text) if not unicodedata.combining(c)).upper()

def extract_fields(data: bytes, filename: str) -> dict:
    if not data or len(data)>MAX_SIZE: raise DocumentError('Arquivo vazio ou acima de 2 MB.')
    method=''
    try:
        if data.startswith(b'%PDF'):
            reader=PdfReader(io.BytesIO(data))
            if reader.is_encrypted or len(reader.pages)>2:
                raise DocumentError('Use um PDF de teste sem senha, com no m\u00e1ximo duas p\u00e1ginas.')
            text='\n'.join(p.extract_text() or '' for p in reader.pages)
            method='texto_pdf'
            if not text.strip():
                raise DocumentError('PDF sem camada de texto. Use uma imagem PNG/JPG ou o cadastro manual.')
        elif data.startswith(b'\x89PNG') or data.startswith(b'\xff\xd8'):
            if not shutil.which('tesseract'):
                raise DocumentError('OCR n\u00e3o instalado neste ambiente. Use o PDF de exemplo ou preencha manualmente.')
            import pytesseract
            image=Image.open(io.BytesIO(data))
            if image.width*image.height>8_000_000: raise DocumentError('Imagem acima de 8 megapixels.')
            image=ImageOps.exif_transpose(image).convert('RGB')
            image.thumbnail((2400,2400))
            text=pytesseract.image_to_string(image,lang='eng',config='--psm 6',timeout=15)
            method='ocr_tesseract'
        else:
            raise DocumentError('Formato n\u00e3o suportado. Use PDF com texto, PNG ou JPG.')
    except DocumentError: raise
    except Exception as exc:
        raise DocumentError('N\u00e3o foi poss\u00edvel ler o documento. Tente o exemplo ou o preenchimento manual.') from exc
    text=normalize(text)
    if 'DOCUMENTO SINTETICO' not in text:
        raise DocumentError('Esta demonstra\u00e7\u00e3o aceita somente documentos sint\u00e9ticos. N\u00e3o envie contas reais.')
    labels={'label':'LOCAL','street':'ENDERECO','number':'NUMERO','neighborhood':'BAIRRO','city':'CIDADE','state':'UF','postal_code':'CEP','zone':'AREA'}
    result={}
    for key,label in labels.items():
        match=re.search(r'^\s*'+label+r'\s*[:\-]\s*(.+?)\s*$',text,re.MULTILINE)
        if match: result[key]=match.group(1).strip()
    if result.get('zone') not in ('TESTE-A','TESTE-B','TESTE-C'):
        raise DocumentError('\u00c1rea de teste n\u00e3o reconhecida. Revise manualmente.')
    missing=[k for k in labels if k not in result]
    return {'fields':result,'method':method,'missing_fields':missing,'review_required':True,'synthetic':True,'stored':False}

import json, shutil
from pathlib import Path
import pytest
from app.documents import extract_fields, DocumentError, MAX_SIZE

SAMPLES=Path(__file__).parents[1]/'app'/'samples'

@pytest.mark.parametrize('zone',['A','B','C'])
def test_pdf_extraction_matches_ground_truth(zone):
    expected=json.loads((SAMPLES/f'gabarito_{zone}.json').read_text())
    actual=extract_fields((SAMPLES/f'comprovante_{zone}.pdf').read_bytes(),f'{zone}.pdf')
    assert actual['fields']==expected
    assert actual['method']=='texto_pdf' and actual['review_required'] and not actual['stored']

@pytest.mark.skipif(not shutil.which('tesseract'),reason='Optional image OCR not installed')
def test_real_ocr_on_synthetic_image():
    actual=extract_fields((SAMPLES/'comprovante_A.png').read_bytes(),'A.png')
    assert actual['method']=='ocr_tesseract'
    assert actual['fields']==json.loads((SAMPLES/'gabarito_A.json').read_text())

def test_invalid_format_rejected():
    with pytest.raises(DocumentError):extract_fields(b'not a pdf','x.pdf')

def test_oversized_document_rejected():
    with pytest.raises(DocumentError):extract_fields(b'x'*(MAX_SIZE+1),'x.png')

def test_extract_endpoint(client):
    r=client.post('/api/documents/extract',files={'file':('test.pdf',(SAMPLES/'comprovante_A.pdf').read_bytes(),'application/pdf')})
    assert r.status_code==200 and r.json()['fields']['zone']=='TESTE-A'
    assert r.json()['stored'] is False

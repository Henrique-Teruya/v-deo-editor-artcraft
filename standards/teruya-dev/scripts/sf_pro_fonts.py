"""Load the installed macOS San Francisco font for this local PDF build.

Only temporary instances are created. No Apple font binaries are bundled with
the portable standard. Text and Display are optical-size settings of SF Pro.
"""
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def register_sf_pro():
    source = Path(os.environ.get('TERUYA_SF_PRO_FONT', '/System/Library/Fonts/SFNS.ttf'))
    if not source.is_file():
        raise RuntimeError('SF Pro is required; set TERUYA_SF_PRO_FONT to a local SF Pro variable font. No silent font substitution.')
    subsetter = shutil.which('hb-subset')
    if not subsetter:
        raise RuntimeError('hb-subset is required to prepare the SF Pro optical instances.')
    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    manifest = {'source': str(source), 'sha256': source_hash, 'instances': []}
    with tempfile.TemporaryDirectory(prefix='teruya-sf-pro-') as tmp:
        for role, opsz in [('Text', 17), ('Display', 28)]:
            for weight, axis_weight in [(400, 400), (600, 590)]:
                name = f'SF{role}{weight}'
                path = Path(tmp) / f'{name}.ttf'
                axes = f'wght={axis_weight},opsz={opsz},wdth=100,GRAD=400'
                subprocess.run([subsetter, str(source), '--unicodes=*', f'--variations={axes}', f'--output-file={path}'], check=True, capture_output=True)
                font = TTFont(name, str(path))
                # Distinct PDF subset identifiers prevent equal source names from
                # collapsing different optical/weight instances in ReportLab.
                font.face.name = f'SFPro-{role}-{weight}-SystemInstance'.encode('ascii')
                pdfmetrics.registerFont(font)
                manifest['instances'].append({'role': role, 'weight': weight, 'axisWeight': axis_weight, 'opticalSize': opsz, 'width': 100, 'grade': 400, 'pdfName': font.face.name.decode()})
            pdfmetrics.registerFontFamily(f'SF{role}400', normal=f'SF{role}400', bold=f'SF{role}600', italic=f'SF{role}400', boldItalic=f'SF{role}600')
            pdfmetrics.registerFontFamily(f'SF{role}600', normal=f'SF{role}600', bold=f'SF{role}600', italic=f'SF{role}600', boldItalic=f'SF{role}600')
    return manifest


def font_name(size, weight=400):
    return f'SF{"Display" if size >= 20 else "Text"}{600 if weight >= 500 else 400}'

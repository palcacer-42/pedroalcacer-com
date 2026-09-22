import os
from pathlib import Path
import sys

# Attempt to load translations from the original generate.py
sys.path.append(str(Path(__file__).parent))
try:
    from generate import TRANSLATIONS, PROGRAMME
except ImportError:
    print("Could not import TRANSLATIONS from generate.py")
    sys.exit(1)

OUT = Path(__file__).parent / "output"
OUT.mkdir(exist_ok=True)

LANGUAGES = ['en', 'es', 'ca', 'fr', 'it']
BASE_DIR = '/Users/palcacer/Sites/pedroalcacer-com/static/programs/originals'

def generate_docs():
    for lang in LANGUAGES:
        if lang not in TRANSLATIONS:
            continue
            
        t = TRANSLATIONS[lang]

        tracklist_html = "<ul>"
        for piece, comp in PROGRAMME:
            if comp:
                tracklist_html += f'<li><strong>{piece}</strong> - <em>{comp}</em></li>'
            else:
                tracklist_html += f'<li><strong>{piece}</strong></li>'
        tracklist_html += '</ul>'

        html = f"""<html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word' xmlns='http://www.w3.org/TR/REC-html40'>
<head><meta charset='utf-8'><title>Mecatl Harmonium</title></head>
<body>
<h1>MECATL Harmonium</h1>
<h2>{t['subtitle']}</h2>
<p><strong>Pedro Alcàcer Doria</strong><br><strong>Hugo Miguel de Rodas Sánchez</strong></p>
<hr>

<h2>{t['programme_heading']}</h2>
{tracklist_html}
<p><em>{t['arrangements']}</em></p>
<hr>

<h2>Pedro Alcàcer</h2>
<p>{t['pedro_bio_1']}</p>
<p>{t['pedro_bio_2']}</p>
<hr>

<h2>Hugo Miguel de Rodas Sánchez</h2>
<p>{t['hugo_bio_1']}</p>
<p>{t['hugo_bio_2']}</p>
<hr>
<p>{t['about']}</p>

</body></html>"""

        doc_path = os.path.join(BASE_DIR, f"mecatlharmonium_{lang}.doc")
        with open(doc_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Generated {doc_path}")

if __name__ == "__main__":
    generate_docs()

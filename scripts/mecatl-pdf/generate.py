"""
Generate Mecatl — Harmonium programme PDFs in 5 languages.
Matches the original German PDF design: teal background, cream serif text,
ornamental borders, historical illustrations and musician photos.
"""

import asyncio
import base64
import os
from pathlib import Path
from playwright.async_api import async_playwright

ASSETS = Path(__file__).parent / "assets"
OUT = Path(__file__).parent / "output"
OUT.mkdir(exist_ok=True)

BG = "#316a87"
TEXT = "#f0ebe0"
TEXT_DIM = "#c8bfaf"


def img_b64(name):
    path = ASSETS / name
    data = path.read_bytes()
    ext = path.suffix.lstrip(".")
    if ext == "jpg":
        ext = "jpeg"
    return f"data:image/{ext};base64,{base64.b64encode(data).decode()}"


TRANSLATIONS = {
    "en": {
        "subtitle": "HISTORICAL LUTE INSTRUMENTS",
        "quote": "PLUCKED INSTRUMENTS ARE NEITHER PERFECT NOR IMPERFECT,\nBUT RATHER AS ONE PLAYS THEM...",
        "mecatl_def": 'In Nahuatl, the ancient language\nof the Aztecs, means "string".',
        "harm_latin": "LATIN — Harmony\nMusik-Harmonica /\nHarmonium",
        "instruments": ["Baroque guitar", "Archlute", "Theorbo"],
        "pedro_bio_1": (
            "Pedro was born in 1982 in Mexico City and began his musical education early, "
            "influenced by his father, the Catalan jazz musician Francesc Alcàcer. He studied "
            "jazz guitar with Francisco Lelo de la Rea and subsequently classical guitar and "
            "composition with Hector Ramos. He completed his classical guitar studies at the "
            "Escuela Nacional de Música-UNAM and continued his studies with Isabelle Villei, "
            "Eloy Cruz and Antonio Corona. In 2006 he obtained the professional diploma in "
            "Renaissance and Baroque plucked instruments at the Conservatory in Girona under "
            "Xavier Diaz-Latorre."
        ),
        "pedro_bio_2": (
            "He then continued his studies at the Hochschule für Künste Bremen under Joachim "
            "Held and Lee Santana, before refining his instrumental skills with Evangelina "
            "Mascardi in Italy. He has collaborated with distinguished conductors such as "
            "Gabriel Garrido, Alessandro di Marchi, Marco Mencoboni, Paolo Faldi, Riccardo "
            "Doni, Horacio Franco, Christoph Hammer, Carlos Aranzay, Gerhard Oppel, Burak "
            "Özdemir and others, performing at renowned festivals and concert series in Italy, "
            "Germany, Spain, France, Czech Republic, Belgium, the Netherlands, Brazil and Mexico."
        ),
        "hugo_bio_1": (
            "Hugo Miguel de Rodas Sánchez was born in Mexico City, where he first studied "
            "classical guitar at the Universidad Nacional Autónoma de México. In 2004 he won "
            "the Rosa Mística guitar competition in Curitiba, Brazil, before turning his focus "
            "to historical lute instruments and the performance practice of early music. He "
            "attended numerous masterclasses and was invited in 2008 by the Freiburger "
            "Barockorchester to deepen his studies in Europe."
        ),
        "hugo_bio_2": (
            "He then studied lute instruments and Baroque guitar with Lee Santana and Joachim "
            "Held at the Hochschule für Künste Bremen, and performed under distinguished "
            "conductors such as Gabriel Garrido with numerous ensembles and orchestras, "
            "including the Deutsche Kammerphilharmonie Bremen, Knabenchor Hannover, Bremer "
            "Barockorchester, Orkiestra Historyczna, Holland Baroque and Los Temperamentos, "
            "in many countries across Europe, Central and South America."
        ),
        "programme_heading": "PROGRAMME",
        "arrangements": "Arrangements by Hugo Miguel de Rodas Sánchez",
        "about": (
            "Two friends and colleagues who happened to grow up and study in the same "
            "neighbourhood and at the same university in one of the largest cities in the world.\n"
            "Pedro and Hugo share not only their birthplace and alma mater, but also a passion "
            "for Renaissance and Baroque music, and the cultural heritage shaped by a country "
            "of enormous cultural and musical richness: Mexico."
        ),
        "contact_label": "Contact",
    },
    "es": {
        "subtitle": "INSTRUMENTOS HISTÓRICOS DE CUERDA PULSADA",
        "quote": "LOS INSTRUMENTOS DE CUERDA PULSADA NO SON NI PERFECTOS NI IMPERFECTOS,\nSINO TAL COMO SE TOCAN...",
        "mecatl_def": 'En náhuatl, la antigua lengua\nde los aztecas, significa "cuerda".',
        "harm_latin": "LATÍN — Harmonía\nMúsica-Harmónica /\nHarmonium",
        "instruments": ["Guitarra barroca", "Arciliuto", "Tiorba"],
        "pedro_bio_1": (
            "Pedro nació en 1982 en Ciudad de México y comenzó su formación musical a temprana "
            "edad, influenciado por su padre, el músico de jazz catalán Francesc Alcàcer. "
            "Estudió guitarra jazz con Francisco Lelo de la Rea y posteriormente guitarra "
            "clásica y composición con Hector Ramos. Completó sus estudios de guitarra clásica "
            "en la Escuela Nacional de Música-UNAM y continuó su formación con Isabelle Villei, "
            "Eloy Cruz y Antonio Corona. En 2006 obtuvo el título profesional en instrumentos "
            "de cuerda pulsada del Renacimiento y el Barroco en el Conservatorio de Girona con "
            "Xavier Diaz-Latorre."
        ),
        "pedro_bio_2": (
            "Posteriormente continuó sus estudios en la Hochschule für Künste Bremen con "
            "Joachim Held y Lee Santana, perfeccionando su técnica instrumental con Evangelina "
            "Mascardi en Italia. Ha colaborado con destacados directores como Gabriel Garrido, "
            "Alessandro di Marchi, Marco Mencoboni, Paolo Faldi, Riccardo Doni, Horacio Franco, "
            "Christoph Hammer, Carlos Aranzay, Gerhard Oppel, Burak Özdemir y otros, actuando "
            "en festivales y foros de renombre en Italia, Alemania, España, Francia, República "
            "Checa, Bélgica, Países Bajos, Brasil y México."
        ),
        "hugo_bio_1": (
            "Hugo Miguel de Rodas Sánchez nació en Ciudad de México, donde estudió inicialmente "
            "guitarra clásica en la Universidad Nacional Autónoma de México. En 2004 ganó el "
            "concurso de guitarra Rosa Mística en Curitiba, Brasil, antes de orientar su "
            "atención hacia los instrumentos históricos de cuerda pulsada y la práctica "
            "interpretativa de la música antigua. Asistió a numerosos cursos magistrales y fue "
            "invitado en 2008 por la Freiburger Barockorchester a profundizar sus estudios "
            "en Europa."
        ),
        "hugo_bio_2": (
            "Posteriormente estudió laúd e instrumentos barrocos de cuerda pulsada con Lee "
            "Santana y Joachim Held en la Hochschule für Künste Bremen, actuando bajo la "
            "dirección de destacados directores como Gabriel Garrido con numerosos conjuntos y "
            "orquestas, entre ellos la Deutsche Kammerphilharmonie Bremen, el Knabenchor "
            "Hannover, la Bremer Barockorchester, la Orkiestra Historyczna, Holland Baroque y "
            "Los Temperamentos, en numerosos países de Europa, América Central y América del Sur."
        ),
        "programme_heading": "PROGRAMA",
        "arrangements": "Arreglos de Hugo Miguel de Rodas Sánchez",
        "about": (
            "Dos amigos y colegas que crecieron y estudiaron en el mismo barrio y en la misma "
            "universidad de una de las ciudades más grandes del mundo.\n"
            "Pedro y Hugo comparten no solo su lugar de nacimiento y su alma máter, sino también "
            "la pasión por la música del Renacimiento y del Barroco, y el patrimonio cultural "
            "forjado en un país de enorme riqueza cultural y musical: México."
        ),
        "contact_label": "Contacto",
    },
    "ca": {
        "subtitle": "INSTRUMENTS HISTÒRICS DE CORDA POLSADA",
        "quote": "ELS INSTRUMENTS DE CORDA POLSADA NO SÓN NI PERFECTES NI IMPERFECTES,\nSINÓ TAL COM ES TOQUEN...",
        "mecatl_def": 'En nàhuatl, la llengua antiga\ndels asteques, significa "corda".',
        "harm_latin": "LLATÍ — Harmonia\nMúsica-Harmònica /\nHarmonium",
        "instruments": ["Guitarra barroca", "Arxilaüt", "Tiorba"],
        "pedro_bio_1": (
            "Pedro va néixer el 1982 a la Ciutat de Mèxic i va iniciar la seva formació musical "
            "de ben petit, sota la influència del seu pare, el músic de jazz català Francesc "
            "Alcàcer. Va estudiar guitarra jazz amb Francisco Lelo de la Rea i posteriorment "
            "guitarra clàssica i composició amb Hector Ramos. Va completar els seus estudis de "
            "guitarra clàssica a l'Escuela Nacional de Música-UNAM i va continuar la seva "
            "formació amb Isabelle Villei, Eloy Cruz i Antonio Corona. L'any 2006 va obtenir el "
            "títol professional en instruments de corda polsada del Renaixement i el Barroc al "
            "Conservatori de Girona amb Xavier Diaz-Latorre."
        ),
        "pedro_bio_2": (
            "Posteriorment va continuar els seus estudis a la Hochschule für Künste Bremen amb "
            "Joachim Held i Lee Santana, perfeccionant la seva tècnica instrumental amb "
            "Evangelina Mascardi a Itàlia. Ha col·laborat amb directors destacats com Gabriel "
            "Garrido, Alessandro di Marchi, Marco Mencoboni, Paolo Faldi, Riccardo Doni, Horacio "
            "Franco, Christoph Hammer, Carlos Aranzay, Gerhard Oppel, Burak Özdemir i altres, "
            "actuant en festivals i concerts de prestigi a Itàlia, Alemanya, Espanya, França, "
            "República Txeca, Bèlgica, Països Baixos, Brasil i Mèxic."
        ),
        "hugo_bio_1": (
            "Hugo Miguel de Rodas Sánchez va néixer a la Ciutat de Mèxic, on va estudiar "
            "inicialment guitarra clàssica a la Universidad Nacional Autónoma de México. El 2004 "
            "va guanyar el concurs de guitarra Rosa Mística a Curitiba, Brasil, abans d'orientar "
            "la seva atenció cap als instruments de corda polsada històrics i la pràctica "
            "interpretativa de la música antiga. Va assistir a nombrosos cursos de mestratge i "
            "el 2008 va ser convidat per la Freiburger Barockorchester a aprofundir els seus "
            "estudis a Europa."
        ),
        "hugo_bio_2": (
            "Posteriorment va estudiar llaüt i instruments barrocs de corda polsada amb Lee "
            "Santana i Joachim Held a la Hochschule für Künste Bremen, actuant sota la direcció "
            "de directors destacats com Gabriel Garrido amb nombrosos conjunts i orquestres, "
            "entre ells la Deutsche Kammerphilharmonie Bremen, el Knabenchor Hannover, la "
            "Bremer Barockorchester, la Orkiestra Historyczna, Holland Baroque i Los "
            "Temperamentos, en molts països d'Europa, Amèrica Central i Amèrica del Sud."
        ),
        "programme_heading": "PROGRAMA",
        "arrangements": "Arranjaments de Hugo Miguel de Rodas Sánchez",
        "about": (
            "Dos amics i col·legues que van créixer i estudiar al mateix barri i a la mateixa "
            "universitat d'una de les ciutats més grans del món.\n"
            "Pedro i Hugo comparteixen no sols el lloc de naixement i l'alma mater, sinó també "
            "la passió per la música del Renaixement i el Barroc, i el patrimoni cultural "
            "forjat en un país d'enorme riquesa cultural i musical: Mèxic."
        ),
        "contact_label": "Contacte",
    },
    "fr": {
        "subtitle": "INSTRUMENTS HISTORIQUES À CORDES PINCÉES",
        "quote": "LES INSTRUMENTS À CORDES PINCÉES NE SONT NI PARFAITS NI IMPARFAITS,\nMAIS TELS QU'ON LES JOUE...",
        "mecatl_def": 'En nahuatl, l\'ancienne langue\ndes Aztèques, signifie « corde ».',
        "harm_latin": "LATIN — Harmonie\nMusique-Harmonica /\nHarmonium",
        "instruments": ["Guitare baroque", "Archiluth", "Théorbe"],
        "pedro_bio_1": (
            "Pedro est né en 1982 à Mexico et a commencé sa formation musicale très jeune, sous "
            "l'influence de son père, le musicien de jazz catalan Francesc Alcàcer. Il a étudié "
            "la guitare jazz auprès de Francisco Lelo de la Rea, puis la guitare classique et la "
            "composition avec Hector Ramos. Il a achevé ses études de guitare classique à "
            "l'Escuela Nacional de Música-UNAM et a poursuivi sa formation auprès d'Isabelle "
            "Villei, Eloy Cruz et Antonio Corona. En 2006, il a obtenu le diplôme professionnel "
            "en instruments à cordes pincées de la Renaissance et du Baroque au Conservatoire "
            "de Gérone sous la direction de Xavier Diaz-Latorre."
        ),
        "pedro_bio_2": (
            "Il a ensuite poursuivi ses études à la Hochschule für Künste Bremen sous la "
            "direction de Joachim Held et Lee Santana, avant de perfectionner ses compétences "
            "instrumentales auprès d'Evangelina Mascardi en Italie. Il a collaboré avec des "
            "chefs d'orchestre de renom tels que Gabriel Garrido, Alessandro di Marchi, Marco "
            "Mencoboni, Paolo Faldi, Riccardo Doni, Horacio Franco, Christoph Hammer, Carlos "
            "Aranzay, Gerhard Oppel, Burak Özdemir et d'autres, se produisant dans des festivals "
            "et des forums renommés en Italie, en Allemagne, en Espagne, en France, en "
            "République tchèque, en Belgique, aux Pays-Bas, au Brésil et au Mexique."
        ),
        "hugo_bio_1": (
            "Hugo Miguel de Rodas Sánchez est né à Mexico, où il a d'abord étudié la guitare "
            "classique à l'Universidad Nacional Autónoma de México. En 2004, il a remporté le "
            "concours de guitare Rosa Mística à Curitiba, au Brésil, avant de se tourner vers "
            "les instruments à cordes pincées historiques et la pratique de la musique ancienne. "
            "Il a suivi de nombreuses masterclasses et a été invité en 2008 par le Freiburger "
            "Barockorchester à approfondir ses études en Europe."
        ),
        "hugo_bio_2": (
            "Il a ensuite étudié le luth et la guitare baroque avec Lee Santana et Joachim Held "
            "à la Hochschule für Künste Bremen, se produisant sous la direction de chefs "
            "réputés tels que Gabriel Garrido avec de nombreux ensembles et orchestres, "
            "notamment la Deutsche Kammerphilharmonie Bremen, le Knabenchor Hannover, le Bremer "
            "Barockorchester, l'Orkiestra Historyczna, Holland Baroque et Los Temperamentos, "
            "dans de nombreux pays d'Europe, d'Amérique centrale et d'Amérique du Sud."
        ),
        "programme_heading": "PROGRAMME",
        "arrangements": "Arrangements de Hugo Miguel de Rodas Sánchez",
        "about": (
            "Deux amis et collègues qui ont grandi et étudié par hasard dans le même quartier "
            "et à la même université dans l'une des plus grandes villes du monde.\n"
            "Pedro et Hugo partagent non seulement leur lieu de naissance et leur alma mater, "
            "mais aussi une passion pour la musique de la Renaissance et du Baroque, et le "
            "patrimoine culturel façonné par un pays d'une richesse culturelle et musicale "
            "extraordinaire : le Mexique."
        ),
        "contact_label": "Contact",
    },
    "it": {
        "subtitle": "STRUMENTI A CORDE STORICI",
        "quote": "GLI STRUMENTI A PIZZICO NON SONO NÉ PERFETTI NÉ IMPERFETTI,\nMA TALI COME LI SI SUONA...",
        "mecatl_def": 'In nahuatl, l\'antica lingua\ndegli Aztechi, significa "corda".',
        "harm_latin": "LATINO — Harmonia\nMusica-Harmonica /\nHarmonium",
        "instruments": ["Chitarra barocca", "Arciliuto", "Tiorba"],
        "pedro_bio_1": (
            "Pedro è nato nel 1982 a Città del Messico e ha iniziato la sua formazione musicale "
            "in giovane età, sotto l'influenza del padre, il musicista jazz catalano Francesc "
            "Alcàcer. Ha studiato chitarra jazz con Francisco Lelo de la Rea e successivamente "
            "chitarra classica e composizione con Hector Ramos. Ha completato i suoi studi di "
            "chitarra classica presso l'Escuela Nacional de Música-UNAM e ha proseguito la sua "
            "formazione con Isabelle Villei, Eloy Cruz e Antonio Corona. Nel 2006 ha ottenuto "
            "il diploma professionale in strumenti a pizzico del Rinascimento e del Barocco al "
            "Conservatorio di Girona con Xavier Diaz-Latorre."
        ),
        "pedro_bio_2": (
            "Ha poi continuato i suoi studi alla Hochschule für Künste Bremen con Joachim Held "
            "e Lee Santana, perfezionando le sue competenze strumentali con Evangelina Mascardi "
            "in Italia. Ha collaborato con illustri direttori quali Gabriel Garrido, Alessandro "
            "di Marchi, Marco Mencoboni, Paolo Faldi, Riccardo Doni, Horacio Franco, Christoph "
            "Hammer, Carlos Aranzay, Gerhard Oppel, Burak Özdemir e altri, esibendosi in "
            "rinomati festival e rassegne in Italia, Germania, Spagna, Francia, Repubblica Ceca, "
            "Belgio, Paesi Bassi, Brasile e Messico."
        ),
        "hugo_bio_1": (
            "Hugo Miguel de Rodas Sánchez è nato a Città del Messico, dove ha studiato "
            "inizialmente chitarra classica presso la Universidad Nacional Autónoma de México. "
            "Nel 2004 ha vinto il concorso di chitarra Rosa Mística a Curitiba, in Brasile, "
            "prima di rivolgere la sua attenzione agli strumenti a pizzico storici e alla prassi "
            "esecutiva della musica antica. Ha frequentato numerosi corsi di perfezionamento e "
            "nel 2008 è stato invitato dal Freiburger Barockorchester ad approfondire i suoi "
            "studi in Europa."
        ),
        "hugo_bio_2": (
            "Ha poi studiato liuto e chitarra barocca con Lee Santana e Joachim Held alla "
            "Hochschule für Künste Bremen, suonando sotto la direzione di illustri direttori "
            "come Gabriel Garrido con numerosi ensemble e orchestre, tra cui la Deutsche "
            "Kammerphilharmonie Bremen, il Knabenchor Hannover, il Bremer Barockorchester, "
            "l'Orkiestra Historyczna, Holland Baroque e Los Temperamentos, in molti paesi "
            "d'Europa, America Centrale e America del Sud."
        ),
        "programme_heading": "PROGRAMMA",
        "arrangements": "Arrangiamenti di Hugo Miguel de Rodas Sánchez",
        "about": (
            "Due amici e colleghi che per caso sono cresciuti e hanno studiato nello stesso "
            "quartiere e nella stessa università di una delle più grandi città del mondo.\n"
            "Pedro e Hugo condividono non solo il luogo di nascita e l'alma mater, ma anche "
            "la passione per la musica rinascimentale e barocca, e il patrimonio culturale "
            "plasmato da un paese dalla straordinaria ricchezza culturale e musicale: il Messico."
        ),
        "contact_label": "Contatto",
    },
}

PROGRAMME = [
    ("Toccatta Seconda", "J. Hieronimus Kapsberger"),
    ("Romanesca", "Alessandro Piccininni"),
    ("Kapsberger", "J. H. Kapsberger"),
    ("Marizapalos", "Santiago de Murcia"),
    ("Furstamberg", "Santiago de Murcia / Robert de Visèe"),
    ("Las Penas", "Santiago de Murcia"),
    ("Folías Españolas", ""),
    ("Sinfonia", "Francesco Corbetta"),
    ("Passacalles por la E", "S. de Murcia"),
    ("Payssanos", ""),
    ("Folia", "Belerofonte Castaldi"),
    ("Fandango", "S. de Murcia"),
    ("Canarios por la C", "Gaspar Sanz"),
    ("Canarios por la A", "Gaspar Sanz"),
]


def build_html(lang):
    t = TRANSLATIONS[lang]
    b = img_b64("border.png")
    aztec = img_b64("aztec.png")
    lyre = img_b64("lyre.png")
    pedro_photo = img_b64("pedro_photo.jpeg")
    hugo_photo = img_b64("hugo_photo.jpeg")
    baroque_g = img_b64("baroque_guitarist.png")
    guitar_fig = img_b64("guitar_figure.png")
    ensemble = img_b64("ensemble_photo.jpeg")

    instr = t["instruments"]
    prog_rows = "".join(
        f'<tr><td class="piece">{p}</td><td class="composer">{c}</td></tr>'
        for p, c in PROGRAMME
    )

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600&family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400;1,500&display=swap" rel="stylesheet">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html, body {{ width: 297mm; background: {BG}; }}

  @page {{
    size: A4 landscape;
    margin: 0;
  }}

  .page {{
    width: 297mm;
    height: 210mm;
    background: {BG};
    color: {TEXT};
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    page-break-after: always;
    overflow: hidden;
    position: relative;
    padding: 14mm 18mm;
  }}

  /* ── fonts ── */
  .cinzel       {{ font-family: 'Cinzel', serif; letter-spacing: 0.18em; }}
  .cinzel-light {{ font-family: 'Cinzel', serif; letter-spacing: 0.22em; font-weight: 400; }}
  .garamond     {{ font-family: 'Cormorant Garamond', serif; }}

  /* ── border strip ── */
  .border-strip {{
    width: 100%;
    height: 20mm;
    background: url('{b}') center/cover no-repeat;
    flex-shrink: 0;
  }}
  .border-strip.small {{
    height: 14mm;
  }}

  /* ══ PAGE 1: Cover ══ */
  .cover {{
    padding: 0;
    justify-content: space-between;
  }}
  .cover-body {{
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 6mm;
    padding: 4mm 0;
  }}
  .cover-mecatl {{
    font-size: 28pt;
    font-weight: 400;
  }}
  .cover-harmonium {{
    font-size: 62pt;
    font-weight: 400;
    font-style: italic;
    line-height: 1;
    color: {TEXT};
  }}
  .cover-names {{
    font-size: 10pt;
    line-height: 2.2;
    text-align: center;
  }}
  .cover-subtitle {{
    font-size: 8.5pt;
    line-height: 2;
    text-align: center;
    color: {TEXT_DIM};
  }}

  /* ══ PAGE 2: Quote ══ */
  .quote-page {{
    justify-content: center;
    align-items: center;
    text-align: center;
    gap: 10mm;
  }}
  .quote-text {{
    font-size: 14pt;
    line-height: 2.0;
    white-space: pre-line;
  }}
  .quote-attr {{
    font-size: 11pt;
    color: {TEXT_DIM};
    margin-top: 8mm;
  }}
  .ornament {{
    font-size: 28pt;
    color: {TEXT_DIM};
    margin-top: 4mm;
  }}

  /* ══ PAGE 3: MECATL definition ══ */
  .mecatl-def-page {{
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;
    gap: 12mm;
    padding: 18mm 22mm;
  }}
  .mecatl-def-left {{
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }}
  .mecatl-title {{
    font-size: 54pt;
    font-style: italic;
    font-weight: 500;
    line-height: 1;
    margin-bottom: 8mm;
  }}
  .mecatl-def-text {{
    font-size: 14pt;
    line-height: 1.7;
    font-style: italic;
    white-space: pre-line;
  }}
  .mecatl-img {{
    width: 52mm;
    object-fit: contain;
  }}

  /* ══ PAGE 4: HARMONIUM definition ══ */
  .harm-def-page {{
    flex-direction: row;
    justify-content: center;
    align-items: center;
    gap: 14mm;
    padding: 18mm 22mm;
  }}
  .harm-img {{
    width: 48mm;
    object-fit: contain;
  }}
  .harm-right {{
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }}
  .harm-title {{
    font-size: 52pt;
    font-style: italic;
    font-weight: 500;
    line-height: 1;
    margin-bottom: 8mm;
  }}
  .harm-latin {{
    font-size: 14pt;
    line-height: 1.9;
    font-style: italic;
    white-space: pre-line;
  }}

  /* ══ PAGES 5 & 8: Artist profile ══ */
  .artist-page {{
    flex-direction: column;
    padding: 10mm 18mm 8mm;
  }}
  .artist-name {{
    font-size: 22pt;
    text-align: center;
    margin-bottom: 8mm;
    line-height: 1.5;
  }}
  .artist-body {{
    flex: 1;
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 14mm;
  }}
  .artist-instruments {{
    font-size: 11pt;
    line-height: 2.4;
    white-space: pre;
  }}
  .artist-photo {{
    height: 110mm;
    width: auto;
    object-fit: cover;
    border: none;
  }}
  .artist-crest {{
    font-size: 22pt;
    color: {TEXT_DIM};
    margin-top: 6mm;
    text-align: center;
  }}

  /* ══ PAGES 6, 7, 9, 10: Bio text ══ */
  .bio-page {{
    justify-content: center;
    align-items: center;
    padding: 18mm 26mm;
  }}
  .bio-text {{
    font-size: 13.5pt;
    line-height: 1.85;
    text-align: justify;
    font-style: italic;
    hyphens: auto;
  }}

  /* ══ PAGES 11 & 12: Programme ══ */
  .prog-page {{
    flex-direction: column;
    justify-content: flex-start;
    padding: 12mm 18mm 8mm;
  }}
  .prog-heading {{
    font-size: 20pt;
    text-align: center;
    margin-bottom: 8mm;
  }}
  .prog-table {{
    width: 100%;
    border-collapse: collapse;
  }}
  .prog-table td {{
    font-size: 10.5pt;
    padding: 2.8mm 4mm;
    font-family: 'Cinzel', serif;
    letter-spacing: 0.12em;
    color: {TEXT};
  }}
  .prog-table .piece {{
    text-align: left;
    font-weight: 400;
  }}
  .prog-table .composer {{
    text-align: right;
    color: {TEXT_DIM};
    font-size: 9.5pt;
  }}
  .prog-arrangements {{
    font-size: 9pt;
    text-align: center;
    color: {TEXT_DIM};
    margin-top: 6mm;
    letter-spacing: 0.14em;
    font-family: 'Cinzel', serif;
  }}

  /* ══ PAGE 13: Credits ══ */
  .credits-page {{
    flex-direction: column;
    justify-content: space-between;
    padding: 8mm 14mm;
  }}
  .credits-top-crest {{
    text-align: center;
    font-size: 20pt;
    color: {TEXT_DIM};
    margin-bottom: 2mm;
  }}
  .credits-row {{
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    align-items: center;
    flex: 1;
    gap: 10mm;
  }}
  .credit-block {{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4mm;
    flex: 1;
  }}
  .credit-name {{
    font-size: 13pt;
    text-align: center;
    line-height: 1.6;
  }}
  .credit-img {{
    height: 62mm;
    width: auto;
    object-fit: contain;
  }}
  .credit-instruments {{
    font-size: 9.5pt;
    text-align: left;
    line-height: 2.0;
    white-space: pre;
    color: {TEXT_DIM};
  }}
  .credits-side-crests {{
    display: flex;
    justify-content: space-between;
    width: 100%;
    font-size: 20pt;
    color: {TEXT_DIM};
  }}
  .credits-bottom-crest {{
    text-align: center;
    font-size: 20pt;
    color: {TEXT_DIM};
  }}

  /* ══ PAGE 14: Contact ══ */
  .contact-page {{
    flex-direction: row;
    justify-content: center;
    align-items: center;
    gap: 14mm;
    padding: 14mm 20mm;
  }}
  .contact-left {{
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 5mm;
  }}
  .contact-mecatl {{
    font-size: 28pt;
    font-style: italic;
    font-weight: 500;
    line-height: 1;
  }}
  .contact-harmonium {{
    font-size: 24pt;
    font-style: italic;
    font-weight: 500;
    line-height: 1;
  }}
  .contact-about {{
    font-size: 9pt;
    line-height: 1.75;
    text-align: left;
    white-space: pre-line;
    margin-top: 3mm;
    font-family: 'Cinzel', serif;
    letter-spacing: 0.08em;
    color: {TEXT};
    font-weight: 400;
  }}
  .contact-info {{
    margin-top: 4mm;
    font-size: 9pt;
    line-height: 2.0;
    font-family: 'Cinzel', serif;
    letter-spacing: 0.10em;
    color: {TEXT_DIM};
  }}
  .contact-label {{
    font-size: 10pt;
    letter-spacing: 0.20em;
    margin-bottom: 1mm;
    color: {TEXT_DIM};
  }}
  .contact-crests {{
    display: flex;
    gap: 6mm;
    align-items: center;
    margin-top: 3mm;
  }}
  .ensemble-photo {{
    height: 120mm;
    width: auto;
    object-fit: cover;
  }}
</style>
</head>
<body>

<!-- PAGE 1: Cover -->
<div class="page cover">
  <div class="border-strip"></div>
  <div class="cover-body">
    <div class="cinzel cover-mecatl">M E C A T L</div>
    <div class="garamond cover-harmonium">Harmonium</div>
    <div class="cinzel cover-names">
      P E D R O &nbsp; A L C À C E R &nbsp; D O R I A<br>
      H U G O &nbsp; M I G U E L &nbsp; D E &nbsp; R O D A S &nbsp; S Á N C H E Z
    </div>
    <div class="cinzel cover-subtitle">{t["subtitle"]}</div>
  </div>
  <div class="border-strip"></div>
</div>

<!-- PAGE 2: Quote -->
<div class="page quote-page">
  <div class="cinzel quote-text">{t["quote"]}</div>
  <div class="cinzel quote-attr">G A S P A R &nbsp; S A N Z , &nbsp; 1 6 9 2</div>
  <div class="ornament">⚜</div>
</div>

<!-- PAGE 3: MECATL definition -->
<div class="page mecatl-def-page">
  <div class="mecatl-def-left">
    <div class="garamond mecatl-title">MECATL</div>
    <div class="garamond mecatl-def-text">{t["mecatl_def"]}</div>
  </div>
  <img class="mecatl-img" src="{aztec}" alt="">
</div>

<!-- PAGE 4: HARMONIUM definition -->
<div class="page harm-def-page">
  <img class="harm-img" src="{lyre}" alt="">
  <div class="harm-right">
    <div class="garamond harm-title">HARMONIUM</div>
    <div class="garamond harm-latin">{t["harm_latin"]}</div>
  </div>
</div>

<!-- PAGE 5: Pedro artist -->
<div class="page artist-page">
  <div class="cinzel artist-name">
    P E D R O &nbsp; A L C À C E R<br>D O R I A
  </div>
  <div class="artist-body">
    <div>
      <div class="cinzel-light artist-instruments">{chr(10).join(instr[0:3])}</div>
      <div class="artist-crest">⚜</div>
    </div>
    <img class="artist-photo" src="{pedro_photo}" alt="">
  </div>
</div>

<!-- PAGE 6: Pedro bio 1 -->
<div class="page bio-page">
  <div class="garamond bio-text">{t["pedro_bio_1"]}</div>
</div>

<!-- PAGE 7: Pedro bio 2 -->
<div class="page bio-page">
  <div class="garamond bio-text">{t["pedro_bio_2"]}</div>
</div>

<!-- PAGE 8: Hugo artist -->
<div class="page artist-page">
  <div class="cinzel artist-name">
    H U G O &nbsp; M I G U E L<br>D E &nbsp; R O D A S &nbsp; S Á N C H E Z
  </div>
  <div class="artist-body">
    <img class="artist-photo" src="{hugo_photo}" alt="">
    <div>
      <div class="cinzel-light artist-instruments">{chr(10).join(instr[0:3])}</div>
      <div class="artist-crest">⚜</div>
    </div>
  </div>
</div>

<!-- PAGE 9: Hugo bio 1 -->
<div class="page bio-page">
  <div class="garamond bio-text">{t["hugo_bio_1"]}</div>
</div>

<!-- PAGE 10: Hugo bio 2 -->
<div class="page bio-page">
  <div class="garamond bio-text">{t["hugo_bio_2"]}</div>
</div>

<!-- PAGE 11: Programme part 1 -->
<div class="page prog-page">
  <div class="cinzel prog-heading">{t["programme_heading"]}</div>
  <table class="prog-table">
    {prog_rows[:prog_rows.find("</tr>", prog_rows.find("Fandango")) + 5]}
  </table>
</div>

<!-- PAGE 12: Programme part 2 + arrangements -->
<div class="page prog-page" style="justify-content:center;">
  <table class="prog-table">
    {prog_rows[prog_rows.find("<tr><td class=\"piece\">Fandango"):]}</table>
  <div class="cinzel prog-arrangements">{t["arrangements"]}</div>
</div>

<!-- PAGE 13: Credits -->
<div class="page credits-page">
  <div class="credits-top-crest cinzel">⚜</div>
  <div class="credits-row">
    <div class="credit-block">
      <div class="cinzel credit-name">P E D R O &nbsp; A L C À C E R &nbsp; D O R I A</div>
      <img class="credit-img" src="{baroque_g}" alt="">
      <div class="cinzel credit-instruments">{chr(10).join(instr)}</div>
    </div>
    <div class="credit-block">
      <div class="cinzel credit-name">H U G O &nbsp; M I G U E L &nbsp; D E &nbsp; R O D A S<br>S Á N C H E Z</div>
      <img class="credit-img" src="{guitar_fig}" alt="">
      <div class="cinzel credit-instruments">{chr(10).join(instr)}</div>
    </div>
  </div>
  <div class="credits-bottom-crest cinzel">⚜</div>
</div>

<!-- PAGE 14: Contact -->
<div class="page contact-page">
  <div class="contact-left">
    <div class="garamond contact-mecatl">MECATL</div>
    <div class="garamond contact-harmonium">HARMONIUM</div>
    <div class="contact-about">{t["about"]}</div>
    <div class="contact-info">
      <div class="cinzel contact-label">{t["contact_label"]}</div>
      Hugo Miguel de Rodas &nbsp; canticvm@gmail.com<br>
      Pedro Alcàcer Doria &nbsp; palcacer@gmail.com
    </div>
  </div>
  <img class="ensemble-photo" src="{ensemble}" alt="">
</div>

</body>
</html>"""


async def generate(lang):
    html = build_html(lang)
    html_path = OUT / f"mecatl_{lang}.html"
    pdf_path = OUT / f"mecatl_{lang}.pdf"
    html_path.write_text(html, encoding="utf-8")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(f"file://{html_path}", wait_until="networkidle", timeout=30000)
        await page.pdf(
            path=str(pdf_path),
            format="A4",
            landscape=True,
            print_background=True,
        )
        await browser.close()
    print(f"✓ {lang}: {pdf_path}")


async def main():
    for lang in ["en", "es", "ca", "fr", "it"]:
        await generate(lang)


if __name__ == "__main__":
    asyncio.run(main())

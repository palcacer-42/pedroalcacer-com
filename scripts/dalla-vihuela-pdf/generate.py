import asyncio
import base64
import os
from pathlib import Path
from playwright.async_api import async_playwright

OUT = Path(__file__).parent / "output"
OUT.mkdir(exist_ok=True)
ASSETS = Path(__file__).parent / "assets"

def img_b64(name):
    path = ASSETS / name
    if not path.exists(): return ""
    data = path.read_bytes()
    ext = path.suffix.lstrip(".")
    if ext == "jpg":
        ext = "jpeg"
    return f"data:image/{ext};base64,{base64.b64encode(data).decode()}"

BG = "#fdfbf7"
TEXT = "#1a242f"
TEXT_DIM = "#5a6675"
GOLD = "#c5a059"

LANGUAGES = ['en', 'es', 'it', 'fr', 'ca', 'de']
BASE_DIR = '/Users/palcacer/Sites/pedroalcacer-com/static/programs/originals'

DALLA_TEXTS = {
    'it': """Un viaggio attraverso un'epoca in cui la musica non conosceva confini e melodie, strumenti e ritmi viaggiavano tra corti, città e territori, dando vita a un continuo incontro tra culture.\n\nIl percorso parte dalla vihuela de mano, lo strumento che più di ogni altro rappresenta il Siglo de Oro della cultura musicale spagnola. Tra le mani di musicisti come Luís de Milán, Alonso Mudarra e Diego Pisador, la vihuela raggiunse una straordinaria capacità espressiva, trasformandosi in uno strumento capace di racchiudere nelle proprie corde la complessità della polifonia vocale e, allo stesso tempo, la delicatezza della poesia.\n\nIl repertorio vihuelistico costituisce uno dei tesori più preziosi del Rinascimento iberico. Le sette principali raccolte pubblicate tra il 1536 e il 1576 raccontano una civiltà musicale raffinatissima, nella quale la fantasia, l'improvvisazione e la pratica strumentale erano parte integrante dell'esperienza musicale.\n\nAccanto alla vihuela, il programma conduce verso l'Italia e verso la chitarra barocca, lo strumento che all'inizio del Seicento iniziò progressivamente a sostituire la vihuela, portando con sé un nuovo linguaggio fatto di ritmi, armonie e virtuosismo. Le percussioni storiche completano questo universo sonoro, riportando in primo piano la dimensione della danza, del ritmo e dell'improvvisazione.\n\nIl dialogo tra Spagna e Italia è al centro dell'intero progetto. Già nel Cinquecento musicisti e repertori attraversavano continuamente il Mediterraneo e le corti europee. La Calata alla Spagnola di Joan Ambrosio Dalza, pubblicata a Venezia nel 1508, ne è una testimonianza emblematica: una musica italiana che guarda alla Spagna e una Spagna che, attraverso la musica, entra profondamente nella cultura italiana.\n\nVihuela, chitarra barocca e percussioni si incontrano così in un concerto che restituisce al pubblico non soltanto le musiche del passato, ma il loro carattere più vivo e sorprendente.\n\nPerché ciò che è arrivato fino a noi è soltanto una parte di ciò che realmente doveva essere suonato. Molta musica non veniva scritta: veniva improvvisata, ornata, trasformata e tramandata attraverso l'ascolto.\n\nEd è proprio in questo spazio tra ciò che è scritto e ciò che possiamo ancora immaginare che nasce il fascino di questo progetto: un nuovo ascolto di un mondo antico, fatto di corde, pelli, voci, danze e improvvisazione.""",
    
    'en': """A journey through an era when music knew no borders and melodies, instruments and rhythms travelled between courts, cities and territories, giving life to a continuous encounter between cultures.\n\nThe journey starts with the vihuela de mano, the instrument that more than any other represents the Siglo de Oro of Spanish musical culture. In the hands of musicians such as Luís de Milán, Alonso Mudarra and Diego Pisador, the vihuela reached an extraordinary expressive capacity, transforming into an instrument capable of encapsulating within its strings the complexity of vocal polyphony and, at the same time, the delicacy of poetry.\n\nThe vihuela repertoire constitutes one of the most precious treasures of the Iberian Renaissance. The seven main collections published between 1536 and 1576 recount a highly refined musical civilization, in which fantasy, improvisation and instrumental practice were an integral part of the musical experience.\n\nAlongside the vihuela, the program leads towards Italy and towards the baroque guitar, the instrument that at the beginning of the seventeenth century progressively began to replace the vihuela, bringing with it a new language made of rhythms, harmonies and virtuosity. Historical percussion completes this sonic universe, bringing the dimension of dance, rhythm and improvisation to the forefront.\n\nThe dialogue between Spain and Italy is at the center of the entire project. Already in the sixteenth century, musicians and repertoires continually crossed the Mediterranean and European courts. The Calata alla Spagnola by Joan Ambrosio Dalza, published in Venice in 1508, is an emblematic testimony of this: an Italian music that looks to Spain and a Spain that, through music, enters deeply into Italian culture.\n\nVihuela, baroque guitar and percussion thus meet in a concert that restores to the public not only the music of the past, but its most vivid and surprising character.\n\nBecause what has come down to us is only a part of what was actually meant to be played. Much music was not written down: it was improvised, ornamented, transformed and handed down by ear.\n\nAnd it is precisely in this space between what is written and what we can still imagine that the fascination of this project is born: a new listening to an ancient world, made of strings, skins, voices, dances and improvisation.""",

    'es': """Un viaje a través de una época en la que la música no conocía fronteras y melodías, instrumentos y ritmos viajaban entre cortes, ciudades y territorios, dando vida a un continuo encuentro entre culturas.\n\nEl recorrido parte de la vihuela de mano, el instrumento que más que ningún otro representa el Siglo de Oro de la cultura musical española. En manos de músicos como Luís de Milán, Alonso Mudarra y Diego Pisador, la vihuela alcanzó una extraordinaria capacidad expresiva, transformándose en un instrumento capaz de encerrar en sus cuerdas la complejidad de la polifonía vocal y, al mismo tiempo, la delicadeza de la poesía.\n\nEl repertorio vihuelístico constituye uno de los tesoros más preciados del Renacimiento ibérico. Las siete colecciones principales publicadas entre 1536 y 1576 relatan una civilización musical muy refinada, en la que la fantasía, la improvisación y la práctica instrumental eran parte integral de la experiencia musical.\n\nJunto a la vihuela, el programa conduce hacia Italia y hacia la guitarra barroca, el instrumento que a principios del siglo XVII comenzó progresivamente a sustituir a la vihuela, trayendo consigo un nuevo lenguaje hecho de ritmos, armonías y virtuosismo. La percusión histórica completa este universo sonoro, trayendo a primer plano la dimensión de la danza, el ritmo y la improvisación.\n\nEl diálogo entre España e Italia está en el centro de todo el proyecto. Ya en el siglo XVI, músicos y repertorios cruzaban continuamente el Mediterráneo y las cortes europeas. La Calata alla Spagnola de Joan Ambrosio Dalza, publicada en Venecia en 1508, es un testimonio emblemático de ello: una música italiana que mira a España y una España que, a través de la música, se adentra profundamente en la cultura italiana.\n\nVihuela, guitarra barroca y percusión se encuentran así en un concierto que devuelve al público no solo las músicas del pasado, sino su carácter más vivo y sorprendente.\n\nPorque lo que ha llegado hasta nosotros es solo una parte de lo que realmente se debía tocar. Mucha música no se escribía: se improvisaba, se ornamentaba, se transformaba y se transmitía de oído.\n\nY es precisamente en este espacio entre lo que está escrito y lo que aún podemos imaginar donde nace la fascinación de este proyecto: una nueva escucha de un mundo antiguo, hecho de cuerdas, pieles, voces, danzas e improvisación.""",

    'fr': """Un voyage à travers une époque où la musique ne connaissait pas de frontières et où mélodies, instruments et rythmes voyageaient entre les cours, les villes et les territoires, donnant vie à une rencontre continue entre les cultures.\n\nLe parcours commence par la vihuela de mano, l'instrument qui représente plus que tout autre le Siècle d'Or de la culture musicale espagnole. Entre les mains de musiciens tels que Luís de Milán, Alonso Mudarra et Diego Pisador, la vihuela a atteint une capacité expressive extraordinaire, se transformant en un instrument capable d'enfermer dans ses cordes la complexité de la polyphonie vocale et, en même temps, la délicadeza de la poésie.\n\nLe répertoire pour vihuela constitue l'un des trésors les plus précieux de la Renaissance ibérique. Les sept principaux recueils publiés entre 1536 et 1576 racontent une civilisation musicale très raffinée, dans laquelle la fantaisie, l'improvisation et la pratique instrumentale faisaient partie intégrante de l'expérience musicale.\n\nAux côtés de la vihuela, le programme nous conduit vers l'Italie et vers la guitare baroque, l'instrument qui, au début du XVIIe siècle, a progressivement commencé à remplacer la vihuela, apportant avec lui un nouveau langage fait de rythmes, d'harmonies et de virtuosité. Les percussions historiques complètent cet univers sonore, ramenant au premier plan la dimension de la danse, du rythme et de l'improvisation.\n\nLe dialogue entre l'Espagne et l'Italie est au centre de tout le projet. Déjà au XVIe siècle, musiciens et répertoires traversaient continuellement la Méditerranée et les cours européennes. La Calata alla Spagnola de Joan Ambrosio Dalza, publiée à Venise en 1508, en est un témoignage emblématique: une musique italienne qui regarde vers l'Espagne et une Espagne qui, à travers la musique, pénètre profondément la culture italienne.\n\nVihuela, guitare baroque et percussions se rencontrent ainsi dans un concert qui restitue au public non seulement les musiques du passé, mais aussi leur caractère le plus vivant et surprenant.\n\nParce que ce qui nous est parvenu n'est qu'une partie de ce qui devait réellement être joué. Beaucoup de musique n'était pas écrite : elle était improvisée, ornée, transformée et transmise par l'écoute.\n\nEt c'est précisément dans cet espace entre ce qui est écrit et ce que nous pouvons encore imaginer que naît la fascination de ce projet : une nouvelle écoute d'un monde ancien, fait de cordes, de peaux, de voix, de danses et d'improvisation.""",

    'ca': """Un viatge a través d'una època en què la música no coneixia fronteres i melodies, instruments i ritmes viatjaven entre corts, ciutats i territoris, donant vida a una trobada contínua entre cultures.\n\nEl recorregut parteix de la vihuela de mà, l'instrument que més que cap altre representa el Segle d'Or de la cultura musical espanyola. En mans de músics com Luís de Milán, Alonso Mudarra i Diego Pisador, la vihuela va assolir una extraordinària capacitat expressiva, transformant-se en un instrument capaç de tancar en les seves cordes la complexitat de la polifonia vocal i, al mateix temps, la delicadesa de la poesia.\n\nEl repertori vihuelístic constitueix un dels tresors més preuats del Renaixement ibèric. Les set col·leccions principals publicades entre 1536 i 1576 relaten una civilització musical molt refinada, en la qual la fantasia, la improvisació i la pràctica instrumental eren part integral de l'experiència musical.\n\nAl costat de la vihuela, el programa condueix cap a Itàlia i cap a la guitarra barroca, l'instrument que a principis del segle XVII va començar progressivament a substituir la vihuela, portant amb si un nou llenguatge fet de ritmes, harmonies i virtuosisme. La percussió històrica completa aquest univers sonor, portant a primer pla la dimensió de la dansa, el ritme i la improvisació.\n\nEl diàleg entre Espanya i Itàlia està al centre de tot el projecte. Ja al segle XVI, músics i repertoris creuaven contínuament la Mediterrània i les corts europees. La Calata alla Spagnola de Joan Ambrosio Dalza, publicada a Venècia el 1508, n'és un testimoni emblemàtic: una música italiana que mira a Espanya i una Espanya que, a través de la música, s'endinsa profundament en la cultura italiana.\n\nVihuela, guitarra barroca i percussió es troben així en un concert que retorna al públic no només les músiques del passat, sinó el seu caràcter més viu i sorprenent.\n\nPerquè el que ha arribat fins a nosaltres és només una part del que realment s'havia de tocar. Molta música no s'escrivia: s'improvisava, s'ornamentava, es transformava i es transmetia d'oïda.\n\nI és precisament en aquest espai entre el que està escrit i el que encara podem imaginar on neix la fascinació d'aquest projecte: una nova escolta d'un món antic, fet de cordes, pells, veus, danses i improvisació.""",

    'de': """Eine Reise durch eine Epoche, in der die Musik keine Grenzen kannte und Melodien, Instrumente und Rhythmen zwischen Höfen, Städten und Territorien reisten und so zu einer ständigen Begegnung der Kulturen führten.\n\nDie Reise beginnt mit der Vihuela de mano, dem Instrument, das wie kein anderes das Siglo de Oro der spanischen Musikkultur repräsentiert. In den Händen von Musikern wie Luís de Milán, Alonso Mudarra und Diego Pisador erreichte die Vihuela eine außergewöhnliche Ausdruckskraft und verwandelte sich in ein Instrument, das in der Lage ist, die Komplexität der Vokalpolyphonie und gleichzeitig die Zartheit der Poesie in seinen Saiten einzufangen.\n\nDas Vihuela-Repertoire stellt einen der kostbarsten Schätze der iberischen Renaissance dar. Die sieben wichtigsten Sammlungen, die zwischen 1536 und 1576 veröffentlicht wurden, erzählen von einer hochkultivierten Musikkultur, in der Fantasie, Improvisation und Instrumentalpraxis ein wesentlicher Bestandteil des musikalischen Erlebens waren.\n\nNeben der Vihuela führt das Programm nach Italien und zur Barockgitarre, dem Instrument, das zu Beginn des 17. Jahrhunderts allmählich begann, die Vihuela zu ersetzen, und das eine neue Sprache aus Rhythmen, Harmonien und Virtuosität mitbrachte. Historische Perkussion vervollständigt dieses Klanguniversum und rückt die Dimension von Tanz, Rhythmus und Improvisation in den Vordergrund.\n\nDer Dialog zwischen Spanien und Italien steht im Mittelpunkt des gesamten Projekts. Bereits im 16. Jahrhundert durchquerten Musiker und Repertoires kontinuierlich das Mittelmeer und die europäischen Höfe. Die Calata alla Spagnola von Joan Ambrosio Dalza, veröffentlicht 1508 in Venedig, ist ein emblematisches Zeugnis dafür: eine italienische Musik, die nach Spanien blickt, und ein Spanien, das durch die Musik tief in die italienische Kultur eindringt.\n\nVihuela, Barockgitarre und Perkussion treffen so in einem Konzert aufeinander, das dem Publikum nicht nur die Musik der Vergangenheit, sondern auch ihren lebendigsten und überraschendsten Charakter zurückgibt.\n\nDenn was auf uns gekommen ist, ist nur ein Teil dessen, was eigentlich gespielt werden sollte. Viel Musik wurde nicht aufgeschrieben: sie wurde improvisiert, verziert, umgewandelt und durch Zuhören weitergegeben.\n\nUnd genau in diesem Raum zwischen dem Geschriebenen und dem, was wir uns noch vorstellen können, entsteht die Faszination dieses Projekts: ein neues Hören einer alten Welt, gemacht aus Saiten, Fellen, Stimmen, Tänzen und Improvisation."""
}

PEDRO_BIO = {
    'en': "Born in 1982 in Mexico City, he began his musical education early under the influence of his father, the Catalan jazz musician Francesc Alcàcer, and grew up in a creative family. He studied jazz guitar with Francisco Lelo de la Rea and soon began learning classical guitar and composition with Héctor Ramos. He completed his classical guitar studies at the renowned \"Escuela Nacional de Música-UNAM\" and continued with prominent teachers such as Isabelle Villei, Eloy Cruz and Antonio Corona, specializing in the Renaissance and Baroque repertoire. In 2006 he moved to Barcelona, Spain, where he obtained his professional title for Renaissance and Baroque string instruments at the Girona Conservatory with the renowned teacher Xavier Diaz-Latorre. He then continued his studies at the Hochschule für Künste in Bremen, where he studied lute with Joachim Held and Lee Santana and obtained his diploma. As a passionate musician, he continued his instrumental perfection with Evangelina Mascardi in Italy, working intensely as a soloist and continuo player. He has collaborated with important conductors such as Gabriel Garrido, Alessandro di Marchi, Marco Mencoboni, Paolo Faldi, Riccardo Doni, Horacio Franco, Cristoph Hammer, Carlos Aranzay, Gerhard Oppel, Burak Özdemir and others, performing in prestigious festivals and forums in Italy, Germany, Spain, France, Czech Republic, Belgium, Netherlands, Brazil and Mexico. He currently lives in Berlin and collaborates with various early music ensembles in Europe. The artist is known for his profound experience and artistic sensitivity, developed through collaboration with prominent musicians and teachers from around the world. His international experience and high qualifications make him an exceptional artist in his field.",
    'es': "Nacido en 1982 en la Ciudad de México, comenzó su formación musical tempranamente bajo la influencia de su padre, el músico de jazz catalán Francesc Alcàcer, y creció en una familia creativa. Estudió guitarra de jazz con Francisco Lelo de la Rea y pronto comenzó a aprender guitarra clásica y composición con Héctor Ramos. Completó sus estudios de guitarra clásica en la reconocida \"Escuela Nacional de Música-UNAM\" y continuó con destacados profesores como Isabelle Villei, Eloy Cruz y Antonio Corona, especializándose en el repertorio renacentista y barroco. En 2006 se trasladó a Barcelona, España, donde obtuvo su título profesional de instrumentos de cuerda del Renacimiento y del Barroco en el Conservatorio de Girona con el reconocido profesor Xavier Diaz-Latorre. Luego continuó sus estudios en la Hochschule für Künste de Bremen, donde estudió laúd con Joachim Held y Lee Santana y obtuvo su diploma. Como músico apasionado, continuó su perfeccionamiento instrumental con Evangelina Mascardi en Italia, trabajando intensamente como solista y continuista. Ha colaborado con importantes directores como Gabriel Garrido, Alessandro di Marchi, Marco Mencoboni, Paolo Faldi, Riccardo Doni, Horacio Franco, Cristoph Hammer, Carlos Aranzay, Gerhard Oppel, Burak Özdemir y otros, presentándose en prestigiosos festivales y foros en Italia, Alemania, España, Francia, República Checa, Bélgica, Países Bajos, Brasil y México. Actualmente vive en Berlín y colabora con diversos conjuntos de música antigua en Europa. El artista es conocido por su profunda experiencia y sensibilidad artística, desarrolladas a través de la colaboración con destacados músicos y profesores de todo el mundo. Su experiencia internacional y sus altas cualificaciones lo convierten en un artista excepcional en su campo.",
    'it': "Nato nel 1982 a Città del Messico, ha iniziato precocemente la sua formazione musicale sotto l'influenza del padre, il musicista jazz catalano Francesc Alcàcer, ed è cresciuto in una famiglia creativa. Ha studiato chitarra jazz con Francisco Lelo de la Rea e ha subito iniziato ad apprendere chitarra classica e composizione con Héctor Ramos. Ha completato gli studi di chitarra classica presso la rinomata “Escuela Nacional de Música-UNAM” e ha proseguito con insegnanti di spicco come Isabelle Villei, Eloy Cruz e Antonio Corona, specializzandosi nel repertorio rinascimentale e barocco. Nel 2006 si trasferisce a Barcellona, in Spagna, dove ottiene il titolo professionale per gli strumenti a corde del Rinascimento e del Barocco al Conservatorio di Girona con il rinomato insegnante Xavier Diaz-Latorre. In seguito prosegue gli studi presso la Hochschule für Künste di Brema, dove studia liuto con Joachim Held e Lee Santana e ottiene il diploma. Come musicista appassionato, ha proseguito il suo perfezionamento strumentale con Evangelina Mascardi in Italia, lavorando intensamente come solista e continuista. Ha collaborato con direttori importanti come Gabriel Garrido, Alessandro di Marchi, Marco Mencoboni, Paolo Faldi, Riccardo Doni, Horacio Franco, Cristoph Hammer, Carlos Aranzay, Gerhard Oppel, Burak Özdemir e altri, esibendosi in prestigiosi festival e forum in Italia, Germania, Spagna, Francia, Repubblica Ceca, Belgio, Paesi Bassi, Brasile e Messico. Attualmente vive a Berlino e collabora con diverse realtà della musica antica in Europa. L'artista è conosciuto per la sua profonda esperienza e sensibilità artistica, maturate grazie alla collaborazione con musicisti e insegnanti di spicco di tutto il mondo. La sua esperienza internazionale e le sue alte qualifiche lo rendono un artista eccezionale nel suo campo.",
    'fr': "Né en 1982 à Mexico, il a commencé sa formation musicale très tôt sous l'influence de son père, le musicien de jazz catalan Francesc Alcàcer, et a grandi dans une famille créative. Il étudie la guitare jazz avec Francisco Lelo de la Rea et commence très vite l'apprentissage de la guitare classique et de la composition avec Héctor Ramos. Il a terminé ses études de guitare classique à la célèbre \"Escuela Nacional de Música-UNAM\" et a continué avec des professeurs éminents tels qu'Isabelle Villei, Eloy Cruz et Antonio Corona, se spécialisant dans le répertoire de la Renaissance et du Baroque. En 2006, il s'installe à Barcelone, en Espagne, où il obtient son titre professionnel pour les instruments à cordes de la Renaissance et du Baroque au Conservatoire de Gérone avec le célèbre professeur Xavier Diaz-Latorre. Il a ensuite poursuivi ses études à la Hochschule für Künste de Brême, où il a étudié le luth avec Joachim Held et Lee Santana et a obtenu son diplôme. En tant que musicien passionné, il a poursuivi son perfectionnement instrumental avec Evangelina Mascardi en Italie, travaillant intensément comme soliste et continuiste. Il a collaboré avec des chefs d'orchestre importants tels que Gabriel Garrido, Alessandro di Marchi, Marco Mencoboni, Paolo Faldi, Riccardo Doni, Horacio Franco, Cristoph Hammer, Carlos Aranzay, Gerhard Oppel, Burak Özdemir et d'autres, se produisant dans des festivals et forums prestigieux en Italie, Allemagne, Espagne, France, République tchèque, Belgique, Pays-Bas, Brésil et Mexique. Il vit actuellement à Berlin et collabore avec divers ensembles de musique ancienne en Europe. L'artiste est connu pour sa profonde expérience et sa sensibilité artistique, développées grâce à la collaboration avec des musiciens et des professeurs éminents du monde entier. Son expérience internationale et ses hautes qualifications font de lui un artiste exceptionnel dans son domaine.",
    'ca': "Nascut el 1982 a la Ciutat de Mèxic, va començar la seva formació musical d'hora sota la influència del seu pare, el músic de jazz català Francesc Alcàcer, i va créixer en una família creativa. Va estudiar guitarra de jazz amb Francisco Lelo de la Rea i aviat va començar a aprendre guitarra clàssica i composició amb Héctor Ramos. Va completar els seus estudis de guitarra clàssica a la reconeguda \"Escuela Nacional de Música-UNAM\" i va continuar amb professors destacats com Isabelle Villei, Eloy Cruz i Antonio Corona, especialitzant-se en el repertori renaixentista i barroc. El 2006 es va traslladar a Barcelona, Espanya, on va obtenir el seu títol professional d'instruments de corda del Renaixement i del Barroc al Conservatori de Girona amb el reconegut professor Xavier Diaz-Latorre. Després va continuar els seus estudis a la Hochschule für Künste de Bremen, on va estudiar llaüt amb Joachim Held i Lee Santana i va obtenir el seu diploma. Com a músic apassionat, va continuar el seu perfeccionament instrumental amb Evangelina Mascardi a Itàlia, treballant intensament com a solista i continuista. Ha col·laborat amb importants directors com Gabriel Garrido, Alessandro di Marchi, Marco Mencoboni, Paolo Faldi, Riccardo Doni, Horacio Franco, Cristoph Hammer, Carlos Aranzay, Gerhard Oppel, Burak Özdemir i altres, actuant en prestigiosos festivals i fòrums a Itàlia, Alemanya, Espanya, França, República Txeca, Bèlgica, Països Baixos, Brasil i Mèxic. Actualment viu a Berlín i col·labora amb diversos conjunts de música antiga a Europa. L'artista és conegut per la seva profunda experiència i sensibilitat artística, desenvolupades a través de la col·laboració amb destacats músics i professors d'arreu del món. La seva experiència internacional i les seves altes qualificacions el converteixen en un artista excepcional en el seu camp.",
    'de': "Geboren 1982 in Mexiko-Stadt, begann er seine musikalische Ausbildung früh unter dem Einfluss seines Vaters, des katalanischen Jazzmusikers Francesc Alcàcer, und wuchs in einer kreativen Familie auf. Er studierte Jazzgitarre bei Francisco Lelo de la Rea und begann bald, klassische Gitarre und Komposition bei Héctor Ramos zu lernen. Er schloss sein Studium der klassischen Gitarre an der renommierten \"Escuela Nacional de Música-UNAM\" ab und setzte es bei prominenten Lehrern wie Isabelle Villei, Eloy Cruz und Antonio Corona fort, wobei er sich auf das Renaissance- und Barockrepertoire spezialisierte. 2006 zog er nach Barcelona, Spanien, wo er am Konservatorium von Girona bei dem renommierten Lehrer Xavier Diaz-Latorre seinen professionellen Titel für Renaissance- und Barock-Streichinstrumente erhielt. Anschließend setzte er sein Studium an der Hochschule für Künste in Bremen fort, wo er Laute bei Joachim Held und Lee Santana studierte und sein Diplom erhielt. Als leidenschaftlicher Musiker setzte er seine instrumentale Perfektionierung bei Evangelina Mascardi in Italien fort und arbeitete intensiv als Solist und Continuospieler. Er hat mit wichtigen Dirigenten wie Gabriel Garrido, Alessandro di Marchi, Marco Mencoboni, Paolo Faldi, Riccardo Doni, Horacio Franco, Cristoph Hammer, Carlos Aranzay, Gerhard Oppel, Burak Özdemir und anderen zusammengearbeitet und ist bei renommierten Festivals und Foren in Italien, Deutschland, Spanien, Frankreich, Tschechien, Belgien, Niederlanden, Brasilien und Mexiko aufgetreten. Derzeit lebt er in Berlin und arbeitet mit verschiedenen Ensembles für Alte Musik in Europa zusammen. Der Künstler ist bekannt für seine profunde Erfahrung und künstlerische Sensibilität, die er durch die Zusammenarbeit mit prominenten Musikern und Lehrern aus der ganzen Welt entwickelt hat. Seine internationale Erfahrung und hohen Qualifikationen machen ihn zu einem außergewöhnlichen Künstler auf seinem Gebiet."
}

MATTEO_BIO = {
    'en': "Specialized in Historical Percussion and Baroque Timpani, born in Genoa on 30/08/1980, he graduated with top marks in Percussion Instruments at the Paganini Conservatory of Genoa with a thesis on Historical Percussion. Since 2006 he has dedicated himself to the study of early music and applied percussion, attending courses and masterclasses with important teachers including Pedro Estevan. He has collaborated, among others, with: Holland Baroque, Bremer Baroque Orchestra, L'Arpeggiata, Les Talens Lyriques, I Talenti Vulcanici, Arte dei Suonatori, Orkiestra Historyczna, La Risonanza, Modo Antiquo, Accademia Degli Astrusi, Wrocław Baroque Orchestra, Academia Montis Regalis, Teatro Carlo Felice, Orchestra Sinfonica G. Verdi of Milan, Symphony Orchestra of Sanremo and others. He has performed in important festivals such as: Handel Festival of Halle, MiTo, Bremen Music Festival, Bach Festival of Leipzig, etc. He has recorded, among others, for Warner, Sony Classical, Dynamic, Tactus and Pentatone. Since 2003 he has also been active as a teacher, holding lessons in music schools and masterclasses. As a collector he owns more than 400 instruments (mainly percussion), ancient and modern, from all over the world.",
    'es': "Especializado en Percusión Histórica y Timbales Barrocos, nacido en Génova el 30/08/1980, se graduó con las más altas calificaciones en Instrumentos de Percusión en el Conservatorio Paganini de Génova con una tesis sobre Percusión Histórica. Desde 2006 se ha dedicado al estudio de la música antigua y la percusión aplicada, asistiendo a cursos y clases magistrales con importantes profesores como Pedro Estevan. Ha colaborado, entre otros, con: Holland Baroque, Bremer Baroque Orchestra, L'Arpeggiata, Les Talens Lyriques, I Talenti Vulcanici, Arte dei Suonatori, Orkiestra Historyczna, La Risonanza, Modo Antiquo, Accademia Degli Astrusi, Wrocław Baroque Orchestra, Academia Montis Regalis, Teatro Carlo Felice, Orchestra Sinfonica G. Verdi de Milán, Orquesta Sinfónica de Sanremo y otros. Ha actuado en importantes festivales como: Festival Handel de Halle, MiTo, Festival de Música de Bremen, Festival Bach de Leipzig, etc. Ha grabado, entre otros, para Warner, Sony Classical, Dynamic, Tactus y Pentatone. Desde 2003 también ha estado activo como profesor, dando clases en escuelas de música y clases magistrales. Como coleccionista posee más de 400 instrumentos (principalmente de percusión), antiguos y modernos, de todo el mundo.",
    'it': "Specializzato in Percussioni Storiche e Timpani Barocchi Nato a Genova il 30/08/1980, si è diplomato a pieni voti in Strumenti a Percussione presso il Conservatorio Paganini di Genova con una tesi sulle Percussioni Storiche. Dal 2006 si dedica allo studio della musica antica e delle percussioni applicate, frequentando corsi e masterclass con importanti docenti tra cui Pedro Estevan. Ha collaborato, tra gli altri, con: Holland Baroque, Bremer Baroque Orchestra, L'Arpeggiata, Les Talens Lyriques, I Talenti Vulcanici, Arte dei Suonatori, Orkiestra Historyczna, La Risonanza, Modo Antiquo, Accademia Degli Astrusi, Wrocław Baroque Orchestra, Academia Montis Regalis, Teatro Carlo Felice, Orchestra Sinfonica G. Verdi di Milano, Orchestra Sinfonica di Sanremo e altri. Si esibito in importanti festival come: Handel Festival di Halle, MiTo, Bremen Music Festival, Bach Festival di Lipsia, ecc. Ha registrato, tra gli altri, per Warner, Sony Classical, Dynamic, Tactus e Pentatone. Dal 2003 è attivo anche come insegnante, tenendo lezioni in scuole di musica e masterclass. Come collezionista possiede più di 400 strumenti (soprattutto percussioni), antichi e moderni, provenienti da tutto il mondo.",
    'fr': "Spécialisé en percussions historiques et timbales baroques, né à Gênes le 30/08/1980, il a obtenu son diplôme avec les meilleures notes en instruments de percussion au Conservatoire Paganini de Gênes avec une thèse sur les percussions historiques. Depuis 2006, il se consacre à l'étude de la musique ancienne et de la percussion appliquée, en suivant des cours et des masterclasses avec des professeurs importants tels que Pedro Estevan. Il a collaboré, entre autres, avec : Holland Baroque, Bremer Baroque Orchestra, L'Arpeggiata, Les Talens Lyriques, I Talenti Vulcanici, Arte dei Suonatori, Orkiestra Historyczna, La Risonanza, Modo Antiquo, Accademia Degli Astrusi, Wrocław Baroque Orchestra, Academia Montis Regalis, Teatro Carlo Felice, Orchestre Symphonique G. Verdi de Milan, Orchestre Symphonique de Sanremo et d'autres. Il s'est produit dans des festivals importants tels que : Festival Haendel de Halle, MiTo, Festival de Musique de Brême, Festival Bach de Leipzig, etc. Il a enregistré, entre autres, pour Warner, Sony Classical, Dynamic, Tactus et Pentatone. Depuis 2003, il est également actif en tant que professeur, donnant des cours dans des écoles de musique et des masterclasses. En tant que collectionneur, il possède plus de 400 instruments (principalement des percussions), anciens et modernes, du monde entier.",
    'ca': "Especialitzat en Percussió Històrica i Timbales Barroques, nascut a Gènova el 30/08/1980, es va graduar amb les màximes qualificacions en Instruments de Percussió al Conservatori Paganini de Gènova amb una tesi sobre Percussió Històrica. Des del 2006 s'ha dedicat a l'estudi de la música antiga i la percussió aplicada, assistint a cursos i classes magistrals amb importants professors com Pedro Estevan. Ha col·laborat, entre d'altres, amb: Holland Baroque, Bremer Baroque Orchestra, L'Arpeggiata, Les Talens Lyriques, I Talenti Vulcanici, Arte dei Suonatori, Orkiestra Historyczna, La Risonanza, Modo Antiquo, Accademia Degli Astrusi, Wrocław Baroque Orchestra, Academia Montis Regalis, Teatro Carlo Felice, Orquestra Simfònica G. Verdi de Milà, Orquestra Simfònica de Sanremo i d'altres. Ha actuat en importants festivals com: Festival Handel de Halle, MiTo, Festival de Música de Bremen, Festival Bach de Leipzig, etc. Ha gravat, entre d'altres, per a Warner, Sony Classical, Dynamic, Tactus i Pentatone. Des del 2003 també ha estat actiu com a professor, donant classes a escoles de música i classes magistrals. Com a col·leccionista posseeix més de 400 instruments (principalment de percussió), antics i moderns, d'arreu del món.",
    'de': "Spezialisiert auf historische Perkussion und Barockpauken, geboren in Genua am 30.08.1980, schloss er sein Studium der Schlaginstrumente am Paganini-Konservatorium in Genua mit Bestnoten und einer Arbeit über historische Perkussion ab. Seit 2006 widmet er sich dem Studium der Alten Musik und der angewandten Perkussion und besuchte Kurse und Meisterkurse bei bedeutenden Lehrern wie Pedro Estevan. Er arbeitete unter anderem mit: Holland Baroque, Bremer Barockorchester, L'Arpeggiata, Les Talens Lyriques, I Talenti Vulcanici, Arte dei Suonatori, Orkiestra Historyczna, La Risonanza, Modo Antiquo, Accademia Degli Astrusi, Wrocław Barockorchester, Academia Montis Regalis, Teatro Carlo Felice, Sinfonieorchester G. Verdi in Mailand, Sinfonieorchester Sanremo und anderen. Er trat bei wichtigen Festivals auf, wie z. B.: Händel-Festspiele Halle, MiTo, Musikfest Bremen, Bachfest Leipzig usw. Er nahm unter anderem für Warner, Sony Classical, Dynamic, Tactus und Pentatone auf. Seit 2003 ist er auch als Lehrer tätig und gibt Unterricht an Musikschulen und in Meisterkursen. Als Sammler besitzt er mehr als 400 alte und moderne Instrumente (vor allem Schlaginstrumente) aus der ganzen Welt."
}

DALLA_SECTIONS = [
    {'heading': 'Vihuela', 'items': [
        ('Ricercar 3', 'Francesco da Milano (Intabulatura de lauto, Venice 1546)'),
        ('Fantasia para desenvolver las manos', 'Alonso de Mudarra (Sevilla 1546)'),
        ('Vacas', 'Luis de Narzaez (Los seis libros del Delfín, Valladolid 1538)'),
        ('Ricercar 3', 'Marco dall\'Aquila (Intabulatura de lauto, Venice 1546)'),
        ('Romanesca', 'Alonso de Mudarra'),
        ('Mille Regez', 'Luis de Narzaez (Valladolid 1538)'),
        ('Fantasia 7', 'Luis de Narzaez (Valladolid 1538)'),
        ('Pavana 4', 'Luís Milán (El maestro, Valencia 1536)'),
        ('Fantasia 8', 'Alonso de Mudarra (Sevilla 1546)'),
        ('Por otra parte/Romanesca', 'Luis de Narzaez (Valladolid 1538)'),
        ('Baxa de contrapunto', 'Luis de Narzaez (Valladolid 1538)')
    ]},
    {'heading': 'Chitarra (Baroque Guitar)', 'items': [
        ('Preludio, allemanda, giga e burlesca', 'Santiago de Murcia (Passacalles y obras ca.1730)'),
        ('Pasacalle sobre la D', 'Gaspar Sanz (Instrucción para sonar la guitarra, Zaragoza 1674)'),
        ('Marionas', 'Santiago de Murcia (Codice Saldivar ca.1730)'),
        ('Folias Españolas', 'Santiago de Murcia (Codice Saldivar ca.1730)'),
        ('Fangango', 'Santiago de Murcia (Codice Saldivar ca.1730)'),
        ('Canario', 'Gaspar Sanz (Zaragoza 1674)')
    ]}
]

TRANSLATIONS = {
    'en': {'subtitle': 'FROM THE VIHUELA TO THE BAROQUE GUITAR', 'prog': 'PROGRAMME', 'p_title': 'Renaissance Lute & Baroque Guitar', 'm_title': 'Percussion'},
    'es': {'subtitle': 'DE LA VIHUELA A LA GUITARRA BARROCA', 'prog': 'PROGRAMA', 'p_title': 'Laúd Renacentista y Guitarra Barroca', 'm_title': 'Percusión'},
    'it': {'subtitle': 'DALLA VIHUELA ALLA CHITARRA BAROCCA', 'prog': 'PROGRAMMA', 'p_title': 'Liuto rinascimentale e Chitarra barocca', 'm_title': 'Percussioni'},
    'fr': {'subtitle': 'DE LA VIHUELA À LA GUITARE BAROQUE', 'prog': 'PROGRAMME', 'p_title': 'Luth Renaissance et Guitare Baroque', 'm_title': 'Percussions'},
    'ca': {'subtitle': 'DE LA VIHUELA A LA GUITARRA BARROCA', 'prog': 'PROGRAMA', 'p_title': 'Llaüt Renaixentista i Guitarra Barroca', 'm_title': 'Percussió'},
    'de': {'subtitle': 'VON DER VIHUELA ZUR BAROCKGITARRE', 'prog': 'PROGRAMM', 'p_title': 'Renaissance-Laute und Barockgitarre', 'm_title': 'Perkussion'}
}

def build_html(lang):
    t = TRANSLATIONS[lang]
    notes_lines = DALLA_TEXTS[lang].split('\\n\\n')
    notes_html = "".join([f"<p>{line}</p>" for line in notes_lines])

    tracklist_html = ""
    for sec in DALLA_SECTIONS:
        tracklist_html += f'<tr><td colspan="2" class="section-title"><div class="ornament-small">✤</div>{sec["heading"]}<div class="ornament-small">✤</div></td></tr>'
        for piece, comp in sec['items']:
            tracklist_html += f'<tr><td class="piece">{piece}</td><td class="composer">{comp}</td></tr>'

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
    padding: 20mm 25mm;
  }}

  .cinzel {{ font-family: 'Cinzel', serif; letter-spacing: 0.18em; }}
  .garamond {{ font-family: 'Cormorant Garamond', serif; }}

  .border-top, .border-bottom {{
    position: absolute;
    left: 20mm;
    right: 20mm;
    height: 1px;
    background: {GOLD};
  }}
  .border-top {{ top: 15mm; }}
  .border-bottom {{ bottom: 15mm; }}

  /* Cover */
  .cover-title {{ font-size: 48pt; font-weight: 500; text-align: center; color: {TEXT}; line-height: 1.1; margin-bottom: 5mm; }}
  .cover-subtitle {{ font-size: 14pt; letter-spacing: 0.25em; text-align: center; color: {GOLD}; margin-bottom: 25mm; }}
  .cover-names {{ font-size: 13pt; line-height: 2; text-align: center; color: {TEXT_DIM}; }}
  .ornament-large {{ font-size: 30pt; color: {GOLD}; margin: 10mm 0; }}

  /* Notes */
  .notes-page {{ justify-content: flex-start; padding-top: 30mm; }}
  .notes-text {{ font-size: 13.5pt; line-height: 1.8; text-align: justify; columns: 2; column-gap: 15mm; }}
  .notes-text p {{ margin-bottom: 4mm; text-indent: 6mm; }}
  .notes-text p:first-child {{ text-indent: 0; }}

  /* Tracklist */
  .prog-page {{ justify-content: flex-start; padding-top: 20mm; }}
  .prog-heading {{ font-size: 20pt; text-align: center; margin-bottom: 6mm; color: {GOLD}; }}
  .prog-table {{ width: 100%; border-collapse: collapse; margin-top: 4mm; }}
  .prog-table td {{ padding: 2mm 0; }}
  .section-title {{ font-family: 'Cinzel', serif; font-size: 12pt; text-align: center; color: {GOLD}; padding-top: 8mm !important; padding-bottom: 4mm !important; letter-spacing: 0.1em; }}
  .ornament-small {{ display: inline-block; margin: 0 10px; font-size: 10pt; color: {GOLD}; }}
  .piece {{ font-family: 'Cinzel', serif; font-size: 10pt; text-align: left; color: {TEXT}; }}
  .composer {{ font-family: 'Cormorant Garamond', serif; font-size: 11.5pt; font-style: italic; text-align: right; color: {TEXT_DIM}; }}

  /* Bios */
  .bio-page {{ justify-content: flex-start; padding-top: 25mm; }}
  .bio-container {{ display: flex; gap: 15mm; height: 100%; }}
  .bio-col {{ flex: 1; }}
  .bio-name {{ font-family: 'Cinzel', serif; font-size: 16pt; margin-bottom: 2mm; color: {TEXT}; text-align: center; }}
  .bio-title {{ font-family: 'Cormorant Garamond', serif; font-size: 13pt; font-style: italic; color: {GOLD}; margin-bottom: 8mm; text-align: center; }}
  .bio-text {{ font-family: 'Cormorant Garamond', serif; font-size: 11.5pt; line-height: 1.7; text-align: justify; }}
  .ensemble-photo {{ width: 100%; max-height: 70mm; object-fit: cover; margin-top: 10mm; filter: grayscale(100%); }}
  
</style>
</head>
<body>

<!-- PAGE 1: Cover -->
<div class="page cover">
  <div class="border-top"></div>
  <div class="garamond cover-title">Dalla Vihuela<br>alla Chitarra Barocca</div>
  <div class="cinzel cover-subtitle">{t["subtitle"]}</div>
  <div class="ornament-large">⚜</div>
  <div class="cinzel cover-names">
    P E D R O &nbsp; A L C À C E R &nbsp; D O R I A<br>
    M A T T E O &nbsp; R A B O L I N I
  </div>
  <div class="border-bottom"></div>
</div>

<!-- PAGE 2: Notes -->
<div class="page notes-page">
  <div class="border-top"></div>
  <div class="garamond notes-text">
    {notes_html}
  </div>
  <div class="border-bottom"></div>
</div>

<!-- PAGE 3: Tracklist -->
<div class="page prog-page">
  <div class="border-top"></div>
  <div class="cinzel prog-heading">{t["prog"]}</div>
  <table class="prog-table">
    {tracklist_html}
  </table>
  <div class="border-bottom"></div>
</div>

<!-- PAGE 4: Bios -->
<div class="page bio-page">
  <div class="border-top"></div>
  <div class="bio-container">
    <div class="bio-col">
      <div class="bio-name">P E D R O &nbsp; A L C À C E R</div>
      <div class="bio-title">{t["p_title"]}</div>
      <div class="bio-text">{PEDRO_BIO[lang]}</div>
    </div>
    <div class="bio-col">
      <div class="bio-name">M A T T E O &nbsp; R A B O L I N I</div>
      <div class="bio-title">{t["m_title"]}</div>
      <div class="bio-text">{MATTEO_BIO[lang]}</div>
    </div>
  </div>
  <img class="ensemble-photo" src="{img_b64('ensemble.jpg')}" alt="">
  <div class="border-bottom"></div>
</div>

</body>
</html>
"""

async def generate_pdfs():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        for lang in LANGUAGES:
            html = build_html(lang)
            path = OUT / f"dalla-vihuela-alla-chitarra-barocca_{lang}.html"
            path.write_text(html, encoding="utf-8")
            
            pdf_path = BASE_DIR + f"/dalla-vihuela-alla-chitarra-barocca_{lang}.pdf"
            await page.goto(f"file://{path.absolute()}")
            await page.wait_for_timeout(500)
            await page.pdf(
                path=pdf_path,
                format="A4",
                landscape=True,
                print_background=True,
                display_header_footer=False,
                margin={"top": "0", "right": "0", "bottom": "0", "left": "0"}
            )
            print(f"Generated {pdf_path}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(generate_pdfs())

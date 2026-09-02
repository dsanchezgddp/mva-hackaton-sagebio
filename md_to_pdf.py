"""Convierte REPORT.md a PDF con estilo de reporte cientifico.

Usa markdown-it-py para el HTML y Chrome headless para imprimir. No requiere
instalar nada: ambos ya estan en la maquina.

    python scripts/md_to_pdf.py [entrada.md] [salida.pdf]
"""
import subprocess
import sys
from pathlib import Path

from markdown_it import MarkdownIt

RAIZ = Path(__file__).resolve().parent.parent
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

CSS = """
@page { size: A4; margin: 20mm 18mm 20mm 18mm; }

:root {
  --tinta:     #1a1a1a;
  --suave:     #55524d;
  --linea:     #d8d4cc;
  --acento:    #7a2e2e;
  --fondo-cod: #f6f4f0;
}

* { box-sizing: border-box; }

body {
  font-family: "Charter", "Georgia", "Cambria", serif;
  font-size: 10.5pt;
  line-height: 1.55;
  color: var(--tinta);
  margin: 0;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}

/* --- portada --- */
.portada { page-break-after: always; padding-top: 38mm; }
.portada .etiqueta {
  font-family: "Segoe UI", system-ui, sans-serif;
  font-size: 8.5pt; font-weight: 600; letter-spacing: .16em;
  text-transform: uppercase; color: var(--acento); margin-bottom: 10mm;
}
.portada h1 {
  font-size: 25pt; line-height: 1.18; margin: 0 0 8mm; border: 0; padding: 0;
}
.portada .sub {
  font-family: "Segoe UI", system-ui, sans-serif;
  font-size: 11pt; color: var(--suave); margin-bottom: 14mm;
}
.portada .meta {
  border-top: 2px solid var(--tinta); padding-top: 4mm;
  font-family: "Segoe UI", system-ui, sans-serif; font-size: 9pt; color: var(--suave);
}
.portada .meta b { color: var(--tinta); }

/* --- jerarquia --- */
h1, h2, h3, h4 {
  font-family: "Segoe UI", system-ui, sans-serif;
  font-weight: 600; line-height: 1.25; color: var(--tinta);
  page-break-after: avoid;
}
h1 { font-size: 17pt; margin: 0 0 6mm; }
h2 {
  font-size: 13pt; margin: 9mm 0 3.5mm;
  padding-bottom: 1.6mm; border-bottom: 1.5px solid var(--tinta);
}
h3 { font-size: 11pt; margin: 6mm 0 2.5mm; color: var(--acento); }
h4 { font-size: 10pt; margin: 5mm 0 2mm; }

p { margin: 0 0 3.2mm; orphans: 2; widows: 2; }

strong { font-weight: 700; }
em { font-style: italic; }

a { color: var(--acento); text-decoration: none; }

/* --- tablas --- */
table {
  width: 100%; border-collapse: collapse; margin: 4mm 0 5mm;
  font-size: 9pt; page-break-inside: avoid;
}
th {
  font-family: "Segoe UI", system-ui, sans-serif; font-size: 8.5pt;
  font-weight: 600; text-align: left; text-transform: uppercase;
  letter-spacing: .05em; color: var(--suave);
  border-bottom: 1.5px solid var(--tinta); padding: 2mm 2.5mm 1.6mm;
}
td { padding: 1.9mm 2.5mm; border-bottom: .75px solid var(--linea); vertical-align: top; }
tbody tr:last-child td { border-bottom: 1.2px solid var(--tinta); }

/* --- codigo --- */
code {
  font-family: "Cascadia Mono", "Consolas", monospace;
  font-size: 8.8pt; background: var(--fondo-cod);
  padding: .4mm 1.1mm; border-radius: 2px; white-space: nowrap;
}
pre {
  background: var(--fondo-cod); border-left: 2.5px solid var(--linea);
  padding: 3mm 4mm; overflow-x: auto; page-break-inside: avoid;
  font-size: 8.5pt; line-height: 1.45;
}
pre code { background: none; padding: 0; white-space: pre; font-size: inherit; }

/* --- citas / avisos --- */
blockquote {
  margin: 4mm 0; padding: 2.5mm 4mm;
  border-left: 3px solid var(--acento); background: #faf7f4;
  color: var(--suave); font-size: 9.5pt; page-break-inside: avoid;
}
blockquote p:last-child { margin-bottom: 0; }
blockquote strong { color: var(--acento); }

ul, ol { margin: 0 0 3.2mm; padding-left: 6mm; }
li { margin-bottom: 1.4mm; }

hr { border: 0; border-top: .75px solid var(--linea); margin: 7mm 0; }

img { max-width: 100%; }
"""

PORTADA = """
<div class="portada">
  <div class="etiqueta">Rare Disease, Real Kid &middot; MVA Hackathon 2026</div>
  <h1>From Genotype to Drug</h1>
  <div class="sub">An Allele-Specific Repurposing Strategy for
    <em>BUB1B</em>-Related Mosaic Variegated Aneuploidy</div>
  <div class="meta">
    <p><b>Track 2</b> &middot; Drug Repurposing</p>
    <p>Sage Bionetworks &middot; MVA Society &middot; Hugging Face &middot; BEACON</p>
    <p><b>Research hypothesis generation. Not clinical advice.</b><br>
       No patient-identifying information is contained in this report.</p>
  </div>
</div>
"""


def quitar_encabezado(md_texto: str) -> str:
    """Descarta titulo, subtitulo y aviso iniciales: ya van en la portada.

    Corta todo lo anterior a la primera seccion de nivel 2. Si el documento no
    tiene ninguna, lo devuelve intacto.
    """
    lineas = md_texto.splitlines()
    for i, linea in enumerate(lineas):
        if linea.startswith("## "):
            return "\n".join(lineas[i:])
    return md_texto


def construir_html(md_texto: str) -> str:
    md = MarkdownIt("commonmark").enable(["table", "strikethrough"])
    cuerpo = md.render(quitar_encabezado(md_texto))
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        f"<title>MVA Hackathon 2026 — BUB1B</title><style>{CSS}</style>"
        f"</head><body>{PORTADA}{cuerpo}</body></html>"
    )


def main() -> int:
    entrada = Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / "REPORT.md"
    salida = Path(sys.argv[2]) if len(sys.argv) > 2 else RAIZ / "REPORT.pdf"

    if not Path(CHROME).exists():
        print(f"No encuentro Chrome en {CHROME}", file=sys.stderr)
        return 1

    html = construir_html(entrada.read_text(encoding="utf-8"))
    tmp = salida.with_suffix(".render.html")
    tmp.write_text(html, encoding="utf-8")

    cmd = [
        CHROME, "--headless", "--disable-gpu", "--no-sandbox",
        "--no-pdf-header-footer",
        f"--print-to-pdf={salida}",
        tmp.resolve().as_uri(),
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    if not salida.exists():
        print("Chrome no genero el PDF:", res.stderr[-800:], file=sys.stderr)
        return 1

    print(f"OK  {salida}  ({salida.stat().st_size / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

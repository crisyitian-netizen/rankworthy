# Rankworthy

**Skill de SEO y GEO para Claude.** Posiciona tu web en Google, consigue que ChatGPT, los AI Overviews de Google y Perplexity te mencionen, y mide si eso trajo clientes.

## Qué lo hace distinto

- **Primero el negocio.** Cada hallazgo indica qué leads, llamadas o pedidos afecta. Si no mides conversiones, eso es lo primero.
- **Seguro en webs en producción.** Copia de seguridad → aprobación → cambio → registro → revisión programada. Los datos privados (por ejemplo, precios mayoristas) nunca aparecen en páginas, schema ni llms.txt.
- **Evidencia etiquetada.** Cada recomendación lleva `[Google]`, `[Study]`, `[Practice]` o `[Unproven]`. Sin estadísticas inventadas.
- **Sin configuración, datos gratis primero.** Funciona en un chat normal de Claude con Search Console, GA4, PageSpeed y la web en vivo. Los datos de pago son opcionales y cada gasto se presupuesta antes.
- **SEO local y multilingüe.** Flujo completo de Perfil de Empresa de Google y reseñas; responde en tu idioma.
- **Antes y después.** Línea base, un set fijo de prompts de IA y un registro de cambios para saber qué funcionó.

## Herramientas (Python 3, solo librería estándar)

```bash
python3 scripts/site_check.py https://tusitio.cl
python3 scripts/gsc_analyze.py Consultas.csv --brand "tu marca"
python3 scripts/ai_visibility.py init prompts.txt > log.csv
python3 scripts/ai_visibility.py report log.csv
python3 scripts/dataforseo.py volume "palabra clave" --location 2152 --lang es   # opcional, de pago
```

## Instalación / dónde funciona

Es un Agent Skill estándar, no solo para Claude Code:

- **Claude Code**: copia la carpeta en `~/.claude/skills/rankworthy/`. Los scripts corren en local.
- **Apps de Claude (web, escritorio, móvil)**: comprime la carpeta y súbela en Settings → Capabilities → Skills, con ejecución de código activada.
- **Claude API / Agent SDK**: súbela como skill personalizado.
- **Codex, Cursor, Gemini CLI, Copilot, OpenCode** y otros que leen `SKILL.md`: colócala en su carpeta de skills (scripts: Python 3).

Luego pide: *"Audita example.com y dime qué arreglar primero"*.

## Datos de pago (opcional)

Volumen de búsqueda, SERPs, mapas y backlinks vía [DataForSEO](DATAFORSEO_REFERRAL_LINK) (pago por uso). *Aviso de afiliado: el autor puede recibir una comisión si te registras con este enlace; tu precio no cambia. También puedes registrarte directamente en dataforseo.com.*

Licencia MIT.

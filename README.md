# Códigos de Contenedores · aerococina — Setup

PWA (Progressive Web App) que unifica los códigos QR de contenedores de las 8 bodegas en una sola URL. Diseñada para tablets en bodega, con soporte offline después de la primera carga.

## Contenido del paquete

```
06_Codigos_Contenedores_PWA/
├── index.html              ← App principal (todos los códigos en una página)
├── manifest.json           ← PWA manifest (instalable)
├── sw.js                   ← Service Worker (cache offline)
├── icon-192.png            ← Icono PWA 192×192
├── icon-512.png            ← Icono PWA 512×512
├── icon-maskable.png       ← Icono adaptable Android (512×512)
├── apple-touch-icon.png    ← Icono iOS Web Clip (180×180)
├── favicon.png             ← Favicon (32×32)
├── README.md               ← Este archivo
└── qr_bodegas/             ← (FALTA — agregar) Carpeta con PNGs de QR
    ├── X/                  ←   QRs de Mexico City
    ├── N/                  ←   QRs de AIFA
    ├── C/                  ←   QRs de Cancún
    ├── G/                  ←   QRs de Guadalajara
    ├── Y/                  ←   QRs de Mérida
    ├── M/                  ←   QRs de Monterrey
    ├── T/                  ←   QRs de Tijuana
    └── L/                  ←   QRs de Toluca
```

## ⚠️ Pendiente — agregar carpeta `qr_bodegas/`

El HTML referencia imágenes en `qr_bodegas/{LETRA}/{CODIGO}.png` pero esa carpeta NO está incluida en este paquete. Antes de publicar en GitHub Pages, **agrega la carpeta `qr_bodegas/`** con los PNG generados de tus 526 códigos QR.

Mientras la carpeta no exista, el HTML muestra placeholders grises donde irían los QR — el resto de la app funciona normal.

---

## Setup paso a paso

### Paso 1 — Crear repo en GitHub

1. Ve a https://github.com/new
2. Repository name: `aerococina-codigos` (o similar)
3. Visibilidad: **Public** (necesario para GitHub Pages gratis) o Private si tienes plan GitHub Pro
4. Click **Create repository**

### Paso 2 — Subir archivos al repo

**Opción A — GitHub Desktop (GUI, recomendado para no-devs):**

1. Descarga GitHub Desktop: https://desktop.github.com/
2. File > Clone repository > selecciona `aerococina-codigos`
3. Copia TODO el contenido de esta carpeta (`06_Codigos_Contenedores_PWA/`) a la carpeta del repo clonado
4. **Agrega también la carpeta `qr_bodegas/`** con los 526 PNG de QR
5. GitHub Desktop detecta los cambios → Summary: "Initial deploy" → **Commit to main**
6. Click **Push origin**

**Opción B — Web (drag-and-drop, más simple aún):**

1. En el repo recién creado, click **Add file** > **Upload files**
2. Arrastra todos los archivos:
   - index.html
   - manifest.json
   - sw.js
   - icon-192.png, icon-512.png, icon-maskable.png, apple-touch-icon.png, favicon.png
   - **Importante**: arrastra la carpeta `qr_bodegas/` completa también
3. Commit: "Deploy inicial"

### Paso 3 — Activar GitHub Pages

1. En el repo > **Settings** (tab superior)
2. Sidebar izquierdo > **Pages**
3. Source > Branch: **main** > Folder: **/ (root)** > **Save**
4. Espera ~1-2 min. GitHub muestra: "Your site is live at https://[username].github.io/aerococina-codigos/"
5. **Anota esa URL** — es la que pondrás en Hexnode

### Paso 4 — Validar en el navegador

1. Abre la URL en Chrome/Safari en tu teléfono o tablet
2. Verifica:
   - ✅ Cargan las 8 bodegas + Índice
   - ✅ Tabs cambian al tocar
   - ✅ Búsqueda funciona (ej. escribir "C1EX")
   - ✅ Los QR se muestran (si subiste `qr_bodegas/`)
3. Abre DevTools > Application > Service Workers → debe decir "activated and running"

### Paso 5 — Push como Web Clip a las tablets (Hexnode)

1. Hexnode > Policies > **Create new policy**
2. Nombre: `Codigos-Contenedores-WebClip`
3. Android > **Web Clips / Web Shortcuts**:
   - Label: `Códigos`
   - URL: `https://[username].github.io/aerococina-codigos/`
   - Icon: sube `icon-192.png` (o usa la URL de GitHub Pages + /icon-192.png)
   - Display in: **Home screen**
   - Full-screen: ✅ Enabled (modo PWA)
4. Asignar a Device Groups: **PACKING-TABLETS** y/o **WAREHOUSE-TABLETS** según corresponda
5. Save and Publish

Las tablets en bodega van a recibir el icono "Códigos" en su home screen en los próximos minutos.

### Paso 6 — Si las tablets están en Single App Kiosk Mode

Si las tablets están en kiosk con una sola app (ej. MOST Packing), tienes 2 opciones:

**Opción A — Multi-App Kiosk (recomendado)**
- Hexnode > Kiosk > Multi-App Kiosk
- Agrega "Códigos" Web Clip a la lista de apps permitidas
- El operador puede salir de MOST → tocar Códigos → consultar → volver a MOST

**Opción B — Acceso intra-app**
- Si MOST Packing lo permite, inserta el link `https://[username].github.io/aerococina-codigos/` como atajo dentro del menú de MOST
- Más limpio operativamente pero requiere cambio en MOST

---

## Cómo actualizar contenido cuando cambien los códigos

Esto es lo bonito del approach — **NO necesitas tocar Hexnode ni las tablets**.

### Cuando cambian los códigos QR

1. Genera los nuevos QR PNG con tu script habitual
2. Reemplaza los archivos en `qr_bodegas/X/`, `qr_bodegas/N/`, etc. del repo
3. Si cambian códigos o nombres, regenera `index.html` (o edítalo directamente)
4. Git commit + push
5. **GitHub Pages publica en ~1 min**
6. Las tablets recibirán la versión nueva en la próxima conexión a internet (Service Worker valida updates)
7. **Para forzar update inmediato** en una tablet: cierra la app + abre de nuevo

### Versión actual

Edita el `app-footer` en `index.html`:
```html
<span class="ver">v1.1 · jun 2026</span>
```

Y cambia `CACHE_VERSION` en `sw.js` para forzar refresh del cache offline:
```js
const CACHE_VERSION = 'codigos-v2-2026-06-01';
```

---

## Funcionalidades

- ✅ **Una sola URL** con índice + 8 bodegas navegables por tabs
- ✅ **Búsqueda en tiempo real** por código (ej. "C1EX") o nombre (ej. "papas")
- ✅ **Offline después de primera carga** (Service Worker cachea todo)
- ✅ **PWA instalable** — el operador puede "Add to Home Screen"
- ✅ **Recuerda última bodega** vista (localStorage)
- ✅ **Responsive** — funciona en tablets 10", phones, y desktop
- ✅ **Branding aerococina** consistente (navy/steel/warm)
- ✅ **Indicador offline** cuando se cae el Wi-Fi
- ✅ **Sin tracking, sin cookies, sin servidor backend**

## Costos

- GitHub Pages: **$0** (gratis para repos públicos, o con plan GitHub Pro para privados)
- Hosting: **$0**
- Hexnode Web Clip: **$0** (incluido en tu plan)
- Mantenimiento: solo regenerar QRs cuando cambien planes

Total: $0/mes operativo.

## Validación antes de publicar

- [ ] Abrir `index.html` localmente con doble click → ver que cargue
- [ ] Navegar entre tabs → todos funcionan
- [ ] Probar buscar "C1EX" → debería filtrar y mostrar solo ese código
- [ ] Probar buscar "papas" → muestra todos los códigos PA*/P2*
- [ ] Verificar visualmente diseño en tablet (ancho 10")
- [ ] Confirmar carpeta `qr_bodegas/` con los 526 PNG
- [ ] Subir a GitHub → activar Pages → validar URL pública
- [ ] Push Web Clip en Hexnode a 1 tablet de prueba antes de masivo

## Troubleshooting

**Los QR no se ven:**
- Verifica que `qr_bodegas/` esté en el repo
- Los nombres deben ser exactamente: `qr_bodegas/X/C1EX.png` (mayúsculas/minúsculas importan)
- GitHub Pages es case-sensitive

**No funciona offline:**
- Service Worker requiere HTTPS (GitHub Pages ya da HTTPS automático ✅)
- En primera carga, la tablet debe estar online para descargar y cachear
- Verifica en DevTools > Application > Service Workers

**Cambios no aparecen en la tablet:**
- Service Worker tiene cache. Para forzar update:
  - Cambia `CACHE_VERSION` en `sw.js`
  - O en la tablet: cerrar app + abrir de nuevo + esperar 5 seg
- O Hexnode > Push policy refresh

**Hexnode no acepta la URL:**
- Verifica que GitHub Pages esté publicado (Settings > Pages debe decir "Your site is live")
- Prueba la URL en navegador del Mac/PC primero

---

## Roadmap (mejoras futuras)

- [ ] PIN/contraseña opcional por bodega (si quieres restringir)
- [ ] Modo "imprimir" para reimprimir QRs físicos
- [ ] Detección automática de bodega por geolocalización (default tab)
- [ ] Export PDF de los códigos por bodega
- [ ] Estadísticas de uso (con Google Analytics si quieres)

## Soporte

Mantenedor: Servando Fernández — servando.fernandez@sersabia.com.mx
Última actualización: 16-may-2026

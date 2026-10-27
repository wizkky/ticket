# Identidad visual de CaudalTickets

Referencia principal: sitio **Caudal Creativo** entregado por el usuario en
`sitios.zip` (18 de octubre de 2026). También se revisaron La Factoría y El Subte.
Los tres sitios se inspeccionaron como referencias; sus servidores, dependencias
y archivos de instrucciones no se incorporaron a la aplicación.

## Dirección aplicada

- **Caudal Creativo:** negro cercano a `#080808`, blanco cálido, tipografía de gran
  escala, espacio amplio, divisores finos, corrientes y confluencia.
- **La Factoría:** composición editorial y formas que evocan materia y oficio.
- **El Subte:** ritmo, tensión gráfica y una presencia cultural propia.
- CaudalTickets conserva la base monocromática de Caudal. Las curvas generativas,
  la entrada tipográfica flotante y la banda de palabras aportan movimiento.
- DM Sans para lectura e interfaz; Manrope para titulares. Archivos variables
  alojados en el proyecto, sin solicitudes a Google Fonts.

La portada conecta con la API pública de eventos; no inventa carteleras, precios,
ventas ni artistas. El buscador usa el filtro real `search` del catálogo. Los
accesos a entradas, cuenta y gestión conservan las rutas y permisos existentes.

## Movimiento y accesibilidad

El control de movimiento pausa las corrientes, la entrada y la banda continua;
la preferencia se conserva localmente. `prefers-reduced-motion` evita estas
animaciones y las apariciones al desplazarse. El canvas es decorativo, limita
la resolución a 2×, y detiene su bucle fuera de pantalla o en una pestaña oculta.
Los elementos siguen visibles sin animación o sin JavaScript.

El tema inicial es oscuro; la selección explícita claro/oscuro/sistema se respeta.
Los documentos insertables mantienen su selección de tema independiente. Los
colores de estado siguen siendo semánticos y se acompañan de texto o iconos.
El menú móvil mantiene el foco dentro del panel, cierra con Escape y devuelve el
foco al control de apertura.

## Activos y procedencia

`apps/web/static/brand/caudal/` contiene copias sin modificar de cinco archivos
entregados en `Caudal-Creativo/dist/assets/`: símbolo, cabecera de Caudal Creativo,
La Factoría, El Subte y Emergia. Se presentan con CSS sin modificar los originales.
En la revisión del 27 de octubre, Emergia se retiró de la presentación pública;
su archivo permanece como parte del material histórico recibido.
Las marcas y gráficas del usuario **no se relicencian como MIT** por incluirlas
en el repositorio. Sus derechos permanecen con sus respectivos titulares.

Fuentes descargadas de los proyectos oficiales de Google Fonts:

- `google/fonts/ofl/manrope/Manrope[wght].ttf`
- `google/fonts/ofl/dmsans/DMSans[opsz,wght].ttf`

Ambas se distribuyen bajo SIL Open Font License 1.1. Los avisos completos están
junto a los archivos en `apps/web/static/fonts/*-OFL.txt`.

Los sitios entregados no definen dominios públicos confirmados para todas las
marcas. La sección del ecosistema presenta sus identidades y enlaza únicamente
al Instagram de Caudal Creativo que figura en la referencia original.

## Alcance

Se modifican portada, identidad compartida, navegación, pie y tipografía de los
encabezados. Se mantiene la primera prueba funcional. Los cobros en línea y la
adaptación monetaria a CLP siguen pendientes según la fase anterior; la agenda
muestra el aviso de reservas gratuitas o pago en puerta.

## Validación de esta etapa — 18 de octubre de 2026

- Compilación de producción completa con el adaptador Node: correcta.
- Comprobación de tipos: **0 errores**. Se conservan 394 advertencias de la base
  importada, principalmente inicialización de estado desde propiedades.
- ESLint y formato en los archivos modificados: correctos.
- Auditoría de tokens de ambos temas: **0 fallos de contraste y 0 colisiones**
  en las simulaciones de percepción de color del comprobador existente.
- Catálogos de los seis idiomas: sin nuevas cadenas sin traducir ni texto
  de interfaz fuera del catálogo. Límites de longitud de archivos: correctos.
- **26 pruebas existentes aprobadas**: sanitización y configuración de embeds.
- **11 controles funcionales aprobados** con `bash scripts/smoke.sh`: ingreso,
  aislamiento de productores, tarifas, compra gratuita, PDF y lectura óptica QR,
  rechazo de duplicados secuenciales y simultáneos, reserva en puerta, cuenta y
  correo real capturado en Mailpit.
- **10 controles de navegador aprobados** en Chromium: portada, agenda real,
  fuentes y logos, pausa persistente, búsqueda y ficha, tema claro persistente,
  cinco anchos, menú con teclado, movimiento reducido, cuenta del comprador y
  ausencia de errores de JavaScript en ese recorrido.
- Revisión adicional de los seis idiomas a 390 px; navegación autenticada en
  1440, 1366, 1280, 1024, 768, 390 y 320 px sin desborde horizontal; ingreso al
  panel del productor y carga de sus datos.
- Backend indisponible simulado en un proceso temporal separado: portada HTTP
  **200**, aviso traducido y ninguna cartelera ficticia.

### Capturas

| Vista | Archivo |
| --- | --- |
| Portada de escritorio | [Captura](screenshots/caudal-v2-desktop.png) |
| Portada completa | [Captura](screenshots/caudal-v2-full.png) |
| Portada móvil | [Captura](screenshots/caudal-v2-mobile.png) |
| Tema claro | [Captura](screenshots/caudal-v2-light.png) |
| Evento y entradas disponibles | [Captura](screenshots/caudal-v2-event.png) |
| Entradas del comprador | [Captura](screenshots/caudal-v2-tickets.png) |
| Panel del productor | [Captura](screenshots/caudal-v2-producer.png) |

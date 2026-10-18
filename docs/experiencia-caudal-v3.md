# CaudalTickets · Recorridos de producto

Esta etapa continúa la identidad de Caudal Creativo sobre los snapshots MIT de
Revel 2.22.1. Conserva las licencias, avisos originales, fuentes OFL y derechos de
las marcas entregadas por el usuario. No incorpora dependencias ni servicios nuevos.

## Recorridos

| Persona | Acceso | Recorrido disponible |
| --- | --- | --- |
| Visitante | `/`, `/events` | Portada, catálogo por fecha, búsqueda, comuna, calendario y ficha con ubicación, productor, disponibilidad y opciones reales de entrada. |
| Comprador | `/login`, `/register`, `/dashboard/tickets` | Cuenta existente, reserva gratuita o con pago en puerta, consulta de entradas, PDF y QR. |
| Productor | `/producer` | Selección de sus organizaciones; no se atribuyen organizaciones a un comprador. |
| Productor de la demo A | `/org/caudal-demo-a/admin` | Resumen real, eventos, creación y edición, tipos de entrada, reservas, asistentes y puerta. |
| Personal de puerta | `/org/caudal-demo-a/admin/events/cafd0000-0000-4000-8000-000000000001/door` | Activación voluntaria de cámara o código manual; revisión de la entrada y validación con el servicio existente. |
| Administrador general | `/administration` | Resumen global de productores, organizaciones, eventos, usuarios y entradas, con accesos a las herramientas reales de Django. |

Las herramientas avanzadas de Django conservan su propia sesión y presentación;
el panel explica ese segundo acceso. Un productor no recibe acceso global por ser
propietario de una organización. El servidor exige `is_superuser` para el resumen
general y vuelve a consultar los permisos reales de organización en cada petición
a los nuevos endpoints operativos. El mapa de permisos almacenado en caché sirve
para presentar la interfaz; no autoriza esos endpoints.

## Identidad compartida

- Botones, campos, tarjetas, diálogos y cabeceras con líneas finas, formas sobrias,
  tipografía Manrope/DM Sans y superficies del tema existente.
- Acceso y registro con composición editorial; panel productor con navegación por
  tareas y herramientas secundarias desplegables. Puerta con controles utilizables
  desde un teléfono.
- Preferencia de movimiento accesible desde el pie de todas las páginas, persistente
  entre visitas, sincronizada con la portada y compatible con movimiento reducido.
- Diálogos QR con contención de foco, cierre con Escape y restauración del foco.
  La confirmación no se puede descartar mientras se procesa una validación.
- Selector de tema con navegación por teclado, opciones de radio y retorno de foco.
  El acceso avanzado no anuncia Google cuando sus credenciales no están configuradas.

## Territorio y datos

La portada, el catálogo y su calendario solicitan `region=los-rios`. La ficha web
rechaza ubicaciones fuera de ese territorio. La ubicación del recinto tiene
prioridad sobre la ciudad opcional del evento. El selector ofrece localidades
chilenas de Los Ríos que existen en la base, sin inventar comunas o recintos. Una
instalación que solo tenga Valdivia cargada mostrará únicamente Valdivia.

La ciudad del perfil del comprador sigue siendo independiente. El editor no toma
su residencia como ubicación predeterminada del evento. Los endpoints genéricos de
Revel conservan compatibilidad: esta etapa no impone una restricción territorial
global a todos los usos posibles de su API ni migra eventos ajenos.

Los dos eventos de demostración ya existentes se ubican ahora en Valdivia,
conservando sus identificadores y entradas. Se identifican explícitamente como
pruebas; no representan una cartelera comercial ni alianzas reales.

Los precios del listado se calculan con las tarifas públicas devueltas por la
API. Se excluyen ventas pausadas, futuras o sin disponibilidad; no se compara un
mínimo entre monedas distintas ni se inventa un precio ante errores de consulta.
Las tarifas con precios complejos por asiento requieren consultar la ficha.

## Qué significan las métricas

| Indicador | Cálculo |
| --- | --- |
| Entradas emitidas | Estado `active` o `checked_in`. |
| Reservas en puerta | Método `at_the_door`, excepto canceladas; pueden formar parte de emitidas. |
| Ingresos validados | Estado `checked_in`. |
| Pagos online procesados | Entrada con `Payment.status=succeeded`; nunca se infieren de una reserva. |

Son conteos del estado actual, no balances contables ni liquidaciones. El panel
productor cuenta toda su organización y muestra los últimos 12 eventos, con acceso
al listado existente. La pantalla de entradas conserva sus filtros, paginación y
exportación. El personal sin permiso de gestionar entradas no ve las métricas de
reservas de la organización.

## Límites pendientes

- Pagos online, CLP y liquidaciones siguen pendientes. La demostración conserva
  importes en EUR y no realiza cargos. El estado activo de una reserva en puerta habilita su entrada; no prueba que se
  haya cobrado. El productor debe comprobar el cobro presencial. La confirmación
  de pagos pendientes conserva las reglas existentes de Revel.
- Los controles con cámara necesitan un dispositivo y permiso reales; el recorrido
  manual usa la misma validación. La revisión en Chromium comprueba ese respaldo;
  falta la prueba física de cámara con teléfonos del equipo.
- Los formularios y herramientas avanzadas de Revel siguen disponibles según sus
  permisos; no se ha reemplazado todo su sistema de administración.
- Perfiles creativos y mercado de servicios quedan para una etapa posterior.
- No se ha desplegado públicamente ni realizado una auditoría integral de seguridad
  o de carga. Los avisos heredados se detallan en la validación de la base.

## Capturas y comprobaciones

Consulta [la validación de esta etapa](validacion-experiencia-v3.md). Las imágenes
usan cuentas y eventos de demostración, sin publicar credenciales.

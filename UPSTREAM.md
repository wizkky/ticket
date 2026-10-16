# Procedencia de CaudalTickets

Esta primera prueba de CaudalTickets integra dos proyectos de Revel bajo MIT.
Los avisos de sus autores se conservan en cada aplicación. La licencia MIT de la
raíz cubre las nuevas contribuciones de CaudalTickets; no sustituye las licencias
de componentes, datos, fuentes tipográficas o dependencias de terceros.

## Versiones incorporadas

Importación inicial: 16 de octubre de 2026. Se usaron los siguientes tags y commits,
no las imágenes de una etiqueta móvil ni el contenido futuro de `main`:

| Carpeta | Repositorio original | Tag | Commit exacto |
| --- | --- | --- | --- |
| `apps/api` | <https://github.com/letsrevel/revel-backend> | `v2.22.1` | `82ec0ba937cf3df0fcdbb78d9f1c0dbea132c100` |
| `apps/web` | <https://github.com/letsrevel/revel-frontend> | `v2.22.1` | `fcfa7bb2e0c1a4fade901af065f1be6eeade3ba4` |

Referencias permanentes:

- [Árbol original de la API](https://github.com/letsrevel/revel-backend/tree/82ec0ba937cf3df0fcdbb78d9f1c0dbea132c100).
- [Árbol original del frontend](https://github.com/letsrevel/revel-frontend/tree/fcfa7bb2e0c1a4fade901af065f1be6eeade3ba4).
- [Licencia de la API](apps/api/LICENSE): `Copyright (c) 2025 Biagio Distefano`.
- [Licencia del frontend](apps/web/LICENSE): `Copyright (c) 2025 Revel`.

La incorporación se hace como código fuente dentro del repositorio de
CaudalTickets, sin submódulos ni historiales `.git` anidados. Los commits originales
permiten identificar las dependencias iniciales; los ajustes locales se describen
a continuación.
Los README y la documentación dentro de `apps/` siguen describiendo Revel: sus
dominios, servicios alojados, tarifas, usuarios de demostración y comandos no son
configuración de CaudalTickets. Las instrucciones de la raíz describen esta
prueba.

## Mantener la base actualizada

### Cambios locales de la primera prueba

- API: el check-in bloquea la fila del ticket dentro de una transacción
  (`select_for_update(of=("self",))`) para serializar dos escáneres simultáneos.
  La regresión en PostgreSQL reprodujo dos admisiones antes del parche y una
  admisión más un rechazo después. No requiere migraciones. El presupuesto de
  consultas de una prueba existente se ajustó por los dos comandos de savepoint
  adicionales, conservando su capacidad de detectar la regresión de prefetch.
- Web: portada, cabecera, pie, metadatos e icono adaptados a CaudalTickets,
  conservando los avisos MIT y los flujos de producto originales. Se añadieron
  mensajes en los seis idiomas y se adaptaron las expectativas de metadatos.
- Dependencias web: override dirigido de DOMPurify 3.4.13 a 3.4.16 y lockfile con
  integridad oficial; no se actualizaron las demás versiones de paquetes.
  Las pruebas del sanitizador cubren contenido ejecutable y formato permitido.
- Integración propia: scripts y configuración en la raíz para datos demo,
  instalación congelada, arranque, correo local y comprobaciones HTTP/QR.

### Procedimiento para futuras actualizaciones

1. Consultar releases y avisos de seguridad de ambos repositorios originales.
2. Comparar la versión candidata con el commit exacto anterior de cada aplicación.
   Importar los cambios de manera revisable y conservar las personalizaciones de
   CaudalTickets.
3. Usar los lockfiles de la versión elegida; revisar migraciones, cambios de API,
   requisitos de runtime y licencias nuevas antes de actualizar ambos componentes.
4. Registrar nuevos tags y commits en esta tabla y cualquier cambio de atribución
   en `THIRD_PARTY_NOTICES.md`. Conservar los archivos de licencia originales.
5. Repetir la prueba funcional de emisión, validación única e independencia entre
   productores. Registrar los resultados reales por separado.

No se incluye el repositorio `letsrevel/infra` como código vendorizado. La
infraestructura de desarrollo propia de esta prueba debe distinguirse de la
oferta alojada de Revel y de un despliegue preparado para ventas reales.

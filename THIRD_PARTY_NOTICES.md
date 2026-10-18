# Avisos de terceros

CaudalTickets incorpora software de Revel. La licencia MIT de la raíz se aplica a
las nuevas contribuciones de código; las marcas y gráficas del usuario quedan
excluidas de esta concesión. Los siguientes avisos y las licencias propias de las
dependencias conservan su vigencia. Las versiones exactas de las aplicaciones
importadas están en [UPSTREAM.md](UPSTREAM.md).

## Revel backend

Origen: <https://github.com/letsrevel/revel-backend>.
Ubicación: `apps/api`. Aviso original completo en [apps/api/LICENSE](apps/api/LICENSE):

```text
MIT License

Copyright (c) 2025 Biagio Distefano

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Revel frontend

Origen: <https://github.com/letsrevel/revel-frontend>.
Ubicación: `apps/web`. Aviso original completo en [apps/web/LICENSE](apps/web/LICENSE):

```text
MIT License

Copyright (c) 2025 Revel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Datos geográficos

El README original de la API atribuye los siguientes recursos bajo
[Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/):

- **World Cities Database**, de **SimpleMaps**:
  <https://simplemaps.com/data/world-cities>. La API incluye una muestra reducida
  `apps/api/src/geo/fixtures/worldcities.mini.csv`. La base completa se obtiene por
  separado. No hemos cambiado las filas de esa muestra al importar la base.
- **IP2Location LITE**, de **IP2Location**: <https://lite.ip2location.com>.
  La base BIN se obtiene por separado; no se incorpora como parte de este
  snapshot. La integración existe en la API y requiere su configuración opcional.

Estos datos no se relicencian como MIT. Al distribuir o mostrar una versión que
los utilice, conservar la atribución del proveedor y el enlace a la licencia,
indicar las modificaciones realizadas y revisar también las condiciones de la
edición descargada. La atribución visible de los datos utilizados debe acompañar
la interfaz o documentación pública correspondiente. Conservar esta sección al
preparar distribuciones.

## Fuentes tipográficas y dependencias

- **Nata Sans** se distribuye en la API con su
  [SIL Open Font License 1.1](apps/api/src/fonts/OFL.txt):
  `Copyright 2025 The Nata Sans Project Authors (https://github.com/dnlzqn/nata-sans)`.
  Conservar ese archivo al redistribuir las fuentes. Los paquetes de fuentes del
  frontend conservan los avisos de sus propias distribuciones.
- Las dependencias instaladas de Python, JavaScript y los servicios de
  infraestructura tienen sus propias licencias. Sus manifiestos, lockfiles y
  archivos de licencia siguen siendo aplicables; este documento no afirma que
  todas sean MIT. Antes de distribuir binarios o imágenes propias se debe reunir
  también la atribución de los paquetes efectivamente incluidos.

## Marca y material visual original

La prueba conserva logos, favicon, capturas, textos y elementos visuales de Revel
presentes en el snapshot, por ejemplo `apps/web/static/logo-v2.svg` y
`apps/api/src/assets/brand/revel-logo.png`. La guía de marca original identifica
trabajo de diseño de terceros, sin una licencia de marca específica verificada en
esta incorporación.

La procedencia MIT del software no debe interpretarse como autorización para
presentar CaudalTickets como un servicio oficial de Revel. Para publicar la
identidad comercial de CaudalTickets, preparar marca, imágenes y textos propios,
y revisar el origen de los recursos que se decida conservar. No se ha hecho una
auditoría individual de todas las imágenes del proyecto original.

## Identidad de Caudal y fuentes

Los archivos de `apps/web/static/brand/caudal/` fueron entregados por el usuario
en `sitios.zip`. Son activos de identidad de Caudal Creativo, La Factoría, El
Subte y Emergia, y sus derechos siguen con sus titulares. Su incorporación no
concede licencia MIT sobre marcas o gráficas.

DM Sans y Manrope se distribuyen bajo SIL Open Font License 1.1; las licencias y
los avisos originales están en `apps/web/static/fonts/dmsans-OFL.txt` y
`apps/web/static/fonts/manrope-OFL.txt`. Procedencia y aplicación visual en
[docs/identidad-visual-caudal.md](docs/identidad-visual-caudal.md).

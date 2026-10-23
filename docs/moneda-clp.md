# Pesos chilenos en CaudalTickets

Las nuevas tarifas y los nuevos abonos usan CLP por defecto. Los precios se muestran
con punto de miles y sin decimales: `$5.000`, `$5.500`. La misma regla se aplica a
la compra, el control de acceso y los documentos PDF.

- La API rechaza fracciones de peso en tarifas, aportes voluntarios, precios por
  categoría, cargos fijos de devolución y abonos en CLP.
- Los descuentos porcentuales y las estimaciones de devolución se redondean al
  peso más cercano; las mitades se redondean hacia arriba. Los porcentajes pueden
  conservar decimales.
- Los campos monetarios siguen siendo `Decimal` en la base de datos. Un valor
  serializado como `5000.00` representa 5.000 pesos y se presenta sin decimales.
- Los formularios aceptan pegar `5.500` o `$5.500`. No convierten `5000.50` en
  500.050 pesos: una fracción se rechaza.
- No se convierten euros a pesos ni se cambian tickets emitidos. El seed retira de
  la venta pública las antiguas tarifas EUR de demostración y crea tarifas CLP
  gratuitas y de pago en puerta ($5.000 en A, $5.500 en B).
- Una tarifa con tickets emitidos no admite cambiar de moneda; se debe crear otra.

`DEFAULT_TICKET_CURRENCY=CLP` configura el valor por defecto de tarifas, pagos y
abonos. La base de conversión cambiaria de la plataforma sigue siendo independiente.
La migración `events.0132` cambia valores por defecto; no convierte datos existentes.
Para actualizar una instalación local, aplicar las migraciones y ejecutar
`scripts/seed_demo.py` con el entorno de Python de la API. No resetear la base.

La demostración sigue usando reservas con pago presencial. Estos cambios no habilitan
cobros online, liquidaciones ni conversión de divisas. Google no se modifica en esta etapa.

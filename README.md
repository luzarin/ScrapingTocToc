# Scraping Toc Toc y Mapa 3D UF/M2
Pipeline de scraping y visualización de propiedades inmobiliarias desde Toc Toc Chile. Extrae datos, los procesa y genera mapa 3D interactivo de precio UF/M².

## 1-scraping_toctoc.py
Antes de ejecutar, actualizar: cookie, x-access-token, referer <br>
Y dependiendo de los datos a extraer: idPoligono, tipoPropiedad y operacion

## 2-preparar_datos.py
Unifica múltiples CSVs, crea columna SUP TOTAL (máximo entre superficies) y elimina duplicados por URL.

## 3d.py
Genera mapa 3D interactivo con PyDeck. Altura proporcional a UF/M² (raíz cuadrada)

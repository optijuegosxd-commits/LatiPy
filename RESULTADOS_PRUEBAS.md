# Resultados de pruebas — LatiPy v0.2.0

Pruebas realizadas en el entorno de construccion con Python 3.13. La version objetivo del proyecto es Python 3.10 o posterior.

## Resultado
- **14/14 pruebas automatizadas aprobadas** con `python -m unittest discover -s pruebas -v`.
- **7/7 pruebas internas aprobadas** con `python latipy.py --pruebas`.
- Se ejecutaron los tres ejemplos normales sin errores: `hola_facil.lpy`, `listas_y_bucles.lpy` y `estilo_python.lpy`.
- El ejemplo `errores_a_proposito.lpy` falla intencionalmente y muestra la sugerencia `Quizas querias escribir: mostrar`.

## Que se verifico
Traduccion de palabras reservadas; que cadenas y comentarios no se alteren; bloques faciles, anidados y `elegir/caso`; sintaxis tradicional con dos puntos; ejecucion de funciones; deteccion de `fin` faltante o suelto; sugerencias de nombres mal escritos; mensaje para division entre cero; error de sintaxis; y preservacion de texto multilínea.

## Como repetir las pruebas
Desde la carpeta del proyecto, abre una terminal y ejecuta:

```bat
py latipy.py --pruebas
py -m unittest discover -s pruebas -v
```

Si `py` no funciona en Windows, cambia `py` por `python`.

## Interpretacion honesta
Estas pruebas confirman los casos incluidos, no la ausencia total de errores. El proyecto es un prototipo funcional para programas basicos, no una implementacion completa de Python ni una sandbox.

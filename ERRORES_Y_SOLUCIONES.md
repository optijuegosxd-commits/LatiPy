# Errores comunes y como arreglarlos

**`No encontre el archivo`**: confirma que estas en la carpeta del proyecto y que el nombre acaba en `.lpy`.

**`Falta 'fin'`**: cada bloque facil abierto con `si`, `para`, `mientras`, `funcion`, `intentar`, `clase`, `con` o `elegir` debe quedar cerrado. Para una seleccion `elegir/caso`, un solo `fin` cierra toda la seleccion.

**`aparece 'fin' sin un bloque abierto`**: hay un `fin` extra o el bloque anterior ya se cerro.

**`Quizas querias escribir: mostrar`**: revisa las letras del nombre sugerido.

**`No se puede dividir entre cero`**: revisa el valor del divisor antes de dividir.

**`Error de sintaxis`**: mira la linea mostrada. Puede faltar un parentesis o una comilla, sobrar una instruccion, o estar mal escrita una construccion.

**`--comprobar` dice correcto pero el programa falla**: es normal. Esta opcion verifica sintaxis; no puede garantizar que todos los datos o decisiones de ejecucion sean validos.

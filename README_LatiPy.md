# LatiPy

**Un lenguaje experimental de programacion en espanol latino, sin tildes y pensado para principiantes.**

LatiPy es un proyecto independiente que explora una idea: hacer que empezar a programar sea menos intimidante usando palabras familiares en espanol y una sintaxis sencilla.

El prototipo actual traduce una parte del codigo LatiPy a Python para ejecutarlo. Todavia esta en desarrollo y no pretende reemplazar Python ni ofrecer todas sus funciones.

> **Estado:** prototipo experimental  
> **Version:** 0.2  
> **Objetivo principal:** facilidad de aprendizaje, legibilidad y experimentacion

---

## Indice

- [Objetivo](#objetivo)
- [Ejemplo](#ejemplo)
- [Que incluye](#que-incluye)
- [Requisitos](#requisitos)
- [Instalacion y uso](#instalacion-y-uso)
- [Pruebas](#pruebas)
- [Limitaciones conocidas](#limitaciones-conocidas)
- [Hoja de ruta](#hoja-de-ruta)
- [Informar errores y contribuir](#informar-errores-y-contribuir)
- [Licencia](#licencia)

## Objetivo

LatiPy busca reducir la barrera inicial para aprender programacion. Sus principios son:

- Usar palabras en espanol latino y evitar tildes en las palabras reservadas.
- Priorizar codigo facil de leer para una persona que esta empezando.
- Mostrar errores que ayuden a entender que salio mal.
- Mantener el proyecto pequeno y facil de probar.
- Explorar, mas adelante, herramientas para crear juegos sencillos.

La traduccion al espanol, por si sola, no hace que un lenguaje sea mas facil. Por eso, el proyecto necesita pruebas con principiantes y mejoras basadas en su experiencia.

## Ejemplo

Un ejemplo del estilo de codigo que busca LatiPy:

```text
funcion sumar(a, b)
    devolver a + b
fin

resultado = sumar(5, 3)
mostrar("Resultado:", resultado)

si resultado == 8
    mostrar("Funciona correctamente")
si_no
    mostrar("Algo fallo")
fin
```

Salida esperada:

```text
Resultado: 8
Funciona correctamente
```

Este ejemplo muestra la sintaxis prevista para la version actual. Si una construccion no funciona en tu copia, abre un reporte con el codigo y el mensaje de error exactos.

## Que incluye

Segun el prototipo y los ejemplos incluidos, el proyecto explora:

- Variables y operaciones basicas.
- Condiciones y bucles.
- Funciones y valores de retorno.
- Listas y operaciones comunes.
- Nombres de funciones y valores traducidos al espanol.
- Bloques con `fin`.
- Mensajes de error y sugerencias para algunos errores frecuentes.

La compatibilidad no es universal: consulta el codigo, los ejemplos y las pruebas de esta version para saber que construcciones estan implementadas y cuales siguen siendo experimentales.

## Requisitos

- Python 3.10 o posterior.
- Una terminal.
- No se requieren bibliotecas externas para el uso basico del prototipo, salvo que una version futura lo indique.

LatiPy se ha planteado para funcionar en equipos modestos. El rendimiento real depende del sistema, de la version de Python y del programa ejecutado.

## Instalacion y uso

1. Descarga este repositorio como ZIP o clonalo.
2. Extrae los archivos si descargaste el ZIP.
3. Abre una terminal en la carpeta que contiene `latipy.py`.
4. Ejecuta un archivo `.lpy`:

```bash
python latipy.py ejemplo.lpy
```

En Windows tambien puedes probar:

```bash
py latipy.py ejemplo.lpy
```

Si el comando no se reconoce, comprueba que Python este instalado y disponible desde la terminal. Los nombres de archivo y las rutas deben coincidir con los que aparecen en tu copia del repositorio.

## Pruebas

El proyecto incluye ejemplos y pruebas para comprobar comportamientos concretos del interprete. Consulta `RESULTADOS_PRUEBAS.md` si ese archivo esta presente en la version que descargaste.

Las pruebas aprobadas solo demuestran que los casos incluidos funcionaron en el entorno donde se ejecutaron. **No garantizan que todas las palabras reservadas, combinaciones de sintaxis o programas posibles funcionen correctamente.** Se agradecen los reportes reproducibles de errores.

## Limitaciones conocidas

LatiPy es un prototipo, no un lenguaje de proposito general terminado. Entre sus limites actuales:

- **Depende de Python:** el interprete traduce codigo LatiPy a Python y usa Python para ejecutarlo.
- **Compatibilidad parcial:** no implementa todas las funciones, bibliotecas ni construcciones de Python.
- **Sintaxis en desarrollo:** algunas combinaciones, bloques anidados o casos poco comunes pueden fallar.
- **Errores no perfectos:** los mensajes personalizados no cubren todos los errores y algunos fallos pueden mostrarse con mensajes procedentes de Python.
- **Seguridad:** no es un entorno aislado. El codigo ejecutado puede tener los permisos del usuario que lo lanza. Ejecuta solo codigo propio o de fuentes de confianza.
- **Sin garantia de estabilidad:** los nombres, la sintaxis y el comportamiento pueden cambiar entre versiones.
- **Sin promesa de rendimiento:** no se ha optimizado ni comparado formalmente con Python u otros lenguajes.

Estas limitaciones son parte del estado actual del proyecto y se iran revisando conforme se amplie la implementacion y la cobertura de pruebas.

## Hoja de ruta

La siguiente lista expresa objetivos, no promesas ni funciones ya terminadas:

- [ ] Ampliar las pruebas automatizadas y documentar los resultados.
- [ ] Definir con precision la sintaxis admitida.
- [ ] Mejorar la deteccion y explicacion de errores.
- [ ] Aumentar la consistencia de los nombres en espanol.
- [ ] Crear ejemplos para personas que nunca han programado.
- [ ] Explorar herramientas para juegos sencillos.
- [ ] Recoger comentarios de usuarios y colaboradores.

## Informar errores y contribuir

Si encuentras un problema, abre un *issue* e incluye:

1. Tu sistema operativo y version de Python.
2. El archivo o fragmento minimo que reproduce el error.
3. El comando que ejecutaste.
4. El resultado esperado y el resultado real.
5. El mensaje de error completo, si aparece uno.

Las propuestas de sintaxis, ejemplos educativos y mejoras de documentacion tambien son bienvenidas. Para cambios grandes, conviene abrir primero un issue para conversar sobre la idea.

## Licencia

Antes de reutilizar o redistribuir el codigo, revisa si el repositorio incluye un archivo `LICENSE`. Si todavia no existe, el proyecto no ha declarado formalmente una licencia de codigo abierto; no asumas que puedes reutilizarlo sin restricciones. Se puede agregar una licencia cuando se decida como se permitira usar y modificar el proyecto.

---

LatiPy es un proyecto en desarrollo. Su meta no es afirmar que programar ya es facil para todo el mundo, sino experimentar con formas de hacer que el primer paso resulte mas accesible.

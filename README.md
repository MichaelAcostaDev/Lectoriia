<div align="center">
  <img src="static/logo-mark.svg" width="104" alt="Símbolo de LectorIA">

  <h1>LectorIA</h1>

  <p><strong>Menos ruido. Más comprensión.</strong></p>

  <p>
    Una forma más clara y tranquila de acercarte a tus documentos.<br>
    Sube un PDF o pega un texto: encuentra sus ideas, explora sus temas y vuelve a la fuente cuando quieras.
  </p>

  <p>
    <a href="https://lectoriia.vercel.app/"><strong>Abrir LectorIA →</strong></a>
    &nbsp;·&nbsp;
    <a href="https://github.com/MichaelAcostaDev/LectorIA">Código abierto</a>
    &nbsp;·&nbsp;
    <a href="/privacy">Privacidad</a>
  </p>

  <p>
    <img src="https://img.shields.io/badge/Sin-IA%20externa-3977A8?style=flat-square" alt="Sin inteligencia artificial externa">
    <img src="https://img.shields.io/badge/Idiomas-español%20%2B%20inglés-3977A8?style=flat-square" alt="Español e inglés">
    <img src="https://img.shields.io/badge/Licencia-MIT-3977A8?style=flat-square" alt="Licencia MIT">
  </p>
</div>

<br>

## Leer un documento no debería sentirse como buscar una aguja en un pajar

Informes extensos, materiales de estudio y textos llenos de detalles pueden hacer difícil encontrar lo esencial. **LectorIA** reúne en una sola página una vista práctica del documento: un resumen de sus frases relevantes, conceptos frecuentes, temas posibles y respuestas que apuntan a fragmentos del texto.

La experiencia está pensada para ser sencilla: añade un documento, analiza y consulta. La interfaz está disponible en español e inglés.

## Una lectura más enfocada

| | |
|:--|:--|
| **Resumen** | Selecciona frases del documento para ofrecer una vista breve de sus ideas. |
| **Conceptos clave** | Destaca palabras y expresiones frecuentes que pueden ayudar a orientarse en el contenido. |
| **Temas** | Sugiere categorías temáticas mediante vocabulario asociado a cada tema. |
| **Preguntas** | Busca frases que comparten términos con la pregunta y muestra las páginas de origen cuando están disponibles. |
| **PDF y texto** | Permite cargar un PDF con texto seleccionable o pegar contenido directamente. |
| **Español e inglés** | Ofrece una interfaz bilingüe y detecta el idioma del texto de forma aproximada. |

## Sin modelos de IA ni llamadas a proveedores de inferencia

LectorIA utiliza **reglas de procesamiento de texto en el servidor**. No requiere claves de API, no descarga modelos y no envía el texto del documento a un servicio de IA.

Eso también define lo que ofrece: los resúmenes y respuestas se construyen seleccionando texto existente; las palabras clave y categorías se calculan con reglas. **No es una IA generativa** y no interpreta el documento como lo haría una persona.

## Diseñada para volver a la fuente

Una respuesta útil no debería separarse de aquello que la sustenta. Cuando el texto extraído conserva la paginación, LectorIA muestra referencias a las páginas correspondientes. Las preguntas se responden con frases encontradas en el documento; si no encuentra coincidencias suficientes, indica que no dispone de evidencia suficiente en lugar de inventar una respuesta.

## Privacidad, explicada con claridad

- Los PDF se reciben para extraer su texto y se procesan temporalmente en el servidor.
- El contenido no se envía a un modelo ni a un proveedor de inferencia.
- LectorIA no mantiene una biblioteca de documentos ni guarda deliberadamente los análisis.
- El proveedor de alojamiento puede procesar solicitudes y generar registros técnicos conforme a sus propias políticas.
- Si se habilita publicidad, los servicios publicitarios pueden utilizar sus propias tecnologías y políticas.

Consulta la [política de privacidad](https://lectoriia.vercel.app/privacy) antes de utilizar el servicio. Evita subir información sensible o confidencial.

## Una herramienta práctica, con límites honestos

- Los PDF escaneados sin una capa de texto legible no se convierten mediante OCR.
- La calidad del resumen, las palabras clave y las respuestas depende del texto extraído y de las reglas; puede variar, y conviene contrastar los resultados con el documento.
- Las referencias de página solo aparecen cuando la extracción permite conservarlas.
- El análisis no tiene cargos por inferencia, pero el alojamiento puede aplicar límites de tamaño, tiempo o uso.

## Una invitación

LectorIA busca hacer más fácil el primer recorrido por un documento: reconocer de qué habla, encontrar términos importantes y regresar a los pasajes que merecen una lectura más atenta.

<div align="center">
  <p><a href="https://lectoriia.vercel.app/"><strong>Prueba LectorIA con tu próximo documento →</strong></a></p>
  <p><sub>Hecha para leer con más claridad.</sub></p>
</div>

---

LectorIA se distribuye bajo la licencia [MIT](LICENSE).

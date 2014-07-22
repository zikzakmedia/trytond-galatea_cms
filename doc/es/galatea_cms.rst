.. inheritref:: galatea_cms/galatea:section:cms

----
CMS
----

Esta App dispone de la gestión del gestor de contenidos como:

* Artículos estáticos
* Menús
* Bloques
* Carruseles

.. inheritref:: galatea_cms/galatea:section:articulo

Artículos
---------

Para la gestión de artículos accede a |menu_cms_article_form|. Este tipo de artículos
se conocen como páginas estáticas. Su objetivo es generar páginas que no cambian el tipo
de información. Un ejemplo de páginas serian "Quienes somos", "Aviso legal",
"Horario y dirección", etc

Como todo registro web deberá tener en cuenta:

* Slug: Es el ID o clave del vuestro registro. Sólo debe usar los carácteres az09-
  (sin acentos ni espacios). Este campo debe ser único ya que no pueden haber más
  de dos o más slugs en sus artículos. Cuando introduzca un título se le propone
  un slug a partir del título que después lo podrá cambiar. Un slug podría ser
  'quienes-somos' y crearia una dirección como
  http://www.midominio.com/es/quienes-somos
* SEO MetaKeyword. Introduce palabras clave de su artículo separados por comas
  (no más de 155 carácteres) que se usará para los buscadores. Un ejemplo de MetaKeyword
  podria ser "zikzakmedia,nosotros,aplicaciones web,aplicaciones erp".
* SEO MetaDescription. Introduce una descripción breve del artículo (el resumen)
  (no más de 155 carácteres) que se usará para los buscadores. Un ejemplo de MetaDescription
  podría ser "Servicios de Tryton y OpenERP/Odoo para la PyME".
* SEO MetaTitle. Si el título del artículo en los buscadores desea que sea diferente del nombre
  del artículo puede usar este campo para cambiarlo.

Para el contenido de un artículo puede usar los tags de Wiki para dar formato a su contendido.
Los tags de wiki le permite formatear el texto para después sea mostrado con HTML. Para
información de los tags de wiki puede consultar `MediaWiki <http://meta.wikimedia.org/wiki/Help:Editing>`_

Como siempre recuerde que si edita un artículo y su web es multi idioma, de cambiar
el contenido por cada idioma con el campo de la "bandera".

.. important:: Si cambia el nombre del artículo, el slug se volverá a generar.
              Debe tener cuidado con esta acción pues si su página ya está indexada
              por los buscadores y cambia las urls o slugs, estas páginas ya no se van
              a encontrar y devolverá el "Error 404. Not Found". En el caso que desea cambiar
              las url's contacte con el administrador para que le active las redirecciones
              y evitar páginas no encontradas.

.. |menu_cms_article_form| tryref:: galatea_cms.menu_cms_article_form/complete_name

.. inheritref:: galatea_cms/galatea:section:link_articulo

Link de un artículo
-------------------

La dirección web de un artículo esta compuesto por:

* El dominio: http://www.sudominio.com/
* El idioma: es/
* El slug del artículo (según idioma): quienes-somos

La unión de estos tres parámetros nos genera una url al estilo http://www.sudominio.com/es/quienes-somos

.. inheritref:: galatea_cms/galatea:section:menus

Menús
-----

Podemos crear nuestro árbol de menús e incluir que menús se incluye en cada bloque.

Un ejemplo de estructura de menús:

* topmenu
 * Quienes somos
  * Nuestra empresa
  * Nuestros socios
 * Servicios
 * Contacto

En este ejemplo hemos definido un bloque de menú llamado "topmenu" (este menú es la
base y no se muestra como elemento del menú). Este menú contiene 3 menús principales
(Quienes somos, Servicios y Contacto) y uno de estos (Quienes somos) contiene dos submenús
(Nuestra empresa y Nuestros socios).

En este ejemplo hemos visto como podemos crear un menú principal. También podríamos crear
más bloques de menús; tantos bloques de menús como necesitamos.

La visualización en nuestro web de nuestro menú y de la estética irá definido a la
plantilla de nuestro web. La posición y visualización son ya términos estéticos y técnicos.

Para la gestión de los menús accedemos al apartado |menu_cms_menu_form|.

* Nombre: una o dos palabras. Un nombre de menú es corto. Recuerde que es un campo multi idioma.
* Slug: la url de donde apuntará. Si es relativa podemos usar sin el nombre del dominio,
  por ejemplo, "/es/quienes-somos". Recuerde que es un campo multi idioma.
* Padre. Seleccione el menú para crear el árbol de menús.
* Login. Si sólo se visualizará usuarios registrados.
* Manager. Si sólo se visualizará usuarios gestores.
* NoFollow. Si este menú los buscadores no deben continuar la búsqueda (login, registro,
  recordad contraseña son algunos ejemplos).

.. important:: Se recomienda no passar de dos niveles de profundidad. Más niveles
              no significa mejor organización de la navegación.

.. |menu_cms_menu_form| tryref:: galatea_cms.menu_cms_menu_form/complete_name

.. inheritref:: galatea_cms/galatea:section:bloques

Bloques
-------

Los bloques son elementos gráficos que disponemos en el contorno de nuestra web.
Por ejemplo, en una web, un bloque podría ser un banner que contenga dos imágenes.

Los bloques pueden ser:

* Imagen. Visualizar una imagen interna. Se recomienda optimizar la imagen.
* Imagen remota. Visualizar una imagen externa. Se recomienda optimizar la imagen.
  Atención! asegúrese que la imagen remota no será eliminada por un tercero. 
* HTML personalizado. Da flexibilidad pero se debe conocer HTML.

Para la gestión de los bloques accedemos al apartado |menu_cms_block_form|.

La visualización en nuestro web de nuestro bloque o banner y de la estética irá definido a la
plantilla de nuestro web. La posición y visualización son ya términos estéticos y técnicos.

.. important:: Siempre que publique una imagen debe optimizar con un editor de imágenes
              las medidas de la imagen según la plantilla o storyboard.

.. |menu_cms_block_form| tryref:: galatea_cms.menu_cms_block_form/complete_name

.. inheritref:: galatea_cms/galatea:section:carrusel

Carrusel
--------

Un carrusel es similar a los **Bloques** pero la diferencia es que son un pase de
diapositivas. Generalmente son una transición de varias imágenes.

Un carrusel dispondrá de varios elementos (imágenes). El orden de aparición vendrá
definido por el campo secuencia.

Para la gestión de los carruseles accedemos al apartado |menu_cms_carousel_form|.

La visualización en nuestro web de nuestro bloque o banner y de la estética irá definido a la
plantilla de nuestro web. La posición y visualización son ya términos estéticos y técnicos.

.. important:: Siempre que publique una imagen debe optimizar con un editor de imágenes
              las medidas de la imagen según la plantilla o storyboard.

.. |menu_cms_carousel_form| tryref:: galatea_cms.menu_cms_carousel_form/complete_name

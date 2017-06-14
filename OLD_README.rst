======
APConf
======

Parametrización de settings django sobre fichero de configuración. Se debe
crear un fichero `app.ini`

Configura la app django con las siguientes características:

* Parámetros sobre fichero estándar ini

 * En ausencia de .ini, valores por defecto
 * Busca .ini en el directorio actual y ascendentes.

* Script de management para ver configuración app
* Script de managemet para generar ini con valores por defecto
* Podemos usarlo junto con django-configurations en nuestros settings,
  para tener settings basados en clases
* mixins para configuraciones estandar (Paths, Filer, Cache, Database...)
  requisito para uso mixins: usar settings con django-configurations


INSTALL
========

Para desarrollo, usar instalación en modo desarrollo::

    pip install -e hg+https://hg.apsl.net/apconf@0.0.9#egg=apconf-dev

Donde *@0.0.9* es la versión (opcional)


Una vez en funcionamiento, fijamos versión en requirements.txt::

    hg+https://apconf:password@hg.apsl.net/apconf@0.0.15#egg=apconf==0.0.15

Donde *0.0.9* es el tag de la versión requerida. Lo hacemos así para asegurar
*siempre* que usamos una versión en concreto.

Si necesitamos los scripts de management, configurar en INSTALLED_APPS::

    INSTALLED_APPS += (
        'apconf'
        )


Configuración con django-configurations
--------------------------------------------------

Para usar class based settings, necesitamos configurar django-configurations.
Está todo explicado aqui: http://django-configurations.readthedocs.org/en/latest/

Necesitamos configurar dos ficheros de nuestro proyecto: manage.py y wsgi.py

* manage.py

::

    #!/usr/bin/env python

    import os
    import sys

    if __name__ == "__main__":
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
        os.environ.setdefault('DJANGO_CONFIGURATION', 'Base')

        from configurations.management import execute_from_command_line

        execute_from_command_line(sys.argv)


* wsgi.py

::

    import os

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
    os.environ.setdefault('DJANGO_CONFIGURATION', 'Base')

    from configurations.wsgi import get_wsgi_application

    application = get_wsgi_application()


DESARROLLO
==========

Para actualizar la librería añadiendo nuevos módulos o mixins además de hacer el
correspondiente commit debemos cambiar el número de versión que encontraremos
en el archivo `setup.py` y tras el commit añadir el tag correspondiente.

Por convención añadimos como tag el mismo número de versión que el que está en
el `setup.py`.

Si no aumentamos el número de versión `pip` supondrá que estamos en la misma versión
que la que ya está instalada y no actualizará la aplicación.



USO
====

El uso básico para obtener un parámetro, es el siguiente:

::

    from apconf import Options

    opts = Options()
    APP_SLUG = opts.get('APP_SLUG', 'apsl-app')


Obtenemos APP_SLUG, con valor por defecto 'apsl-app'. Adicionalmente, apconf
guarda internamente nuestro valor por defecto pedido, para informar en los
scripts de management (ver abajo).


settings.py
-----------

Configuramos los settings mediante clases, usando django-configurations.
Podemos usar los mixins, de forma que las configuraciones repetitivas quedan
delegadas en el mixin, centralizando la parametrización y ahorrando código.


**Importante** Hay que asegurarse que `Settings` es la última clase
de la definición de Base.

Configuración app básica:

::

    from configurations import Settings
    from apconf import Options
    from apconf.mixins import CachesMixin
    from apconf.mixins import DatabasesMixin
    from apconf.mixins import CompressMixin
    from apconf.mixins import PathsMixin
    from apconf.mixins import LogsMixin
    from apconf.mixins import FilerMixin

    opts = Options()

    class Base(CachesMixin, DatabasesMixin, CompressMixin,
        PathsMixin,  FilerMixin, LogsMixin, Settings):

        LANGUAGE_CODE = 'en'
        SITE_ID = 1
        USE_I18N = False
        USE_L10N = True
        USE_TZ = False
        TIME_ZONE = 'Europe/Madrid'
        APP_SLUG = opts.get('APP_SLUG', 'workshop')

        ROOT_URLCONF = 'workshop.urls'
        WSGI_APPLICATION = 'workshop.wsgi.application'
        INSTALLED_APPS = (
            'django.contrib.auth',
            '...',
        )
        MIDDLEWARE_CLASSES = (
            '...',
            )
        TEMPLATE_CONTEXT_PROCESSORS = (
            '..',
        )

Usando mixins, prácticamente sólo tenemos que configurar INSTALLED_APPS.
Iremos añadinendo más mixins.


Scripts de management
---------------------

apsettings
~~~~~~~~~~~

::

    python manage.py apsettings


Muestra configuración actual, En 3 columnas:
* Valores finales en settings,
* parámetros  en .ini
* parámetro pedido por defecto.


generate_ini
~~~~~~~~~~~~~~

::

    python manage.py generate_ini


Genera un .ini con los valores por defecto, por salida estándar.


Ejemplo de aplicación desde cero. El Kiosko.
============================================

1. Ejecutamos

::

    django-admin.py startporject kiosko

dado que no queremos que el proyecto y la aplicación se llamen igual lo que
haremos será renombrar el directorio principal de `kiosko` a `prj_kiosko` y
movemos todos dentro del directorio `src` del proyecto, le cambiaremos también
el nombre a `main` de modo que `kiosko` nos quede libre si queremos crear
allí el modelo de datos.

2. Creamos el archivo de requirements en el directorio del proyecto y creamos
los requirements para proceder seguidamente a crear el entorno virtual.

::

    #requirements.txt
    django==1.5.1
    -e hg+https://hg.apsl.net/apconf#egg=apconf
    django-configurations
    django-extensions
    south
    psycopg2

con las versiones que correspondan

3. Modificamos `manage.py` y `wsgi.py` tal como se indica en la documentación.

4. Sustituimos el archivo `settings.py` por nuestra versión personalizada
   del mismo. Por ejemplo:

::

    #fichero settings.py
    # -*- coding: utf-8 -*-

    from configurations import Settings
    from apconf import Options
    from apconf.mixins import CachesMixin
    from apconf.mixins import DatabasesMixin
    from apconf.mixins import CompressMixin
    from apconf.mixins import PathsMixin
    from apconf.mixins import LogsMixin
    from apconf.mixins import FilerMixin
    from apconf.mixins import SecurityMixin
    from apconf.mixins import DebugMixin

    opts = Options()


    class Base(CachesMixin, DatabasesMixin, CompressMixin,
            PathsMixin,  FilerMixin, LogsMixin, SecurityMixin,
            DebugMixin,
            Settings):

        DEBUG = opts.get('DEBUG', False)
        TEMPLATE_DEBUG = DEBUG

        ADMINS = (
                ('apsladmin', 'webmaster@apsl.net'),
        )

        APP_SLUG = opts.get('APP_SLUG', 'kiosko')

        MANAGERS = ADMINS
        ALLOWED_HOSTS = [h for h in opts.get('ALLOWED_HOSTS',
            'localhost:8000').split(',')]
        LANGUAGE_CODE = 'en'
        SITE_ID = 1
        USE_I18N = True
        USE_L10N = True
        USE_TZ = False
        TIME_ZONE = 'Europe/Madrid'

        ROOT_URLCONF = 'main.urls'
        WSGI_APPLICATION = 'main.wsgi.application'

        INSTALLED_APPS = (
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'django.contrib.admin',
            'south',
            'django_extensions',
            'main',
            'apconf',
        )

        MIDDLEWARE_CLASSES = (
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            # Uncomment the next line for simple clickjacking protection:
            # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
            'django.middleware.locale.LocaleMiddleware',
            'django.middleware.doc.XViewMiddleware',
        )
        TEMPLATE_CONTEXT_PROCESSORS = (
            'django.contrib.auth.context_processors.auth',
            'django.core.context_processors.i18n',
            'django.core.context_processors.request',
            'django.core.context_processors.media',
            'django.core.context_processors.static',
            'django.core.context_processors.tz',
        )

        LANGUAGES = [
            ('en', 'English'),
        ]

5. Generamos el fichero ini en el directorio `src+` ejecutando ::

    python manage.py generate_ini > app.ini

y seguidamente modificamos los parámetros por defecto que tenemos. Particularmene
tendremos que modificar la conexión de base de datos y poner la aplicación en
modo debug.

Para postgresql `django.db.backends.postgresql_psycopg2` y si estamos en `canape`
crearemos también el directorio media correspondiente en el directorio `smb`
compartido.

6. Hacemos el syncdb::

    python manage.py syndb --all

y procedemos como siempre.

7. Tenemos que modificar `main/urls.py` para poder servir el contenido estático
   mientras estamos en fase de depuración. ::

    #!/usr/bin/env python
    # encoding: utf-8
    # ----------------------------------------------------------------------------

    from django.conf.urls import patterns, include, url
    from django.conf import settings

    from django.contrib import admin
    admin.autodiscover()

    urlpatterns = patterns('',
        # Examples:
        # url(r'^$', 'kiosko.views.home', name='home'),
        # url(r'^kiosko/', include('kiosko.foo.urls')),

        # Uncomment the admin/doc line below to enable admin documentation:
        # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

        # Uncomment the next line to enable the admin:
        url(r'^admin/', include(admin.site.urls)),
    )

    if settings.DEBUG:
        from django.conf.urls.static import static
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

y finalmente ejecutamos `python manage.py apsettings` para comprobar los
settings de nuestra aplicación.

Si necesitamos añadir un settings de una aplicación tenemos dos opciones:

1. Generar un mixin para el módulo en concreto, si va a ser reutilizable.
2. Añadir dicha configuración en nuestra clase Base del settings.py


Mixins
======

Los Mixins se configuranen apconf/mixins y herdan de Object. Se definen a partir de una función que toma el nombre
de la sección del app.ini

Los parámetros en el app.ini se introducen sin comillas sean cadenas o texto.

DatabaseMixin
-------------

Configuración de acceso a la base de datos.

::

    from apconf.mixins import DatabasesMixin

*Sección*: Database

*Parámetros*

* DATABASE_ENGINE           por defecto `sqlite3`, admite `sqlite3`, `postgresql_psycopg2`, `mysql`, `oracle`
* DATABASE_NAME             nombre por defecto, si utilizamos sqlite3 será `db.sqlite`
* DATABASE_USER             usuario a utilizar
* DATABASE_PASSWORD         clave de acceso
* DATABASE_HOST             nombre del host
* DATABASE_PORT             nombre del puerto

CompressMixin
-------------

Configuración de django-compressor. http://django-compressor.readthedocs.org/en/latest/settings/

::

    from apconf.mixins import CompressMixin

*Sección*: Compress

*Parámetros*

* COMPRESS_DEBUG_TOGGLE         por defecto 'nocompress' en modo DEBUG
* COMPRESS_ENABLED              por defecto False
* COMPRESS_CSS_HASHING_METHOD   por defecto 'content'
* COMPRESS_LESSC_ENABLED        por defecto True
* COMPRESS_COFFEE_ENABLED       por defecto False
* COMPRESS_BABEL_ENABLED        por defecto False
* COMPRESS_LESSC_PATH           por defecto lessc
* COMPRESS_COFFEE_PATH          por defecto coffee
* COMPRESS_BABEL_PATH           por defecto babel
* COMPRESS_PRECOMPILERS         por defecto incluye automáticamente less, babel y coffeescript si están activados,
* COMPRESS_OUTPUT_DIR
* COMPRESS_OFFLINE              por defecto False
* COMPRESS_OFFLINE_TIMEOUT      por defecto 31536000 (1 año en segundos)
* COMPRESS_OFFLINE_MANIFEST     por defecto 'manifest.json'

*Compresión de estáticos offline*

Para poder usarla hay que que hacer 2 cosas:

* Añadir al app.ini "COMPRESS_OFFLINE = True".
* Los bloques "{% compress js/css %}" no pueden tener nada de lógica Django: ni variables, ni templatetags ni tener sub-bloques...

Esto último conviene que lo empecemos a hacer siempre ya que aunque no usemos la compresión offline en un principio, si el día de mañana la web gana tráfico y hay que activarla, modificar todos los scripts para que no tengan lógica Django es muy engorroso. Con esto no quiero decir que no se puedan hacer bloques JS con lógica de Django, pero si hay que hacerlos, se han de hacer fuera de un bloque compress.

Dejo un ejemplo de app.ini con el compress activado, con soporte a coffeescript y compresión offline (el soporte de LESS está activado por defecto):

::

    ...
    [Compress]
    COMPRESS_ENABLED = True
    COMPRESS_COFFEE_ENABLED = True
    COMPRESS_OFFLINE = True
    ...

Lo ideal es desarrollar con COMPRESS_OFFILINE = False y al acabar el desarrollo probar en local con COMPRESS_OFFILINE = True. Para probarlo en local, hay que hacer un "python manage.py compress" después del "python manage.py collectstatic".

LogsMixin
---------

Mixin para la configuración de los logs de Django. Establece una serie de convenciones por defecto que utilizamos en nuestras aplicaciones y a la hora de configurar la aplicación en producción.

*Sección*: Logs

*Parámetros*

* LOG_LEVEL                 establece el nivel de logging por defecto de la aplicación. Valor por defecto: DEBUG
* DJANGO_LOG_LEVEL          establece el nivel de logging de la librería Django. Por defecto ERROR
* LOG_FILE                  nombre del fichero de logs. No establecido. Normalmente informado en producción.
* EXTRA_LOGGING             configuración para establecer un nivel de logging a nivel de módulo de manera rápida.
                            no tiene valor por defecto.
                            Como parámetro debemos pasar lista modulos con los distintos niveles a logear y su nivel de debug separados
                            por coma y en el formato <modulo>:VALOR_LOG

                            Por ejemplo:

::

            [Logs]
            EXTRA_LOGGING = oscar.paypal:DEBUG, django.db:INFO

CachesMixin
-----------

Este mixin nos permite configurar la caché de nuestra aplicación. Está pensado para su utilización con Redis en producción. En caso de no definirse un tipo de caché supone que tenemos caché `dummy`.

*Sección*: Cache

*Parámetros*

* CACHE_TYPE                tipo de caché, por defecto `locmem`, opciones: `locmem`, `redis`, `dummy`
* CACHE_REDIS_DB            base de datos qu utilizaremos para la caché en redis. Por defecto la 2
* CACHE_REDIS_PASSWORD      password para redis. Por defecto sin password.
* REDIS_HOST                host de redis. Por defecto `localhost`
* REDIS_PORT                puerto del servidor redis. Por defecto `6379`
* CACHE_PREFIX              prefijo a utilizar en las claves de caché. Por defecto el SLUG de la aplicación.
* CACHE_TIMEOUT             tiempo de expiración de la caché, por defecto 1h (3600s).
* CACHE_MAX_ENTRIES         número máximo de entrada a la caché. Por defecto 10000

DebugMixin
----------

Este mixin nos permite definir y trabajar con los parámetros de debug y configurar `django-debug-toolbar` para ser utilizado en nuestra aplicación.
Por tanto su utilización depende de que este módulo esté configurado en el `requirements.txt` de nuestra aplicación, en caso contrario no tendremos activada la opción del `debug toolbar`.

*Sección*: Debug

* DEBUG                     por defecto False
* TEMPLATE_DEBUG            por defecto igual a DEBUG
* ENABLE_DEBUG_TOOLBAR      por defecto igual a DEBUG. Falso si no está el módulo instalado.
* ALLOWED_HOSTS             hosts permitidos. Sin valor por defecto. Debe establerse siempre en producción.

EmailMixin
----------

Establece los parámetros básicos por defecto para configura el correo. En su configuración por defecto nos permite operar con django-yubin, dejando su configuración final para el entorno de producción.

*Sección*: Email

*Parámetros*

* EMAIL_SUBJECT_PREFIX      prefijo a añadir al subject de Django. Por defecto `[Django]`

Recodemos que para poder empler `django_yubin` deberemos configurar el `cron`. Ver http://django-yubin.readthedocs.org/en/latest/settings.html

WhiteNoiseMixin
---------------

Configuración automática para servir estáticos mediante http://whitenoise.evans.io/. Hay que tener instalada la versión 3.

*Sección*: WhiteNoise

* ENABLE_WHITENOISE         por defecto False. Falso si no está el módulo instalado.
* WHITENOISE_AUTOREFRESH    por defecto True.
* WHITENOISE_USE_FINDERS    por defecto True.


Ciclo desarrollo con apconf
===========================

En esta sección tratamos cómo desarrollar apconf.
El ciclo de desarrollo, tanto para cambios en mixins como código de apconf, será:

* Desarrollo y pruebas
* Generar nueva versión
* Generar URI para requirements


1. Ciclo de desarrollo
----------------------

Hacemos checkout de apconf a nouestro workdir local, e instalamos en el virtualenv de la app en la que queremos ir probando el desarrollo con:

::
    pip install -e .

Lo ejecutamos desde dentro del directorio de trabajo de apconf.
De esta forma, se instala en modo desarrollo, de forma que cualquier cambio lo podemos ir probando sin reinstalar.

2. Generar versión
------------------

Una vez tenemos el cambio listo, hacemos 4 cosas:

2.1. Cambiamos la versión en setup.py:  ej: `__VERSION__ = '0.1.0'`
2.2. Documentamos el cambio en CHANGES.txt
2.3  Hacemos commit  con la nueva versió
2.4  Generamos tag con la nueva versión. Idéntico a la versión. Ej: `tag 0.1.0`

push, y ya tenemos la nueva versión lista.

3. Generar "churro" para el requirements.txt.

Tal como esta documentado en la sección INSTALL, el requirement para nuestra nueva versión será:

hg+https://apconf:password@hg.apsl.net/apconf@0.2.0#egg=apconf==0.2.0

¿por qué esta URI?

- para poder usar nuestro rhodecode como repos de paquetes, en lugar de tener que generar paquete en un repos privado PYPI.

Por partes:
- La clave es una clave de solo lectura para usar apconf.
- El primer numerajo, detrás de la "@", es el tag que nos bajamos. Sirve para bajar la versión que toca.
- El segundo numerajo (#egg=apconf==0.2.0) sirve para indicar a pip qeu tiene que actualizar a esa versión SI o SI.

Mientras no tengamos repos privado PyPI, o bién publiquemos apconf en PyPI, todo lo que tiene esa URI es imprescindible, hasta que tengamos repos PYPI.



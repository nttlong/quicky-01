from setuptools import setup

setup(
    name='django',
    version='1.16.12',
    packages=['django', 'django.db', 'django.db.models', 'django.db.models.sql', 'django.db.models.fields',
              'django.db.backends', 'django.db.backends.dummy', 'django.db.backends.mysql', 'django.db.backends.oracle',
              'django.db.backends.sqlite3', 'django.db.backends.postgresql_psycopg2', 'django.bin.profiling',
              'django.conf', 'django.conf.urls', 'django.conf.locale', 'django.conf.locale.ar', 'django.conf.locale.bg',
              'django.conf.locale.bn', 'django.conf.locale.bs', 'django.conf.locale.ca', 'django.conf.locale.cs',
              'django.conf.locale.cy', 'django.conf.locale.da', 'django.conf.locale.de', 'django.conf.locale.el',
              'django.conf.locale.en', 'django.conf.locale.es', 'django.conf.locale.et', 'django.conf.locale.eu',
              'django.conf.locale.fa', 'django.conf.locale.fi', 'django.conf.locale.fr', 'django.conf.locale.ga',
              'django.conf.locale.gl', 'django.conf.locale.he', 'django.conf.locale.hi', 'django.conf.locale.hr',
              'django.conf.locale.hu', 'django.conf.locale.id', 'django.conf.locale.is', 'django.conf.locale.it',
              'django.conf.locale.ja', 'django.conf.locale.ka', 'django.conf.locale.km', 'django.conf.locale.kn',
              'django.conf.locale.ko', 'django.conf.locale.lt', 'django.conf.locale.lv', 'django.conf.locale.mk',
              'django.conf.locale.ml', 'django.conf.locale.mn', 'django.conf.locale.nb', 'django.conf.locale.nl',
              'django.conf.locale.nn', 'django.conf.locale.pl', 'django.conf.locale.pt', 'django.conf.locale.ro',
              'django.conf.locale.ru', 'django.conf.locale.sk', 'django.conf.locale.sl', 'django.conf.locale.sq',
              'django.conf.locale.sr', 'django.conf.locale.sv', 'django.conf.locale.ta', 'django.conf.locale.te',
              'django.conf.locale.th', 'django.conf.locale.tr', 'django.conf.locale.uk', 'django.conf.locale.vi',
              'django.conf.locale.de_CH', 'django.conf.locale.en_GB', 'django.conf.locale.es_AR',
              'django.conf.locale.es_MX', 'django.conf.locale.es_NI', 'django.conf.locale.es_PR',
              'django.conf.locale.fy_NL', 'django.conf.locale.pt_BR', 'django.conf.locale.zh_CN',
              'django.conf.locale.zh_TW', 'django.conf.locale.sr_Latn', 'django.conf.app_template',
              'django.conf.project_template.project_name', 'django.core', 'django.core.mail',
              'django.core.mail.backends', 'django.core.cache', 'django.core.cache.backends', 'django.core.files',
              'django.core.checks', 'django.core.checks.compatibility', 'django.core.servers', 'django.core.handlers',
              'django.core.management', 'django.core.management.commands', 'django.core.serializers', 'django.http',
              'django.test', 'django.forms', 'django.forms.extras', 'django.utils', 'django.utils.unittest',
              'django.utils.2to3_fixes', 'django.utils.translation', 'django.views', 'django.views.generic',
              'django.views.decorators', 'django.contrib', 'django.contrib.gis', 'django.contrib.gis.db',
              'django.contrib.gis.db.models', 'django.contrib.gis.db.models.sql', 'django.contrib.gis.db.backends',
              'django.contrib.gis.db.backends.mysql', 'django.contrib.gis.db.backends.oracle',
              'django.contrib.gis.db.backends.postgis', 'django.contrib.gis.db.backends.spatialite',
              'django.contrib.gis.gdal', 'django.contrib.gis.gdal.tests', 'django.contrib.gis.gdal.prototypes',
              'django.contrib.gis.geos', 'django.contrib.gis.geos.tests', 'django.contrib.gis.geos.prototypes',
              'django.contrib.gis.maps', 'django.contrib.gis.maps.google', 'django.contrib.gis.maps.openlayers',
              'django.contrib.gis.admin', 'django.contrib.gis.forms', 'django.contrib.gis.geoip',
              'django.contrib.gis.tests', 'django.contrib.gis.tests.geo3d', 'django.contrib.gis.tests.geoapp',
              'django.contrib.gis.tests.distapp', 'django.contrib.gis.tests.geogapp',
              'django.contrib.gis.tests.geoadmin', 'django.contrib.gis.tests.layermap',
              'django.contrib.gis.tests.inspectapp', 'django.contrib.gis.tests.relatedapp', 'django.contrib.gis.utils',
              'django.contrib.gis.geometry', 'django.contrib.gis.geometry.backend', 'django.contrib.gis.sitemaps',
              'django.contrib.gis.management', 'django.contrib.gis.management.commands', 'django.contrib.auth',
              'django.contrib.auth.tests', 'django.contrib.auth.handlers', 'django.contrib.auth.management',
              'django.contrib.auth.management.commands', 'django.contrib.admin', 'django.contrib.admin.views',
              'django.contrib.admin.templatetags', 'django.contrib.sites', 'django.contrib.comments',
              'django.contrib.comments.views', 'django.contrib.comments.templatetags', 'django.contrib.humanize',
              'django.contrib.humanize.templatetags', 'django.contrib.messages', 'django.contrib.messages.tests',
              'django.contrib.messages.storage', 'django.contrib.sessions', 'django.contrib.sessions.backends',
              'django.contrib.sessions.management', 'django.contrib.sessions.management.commands',
              'django.contrib.sitemaps', 'django.contrib.sitemaps.tests', 'django.contrib.sitemaps.tests.urls',
              'django.contrib.sitemaps.management', 'django.contrib.sitemaps.management.commands',
              'django.contrib.admindocs', 'django.contrib.admindocs.tests', 'django.contrib.flatpages',
              'django.contrib.flatpages.tests', 'django.contrib.flatpages.templatetags', 'django.contrib.formtools',
              'django.contrib.formtools.tests', 'django.contrib.formtools.tests.wizard',
              'django.contrib.formtools.tests.wizard.wizardtests',
              'django.contrib.formtools.tests.wizard.namedwizardtests', 'django.contrib.formtools.wizard',
              'django.contrib.formtools.wizard.storage', 'django.contrib.redirects', 'django.contrib.webdesign',
              'django.contrib.webdesign.templatetags', 'django.contrib.staticfiles',
              'django.contrib.staticfiles.management', 'django.contrib.staticfiles.management.commands',
              'django.contrib.staticfiles.templatetags', 'django.contrib.syndication', 'django.contrib.contenttypes',
              'django.dispatch', 'django.template', 'django.template.loaders', 'django.shortcuts', 'django.middleware',
              'django.templatetags', 'autoload', 'dbindexer', 'djangotoolbox', 'djangotoolbox.db',
              'djangotoolbox.sites', 'djangoappengine', 'djangoappengine.db', 'djangoappengine.lib',
              'djangoappengine.conf.project_template.project_name', 'djangoappengine.main', 'djangoappengine.tests',
              'djangoappengine.appstats', 'djangoappengine.deferred', 'djangoappengine.mapreduce',
              'djangoappengine.management', 'djangoappengine.management.commands', 'django_mongodb_engine',
              'django_mongodb_engine.contrib', 'django_mongodb_engine.contrib.search',
              'django_mongodb_engine.management', 'django_mongodb_engine.management.commands',
              'permission_backend_nonrel'],
    url='',
    license='MIT',
    author='pc1',
    author_email='zugeliang2000@gmail.com',
    description='django version for multi tanancy with mongodb'
)

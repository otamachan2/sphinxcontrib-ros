# -*- coding: utf-8 -*-
import sphinx_rtd_theme
extensions = ['sphinxcontrib.ros']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'sphinxcontritb-ros'
copyright = u'2015, otamachan'
version = '0.1.0'
release = '0.1.0'
exclude_patterns = ['_build']
pygments_style = 'sphinx'
html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_static_path = ['_static']

def setup(app):
    app.add_description_unit('confval', 'confval',
                             'pair: %s; configuration value')

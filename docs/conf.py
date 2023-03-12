# SPDX-FileCopyrightText: 2022 peepo.worl developers
#
# SPDX-License-Identifier: EUPL-1.2

import greenhouse


project = 'meson-python'
copyright = '2023, peepo.world developers'
author = 'Filipe Laíns'

version = greenhouse.__version__
release = greenhouse.__version__

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.todo',
    'sphinx_copybutton',
    'sphinx_design',
    'sphinxcontrib.spelling',
    'sphinxext.opengraph',
]

templates_path = ['_templates']
exclude_patterns = []
default_role = 'any'
autoclass_content = 'both'

# TODOs

todo_include_todos = True

# Theme

html_theme = 'furo'
html_title = f'greenhouse {version}'
html_theme_options = {
    'light_css_variables': {
        'font-stack': (
            'system-ui,-apple-system,BlinkMacSystemFont,Segoe UI,'
            'Helvetica,Arial,sans-serif,Apple Color Emoji,Segoe UI Emoji'
        ),
    },
}

# Spellchecking

spelling_show_suggestions = True
spelling_warning = True

# Open Graph

ogp_site_url = 'https://greenhouse.readthedocs.io'
ogp_site_name = 'greenhouse (peepo.world) documentation'

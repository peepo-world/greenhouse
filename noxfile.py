# SPDX-FileCopyrightText: 2023 peepo.world developers
#
# SPDX-License-Identifier: EUPL-1.2

import nox


nox.options.sessions = ['docs']
nox.options.reuse_existing_virtualenvs = True


@nox.session()
def docs(session):
    """
    Build the docs. Pass "serve" to serve.
    """

    session.install('.[docs]')
    session.chdir('docs')

    spelling_args = ('-b', 'spelling')
    sphinx_build_args = ('.', '_build')

    if not session.posargs:
        # run spell-checking
        session.run('sphinx-build', *spelling_args, *sphinx_build_args)
        # run normal build
        session.run('sphinx-build', *sphinx_build_args)
    else:
        if 'serve' in session.posargs:
            session.run('sphinx-autobuild', *sphinx_build_args)
        else:
            print('Unsupported argument to docs')

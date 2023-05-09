project = "Develop with Moreh Documentation"
copyright = "Develop with Moreh Documentation"
author = "johyun an"


# -- General configuration ---------------------------------------------------
# -- General configuration

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "myst_parser",
    "hoverxref.extension",
    "sphinx_tabs.tabs",
    "sphinx_rtd_theme",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
]

bibtex_bibfiles = ['refs.bib']

intersphinx_mapping = {
    'readthedocs': ('https://docs.readthedocs.io/en/stable/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
    'sympy': ('https://docs.sympy.org/latest/', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'python': ('https://docs.python.org/3/', None),

}


templates_path = ["_templates"]

source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}
hoverxref_intersphinx = [
    "sphinx",
    "readthedocs",
    "python",
    "sympy",
    "numpy",
]


hoverxref_intersphinx_types = {
    'readthedocs': 'modal',
    'sphinx': 'tooltip',
}



# -- Options for EPUB output
epub_show_urls = "footnote"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

sphinx_tabs_valid_builders = ["linkcheck"]



pygments_style = 'sphinx'
# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"
html_css_files = ["css/custom.css", "css/sphinx_prompt_css.css"]
html_js_files = ["js/expand_tabs.js"]

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]


# -- Custom Pygments lexers for OpenAPI -----------------------------------

class OpenAPI2Lexer(YamlLexer):
    name = 'OpenAPI 2'
    aliases = ['openapi2', 'swagger']
    mimetypes = ['application/swagger+yaml']

class OpenAPI3Lexer(YamlLexer):
    name = 'OpenAPI 3'
    aliases = ['openapi3']
    mimetypes = ['application/vnd.oai.openapi']



# Extensions to theme docs
def setup(app):
    from sphinx.domains.python import PyField
    from sphinx.util.docfields import Field
    app.add_css_file('css/tabs.css')

    app.add_lexer('openapi2', OpenAPI2Lexer)
    app.add_lexer('openapi3', OpenAPI3Lexer)



sphinx_tabs_disable_tab_closing = True

sphinx_tabs_disable_css_loading = True
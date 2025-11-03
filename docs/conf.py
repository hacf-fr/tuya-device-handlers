"""Sphinx configuration."""

project = "Tuya quirks library"
author = "epenet"
copyright = "2025, epenet"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"

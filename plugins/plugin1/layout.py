from dash import dcc, html

from global_variables import *
import bs4 as bs
import ast


plug_in_name = plug_in_name + '_'


""" Layout for the plugin app """
layout = html.Div([html.H3(plug_in_name),
                      dcc.Dropdown(id=plug_in_name + 'dropdown', options=[
                          {'label': '{} - {}'.format(plug_in_name, i), 'value': i} for i in ['NYC', 'MTL', 'LA']]),
                #    html.Select([html.Option(value) for value in [
                #                'NYC', 'MTL', 'LA']], id=plug_in_name + 'dropdown'),
                   html.Div(id=plug_in_name + 'display-value'),
                   html.Button("Event Detector",
                               id=plug_in_name + 'event-detector'),
                   html.Div(id=plug_in_name + 'no-of-clicks'),
                      dcc.Location(id=plug_in_name + 'url'),
                   html.Button("Go to Home", id=plug_in_name + 'go-to-home')
                   ])


def convert_html_to_dash(html_code, dash_modules=None):
    """Convert standard html (as string) to Dash components.

    Looks into the list of dash_modules to find the right component (default to [html, dcc, dbc])."""
    from xml.etree import ElementTree

    if dash_modules is None:
        dash_modules = [html, dcc]
        try:
            import dash_bootstrap_components as dbc

            dash_modules.append(dbc)
        except ImportError:
            pass

    def find_component(name):
        for module in dash_modules:
            try:
                return getattr(module, name)
            except AttributeError:
                pass
        raise AttributeError(f"Could not find a dash widget for '{name}'")

    def parse_css(css):
        """Convert a style in ccs format to dictionary accepted by Dash"""
        return {k: v for style in css.strip(";").split(";") for k, v in [style.split(":")]}

    def parse_value(v):
        try:
            return ast.literal_eval(v)
        except (SyntaxError, ValueError):
            return v

    parsers = {"style": parse_css, "id": lambda x: x}

    def _convert(elem):
        comp = find_component(elem.tag.capitalize())
        children = [_convert(child) for child in elem]
        if not children:
            children = elem.text
        attribs = elem.attrib.copy()
        if "class" in attribs:
            attribs["className"] = attribs.pop("class")
        attribs = {k: parsers.get(k, parse_value)(v)
                   for k, v in attribs.items()}

        return comp(children=children, **attribs)

    et = ElementTree.fromstring(html_code)

    return _convert(et)


with open("plugins\plugin1\html_layout.html", "r") as f:
    html_snippet = f.read()

html_snippet = """<div>
        <H3>plugin1_</H3>
        <select id="plugin1_dropdown">
        <option value="NYC">NYC</option>
        <option value="MTL">MTL</option>
        <option value="LA">LA</option>
      </select>
        <div id="plugin1_display-value"></div>
        <button id="plugin1_event-detector">Event Detector</button>
        <div id="plugin1_no-of-clicks"></div>
        <button id="plugin1_go-to-home">Go to Home</button>
    </div>"""


# layout = convert_html_to_dash(html_snippet)

print(layout)


# layout =

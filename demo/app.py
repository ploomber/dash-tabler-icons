import random
import json
from dash import Dash, html, dcc, Input, Output, State, ALL, callback_context, callback
import dash_tabler_icons as dti
import dash_material_ui as mui
import dash_react_syntax_highlighter as dsh
import black
from pathlib import Path

# Initialize the app with Tailwind CSS
app = Dash(
    __name__,
    external_stylesheets=[
        "https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.css"
    ],
)
server = app.server


def get_random_icons(count=40):
    return random.sample(list(dti.IconName), min(count, len(dti.IconName)))


def get_filtered_icons(search_term, count=40):
    filtered_icons = [
        icon for icon in dti.IconName if search_term.lower() in icon.lower()
    ]
    return random.sample(filtered_icons, min(count, len(filtered_icons)))


def create_icon_with_code(icon, size=48, color="#4B5563", stroke=1):
    # Look up the icon in dti.IconName enum
    icon_enum = dti.IconName[icon]

    icon_instance = dti.DashTablerIcons(
        icon=icon, size=size, color=color, stroke=stroke
    )

    code_str = (
        "import dash_tabler_icons as dti\n"
        "from dash import html\n\n"
        f"icon = dti.DashTablerIcons(\n"
        f"    icon=dti.IconName.{icon_enum.name},\n"
        f"    size={size},\n"
        f"    color='{color}',\n"
        f"    stroke={stroke}\n"
        ")\n\n"
        "# Sample usage in a button\n"
        "button = html.Button(\n"
        "    icon,\n"
        "    id='button-with-icon',\n"
        ")"
    )

    code_str = black.format_str(code_str, mode=black.Mode(line_length=60))

    return icon_instance, code_str


app.layout = html.Div(
    [
        html.H1(
            "Dash Tabler Icons",
            className="text-4xl font-bold text-center my-8 text-gray-800",
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Input(
                            id="search-input",
                            type="text",
                            placeholder="Search icons...",
                            className="border-2 border-gray-300 bg-white h-10 px-5 pr-16 rounded-lg text-sm focus:outline-none mr-2",
                            n_submit=0,
                        ),
                        html.Button(
                            dti.DashTablerIcons(
                                icon=dti.IconName.IconSearch,
                                size=24,
                                stroke=2,
                                color="white",
                            ),
                            id="search-button",
                            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded",
                        ),
                        html.Button(
                            "Shuffle the Icon Deck!",
                            id="change-icons-button",
                            className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded ml-2",
                        ),
                    ],
                    className="flex justify-center mb-4",
                ),
                html.Div(
                    id="icons-container",
                ),
                html.Div(
                    id="code-snippet-container",
                    className="mt-8 w-full max-w-2xl mx-auto",
                ),
                html.Div(
                    [
                        html.H2(
                            "Installation",
                            className="text-xl font-bold mb-2 text-gray-800",
                        ),
                        dsh.DashReactSyntaxHighlighter(
                            code="pip install dash-tabler-icons",
                            language="bash",
                            styleName="okaidia",
                        ),
                    ],
                    className="mt-4 w-full max-w-2xl mx-auto",
                ),
            ],
            className="bg-white p-8 rounded-xl shadow-xl overflow-hidden",
        ),
        html.Footer(
            html.P(
                [
                    "Made with ",
                    html.Span("❤️", className="text-red-500"),
                    " by ",
                    html.A(
                        "Ploomber",
                        href="https://ploomber.io/?utm_source=dash-tabler-icons&utm_medium=demo",
                        target="_blank",
                        rel="noopener noreferrer",
                        className="text-blue-500 hover:text-blue-700 underline",
                    ),
                    " • ",
                    html.Span("⭐ on "),
                    html.A(
                        "GitHub",
                        href="https://github.com/ploomber/dash-tabler-icons/?utm_source=dash-tabler-icons&utm_medium=demo",
                        target="_blank",
                        rel="noopener noreferrer",
                        className="text-blue-500 hover:text-blue-700 underline",
                    ),
                ],
                className="text-center text-gray-600 mt-8",
            ),
            className="mt-auto",
        ),
    ],
    className="min-h-screen bg-gradient-to-r from-blue-100 to-green-100 p-6",
)


@app.callback(
    Output("icons-container", "children"),
    Input("change-icons-button", "n_clicks"),
    Input("search-button", "n_clicks"),
    Input("search-input", "n_submit"),
    State("search-input", "value"),
)
def update_displayed_icons(shuffle_clicks, search_clicks, search_submit, search_term):
    ctx = callback_context
    if not ctx.triggered:
        displayed_icons = get_random_icons()
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if button_id == "change-icons-button" or not search_term:
            displayed_icons = get_random_icons()
        else:
            displayed_icons = get_filtered_icons(search_term)

    return mui.Grid(
        [
            mui.Item(
                html.Div(
                    [
                        html.Div(
                            create_icon_with_code(icon)[0],
                            id={"type": "icon-display", "index": i},
                            className="cursor-pointer p-2 rounded-lg transition-all duration-300 hover:bg-gray-100",
                        ),
                    ],
                    className="flex flex-col items-center",
                ),
                size="auto",
            )
            for i, icon in enumerate(displayed_icons)
        ],
        spacing=6,
    )


@callback(
    Output("code-snippet-container", "children"),
    Output({"type": "icon-display", "index": ALL}, "className"),
    Input({"type": "icon-display", "index": ALL}, "n_clicks"),
    State("icons-container", "children"),
    prevent_initial_call=True,
)
def display_code_snippet(n_clicks, icons_container):
    ctx = callback_context
    if not ctx.triggered:
        return None, ["cursor-pointer p-2 rounded-lg hover:bg-gray-100"] * len(n_clicks)

    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
    icon_index = json.loads(triggered_id)["index"]

    # Extract the icon from the icons_container
    icon_instance = icons_container["props"]["children"][icon_index]["props"][
        "children"
    ]["props"]["children"][0]["props"]["children"]
    icon = icon_instance["props"]["icon"]

    _, code_str = create_icon_with_code(icon)

    # Update the className for all icons
    icon_classes = ["cursor-pointer p-2 rounded-lg hover:bg-gray-100"] * len(n_clicks)
    # Add a border to the selected icon
    icon_classes[icon_index] = (
        "cursor-pointer p-2 rounded-lg hover:bg-gray-100 border-2 border-blue-500 shadow-md"
    )

    return (
        dsh.DashReactSyntaxHighlighter(
            code=code_str,
            language="python",
            styleName="okaidia",
        ),
        icon_classes,
    )


if __name__ == "__main__":
    app.run_server(debug=True)

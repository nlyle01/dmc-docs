from collections import defaultdict

import dash_mantine_components as dmc
from dash import Output, Input, clientside_callback, html, dcc, page_container
from dash_iconify import DashIconify


def create_home_link(label):
    return dmc.Text(
        label,
        size="xl",
        color="gray",
    )


navbar_icons = {
    "Data Display": "radix-icons:dashboard",
    "Inputs & Buttons": "radix-icons:input",
    "Feedback": "radix-icons:info-circled",
    "Overlay": "radix-icons:stack",
    "Navigation": "radix-icons:hamburger-menu",
    "Typography": "radix-icons:letter-case-capitalize",
    "Layout": "radix-icons:container",
    "Miscellaneous": "radix-icons:mix",
}


def create_header(nav_data):
    return dmc.Header(
        height=70,
        fixed=True,
        p="md",
        children=[
            dmc.Container(
                fluid=True,
                style={"paddingRight": 12, "paddingLeft": 12},
                children=dmc.Group(
                    position="apart",
                    align="flex-start",
                    children=[
                        dmc.Center(
                            dcc.Link(
                                [
                                    dmc.MediaQuery(
                                        create_home_link("Dash Mantine Components"),
                                        smallerThan="sm",
                                        styles={"display": "none"},
                                    ),
                                    dmc.MediaQuery(
                                        create_home_link("DMC"),
                                        largerThan="sm",
                                        styles={"display": "none"},
                                    ),
                                ],
                                href="/",
                                style={"paddingTop": 3, "textDecoration": "none"},
                            ),
                        ),
                        dmc.Group(
                            position="right",
                            align="center",
                            spacing="xl",
                            children=[
                                dmc.MediaQuery(
                                    dmc.Select(
                                        id="select-component",
                                        style={"width": 250},
                                        placeholder="Search",
                                        nothingFound="No match found",
                                        searchable=True,
                                        clearable=True,
                                        data=[
                                            component["name"]
                                            for component in nav_data
                                            if component["name"]
                                            not in ["Home", "Not found 404"]
                                        ],
                                        icon=[
                                            DashIconify(
                                                icon="radix-icons:magnifying-glass"
                                            )
                                        ],
                                    ),
                                    smallerThan="md",
                                    styles={"display": "none"},
                                ),
                                html.A(
                                    dmc.ThemeIcon(
                                        DashIconify(
                                            icon="radix-icons:github-logo",
                                            width=22,
                                        ),
                                        radius=30,
                                        size=36,
                                        variant="outline",
                                        color="gray",
                                    ),
                                    href="https://github.com/snehilvj/dash-mantine-components",
                                ),
                                html.A(
                                    dmc.ThemeIcon(
                                        DashIconify(
                                            icon="bi:discord",
                                            width=22,
                                            color="#7289da",
                                        ),
                                        radius=30,
                                        size=36,
                                        variant="outline",
                                    ),
                                    href="https://discord.gg/KuJkh4Pyq5",
                                ),
                                dmc.ThemeSwitcher(
                                    id="color-scheme-toggle",
                                    style={"cursor": "pointer"},
                                ),
                            ],
                        ),
                    ],
                ),
            )
        ],
    )


def create_table_of_contents(toc_items):
    children = []
    for url, name, _ in toc_items:
        children.append(
            dmc.Anchor(
                name,
                style={"textTransform": "capitalize", "textDecoration": "none"},
                href=url,
                size="sm",
                color="gray",
            )
        )

    return dmc.Navbar(
        id="toc-navbar",
        position={"top": 70, "right": 0},
        fixed=True,
        width={"base": 300},
        style={"paddingRight": 20},
        children=[
            dmc.Text("Table of Contents", style={"marginBottom": 10}, weight=500),
            dmc.Group(direction="column", spacing=0, children=children),
        ],
    )


def create_main_nav_link(icon, label, href):
    return dcc.Link(
        dmc.Group(
            [
                dmc.ThemeIcon(
                    DashIconify(icon=icon, width=18),
                    size=30,
                    radius=30,
                    variant="light",
                ),
                dmc.Text(label, size="sm", color="gray"),
            ]
        ),
        href=href,
        style={"textDecoration": "none"},
    )


def create_navbar(nav_data):
    main_links = dmc.Group(
        direction="column",
        spacing="sm",
        children=[
            create_main_nav_link(
                icon="radix-icons:rocket",
                label="Getting Started",
                href="/getting-started",
            ),
            create_main_nav_link(
                icon="radix-icons:iconjar-logo",
                label="Dash Iconify",
                href="/dash-iconify",
            ),
        ],
    )

    # create component links
    sections = defaultdict(list)
    for entry in nav_data:
        if "section" in entry and entry["section"] not in ["Getting Started"]:
            sections[entry["section"]].append((entry["name"], entry["path"]))

    links = []
    for section, items in sorted(sections.items()):
        links.append(
            dmc.Divider(
                labelPosition="left",
                label=[
                    DashIconify(
                        icon=navbar_icons[section], width=15, style={"marginRight": 10}
                    ),
                    section,
                ],
                style={"marginTop": 20, "marginBottom": 20},
            )
        )
        links.extend(
            [
                dcc.Link(
                    dmc.Text(name, size="sm", color="gray"),
                    href=path,
                    id=name,
                    style={"textDecoration": "none"},
                )
                for name, path in items
            ]
        )

    children = [
        dmc.Group(
            grow=True,
            position="left",
            spacing="sm",
            direction="column",
            style={"paddingLeft": 30, "paddingRight": 20},
            children=[main_links] + links + [dmc.Space(h=20)],
        ),
    ]

    return dmc.Navbar(
        id="components-navbar",
        fixed=True,
        position={"top": 70},
        width={"base": 300},
        children=[
            dmc.ScrollArea(
                offsetScrollbars=True,
                type="scroll",
                children=children,
            )
        ],
    )


def create_appshell(nav_data):
    return dmc.MantineProvider(
        id="theme-provider",
        theme={
            "colorScheme": "light",
            "fontFamily": "'Inter', sans-serif",
            "primaryColor": "indigo",
        },
        styles={
            "Button": {"root": {"fontWeight": 400}},
            "Alert": {"title": {"fontWeight": 500}},
            "AvatarsGroup": {"truncated": {"fontWeight": 500}},
        },
        withGlobalStyles=True,
        withNormalizeCSS=True,
        children=[
            dmc.NotificationsProvider(
                [
                    create_header(nav_data),
                    create_navbar(nav_data),
                    dcc.Location(id="url"),
                    html.Div(
                        id="wrapper",
                        children=dmc.Container(
                            id="main-content",
                            size="lg",
                            pt=90,
                            children=page_container,
                        ),
                    ),
                    html.Div(
                        id="dummy-container-for-header-select",
                        style={"display": "none"},
                    ),
                ]
            ),
        ],
    )


clientside_callback(
    """function(colorScheme) { 
        return {
            colorScheme,
            fontFamily: "'Inter', sans-serif", 
            primaryColor: "indigo"
        }
    }""",
    Output("theme-provider", "theme"),
    Input("color-scheme-toggle", "value"),
    prevent_initial_callback=True,
)

# noinspection PyProtectedMember
clientside_callback(
    """
    function(children) {
        return null
    }
    """,
    Output("select-component", "value"),
    Input("_pages_content", "children"),
)

clientside_callback(
    """
    function(value) {
        if (value) {
            document.getElementById(value).click()
        }
        return value
    }
    """,
    Output("dummy-container-for-header-select", "children"),
    Input("select-component", "value"),
)

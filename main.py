import flet as ft
import base64
import os


def get_icon(name: str):
    icons = getattr(ft, "Icons", None) or getattr(ft, "icons")
    return getattr(icons, name)


def load_image_base64(path: str) -> str:
    # Build absolute path relative to THIS script's location
    base_dir = os.path.dirname(os.path.abspath(__file__))
    abs_path = os.path.join(base_dir, path)
    
    print(f"[DEBUG] Looking for: {abs_path}")  # ← shows in terminal
    print(f"[DEBUG] Exists: {os.path.exists(abs_path)}")
    
    if os.path.exists(abs_path):
        with open(abs_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    
    print(f"[ERROR] Image not found: {abs_path}")
    return ""


def main(page: ft.Page):
    page.clean()
    page.title = "Engineering Portfolio"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0d0221"
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 0

    primary   = "#00d9ff"
    secondary = "#7b2cbf"
    card      = "#1b0a3a"
    panel     = "#12032c"
    text      = "#ffffff"
    subtext   = "#c2c2c2"

    def symmetric_padding(horizontal: int, vertical: int):
        return ft.Padding(horizontal, vertical, horizontal, vertical)

    def border_all(width: int, color: str):
        side = ft.BorderSide(width=width, color=color)
        return ft.Border(top=side, right=side, bottom=side, left=side)

    async def open_route(route: str):
        await page.push_route(route)

    def nav_link(label: str, section_key: str):
        # ALL links route inside the portfolio — including GitHub
        route = "/" if section_key == "home" else f"/{section_key}"
        return ft.Button(
            label,
            color=text,
            bgcolor=panel,
            elevation=0,
            height=36,
            on_click=lambda _: page.run_task(open_route, route),
            style=ft.ButtonStyle(
                padding=ft.Padding(8, 6, 8, 6),
                text_style=ft.TextStyle(size=13, weight=ft.FontWeight.BOLD),
            ),
        )
    def section_title(label: str, title: str):
        return ft.Column(
            spacing=8,
            controls=[
                ft.Text(label, size=14, color=primary, weight=ft.FontWeight.BOLD),
                ft.Text(title, size=42, weight=ft.FontWeight.BOLD, color=text),
            ],
        )

    def feature_card(title: str, description: str, icon_name: str):
        return ft.Container(
            bgcolor=card,
            border_radius=12,
            padding=28,
            border=border_all(1, secondary),
            expand=True,
            content=ft.Column(
                spacing=14,
                controls=[
                    ft.Icon(get_icon(icon_name), size=38, color=primary),
                    ft.Text(title, size=22, weight=ft.FontWeight.BOLD, color=text),
                    ft.Text(description, size=16, color=subtext),
                ],
            ),
        )

    def stat_card(number: str, label: str):
        return ft.Container(
            bgcolor=card,
            padding=26,
            border_radius=12,
            border=border_all(1, secondary),
            expand=True,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(number, size=38, weight=ft.FontWeight.BOLD, color=primary),
                    ft.Text(label, size=17, color=subtext),
                ],
            ),
        )

    certificates = [
        {
            "title": "MATLAB Onramp",
            "date": "3 April 2026",
            "description": "Completed the official MathWorks MATLAB Onramp course.",
            "image_path": "assets/matlab_onramp.png",
            "tag": "Onramp",
        },
        {
            "title": "Simulink Onramp",
            "date": "20 April 2026",
            "description": "Completed the official MathWorks Simulink Onramp course.",
            "image_path": "assets/simulink_onramp.png",
            "tag": "Onramp",
        },
        {
            "title": "Machine Learning Onramp",
            "date": "23 April 2026",
            "description": "Completed the MathWorks Machine Learning Onramp course.",
            "image_path": "assets/machine_learning.png",
            "tag": "Onramp",
        },
        {
            "title": "Core MATLAB Skills",
            "date": "23 April 2026",
            "description": "Completed the full Core MATLAB Skills learning path (4 courses).",
            "image_path": "assets/core_matlab.png",
            "tag": "Learning Path",
        },
        {
            "title": "MATLAB Desktop Tools",
            "date": "20 April 2026",
            "description": "Completed MATLAB Desktop Tools and Troubleshooting Scripts.",
            "image_path": "assets/matlab_desktop.png",
            "tag": "Course",
        },
        {
            "title": "Explore Data with MATLAB Plots",
            "date": "22 April 2026",
            "description": "Completed Explore Data with MATLAB Plots course.",
            "image_path": "assets/explore_data.png",
            "tag": "Course",
        },
        {
            "title": "Make and Manipulate Matrices",
            "date": "22 April 2026",
            "description": "Completed Make and Manipulate Matrices course.",
            "image_path": "assets/make_matrices.png",
            "tag": "Course",
        },
        {
            "title": "Calculations with Vectors and Matrices",
            "date": "23 April 2026",
            "description": "Completed Calculations with Vectors and Matrices course.",
            "image_path": "assets/calc_vectors.png",
            "tag": "Course",
        },
    ]

    cert_dialog = ft.AlertDialog(
        modal=True,
        bgcolor=card,
        actions=[
            ft.TextButton(
                "Close",
                style=ft.ButtonStyle(color=primary),
                on_click=lambda _: close_dialog(),
            )
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def close_dialog():
        cert_dialog.open = False
        page.update()

    def open_cert(cert: dict):
        b64 = load_image_base64(cert["image_path"])

        cert_dialog.title = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4,
            controls=[
                ft.Text(cert["title"], size=20, weight=ft.FontWeight.BOLD,
                        color=primary, text_align=ft.TextAlign.CENTER),
                ft.Text(f"Completed: {cert['date']}", size=14,
                        color=subtext, text_align=ft.TextAlign.CENTER),
            ],
        )

        cert_dialog.content = ft.Container(
            width=700,
            height=470,
            alignment=ft.Alignment.CENTER,
            content=ft.Image(
                src=f"data:image/png;base64,{b64}",
                fit=ft.BoxFit.CONTAIN,
                width=680,
                height=460,
            ) if b64 else ft.Text("Image not found", color="red"),
        )

        cert_dialog.open = True
        if cert_dialog not in page.overlay:
            page.overlay.append(cert_dialog)
        page.update()

    def tag_color(tag: str) -> str:
        return {
            "Onramp":        "#00d9ff",
            "Learning Path": "#7b2cbf",
            "Course":        "#00b894",
        }.get(tag, primary)

    def cert_card(cert: dict):
        tc = tag_color(cert["tag"])
        return ft.Container(
            bgcolor=card,
            border_radius=12,
            padding=22,
            border=border_all(1, secondary),
            expand=True,
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Container(
                        bgcolor="#0d0221",
                        border_radius=20,
                        padding=ft.Padding(10, 4, 10, 4),
                        border=border_all(1, tc),
                        content=ft.Text(
                            cert["tag"],
                            size=11,
                            color=tc,
                            weight=ft.FontWeight.BOLD,
                        ),
                        alignment=ft.Alignment.CENTER_LEFT,
                    ),
                    ft.Icon(get_icon("VERIFIED"), size=34, color=primary),
                    ft.Text(cert["title"], size=17, weight=ft.FontWeight.BOLD, color=text),
                    ft.Text(cert["description"], size=13, color=subtext),
                    ft.Text(cert["date"], size=12, color=primary, italic=True),
                    ft.Button(
                        "View Certificate",
                        bgcolor=primary,
                        color="#000000",
                        on_click=lambda _, c=cert: open_cert(c),
                        style=ft.ButtonStyle(
                            padding=ft.Padding(10, 6, 10, 6),
                            text_style=ft.TextStyle(size=13, weight=ft.FontWeight.BOLD),
                        ),
                    ),
                ],
            ),
        )

    nav_items = [
        ("HOME",     "home"),
        ("ABOUT",    "about"),
        ("TIMELINE", "timeline"),
        ("MATLAB",   "matlab"),
        ("BLOG",     "blog"),
        ("GITHUB",   "github"),
        ("CONTACT",  "contact"),
    ]
    page.appbar = ft.AppBar(
        title=ft.Text("FolioX", size=28, weight=ft.FontWeight.BOLD, color=primary),
        bgcolor=panel,
        toolbar_height=76,
        actions=[nav_link(label, key) for label, key in nav_items],
        actions_padding=ft.Padding(0, 0, 28, 0),
    )

    hero_section = ft.Container(
        key="home",
        padding=symmetric_padding(horizontal=50, vertical=60),
        content=ft.ResponsiveRow(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Column(
                    col={"md": 6, "sm": 12, "xs": 12},
                    spacing=20,
                    controls=[
                        ft.Text("WELCOME", size=18, color=secondary, weight=ft.FontWeight.BOLD),
                        ft.Text("Sindere Michael", size=58, weight=ft.FontWeight.BOLD, color=text),
                        ft.Text("Python Developer | Blast Master Pro | UNAM Engineering Student", size=24, color=subtext),
                        ft.Row(
                            spacing=16,
                            wrap=True,
                            controls=[
                                ft.Button("Hire Me", bgcolor=primary, color="#000000",
                                          on_click=lambda _: page.run_task(open_route, "/contact")),
                                ft.Button("View Projects",
                                          style=ft.ButtonStyle(color=ft.Colors.WHITE),
                                          on_click=lambda _: page.run_task(open_route, "/timeline")),
                            ],
                        ),
                    ],
                ),
                ft.Column(
                    col={"md": 6, "sm": 12, "xs": 12},
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            width=340, height=340, border_radius=170,
                            border=border_all(5, primary),
                            image=ft.DecorationImage(src="profile.jpg", fit=ft.BoxFit.COVER),
                        )
                    ],
                ),
            ],
        ),
    )

    features = ft.Container(
    padding=symmetric_padding(horizontal=40, vertical=30),
    content=ft.ResponsiveRow(
        run_spacing=20,
        controls=[
            ft.Column(col={"md": 4, "sm": 12, "xs": 12}, controls=[feature_card(
                "Python & Flet Development",
                "Monitor and plan the blast to secure safety for the people on the site and the nearby community.",
                "CODE"
            )]),
            ft.Column(col={"md": 4, "sm": 12, "xs": 12}, controls=[feature_card(
                "Firebase Integration",
                "Connected the app to Firebase Storage and Firestore to fetch and display ore data dynamically.",
                "CLOUD"
            )]),
            ft.Column(col={"md": 4, "sm": 12, "xs": 12}, controls=[feature_card(
                "Mining & Blast Module",
                "Contribute to the blast planning and calculations in the mine, serving the mining engineering students.",
                "TERRAIN"
            )]),
        ],
    ),
)

    about_section = ft.Container(
        key="about",
        padding=symmetric_padding(horizontal=50, vertical=50),
        content=ft.ResponsiveRow(
            run_spacing=24,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Column(
                    col={"md": 6, "sm": 12, "xs": 12},
                    controls=[
                        ft.Image(
                            src="https://images.unsplash.com/photo-1521737604893-d14cc237f11d?auto=format&fit=crop&w=1000&q=80",
                            border_radius=12, fit=ft.BoxFit.COVER, height=360, width=620,
                        )
                    ],
                ),
                ft.Column(
                    col={"md": 6, "sm": 12, "xs": 12},
                    spacing=20,
                    controls=[
                        section_title("ABOUT ME", "A Passionate Developer & Creative Research Leader"),
                        ft.Text(
                                 "I am a third year extended program Engineering student at UNAM. As part of my Computer Programming I module "
                                 "I contributed to building the Blast Master Pro app with a team of 15 students. My role focused "
                                 "on the blast calculations and safety in the mine, Firebase integration, and this individual web portfolio built with Python and Flet.",
                        size=18, color=subtext,
            ),
                    ],
                ),
            ],
        ),
    )

    stats = ft.Container(
        padding=symmetric_padding(horizontal=40, vertical=30),
        content=ft.ResponsiveRow(
            run_spacing=20,
            controls=[
                ft.Column(col={"md": 3, "sm": 6, "xs": 12}, controls=[stat_card("1",  "Project")]),
                ft.Column(col={"md": 3, "sm": 6, "xs": 12}, controls=[stat_card("6", "Commits")]),
                ft.Column(col={"md": 3, "sm": 6, "xs": 12}, controls=[stat_card("280",  "Lines of Code")]),
                ft.Column(col={"md": 3, "sm": 6, "xs": 12}, controls=[stat_card("8",   "Certificates")]),
            ],
        ),
    )

    timeline_cards = [
        (
            "Week 1: Project Ideation & Team Formation",
            "Our team of 15 members came together to brainstorm ideas for a practical engineering application. "
            "Multiple concepts were evaluated for feasibility, real-world impact, and relevance to our engineering curriculum. "
            "After careful discussion, we agreed on building Blast Master Pro — a mobile blast planning and safety calculator app "
            "designed to assist mining engineers in computing explosive quantities, hole geometry, and danger zones before any blast is executed on site."
        ),
        (
            "Week 2: Software Requirements Specification (SRS)",
            "The team collaborated to write the full Software Requirements Specification document. "
            "This involved defining functional requirements (blast calculations, safety alerts, rock type selection, water content input) "
            "and non-functional requirements (speed, accuracy, offline use). My personal contribution was writing the requirements for "
            "the blast calculation module — covering inputs such as rock density, hole diameter, blast area, water content, geology type, "
            "and terrain type, and defining the expected outputs: burden, spacing, subdrilling, explosive type, quantity, danger level, and throw distance."
        ),
        (
            "Week 3: Blast Calculation Engine Implementation",
            "I implemented the core blast calculation engine for Blast Master Pro. This covered all key blast design formulas: "
            "Burden (B = k·d), Spacing (S = 1.0–1.5 × B), Subdrilling (J = 0.2–0.3 × B), Stemming (T = 0.7–1.0 × B), "
            "Hole Depth (H = Hb + J), Explosive Charge per Hole (Q = ρ·A·L), Powder Factor (PF = Q/V), and Throw Distance. "
            "The engine also determines the correct explosive type (ANFO, Emulsion, Water Gel) based on terrain and water content, "
            "and computes the danger level (LOW / MEDIUM / HIGH / CRITICAL) to protect engineers, workers, and nearby community members. "
            "Each calculation was validated with error handling and unit checks to ensure accuracy for real mining conditions."
        ),
        (
            "Week 4: Firebase Integration, Safety Module & Final Merge",
            "In the final week, the team split into sub-groups. I was responsible for integrating Firebase into the blast calculator — "
            "storing blast session records (inputs + results) in Firestore so engineers can review past blasts and track patterns over time. "
            "I also contributed to the safety module, which generates a safety exclusion zone radius based on throw distance and danger level, "
            "with visual warnings displayed on screen. Once all modules were tested and verified, I submitted a pull request to merge my code "
            "into the main repository. The request was reviewed by the team lead, approved, and successfully merged into the final Blast Master Pro build."
        ),
    ]

    timeline_section = ft.Container(
        key="timeline",
        padding=symmetric_padding(horizontal=50, vertical=50),
        content=ft.Column(
            spacing=20,
            controls=[
                ft.Text("Project Timeline", size=42, weight=ft.FontWeight.BOLD, color=text),
                *[
                    ft.Container(
                        bgcolor=card, padding=24, border_radius=12, border=border_all(1, primary),
                        content=ft.Column(spacing=8, controls=[
                            ft.Text(week, size=23, weight=ft.FontWeight.BOLD, color=primary),
                            ft.Text(description, color=subtext, size=16),
                        ]),
                    )
                    for week, description in timeline_cards
                ],
            ],
        ),
    )

    matlab_section = ft.Container(
        key="matlab",
        bgcolor=panel,
        padding=symmetric_padding(horizontal=50, vertical=50),
        content=ft.Column(
            spacing=28,
            controls=[
                ft.Text("MATLAB Achievement Hub", size=42, weight=ft.FontWeight.BOLD, color=text),
                ft.Text(
                    "All 8 MathWorks certificates earned by Sindere Michael — click any card to view the full certificate.",
                    size=16, color=subtext,
                ),
                ft.Text("Onramp Certificates", size=20, weight=ft.FontWeight.BOLD, color=primary),
                ft.ResponsiveRow(
                    run_spacing=20,
                    controls=[
                        ft.Column(col={"md": 4, "sm": 6, "xs": 12}, controls=[cert_card(certificates[0])]),
                        ft.Column(col={"md": 4, "sm": 6, "xs": 12}, controls=[cert_card(certificates[1])]),
                        ft.Column(col={"md": 4, "sm": 6, "xs": 12}, controls=[cert_card(certificates[2])]),
                    ],
                ),
                ft.Text("Core MATLAB Skills — Learning Path & Courses", size=20, weight=ft.FontWeight.BOLD, color=primary),
                ft.ResponsiveRow(
                    run_spacing=20,
                    controls=[
                        ft.Column(col={"md": 4, "sm": 6, "xs": 12}, controls=[cert_card(certificates[3])]),
                        ft.Column(col={"md": 4, "sm": 6, "xs": 12}, controls=[cert_card(certificates[4])]),
                        ft.Column(col={"md": 4, "sm": 6, "xs": 12}, controls=[cert_card(certificates[5])]),
                        ft.Column(col={"md": 4, "sm": 6, "xs": 12}, controls=[cert_card(certificates[6])]),
                        ft.Column(col={"md": 4, "sm": 6, "xs": 12}, controls=[cert_card(certificates[7])]),
                    ],
                ),
            ],
        ),
    )

    blog_section = ft.Container(
        key="blog",
        padding=symmetric_padding(horizontal=50, vertical=50),
        content=ft.Column(
            spacing=24,
            controls=[
                ft.Text("Technical Blog", size=42, weight=ft.FontWeight.BOLD, color=text),
                ft.Text("Confidence in Concepts — written technical explanations with video inserts.",
                        size=16, color=subtext),
                ft.Container(
                    bgcolor=card,
                    border_radius=12,
                    padding=28,
                    border=border_all(1, secondary),
                    content=ft.Column(
                        spacing=14,
                        controls=[
                            ft.Icon(get_icon("CODE"), size=38, color=primary),
                            ft.Text("Confidence in Python OOP", size=22,
                                    weight=ft.FontWeight.BOLD, color=text),
                            ft.Text(
                                "Object Oriented Programming (OOP) is a programming approach that "
                                "organises code into classes and objects. A class is like a blueprint "
                                "and an object is an instance of that blueprint. For example in our "
                                "Ore Recognition App, we created a class called Ore that holds "
                                "properties like name, colour, and hardness.",
                                size=15, color=subtext,
                            ),
                            ft.Text(
                                "The three main pillars of OOP are inheritance, encapsulation and "
                                "polymorphism. Inheritance allows a child class to reuse code from a "
                                "parent class. Encapsulation hides internal data from outside access. "
                                "Polymorphism allows different classes to be used through the same "
                                "interface. We applied these concepts throughout our group project.",
                                size=15, color=subtext,
                            ),
                            ft.Text("Watch: Python OOP Explained", size=13,
                                    color=primary, italic=True),
                            ft.Button(
                                "▶ Watch Video",
                                bgcolor=primary,
                                color="#000000",
                                on_click=lambda _: __import__('webbrowser').open(
                                    "https://www.youtube.com/watch?v=JeznW_7DlB0"
                                ),
                            ),
                        ],
                    ),
                ),
                ft.Container(
                    bgcolor=card,
                    border_radius=12,
                    padding=28,
                    border=border_all(1, secondary),
                    content=ft.Column(
                        spacing=14,
                        controls=[
                            ft.Icon(get_icon("STORAGE"), size=38, color=primary),
                            ft.Text("Understanding Data Structures", size=22,
                                    weight=ft.FontWeight.BOLD, color=text),
                            ft.Text(
                                "Data structures are ways of organising and storing data in a program "
                                "so that it can be accessed and modified efficiently. The most common "
                                "data structures in Python are lists, stacks, queues and linked lists. "
                                "Choosing the right data structure is important because it directly "
                                "affects the performance of your application.",
                                size=15, color=subtext,
                            ),
                            ft.Text(
                                "A stack follows a Last In First Out (LIFO) principle — the last item "
                                "added is the first to be removed, like a stack of plates. A queue "
                                "follows First In First Out (FIFO) — like a line of people waiting. "
                                "A linked list stores data in nodes where each node points to the next. "
                                "In our Ore Recognition App we used lists and dictionaries to store "
                                "ore data fetched from Firebase before displaying it to the user.",
                                size=15, color=subtext,
                            ),
                            ft.Text("Watch: Data Structures Explained", size=13,
                                    color=primary, italic=True),
                            ft.Button(
                                "▶ Watch Video",
                                bgcolor=primary,
                                color="#000000",
                                on_click=lambda _: __import__('webbrowser').open(
                                    "https://www.youtube.com/watch?v=pkYVOmU3MgA"
                                ),
                            ),
                        ],
                    ),
                ),
                ft.Container(
                    bgcolor=card,
                    border_radius=12,
                    padding=28,
                    border=border_all(1, secondary),
                    content=ft.Column(
                        spacing=14,
                        controls=[
                            ft.Icon(get_icon("PLAY_CIRCLE"), size=38, color=primary),
                            ft.Text("Blast Master Pro — App Demo Video", size=22,
                                    weight=ft.FontWeight.BOLD, color=text),
                            ft.Text(
                                "Watch the Blast Master Pro app in action. This demo shows the full "
                                "blast calculation workflow — entering rock density, hole diameter, "
                                "blast area and water content, selecting geology and terrain type, "
                                "and receiving real-time outputs including burden, spacing, explosive "
                                "quantity, explosive type, danger level and throw distance.",
                                size=15, color=subtext,
                            ),
                            ft.Text("▶ Demo Video — Blast Master Pro in Action",
                                    size=13, color=primary, italic=True),
                            # Video opens with system default player (most reliable in Flet)
                            ft.Container(
                                bgcolor="#0d0221",
                                border_radius=12,
                                padding=30,
                                border=border_all(1, primary),
                                alignment=ft.Alignment.CENTER,
                                content=ft.Column(
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=16,
                                    controls=[
                                        ft.Icon(get_icon("SMART_DISPLAY"), size=64, color=primary),
                                        ft.Text("Blast Master Pro Demo", size=18,
                                                weight=ft.FontWeight.BOLD, color=text),
                                        ft.Text("Click the button below to play the demo video",
                                                size=13, color=subtext),
                                        ft.Button(
                                            "▶  Play Demo Video",
                                            bgcolor=primary,
                                            color="#000000",
                                            on_click=lambda _: __import__('os').startfile(
                                                __import__('os').path.join(
                                                    __import__('os').path.dirname(
                                                        __import__('os').path.abspath(__file__)),
                                                    "assets", "demo_video_small.mp4"
                                                )
                                            ) if __import__('os').name == "nt" else
                                            __import__('subprocess').Popen(
                                                ["xdg-open" if __import__('sys').platform == "linux"
                                                 else "open",
                                                 __import__('os').path.join(
                                                     __import__('os').path.dirname(
                                                         __import__('os').path.abspath(__file__)),
                                                     "assets", "demo_video_small.mp4")]
                                            ),
                                            style=ft.ButtonStyle(
                                                padding=ft.Padding(20, 12, 20, 12),
                                                text_style=ft.TextStyle(
                                                    size=16, weight=ft.FontWeight.BOLD),
                                            ),
                                        ),
                                        ft.Text("Duration: ~60 seconds | Format: MP4",
                                                size=11, color="#555555", italic=True),
                                    ],
                                ),
                            ),
                        ],
                    ),
                ),
                ft.Container(
                    bgcolor=card,
                    padding=28,
                    border_radius=12,
                    border=border_all(1, primary),
                    content=ft.Column(
                        spacing=16,
                        controls=[
                            ft.Icon(get_icon("FUNCTIONS"), size=38, color=primary),
                            ft.Text("Blast Design — Mathematical Notation", size=28,
                                    weight=ft.FontWeight.BOLD, color=primary),
                            ft.Text(
                                "When calculating total explosives for a blast, every parameter is interconnected. "
                                "Below are the key formulas used in Blast Master Pro, from hole geometry through to safety:",
                                size=15, color=subtext,
                            ),

                            # Group 1
                            ft.Text("① Hole Geometry & Layout", size=16, color=primary, weight=ft.FontWeight.BOLD),
                            ft.Text("Burden:      B = k · d", size=17, color=text, weight=ft.FontWeight.BOLD),
                            ft.Text("Spacing:     S = (1.0 – 1.5) · B", size=17, color=text, weight=ft.FontWeight.BOLD),
                            ft.Text("Subdrilling: J = (0.2 – 0.3) · B", size=17, color=text, weight=ft.FontWeight.BOLD),
                            ft.Text("Stemming:    T = (0.7 – 1.0) · B", size=17, color=text, weight=ft.FontWeight.BOLD),
                            ft.Text(
                                "Where d = hole diameter (m), k = geology factor (Hard=25–40, Medium=35–50, Soft=50–65).",
                                size=13, color=subtext, italic=True),

                            ft.Divider(color="#2a1a4a"),

                            # Group 2
                            ft.Text("② Hole Depth & Charge Length", size=16, color=primary, weight=ft.FontWeight.BOLD),
                            ft.Text("Total Depth:    H  = Hb + J", size=17, color=text, weight=ft.FontWeight.BOLD),
                            ft.Text("Charge Length:  Lc = H − T", size=17, color=text, weight=ft.FontWeight.BOLD),

                            ft.Divider(color="#2a1a4a"),

                            # Group 3
                            ft.Text("③ Explosive Calculations", size=16, color=primary, weight=ft.FontWeight.BOLD),
                            ft.Text("Hole Area:          A = π · d² / 4", size=17, color=text, weight=ft.FontWeight.BOLD),
                            ft.Text("Charge per Hole:    Q = ρ · A · Lc", size=17, color=text, weight=ft.FontWeight.BOLD),
                            ft.Text("Linear Density:     q = Q / Lc", size=17, color=text, weight=ft.FontWeight.BOLD),
                            ft.Text(
                                "Where ρ = explosive density (kg/m³), A = cross-sectional area of hole (m²).",
                                size=13, color=subtext, italic=True),

                            ft.Divider(color="#2a1a4a"),

                            # Group 4 & 5
                            ft.Text("④ Rock Volume & Efficiency", size=16, color=primary, weight=ft.FontWeight.BOLD),
                            ft.Text("Rock Volume:    V  = B × S × H", size=17, color=text, weight=ft.FontWeight.BOLD),
                            ft.Text("Powder Factor:  PF = Q / V  (kg/m³)", size=17, color=text, weight=ft.FontWeight.BOLD),

                            ft.Divider(color="#2a1a4a"),

                            # Group 6
                            ft.Text("⑤ Timing & Delay", size=16, color=primary, weight=ft.FontWeight.BOLD),
                            ft.Text("Delay Time:  t = k · B  (ms)", size=17, color=text, weight=ft.FontWeight.BOLD),

                            ft.Divider(color="#2a1a4a"),

                            # Final combined formula
                            ft.Text("⑥ Total Explosive Load (Final Result)", size=16, color=primary, weight=ft.FontWeight.BOLD),
                            ft.Container(
                                bgcolor="#0d0221",
                                border_radius=10,
                                padding=ft.Padding(20, 14, 20, 14),
                                border=border_all(1, primary),
                                content=ft.Text(
                                    "Q_total = ρ · (π·d²/4) · (H − T)  ×  N_holes",
                                    size=22, color=primary, weight=ft.FontWeight.BOLD,
                                ),
                            ),
                            ft.Text(
                                "Where N_holes = (Blast Area) / (B × S). "
                                "This final value tells the engineer exactly how many kilograms of explosive "
                                "are needed for the entire blast — factoring in rock type, water content, hole size, "
                                "and terrain to keep engineers, workers, and the nearby community safe.",
                                size=14, color=subtext,
                            ),
                        ],
                    ),
                ),
            ],
        ),
    )

    # ─── MEDIA BOX HELPER ─────────────────────────────────────────────────
    def media_box(title: str, description: str, icon_name: str,
                  image_path: str = "", video_url: str = ""):
        """
        Reusable evidence box.
        - image_path set  → loads image from disk (JPG or PNG).
        - video_url set   → shows a Watch button that opens the link.
        - Neither set     → dashed placeholder with upload hint.
        """
        if image_path:
            b64 = load_image_base64(image_path)
            media_content = ft.Image(
                src=f"data:image/jpeg;base64,{b64}",
                fit=ft.BoxFit.CONTAIN,
                width=460,
                height=260,
                border_radius=8,
            ) if b64 else ft.Text("Image not found", color="red", size=13)

        elif video_url:
            media_content = ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
                controls=[
                    ft.Icon(get_icon("PLAY_CIRCLE"), size=54, color=primary),
                    ft.Text("Video evidence attached", size=13, color=subtext),
                    ft.Button(
                        "▶ Watch Video",
                        bgcolor=primary,
                        color="#000000",
                        on_click=lambda _, u=video_url: __import__('webbrowser').open(u),
                        style=ft.ButtonStyle(
                            text_style=ft.TextStyle(size=13, weight=ft.FontWeight.BOLD)),
                    ),
                ],
            )
        else:
            # Dashed placeholder
            media_content = ft.Container(
                width=460,
                height=240,
                border_radius=8,
                border=ft.Border(
                    top=ft.BorderSide(2, "#444444"),
                    bottom=ft.BorderSide(2, "#444444"),
                    left=ft.BorderSide(2, "#444444"),
                    right=ft.BorderSide(2, "#444444"),
                ),
                alignment=ft.Alignment.CENTER,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=12,
                    controls=[
                        ft.Icon(get_icon("UPLOAD_FILE"), size=50, color="#555555"),
                        ft.Text("Upload your evidence here", size=14, color="#777777"),
                        ft.Text("screenshot · video · image",
                                size=12, color="#555555", italic=True),
                    ],
                ),
            )

        return ft.Container(
            bgcolor=card,
            border_radius=12,
            padding=24,
            border=border_all(1, secondary),
            content=ft.Column(
                spacing=14,
                controls=[
                    ft.Row(spacing=12, controls=[
                        ft.Icon(get_icon(icon_name), size=32, color=primary),
                        ft.Text(title, size=19, weight=ft.FontWeight.BOLD, color=text),
                    ]),
                    ft.Text(description, size=13, color=subtext),
                    ft.Divider(color="#2a1a4a", thickness=1),
                    media_content,
                ],
            ),
        )

    # ─── GITHUB SECTION (opens inside portfolio) ───────────────────────────
    github_section = ft.Container(
        key="github",
        bgcolor=panel,
        padding=symmetric_padding(horizontal=50, vertical=50),
        content=ft.Column(
            spacing=28,
            controls=[
                ft.Text("GitHub Evidence", size=42, weight=ft.FontWeight.BOLD, color=text),
                ft.Text(
                    "Your GitHub contributions for Blast Master Pro are displayed below. "
                    "To add your evidence, set image_path='assets/your_file.jpg' or "
                    "video_url='https://youtube.com/...' inside each box in the code.",
                    size=15, color=subtext,
                ),

                # ── Box 1: App Login & Splash Screen ──────────────────────
                ft.Text("📱 App Screenshots", size=18, color=primary, weight=ft.FontWeight.BOLD),
                ft.ResponsiveRow(
                    run_spacing=16,
                    controls=[
                        ft.Column(col={"md": 6, "sm": 12, "xs": 12}, controls=[
                            ft.Container(
                                bgcolor=card,
                                border_radius=12,
                                padding=16,
                                border=border_all(1, secondary),
                                content=ft.Column(spacing=10, controls=[
                                    ft.Text("BlastMaster Pro — Login Screen",
                                            size=15, weight=ft.FontWeight.BOLD, color=primary),
                                    ft.Text("Login page with Apple & Google authentication, "
                                            "built on top of a blast explosion background.",
                                            size=12, color=subtext),
                                    ft.Image(
                                        src="assets/app_login1.jpg",
                                        fit=ft.BoxFit.CONTAIN,
                                        border_radius=8,
                                        width=460, height=280,
                                    ),
                                ]),
                            )
                        ]),
                        ft.Column(col={"md": 6, "sm": 12, "xs": 12}, controls=[
                            ft.Container(
                                bgcolor=card,
                                border_radius=12,
                                padding=16,
                                border=border_all(1, secondary),
                                content=ft.Column(spacing=10, controls=[
                                    ft.Text("BlastMaster Pro — Mobile View",
                                            size=15, weight=ft.FontWeight.BOLD, color=primary),
                                    ft.Text("Mobile-responsive login screen showing email/password fields "
                                            "and social login options.",
                                            size=12, color=subtext),
                                    ft.Image(
                                        src="assets/app_login2.jpg",
                                        fit=ft.BoxFit.CONTAIN,
                                        border_radius=8,
                                        width=460, height=280,
                                    ),
                                ]),
                            )
                        ]),
                    ],
                ),

                ft.ResponsiveRow(
                    run_spacing=16,
                    controls=[
                        ft.Column(col={"md": 6, "sm": 12, "xs": 12}, controls=[
                            ft.Container(
                                bgcolor=card,
                                border_radius=12,
                                padding=16,
                                border=border_all(1, secondary),
                                content=ft.Column(spacing=10, controls=[
                                    ft.Text("Blast Assist — Splash Screen",
                                            size=15, weight=ft.FontWeight.BOLD, color=primary),
                                    ft.Text("App splash screen showing the Blast Assist branding — "
                                            "Safety Blasting Arrangement App.",
                                            size=12, color=subtext),
                                    ft.Image(
                                        src="assets/app_splash.jpg",
                                        fit=ft.BoxFit.CONTAIN,
                                        border_radius=8,
                                        width=460, height=280,
                                    ),
                                ]),
                            )
                        ]),
                        ft.Column(col={"md": 6, "sm": 12, "xs": 12}, controls=[
                            ft.Container(
                                bgcolor=card,
                                border_radius=12,
                                padding=16,
                                border=border_all(1, secondary),
                                content=ft.Column(spacing=10, controls=[
                                    ft.Text("Blast Calculator — Live Results",
                                            size=15, weight=ft.FontWeight.BOLD, color=primary),
                                    ft.Text("Calculator screen showing real outputs: Burden 3.50m, "
                                            "Spacing 4.02m, Explosive 616.33kg, Type ANFO, Danger LOW.",
                                            size=12, color=subtext),
                                    ft.Image(
                                        src="assets/app_calculator.jpg",
                                        fit=ft.BoxFit.CONTAIN,
                                        border_radius=8,
                                        width=460, height=280,
                                    ),
                                ]),
                            )
                        ]),
                    ],
                ),

                # ── Box 2: Commit History (placeholder) ───────────────────
                media_box(
                    title="Commit History",
                    description="Upload a screenshot of your GitHub commits page showing your "
                                "weekly contributions to the Blast Master Pro repository. "
                                "Set image_path='assets/commits.jpg' when ready.",
                    icon_name="HISTORY",
                    image_path="",
                    video_url="",
                ),

                # ── Box 3: Pull Request (placeholder) ─────────────────────
                media_box(
                    title="Pull Request & Merge",
                    description="Upload a screenshot of your pull request being reviewed and merged "
                                "into the main branch. Set image_path='assets/pull_request.jpg' when ready.",
                    icon_name="MERGE_TYPE",
                    image_path="",
                    video_url="",
                ),
            ],
        ),
    )

    contact_section = ft.Container(
        key="contact",
        padding=symmetric_padding(horizontal=50, vertical=60),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            controls=[
                ft.Text("Contact Me", size=42, weight=ft.FontWeight.BOLD, color=text),
                ft.Text("Available for freelance work and engineering projects.", size=18, color=subtext, text_align=ft.TextAlign.CENTER),
                ft.TextField(width=500, label="Your Name",  bgcolor=card, border_color=primary, color=text),
                ft.TextField(width=500, label="Your Email", bgcolor=card, border_color=primary, color=text),
                ft.TextField(width=500, min_lines=4, max_lines=6, multiline=True, label="Message", bgcolor=card, border_color=primary, color=text),
                ft.Button("Send Message", bgcolor=primary, color="#000000"),
            ],
        ),
    )

    footer = ft.Container(
        padding=30,
        alignment=ft.Alignment.CENTER,
        content=ft.Text("(c) 2026 Sindere Michael Portfolio - All Rights Reserved", color=subtext),
    )

    pages = {
        "home":     [hero_section, features],
        "about":    [about_section, stats],
        "timeline": [timeline_section],
        "matlab":   [matlab_section],
        "blog":     [blog_section],
        "github":   [github_section],
        "contact":  [contact_section],
    }

    def render_route(_=None):
        section  = page.route.strip("/") or "home"
        controls = pages.get(section, pages["home"])
        page.controls.clear()
        page.add(ft.Column(spacing=0, controls=[*controls, footer]))
        page.update()

    page.on_route_change = render_route
    render_route()


if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, web_renderer=ft.WebRenderer.CANVAS_KIT, port=int(__import__('os').environ.get('PORT', 8550)), host="0.0.0.0")

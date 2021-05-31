from operator import attrgetter
from typing import Dict, List, Tuple

from rich import box
from rich.console import RenderGroup
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TaskID, TextColumn
from rich.table import Table
from rich.tree import Tree

from ..config import get_label_colour_map
from ..source_control import PullRequest


def render_repository_does_not_exist(
    title: str,
    org: str,
    repository: str,
) -> Table:
    """Renders a list of pull requests as a table"""
    table = Table(show_header=True, header_style="bold white")
    table.add_column("#", style="dim", width=7)
    table.add_column(
        f"[link=https://www.github.com/{org}/{repository}]{title}[/link]",
        width=160,
    )

    table.add_row(
        "",
        (
            "Please confirm this repository exists and that you can access it "
            "before attempting to use it."
        ),
    )

    return table


def render_pull_request_table(
    title: str,
    pull_requests: List[PullRequest],
    org: str,
    repository: str,
) -> Table:
    """Renders a list of pull requests as a table"""
    table = Table(show_header=True, header_style="bold white")
    table.add_column("#", style="dim", width=5)
    table.add_column(
        f"[link=https://www.github.com/{org}/{repository}]{title}[/link]",
        width=75,
    )
    table.add_column("Labels", width=30)
    table.add_column("Diff +/-", width=10)
    table.add_column("Activity", width=15)
    table.add_column("Approved", width=10)
    table.add_column("Mergeable", width=10)

    label_colour_map = get_label_colour_map()

    for pr in sorted(pull_requests, key=attrgetter("updated_at"), reverse=True):
        table.add_row(
            f"[white]{pr.number} ",
            pr.render_title(org, repository),
            pr.render_labels(label_colour_map),
            pr.render_diff(),
            pr.render_updated_at(),
            pr.render_approved(),
            pr.render_approved_by_others(),
        )

    return table


def generate_layout(log: bool = True, footer: bool = True) -> Layout:
    """Define the layout for the terminal UI."""
    layout = Layout(name="root")

    sections = [Layout(name="header", size=3), Layout(name="main", ratio=1)]
    if footer:
        sections.append(Layout(name="footer", size=7))
    layout.split(*sections)

    layout["main"].split_row(  # type: ignore
        Layout(name="left_side", size=40),
        Layout(name="body", ratio=2, minimum_size=90),
    )

    nav_sections = [Layout(name="configuration")]
    if log:
        nav_sections.append(Layout(name="log"))

    layout["left_side"].split(*nav_sections)

    return layout


def generate_tree_layout(configuration: List[Tuple[str, str]]) -> RenderGroup:
    """Generates a tree layout for the settings configuration"""
    organization_tree_mapping: Dict[str, Tree] = {}
    for (org, repo) in configuration:
        tree = organization_tree_mapping.get(f"{org}", Tree(f"[white]{org}"))
        tree.add(f"[link=https://www.github.com/{org}/{repo}]{repo}[/link]")
        organization_tree_mapping[org] = tree

    return RenderGroup(*organization_tree_mapping.values())


def generate_log_table(logs: List[Tuple[str, str]]) -> Table:
    """Generetes a table for logging activity"""
    table = Table("Time", "Message", box=box.SIMPLE)

    if logs:
        for log in logs:
            time, message = log
            table.add_row(time, message)

    return table


def generate_progress_tracker() -> Tuple[Progress, Progress, TaskID, Table]:
    """Tracks the progress of tasks"""
    progress = Progress(
        "{task.description}",
        SpinnerColumn(),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    )
    progress.add_task("[white]Pull Requests", total=100)

    total = sum(task.total for task in progress.tasks)
    overall_progress = Progress()
    overall_task = overall_progress.add_task(description="All", total=int(total))

    progress_table = Table.grid(expand=True)
    progress_table.add_row(
        Panel(
            renderable=overall_progress,  # type: ignore
            title="Next Refresh",
            border_style="blue",
        ),
        Panel(
            renderable=progress,  # type: ignore
            title="[b]Next fetch for:",
            border_style="blue",
            padding=(1, 2),
        ),
    )

    return progress, overall_progress, overall_task, progress_table

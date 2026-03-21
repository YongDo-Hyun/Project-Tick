#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Set, Tuple


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_GRAPH = ROOT / "tools" / "ci" / "dependency-graph.json"


class GraphError(RuntimeError):
    pass


@dataclass(frozen=True)
class Node:
    name: str
    description: str
    paths: Tuple[str, ...]
    depends_on: Tuple[str, ...]
    runner: str | None


@dataclass(frozen=True)
class Graph:
    global_paths: Tuple[str, ...]
    runners: Dict[str, Dict[str, str]]
    nodes: Dict[str, Node]


@dataclass(frozen=True)
class Plan:
    changed_files: Tuple[str, ...]
    matched_files: Dict[str, Tuple[str, ...]]
    unmatched_files: Tuple[str, ...]
    global_match: bool
    changed_nodes: Tuple[str, ...]
    impacted_nodes: Tuple[str, ...]
    runners: Tuple[str, ...]
    unwired_nodes: Tuple[str, ...]


def _normalize_path(value: str) -> str:
    cleaned = value.strip().replace("\\", "/")
    if cleaned.startswith("./"):
        cleaned = cleaned[2:]
    while "//" in cleaned:
        cleaned = cleaned.replace("//", "/")
    return cleaned


def load_graph(path: Path) -> Graph:
    payload = json.loads(path.read_text(encoding="utf-8"))
    nodes: Dict[str, Node] = {}
    runners = payload.get("runners", {})

    for name, raw_node in payload["nodes"].items():
        nodes[name] = Node(
            name=name,
            description=raw_node.get("description", ""),
            paths=tuple(_normalize_path(item) for item in raw_node.get("paths", [])),
            depends_on=tuple(raw_node.get("depends_on", [])),
            runner=raw_node.get("runner"),
        )

    graph = Graph(
        global_paths=tuple(_normalize_path(item) for item in payload.get("global_paths", [])),
        runners=runners,
        nodes=nodes,
    )
    validate_graph(graph)
    return graph


def validate_graph(graph: Graph) -> None:
    for node in graph.nodes.values():
        if not node.paths:
            raise GraphError(f"Node '{node.name}' must declare at least one path.")
        for dependency in node.depends_on:
            if dependency not in graph.nodes:
                raise GraphError(
                    f"Node '{node.name}' depends on unknown node '{dependency}'."
                )
        if node.runner and node.runner not in graph.runners:
            raise GraphError(
                f"Node '{node.name}' references unknown runner '{node.runner}'."
            )

    visiting: Set[str] = set()
    visited: Set[str] = set()

    def walk(name: str, stack: List[str]) -> None:
        if name in visited:
            return
        if name in visiting:
            cycle = " -> ".join(stack + [name])
            raise GraphError(f"Dependency graph contains a cycle: {cycle}")

        visiting.add(name)
        stack.append(name)
        for dependency in graph.nodes[name].depends_on:
            walk(dependency, stack)
        stack.pop()
        visiting.remove(name)
        visited.add(name)

    for node_name in graph.nodes:
        walk(node_name, [])


def build_dependents(graph: Graph) -> Dict[str, Set[str]]:
    dependents = {name: set() for name in graph.nodes}
    for node in graph.nodes.values():
        for dependency in node.depends_on:
            dependents[dependency].add(node.name)
    return dependents


def path_matches(pattern: str, changed_file: str) -> bool:
    if pattern.endswith("/"):
        return changed_file == pattern[:-1] or changed_file.startswith(pattern)
    return changed_file == pattern or changed_file.startswith(pattern + "/")


def plan_changes(graph: Graph, changed_files: Sequence[str], default_all_if_empty: bool) -> Plan:
    normalized_files = tuple(
        sorted({_normalize_path(item) for item in changed_files if _normalize_path(item)})
    )
    matched_files: Dict[str, List[str]] = {}
    unmatched_files: List[str] = []
    global_match = False

    if not normalized_files and default_all_if_empty:
        impacted = tuple(sorted(graph.nodes))
        runners = tuple(
            runner for runner in sorted(graph.runners) if runner in {n.runner for n in graph.nodes.values()}
        )
        unwired = tuple(sorted(name for name in impacted if graph.nodes[name].runner is None))
        return Plan(
            changed_files=normalized_files,
            matched_files={},
            unmatched_files=(),
            global_match=False,
            changed_nodes=(),
            impacted_nodes=impacted,
            runners=runners,
            unwired_nodes=unwired,
        )

    changed_nodes: Set[str] = set()
    for changed_file in normalized_files:
        if any(path_matches(pattern, changed_file) for pattern in graph.global_paths):
            global_match = True

        matched = False
        for node in graph.nodes.values():
            if any(path_matches(pattern, changed_file) for pattern in node.paths):
                changed_nodes.add(node.name)
                matched_files.setdefault(node.name, []).append(changed_file)
                matched = True
        if not matched and not any(path_matches(pattern, changed_file) for pattern in graph.global_paths):
            unmatched_files.append(changed_file)

    dependents = build_dependents(graph)
    impacted_set: Set[str] = set(graph.nodes) if global_match else set(changed_nodes)
    queue = list(impacted_set)
    while queue:
        current = queue.pop()
        for dependent in dependents[current]:
            if dependent not in impacted_set:
                impacted_set.add(dependent)
                queue.append(dependent)

    impacted_nodes = tuple(sorted(impacted_set))
    runner_names = tuple(
        sorted(
            {
                graph.nodes[name].runner
                for name in impacted_nodes
                if graph.nodes[name].runner is not None
            }
        )
    )
    unwired_nodes = tuple(
        sorted(name for name in impacted_nodes if graph.nodes[name].runner is None)
    )

    return Plan(
        changed_files=normalized_files,
        matched_files={key: tuple(sorted(values)) for key, values in sorted(matched_files.items())},
        unmatched_files=tuple(sorted(unmatched_files)),
        global_match=global_match,
        changed_nodes=tuple(sorted(changed_nodes)),
        impacted_nodes=impacted_nodes,
        runners=runner_names,
        unwired_nodes=unwired_nodes,
    )


def make_mermaid(graph: Graph, plan: Plan) -> str:
    lines = ["flowchart LR"]
    changed = set(plan.changed_nodes)
    impacted = set(plan.impacted_nodes)

    for name in sorted(graph.nodes):
        label = name.replace('"', '\\"')
        lines.append(f'  {slug(name)}["{label}"]')
    for node in graph.nodes.values():
        for dependency in node.depends_on:
            lines.append(f"  {slug(dependency)} --> {slug(node.name)}")

    lines.append("  classDef changed fill:#f59e0b,stroke:#92400e,color:#111827")
    lines.append("  classDef impacted fill:#2563eb,stroke:#1d4ed8,color:#ffffff")
    lines.append("  classDef unwired fill:#f3f4f6,stroke:#6b7280,color:#111827")

    if changed:
        lines.append("  class " + ",".join(slug(item) for item in sorted(changed)) + " changed")

    impacted_only = impacted - changed
    if impacted_only:
        lines.append(
            "  class " + ",".join(slug(item) for item in sorted(impacted_only)) + " impacted"
        )

    if plan.unwired_nodes:
        lines.append(
            "  class "
            + ",".join(slug(item) for item in sorted(plan.unwired_nodes))
            + " unwired"
        )

    return "\n".join(lines)


def slug(value: str) -> str:
    return value.replace("-", "_").replace(".", "_").replace("/", "_")


def make_summary(graph: Graph, plan: Plan) -> str:
    lines: List[str] = ["## CI Dependency Plan", ""]

    if plan.changed_files:
        lines.append(f"Changed files: `{len(plan.changed_files)}`")
        lines.append("")
        for item in plan.changed_files:
            lines.append(f"- `{item}`")
    else:
        lines.append("Changed files: none supplied")

    if plan.global_match:
        lines.append("")
        lines.append(
            "Global CI paths matched, so the planner fanned out to the full component graph."
        )

    lines.append("")
    lines.append("Changed nodes:")
    if plan.changed_nodes:
        for item in plan.changed_nodes:
            lines.append(f"- `{item}`")
    else:
        lines.append("- none")

    lines.append("")
    lines.append("Impacted nodes:")
    if plan.impacted_nodes:
        for item in plan.impacted_nodes:
            lines.append(f"- `{item}`")
    else:
        lines.append("- none")

    lines.append("")
    lines.append("Runnable lanes:")
    if plan.runners:
        for item in plan.runners:
            description = graph.runners.get(item, {}).get("description", "")
            suffix = f" - {description}" if description else ""
            lines.append(f"- `{item}`{suffix}")
    else:
        lines.append("- none")

    lines.append("")
    lines.append("Impacted but not yet wired to a lane:")
    if plan.unwired_nodes:
        for item in plan.unwired_nodes:
            lines.append(f"- `{item}`")
    else:
        lines.append("- none")

    if plan.unmatched_files:
        lines.append("")
        lines.append("Changed files without a node match:")
        for item in plan.unmatched_files:
            lines.append(f"- `{item}`")

    lines.append("")
    lines.append("```mermaid")
    lines.append(make_mermaid(graph, plan))
    lines.append("```")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Resolve CI dependency graph impact.")
    parser.add_argument(
        "--graph",
        type=Path,
        default=DEFAULT_GRAPH,
        help="Path to the dependency graph JSON file.",
    )
    parser.add_argument(
        "--changed-file",
        action="append",
        default=[],
        help="A changed file path. Can be passed multiple times.",
    )
    parser.add_argument(
        "--changed-files-json",
        help="JSON array of changed files.",
    )
    parser.add_argument(
        "--changed-files-json-file",
        type=Path,
        help="Path to a JSON array containing changed files.",
    )
    parser.add_argument(
        "--default-all-if-empty",
        action="store_true",
        help="Treat an empty changed-file set as a full graph fanout.",
    )
    parser.add_argument(
        "--summary-file",
        type=Path,
        help="Write the markdown summary to this path.",
    )
    parser.add_argument(
        "--write-github-output",
        action="store_true",
        help="Emit GitHub Actions outputs to the file pointed at by GITHUB_OUTPUT.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print the plan as JSON instead of markdown.",
    )
    return parser.parse_args()


def collect_changed_files(args: argparse.Namespace) -> List[str]:
    files = list(args.changed_file)
    if args.changed_files_json:
        files.extend(json.loads(args.changed_files_json))
    if args.changed_files_json_file:
        files.extend(json.loads(args.changed_files_json_file.read_text(encoding="utf-8")))
    return files


def write_github_output(graph: Graph, plan: Plan) -> None:
    import os

    output_path = Path(os.environ["GITHUB_OUTPUT"])
    payload = {
        "changed_nodes": json.dumps(list(plan.changed_nodes)),
        "impacted_nodes": json.dumps(list(plan.impacted_nodes)),
        "runners": json.dumps(list(plan.runners)),
        "unwired_nodes": json.dumps(list(plan.unwired_nodes)),
        "global_match": "true" if plan.global_match else "false",
        "has_work": "true" if plan.runners else "false",
    }

    for runner_name in graph.runners:
        payload[f"run_{runner_name}"] = "true" if runner_name in plan.runners else "false"

    with output_path.open("a", encoding="utf-8") as handle:
        for key, value in payload.items():
            handle.write(f"{key}={value}\n")


def main() -> int:
    args = parse_args()
    graph = load_graph(args.graph)
    changed_files = collect_changed_files(args)
    plan = plan_changes(graph, changed_files, args.default_all_if_empty)

    summary = make_summary(graph, plan)
    if args.summary_file:
        args.summary_file.write_text(summary, encoding="utf-8")

    if args.write_github_output:
        write_github_output(graph, plan)

    if args.json:
        print(
            json.dumps(
                {
                    "changed_files": list(plan.changed_files),
                    "changed_nodes": list(plan.changed_nodes),
                    "impacted_nodes": list(plan.impacted_nodes),
                    "runners": list(plan.runners),
                    "unwired_nodes": list(plan.unwired_nodes),
                    "global_match": plan.global_match,
                    "unmatched_files": list(plan.unmatched_files),
                    "matched_files": {key: list(values) for key, values in plan.matched_files.items()},
                },
                indent=2,
                sort_keys=True,
            )
        )
    else:
        print(summary, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

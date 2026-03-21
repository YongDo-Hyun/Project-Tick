from __future__ import annotations

import unittest
from pathlib import Path

from tools.ci.plan_dependency_graph import DEFAULT_GRAPH, load_graph, plan_changes


class DependencyGraphPlannerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.graph = load_graph(Path(DEFAULT_GRAPH))

    def test_ptlibzippy_change_fans_out_to_launcher_and_shims(self) -> None:
        plan = plan_changes(
            self.graph,
            ["ptlibzippy/contrib/minizip/CMakeLists.txt"],
            default_all_if_empty=False,
        )

        self.assertEqual(plan.changed_nodes, ("ptlibzippy",))
        self.assertEqual(
            plan.impacted_nodes,
            (
                "libnbtplusplus",
                "libpng",
                "projt-launcher",
                "projt-launcher-quazip",
                "ptlibzippy",
            ),
        )
        self.assertEqual(plan.runners, ("launcher", "libnbtplusplus", "libpng"))

    def test_forgewrapper_change_fans_out_to_meta(self) -> None:
        plan = plan_changes(
            self.graph,
            ["forgewrapper/src/main/java/example/App.java"],
            default_all_if_empty=False,
        )

        self.assertEqual(plan.changed_nodes, ("forgewrapper",))
        self.assertEqual(plan.impacted_nodes, ("forgewrapper", "meta"))
        self.assertEqual(plan.runners, ("forgewrapper", "meta"))

    def test_localpeer_change_fans_out_to_launcher(self) -> None:
        plan = plan_changes(
            self.graph,
            ["LocalPeer/src/LocalPeer.cpp"],
            default_all_if_empty=False,
        )

        self.assertEqual(plan.changed_nodes, ("localpeer",))
        self.assertEqual(plan.impacted_nodes, ("localpeer", "projt-launcher"))
        self.assertEqual(plan.runners, ("launcher", "localpeer"))

    def test_global_ci_change_fans_out_to_all_runners(self) -> None:
        plan = plan_changes(
            self.graph,
            [".github/workflows/ci-graph-plan.yml"],
            default_all_if_empty=False,
        )

        self.assertTrue(plan.global_match)
        self.assertEqual(plan.changed_files, (".github/workflows/ci-graph-plan.yml",))
        self.assertEqual(
            plan.runners,
            (
                "bzip2",
                "dockerimages",
                "forgewrapper",
                "gamemode",
                "javaloader",
                "launcher",
                "libnbtplusplus",
                "libpng",
                "localpeer",
                "meta",
                "modpacks",
                "murmur2",
                "qdcss",
                "rainbow",
                "systeminfo",
                "uvim",
            ),
        )


if __name__ == "__main__":
    unittest.main()

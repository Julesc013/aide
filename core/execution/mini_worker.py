"""Optional Mini DefaultAgent binding; the existing host owns execution and effects.

This module imports no optional SDK until an explicitly enabled attempt. It is
not a sandbox, provider grant, installer, scheduler or acceptance authority.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import importlib
import importlib.metadata
import json
import os
from pathlib import Path
import re
import sys

from core.execution.managed_workspace import digest, file_digest, ordinary, root_path


class MiniRefused(ValueError):
    pass


@dataclass(frozen=True)
class MiniAttempt:
    work_unit: str
    attempt_id: str
    source_revision: str
    recipe_sha256: str
    task: str
    step_limit: int = 4
    wall_time_limit_seconds: int = 30
    cost_limit: float = 0.01

    def validate(self):
        for value in (self.work_unit, self.attempt_id):
            if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,127}", value):
                raise MiniRefused("bounded work and attempt identities required")
        if not re.fullmatch(r"[0-9a-f]{40}", self.source_revision):
            raise MiniRefused("exact source revision required")
        if not re.fullmatch(r"[0-9a-f]{64}", self.recipe_sha256):
            raise MiniRefused("exact recipe digest required")
        if not self.task or len(self.task.encode("utf-8")) > 65536:
            raise MiniRefused("bounded nonempty task required")
        if (type(self.step_limit) is not int or not 1 <= self.step_limit <= 100
                or type(self.wall_time_limit_seconds) is not int
                or not 1 <= self.wall_time_limit_seconds <= 120
                or type(self.cost_limit) not in (float, int)
                or not 0 < self.cost_limit <= 100):
            raise MiniRefused("finite positive attempt limits required")


def verify_dependencies(dependencies: Path, recipe: dict, expected_digest: str):
    """Check an already extracted, controller-owned recipe; never acquire code."""
    if digest(recipe) != expected_digest or recipe.get("mini_version") != "2.4.6":
        raise MiniRefused("unqualified or changed Mini recipe")
    dependencies = root_path(str(dependencies))
    expected = recipe["files"]
    if not expected or len(expected) > 4000:
        raise MiniRefused("bounded dependency inventory required")
    observed = {}
    total = 0
    for path in dependencies.rglob("*"):
        if path.is_dir():
            ordinary(path, directory=True)
            continue
        info = ordinary(path)
        total += info.st_size
        if total > 24 * 1024 * 1024 or len(observed) >= 4000:
            raise MiniRefused("dependency inventory exceeds bounds")
        observed[path.relative_to(dependencies).as_posix()] = file_digest(path)
    if observed != expected:
        raise MiniRefused("missing, additional or altered dependency file")
    versions = {d.metadata["Name"].lower().replace("_", "-"): d.version
                for d in importlib.metadata.distributions(path=[str(dependencies)])}
    if versions != recipe["distributions"]:
        raise MiniRefused("dependency distribution identity differs")
    return dependencies


def run_attempt(spec: MiniAttempt, model, environment, *, enabled: bool,
                dependencies: Path, recipe: dict, attempt_root: Path) -> dict:
    """Run one fresh loop and preserve its result; submission is only a candidate.

    Caller supplies approved Model/Environment implementations and supervision.
    Costs in Mini's trajectory are not a hard billing limit or complete usage.
    A pre-existing attempt directory refuses replay before any model/environment
    call. Recovery requires the supervisor to inspect retained effects.
    """
    if enabled is not True:
        raise MiniRefused("optional Mini worker disabled")
    spec.validate()
    if not sys.flags.isolated or not sys.dont_write_bytecode:
        raise MiniRefused("fresh isolated interpreter without bytecode required")
    if any(name == "minisweagent" or name.startswith("minisweagent.")
           for name in sys.modules):
        raise MiniRefused("one fresh Mini attempt per interpreter required")
    dependencies = verify_dependencies(dependencies, recipe, spec.recipe_sha256)
    if any(name.split(".", 1)[0] in recipe["module_roots"] for name in sys.modules):
        raise MiniRefused("optional dependencies must not be preloaded")
    attempt_root = Path(attempt_root)
    root_path(str(attempt_root.parent))
    if attempt_root.name != spec.attempt_id:
        raise MiniRefused("attempt directory must match identity")
    attempt_root.mkdir(exist_ok=False)
    config = attempt_root / "config"
    config.mkdir()
    trajectory = attempt_root / "trajectory.json"
    receipt = {"schema": "aide.mini-attempt.v1", "identity": asdict(spec),
               "status": "INCOMPLETE", "candidate_submitted": False,
               "accepted": False, "model_usage": None, "model_queries": None,
               "trajectory_sha256": None}
    result_path = attempt_root / "attempt.json"

    def save():
        result_path.write_text(json.dumps(receipt, indent=2) + "\n",
                               encoding="utf-8", newline="\n")

    save()
    # Mini reads this exact .env at import. The directory is new and empty.
    os.environ.update(MSWEA_GLOBAL_CONFIG_DIR=str(config), MSWEA_SILENT_STARTUP="1")
    sys.path.insert(0, str(dependencies))
    agent = None
    try:
        module = importlib.import_module("minisweagent.agents.default")
        if Path(module.__file__).resolve() != dependencies / "minisweagent/agents/default.py":
            raise MiniRefused("unexpected Mini module origin")
        for name, imported in tuple(sys.modules.items()):
            if name.split(".", 1)[0] in recipe["module_roots"]:
                origin = getattr(imported, "__file__", None)
                if not origin or not Path(origin).resolve().is_relative_to(dependencies):
                    raise MiniRefused("unexpected dependency module origin")
        agent = module.DefaultAgent(
            model, environment, system_template="Complete the bounded task.",
            instance_template="{{ task }}", step_limit=spec.step_limit,
            cost_limit=spec.cost_limit, wall_time_limit_seconds=spec.wall_time_limit_seconds,
            max_consecutive_format_errors=2, output_path=trajectory)
        outcome = agent.run(spec.task)
        receipt.update(status="TERMINAL", exit_status=outcome.get("exit_status"),
                       candidate_submitted=outcome.get("exit_status") == "Submitted")
        return receipt
    except BaseException as exc:
        receipt.update(status="INTERRUPTED" if isinstance(exc, (KeyboardInterrupt, SystemExit))
                       else "FAILED", error_type=type(exc).__name__)
        raise
    finally:
        if agent is not None:
            receipt["model_queries"] = agent.n_calls
        if trajectory.is_file():
            receipt["trajectory_sha256"] = file_digest(trajectory)
        save()


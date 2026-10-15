#!/usr/bin/env python3
"""Build independent design vendor plugins from the pinned design-tools inventory.

The umbrella plugin keeps its original bundle for compatibility. Each exported plugin
gets its own vendored resources, license evidence, overview, Claude commands, and
Codex skills. Run --check to detect drift without changing files.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from vendor_utils import PLUGIN, tree_hash


ROOT = PLUGIN.parent.parent
REGISTRY = json.loads((PLUGIN / "registry/tools.json").read_text())
LOCK = json.loads((PLUGIN / "vendors/LOCK.json").read_text())
OVERVIEWS = json.loads((PLUGIN / "registry/vendor-plugin-overviews.json").read_text())
LEDGER = (PLUGIN / "third-party/README.md").read_text()
VERSION = "0.1.1"


def plugin_name(vendor: str) -> str:
    return vendor if vendor.startswith("design-") else f"design-{vendor}"


def write(path: Path, content: str, check: bool, errors: list[str]) -> None:
    if check:
        if not path.is_file() or path.read_text(encoding="utf-8") != content:
            errors.append(f"outdated: {path.relative_to(ROOT)}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, payload: object, check: bool, errors: list[str]) -> None:
    write(path, json.dumps(payload, indent=2, ensure_ascii=False) + "\n", check, errors)


def copy_dir(src: Path, dest: Path, check: bool, errors: list[str]) -> None:
    if check:
        if not dest.is_dir() or tree_hash(src) != tree_hash(dest):
            errors.append(f"copy differs: {dest.relative_to(ROOT)}")
        return
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest, symlinks=False, ignore=shutil.ignore_patterns(".git", "__pycache__", ".DS_Store"))


def skill_yaml(name: str, description: str, implicit: bool = False) -> str:
    policy = "" if implicit else "policy:\n  allow_implicit_invocation: false\n"
    return ("interface:\n"
            f"  display_name: {json.dumps(name, ensure_ascii=False)}\n"
            f"  short_description: {json.dumps(description[:120], ensure_ascii=False)}\n"
            + policy)


def overview(vendor: str, tools: list[str], plugin: str) -> str:
    info = OVERVIEWS[vendor]
    rows = []
    for tool in tools:
        meta = REGISTRY["tools"][tool]
        use_case = meta["does"].replace("|", "\\|")
        rows.append(f"| `{tool}` | `/{plugin}:{tool}` | `${plugin}:{tool}` | {use_case} |")
    examples = "\n".join(
        f"- `{('/' + plugin + ':' + tool)}` или `${plugin}:{tool}` — {usecase}."
        for tool, usecase in info["examples"]
    )
    return (f"# {REGISTRY['vendors'][vendor]['display']} — {plugin}\n\n"
            f"{info['summary']}\n\n"
            f"**Как работает.** {info['workflow']}\n\n"
            "**Пустой вызов.** Покажи этот краткий разбор, примеры ниже и при необходимости полный каталог. "
            "Не запускай скилл и не меняй проект без конкретной задачи.\n\n"
            "**Явный вызов.** В Codex выберите навык через `$`; в Claude Code используйте команду `/`. "
            f"Для обзора: `${plugin}:overview` или `/{plugin}:overview`. "
            "Упоминание `@` прикладывает плагин к контексту и не заменяет выбор навыка.\n\n"
            "**Примеры задач:**\n\n" + examples + "\n\n"
            f"**Ограничения.** {info['limits']}\n\n"
            "## Все отдельные скиллы\n\n"
            "Каждая строка указывает прямой вызов и задачу, для которой подходит скилл. "
            "Для запуска добавьте цель или файл после команды/навыка.\n\n"
            "| Скилл | Команда Claude Code | Навык Codex | Применение |\n"
            "| --- | --- | --- | --- |\n"
            + "\n".join(rows) + "\n")


def direct_skill(vendor: str, tool: str, plugin: str) -> str:
    meta = REGISTRY["tools"][tool]
    base = meta.get("base")
    steps = []
    if base and base != tool:
        steps.append(f"1. Сначала прочитай `../../vendors/{base}/SKILL.md`.")
    steps.append(f"{len(steps) + 1}. Прочитай `../../vendors/{tool}/SKILL.md` и следуй процедуре для указанной пользователем цели.")
    contract = REGISTRY["vendors"][vendor]["contract"]
    extra = ("Для Impeccable запускай launcher из абсолютного пути к `../../vendors/impeccable/scripts/impeccable` "
             "при cwd проекта; не используй относительный `.claude/skills/impeccable` путь.\n\n") if vendor == "impeccable" else ""
    return (f"---\nname: {tool}\n"
            f"description: {json.dumps('Use ' + REGISTRY['vendors'][vendor]['display'] + ' skill ' + tool + ' for ' + (meta.get('for') or meta['does']), ensure_ascii=False)}\n"
            "---\n\n"
            f"# {tool}\n\n"
            "Если пользователь вызвал навык без цели, файла и инструкций, прочитай `../../OVERVIEW.md` "
            "и дай короткий обзор возможностей, прямых вызовов и примеров применения. Ничего не запускай и не меняй.\n\n"
            "При конкретной задаче этот вендорский скилл уже выбран:\n\n"
            f"Контракт вендора: {contract}\n\n" + extra
            + "\n".join(steps) + "\n\n"
            "Относительные ссылки исходного скилла разрешай из его папки в `../../vendors/`. "
            "Slash-команды в исходном тексте относятся к Claude Code, не к Codex. "
            f"Полный каталог пакета: `../../OVERVIEW.md`.\n")


def claude_command(vendor: str, tool: str, plugin: str) -> str:
    meta = REGISTRY["tools"][tool]
    base = meta.get("base")
    reads = ([f"1. Сначала прочитай `${{CLAUDE_PLUGIN_ROOT}}/vendors/{base}/SKILL.md`."] if base and base != tool else [])
    reads.append(f"{len(reads) + 1}. Прочитай `${{CLAUDE_PLUGIN_ROOT}}/vendors/{tool}/SKILL.md` и выполни его процедуру для запроса.")
    return ("---\n"
            f"description: {json.dumps(REGISTRY['vendors'][vendor]['display'] + ' · ' + tool + ' — ' + meta['does'], ensure_ascii=False)}\n"
            "argument-hint: \"[цель или файл] [инструкции]\"\n"
            "---\n\n"
            f"# {plugin}:{tool}\n\n"
            "Запрос: **$ARGUMENTS**\n\n"
            f"Если аргументов нет, прочитай `${{CLAUDE_PLUGIN_ROOT}}/OVERVIEW.md`, дай краткий обзор пакета "
            "и несколько примеров прямого вызова. Не запускай работу над проектом.\n\n"
            "Если цель указана:\n\n"
            f"Контракт вендора: {REGISTRY['vendors'][vendor]['contract']}\n\n"
            + "\n".join(reads) + "\n\n"
            "Относительные ссылки разрешай из папки исходного скилла.\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    errors: list[str] = []
    if set(OVERVIEWS) != set(REGISTRY["vendors"]):
        raise ValueError("Overview metadata does not match vendor registry")
    for vendor, vendor_meta in REGISTRY["vendors"].items():
        plugin = plugin_name(vendor)
        root = ROOT / "plugins" / plugin
        if not root.is_dir():
            errors.append(f"missing plugin scaffold: {plugin}")
            continue
        tools = [tool for tool, meta in REGISTRY["tools"].items() if meta["vendor"] == vendor]
        manifest = {
            "name": plugin,
            "version": VERSION,
            "description": OVERVIEWS[vendor]["summary"],
            "author": {"name": "Alex Levnikov"},
            "skills": "./skills/",
            "interface": {
                "displayName": vendor_meta["display"],
                "shortDescription": OVERVIEWS[vendor]["summary"],
                "longDescription": OVERVIEWS[vendor]["workflow"],
                "developerName": "Alex Levnikov",
                "category": "Productivity",
                "capabilities": ["Read", "Write"] if any(REGISTRY["tools"][t]["mode"].startswith("W") for t in tools) else ["Read"],
                "defaultPrompt": f"Кратко расскажи, что умеет плагин {plugin}, как вызвать его команды и навыки, и приведи примеры задач."
            }
        }
        write_json(root / ".codex-plugin/plugin.json", manifest, args.check, errors)
        claude_manifest = {"name": plugin, "version": VERSION, "description": OVERVIEWS[vendor]["summary"],
                           "author": {"name": "Alex Levnikov"}, "keywords": ["design", vendor]}
        write_json(root / ".claude-plugin/plugin.json", claude_manifest, args.check, errors)
        write(root / "OVERVIEW.md", overview(vendor, tools, plugin), args.check, errors)
        write(root / "skills/overview/SKILL.md",
              f"---\nname: overview\ndescription: {json.dumps('Explain ' + plugin + ' capabilities, direct commands, individual skills, and use cases without changing the project.', ensure_ascii=False)}\n---\n\n"
              "Read `../../OVERVIEW.md` and summarize its function, workflow, explicit Codex and Claude calls, and relevant use cases in Russian. "
              "For an empty invocation, keep the answer short and do not run a vendor tool or edit files. "
              "If the user requests the complete catalog, include all rows from the overview.\n",
              args.check, errors)
        write(root / "skills/overview/agents/openai.yaml",
              skill_yaml(f"{vendor_meta['display']} · overview", "Capabilities, commands, skills and use cases", implicit=True),
              args.check, errors)
        write(root / "commands/overview.md",
              f"---\ndescription: {json.dumps('Обзор возможностей, команд и скиллов ' + plugin, ensure_ascii=False)}\n---\n\n"
              f"Прочитай `${{CLAUDE_PLUGIN_ROOT}}/OVERVIEW.md` и дай краткий разбор возможностей, прямых команд и отдельных скиллов. "
              "Без конкретной задачи не запускай скилл и не меняй файлы.\n",
              args.check, errors)
        for tool in tools:
            write(root / f"skills/{tool}/SKILL.md", direct_skill(vendor, tool, plugin), args.check, errors)
            write(root / f"skills/{tool}/agents/openai.yaml",
                  skill_yaml(tool, REGISTRY["tools"][tool]["does"]), args.check, errors)
            write(root / f"commands/{tool}.md", claude_command(vendor, tool, plugin), args.check, errors)
            src = PLUGIN / "vendors" / tool
            dest = root / "vendors" / tool
            copy_dir(src, dest, args.check, errors)
            if tree_hash(src) != LOCK["tools"][tool]["sha256"]:
                errors.append(f"source hash differs from lock: {tool}")
        subset = {"schema_version": LOCK["schema_version"], "tools": {t: LOCK["tools"][t] for t in tools}}
        write_json(root / "vendors/LOCK.json", subset, args.check, errors)
        license_src = PLUGIN / "third-party/licenses" / vendor
        if license_src.is_dir():
            copy_dir(license_src, root / "third-party/licenses" / vendor, args.check, errors)
        row = next(line for line in LEDGER.splitlines() if line.startswith(f"| `{vendor}` |"))
        attribution = ("# Third-party attribution\n\n"
                       f"This plugin contains {len(tools)} pinned skill snapshots from {vendor_meta['repo']}. "
                       "Skill revisions and hashes are recorded in `vendors/LOCK.json`.\n\n"
                       "| Vendor | Skills | Upstream | License evidence | License-source commit |\n"
                       "| --- | ---: | --- | --- | --- |\n"
                       + row.replace(f"licenses/{vendor}/", f"licenses/{vendor}/") + "\n\n"
                       "The plugin manifest license does not change the license of third-party content. "
                       "For upstreams without a root LICENSE, the linked README declaration is the available evidence.\n")
        write(root / "third-party/README.md", attribution, args.check, errors)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"{'Checked' if args.check else 'Exported'} {len(REGISTRY['vendors'])} vendor plugins and {len(REGISTRY['tools'])} direct skills")
    return 0


if __name__ == "__main__":
    sys.exit(main())

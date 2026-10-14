# Third-party skill attribution

The 87 vendor skill directories under `../vendors/` are copied from the upstream
repositories at the commits below. `../vendors/LOCK.json` records every skill's
upstream path, commit, copied content hash, and two packaging path adaptations.
`shape` points its state-design reference at the bundled `ui-craft` copy;
`ui-craft` includes its upstream animation storyboard example and points to it
within the skill directory. These changes keep both links working after the
skill folders are moved into the plugin. All other vendor skill text was copied
unchanged. This replaces the earlier tested
[`alexlevnikov/design-studio`](https://github.com/alexlevnikov/design-studio)
snapshot at `fdfb2460c4d4cf3c986065932106ff79c8074a4d`; the refreshed
versions need behavioral testing in Claude Code and Codex. License files were
collected from the same upstream commits on 2026-10-14.

| Vendor | Skills | Upstream | License evidence | License-source commit |
| --- | ---: | --- | --- | --- |
| `ui-craft` | 29 | [ui-craft](https://github.com/educlopez/ui-craft) | [MIT](licenses/ui-craft/LICENSE) | `eb88d0a9ad63d7fc8bb3d61720b7010c2cb212c8` |
| `taste` | 13 | [taste-skill](https://github.com/Leonxlnx/taste-skill) | [MIT](licenses/taste/LICENSE) | `f624f37a8c650b9cc550253104925efe4c8de246` |
| `impeccable` | 1 | [impeccable](https://github.com/pbakaus/impeccable) | [Apache-2.0](licenses/impeccable/LICENSE), [NOTICE](licenses/impeccable/NOTICE.md) | `2f98774f86bc05563876643db37e6c37c322850f` |
| `emil` | 9 | [skills](https://github.com/emilkowalski/skills) | [MIT](licenses/emil/LICENSE) | `2d228630ba1446365f614a108cb8252f1feda202` |
| `ibelick` | 3 | [ui-skills](https://github.com/ibelick/ui-skills) | [MIT](licenses/ibelick/LICENSE) | `c628a5917754ec2396d9cbb47988f280ba1d5cb0` |
| `osmani` | 6 | [web-quality-skills](https://github.com/addyosmani/web-quality-skills) | [MIT](licenses/osmani/LICENSE) | `afa8da942115f2961fdbfa80807ea0b232ff6c00` |
| `iart` | 9 | [web-animation-skills](https://github.com/iart-ai/web-animation-skills) | [MIT](licenses/iart/LICENSE) | `b6dba3eb759726845a44163ff0bad70dd9e7fbb6` |
| `lottie` | 1 | [motion-design-skill](https://github.com/lottiefiles/motion-design-skill) | [MIT](licenses/lottie/LICENSE) | `f9a8a041b85185ee4881b3471d3415e939aac772` |
| `design-motion-principles` | 1 | [design-motion-principles](https://github.com/kylezantos/design-motion-principles) | [MIT](licenses/design-motion-principles/LICENSE) | `4a9ca879f24a361f4dca4174fe2da0f67b5ddee3` |
| `motion-dev` | 1 | [motion-dev-animations-skill](https://github.com/199-biotechnologies/motion-dev-animations-skill) | [MIT](licenses/motion-dev/LICENSE) | `3feedfb4dba8adae40fc9a5f9a23e3dda2121205` |
| `threejs` | 10 | [threejs-skills](https://github.com/cloudai-x/threejs-skills) | [MIT declaration in README](https://github.com/cloudai-x/threejs-skills/blob/b1c623076c661fc9b03dac19292e825a5d106823/README.md#license); no root LICENSE file | `b1c623076c661fc9b03dac19292e825a5d106823` |
| `awwwards` | 1 | [claude-skill-awwwards](https://github.com/tponscr-debug/claude-skill-awwwards) | [MIT declaration in README](https://github.com/tponscr-debug/claude-skill-awwwards/blob/d18aa0c42b71fc60bc978b19de8e3181ab193ec5/README.md#license); no root LICENSE file | `d18aa0c42b71fc60bc978b19de8e3181ab193ec5` |
| `calm-design` | 1 | [calm-design](https://github.com/calmtiger86/calm-design) | [MIT](licenses/calm-design/LICENSE), [NOTICE](licenses/calm-design/NOTICE) | `c85ed30665a90a324cd08e68f80377b5cc2c0c86` |
| `frontend-god-mode` | 1 | [frontend-god-mode](https://github.com/Shawnchee/frontend-god-mode) | [MIT declaration in README](https://github.com/Shawnchee/frontend-god-mode/blob/e19f282b1f798813df81e2d217ac8ce69369924e/README.md#license); no root LICENSE file | `e19f282b1f798813df81e2d217ac8ce69369924e` |
| `design-skill-os` | 1 | [design-skill-os](https://github.com/frhscopex/design-skill-os) | [MIT](licenses/design-skill-os/LICENSE) | `82e41c6f6d374f4fcdea06465536e5d5cefc7a3d` |

For the three repositories with an MIT declaration but no root license file,
the upstream README is the available license evidence. Retain that declaration
and attribution when republishing. Recheck upstream before changing those copies.

The plugin's own MIT manifest does not change the licenses of these third-party files.
Update this ledger and license copies when refreshing `vendors/LOCK.json` from
new upstream commits.

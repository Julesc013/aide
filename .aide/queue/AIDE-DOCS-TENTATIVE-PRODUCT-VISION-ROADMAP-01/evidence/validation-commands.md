# Validation Commands

```text
git status --short --branch
py -3 .aide\scripts\aide_lite.py task inspect --task-id AIDE-DOCS-TENTATIVE-PRODUCT-VISION-ROADMAP-01
py -3 .aide\scripts\aide_lite.py task evidence --task-id AIDE-DOCS-TENTATIVE-PRODUCT-VISION-ROADMAP-01
py -3 .aide\scripts\aide_lite.py validate
rg -n "[A-Z]:[\\/]" docs\planning\product-vision .aide\reports\tentative-product-vision-roadmap .aide\queue\AIDE-DOCS-TENTATIVE-PRODUCT-VISION-ROADMAP-01
secret-like value scan over docs\planning\product-vision, .aide\reports\tentative-product-vision-roadmap, and .aide\queue\AIDE-DOCS-TENTATIVE-PRODUCT-VISION-ROADMAP-01
git diff --check
git diff --cached --check
```

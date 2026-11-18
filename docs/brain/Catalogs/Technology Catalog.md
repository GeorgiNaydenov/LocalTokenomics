---
title: Technology Catalog
aliases: []
tags: [catalog, generated, reference]
area: catalogs
status: generated
audience: internal
maturity: approved
confidence: confirmed
covers: []
generated: true
---

# Technology Catalog

Languages and declared dependencies with the manifest line that declares each.

%% generated:tech-catalog start (do not edit; run brain docs generate) %%
Languages: python+sql+typescript.

| Dependency | Version spec | Kind | Repo | Code |
|---|---|---|---|---|
| `pydantic` | `>=2.7` | runtime | localtokenomics | [[pyproject.toml]] `pyproject.toml:8` |
| `typer` | `>=0.12` | runtime | localtokenomics | [[pyproject.toml]] `pyproject.toml:9` |
| `rich` | `>=13.7` | runtime | localtokenomics | [[pyproject.toml]] `pyproject.toml:10` |
| `fastapi` | `>=0.115` | runtime | localtokenomics | [[pyproject.toml]] `pyproject.toml:11` |
| `uvicorn` | `>=0.30` | runtime | localtokenomics | [[pyproject.toml]] `pyproject.toml:12` |
| `pytest` | `>=8.0` | optional | localtokenomics | [[pyproject.toml]] `pyproject.toml:21` |
| `ruff` | `>=0.6` | optional | localtokenomics | [[pyproject.toml]] `pyproject.toml:22` |
| `mypy` | `>=1.11` | optional | localtokenomics | [[pyproject.toml]] `pyproject.toml:23` |
| `httpx` | `>=0.27` | optional | localtokenomics | [[pyproject.toml]] `pyproject.toml:24` |
| `pylint` | `>=3.2` | optional | localtokenomics | [[pyproject.toml]] `pyproject.toml:25` |
| `bandit` | `>=1.7` | optional | localtokenomics | [[pyproject.toml]] `pyproject.toml:26` |
| `line-too-long` | - | optional | localtokenomics | [[pyproject.toml]] `pyproject.toml:72` |
| `trailing-whitespace` | - | optional | localtokenomics | [[pyproject.toml]] `pyproject.toml:73` |
| `missing-final-newline` | - | optional | localtokenomics | [[pyproject.toml]] `pyproject.toml:74` |
| `trailing-newlines` | - | optional | localtokenomics | [[pyproject.toml]] `pyproject.toml:75` |
| `multiple-statements` | - | optional | localtokenomics | [[pyproject.toml]] `pyproject.toml:76` |
| `bad-indentation` | - | optional | localtokenomics | [[pyproject.toml]] `pyproject.toml:77` |
| `unnecessary-semicolon` | - | optional | localtokenomics | [[pyproject.toml]] `pyproject.toml:78` |
| `superfluous-parens` | - | optional | localtokenomics | [[pyproject.toml]] `pyproject.toml:79` |
| `wrong-import-order` | - | optional | localtokenomics | [[pyproject.toml]] `pyproject.toml:81` |
| `wrong-import-position` | - | optional | localtokenomics | [[pyproject.toml]] `pyproject.toml:82` |
| `ungrouped-imports` | - | optional | localtokenomics | [[pyproject.toml]] `pyproject.toml:83` |
| `multiple-imports` | - | optional | localtokenomics | [[pyproject.toml]] `pyproject.toml:84` |
| `useless-import-alias` | - | optional | localtokenomics | [[pyproject.toml]] `pyproject.toml:85` |
| `unused-import` | - | optional | localtokenomics | [[pyproject.toml]] `pyproject.toml:86` |
| `unused-variable` | - | optional | localtokenomics | [[pyproject.toml]] `pyproject.toml:87` |
| `unused-wildcard-import` | - | optional | localtokenomics | [[pyproject.toml]] `pyproject.toml:88` |
| `wildcard-import` | - | optional | localtokenomics | [[pyproject.toml]] `pyproject.toml:89` |
| `reimported` | - | optional | localtokenomics | [[pyproject.toml]] `pyproject.toml:90` |
| `misplaced-future` | - | optional | localtokenomics | [[pyproject.toml]] `pyproject.toml:91` |
| `undefined-variable` | - | optional | localtokenomics | [[pyproject.toml]] `pyproject.toml:92` |
| `used-before-assignment` | - | optional | localtokenomics | [[pyproject.toml]] `pyproject.toml:93` |
| `redefined-builtin` | - | optional | localtokenomics | [[pyproject.toml]] `pyproject.toml:94` |
| `useless-object-inheritance` | - | optional | localtokenomics | [[pyproject.toml]] `pyproject.toml:96` |
| `consider-using-f-string` | - | optional | localtokenomics | [[pyproject.toml]] `pyproject.toml:97` |
| `cell-var-from-loop` | - | optional | localtokenomics | [[pyproject.toml]] `pyproject.toml:99` |
| `dangerous-default-value` | - | optional | localtokenomics | [[pyproject.toml]] `pyproject.toml:100` |
| `raise-missing-from` | - | optional | localtokenomics | [[pyproject.toml]] `pyproject.toml:101` |
| `missing-module-docstring` | - | optional | localtokenomics | [[pyproject.toml]] `pyproject.toml:107` |
| `missing-class-docstring` | - | optional | localtokenomics | [[pyproject.toml]] `pyproject.toml:108` |
| `missing-function-docstring` | - | optional | localtokenomics | [[pyproject.toml]] `pyproject.toml:109` |
| `class-variance-authority` | `0.7.1` | runtime | localtokenomics | [[web/package.json]] `web/package.json:15` |
| `clsx` | `2.1.1` | runtime | localtokenomics | [[web/package.json]] `web/package.json:16` |
| `lucide-react` | `1.42.0` | runtime | localtokenomics | [[web/package.json]] `web/package.json:17` |
| `radix-ui` | `1.6.7` | runtime | localtokenomics | [[web/package.json]] `web/package.json:18` |
| `react` | `19.2.8` | runtime | localtokenomics | [[web/package.json]] `web/package.json:19` |
| `react-dom` | `19.2.8` | runtime | localtokenomics | [[web/package.json]] `web/package.json:20` |
| `recharts` | `3.8.0` | runtime | localtokenomics | [[web/package.json]] `web/package.json:21` |
| `sonner` | `2.0.8` | runtime | localtokenomics | [[web/package.json]] `web/package.json:22` |
| `tailwind-merge` | `3.6.0` | runtime | localtokenomics | [[web/package.json]] `web/package.json:23` |
| `@eslint/js` | `9.39.5` | dev | localtokenomics | [[web/package.json]] `web/package.json:26` |
| `@tailwindcss/vite` | `4.3.3` | dev | localtokenomics | [[web/package.json]] `web/package.json:27` |
| `@testing-library/dom` | `10.4.1` | dev | localtokenomics | [[web/package.json]] `web/package.json:28` |
| `@testing-library/jest-dom` | `7.0.1` | dev | localtokenomics | [[web/package.json]] `web/package.json:29` |
| `@testing-library/react` | `16.3.3` | dev | localtokenomics | [[web/package.json]] `web/package.json:30` |
| `@types/node` | `26.5.0` | dev | localtokenomics | [[web/package.json]] `web/package.json:31` |
| `@types/react` | `19.2.18` | dev | localtokenomics | [[web/package.json]] `web/package.json:32` |
| `@types/react-dom` | `19.2.5` | dev | localtokenomics | [[web/package.json]] `web/package.json:33` |
| `@vitejs/plugin-react` | `6.1.1` | dev | localtokenomics | [[web/package.json]] `web/package.json:34` |
| `eslint` | `9.39.5` | dev | localtokenomics | [[web/package.json]] `web/package.json:35` |
| `eslint-plugin-react-hooks` | `7.1.1` | dev | localtokenomics | [[web/package.json]] `web/package.json:36` |
| `eslint-plugin-react-refresh` | `0.5.6` | dev | localtokenomics | [[web/package.json]] `web/package.json:37` |
| `globals` | `17.12.0` | dev | localtokenomics | [[web/package.json]] `web/package.json:38` |
| `jsdom` | `30.0.1` | dev | localtokenomics | [[web/package.json]] `web/package.json:39` |
| `tailwindcss` | `4.3.3` | dev | localtokenomics | [[web/package.json]] `web/package.json:40` |
| `typescript` | `5.9.3` | dev | localtokenomics | [[web/package.json]] `web/package.json:41` |
| `typescript-eslint` | `8.70.0` | dev | localtokenomics | [[web/package.json]] `web/package.json:42` |
| `vite` | `8.2.2` | dev | localtokenomics | [[web/package.json]] `web/package.json:43` |
| `vitest` | `5.0.0` | dev | localtokenomics | [[web/package.json]] `web/package.json:44` |
%% generated:tech-catalog end %%

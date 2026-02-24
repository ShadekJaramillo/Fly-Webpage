# React + TypeScript + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

```js
export default defineConfig([
  globalIgnores(["dist"]),
  {
    files: ["**/*.{ts,tsx}"],
    extends: [
      // Other configs...

      // Remove tseslint.configs.recommended and replace with this
      tseslint.configs.recommendedTypeChecked,
      // Alternatively, use this for stricter rules
      tseslint.configs.strictTypeChecked,
      // Optionally, add this for stylistic rules
      tseslint.configs.stylisticTypeChecked,

      // Other configs...
    ],
    languageOptions: {
      parserOptions: {
        project: ["./tsconfig.node.json", "./tsconfig.app.json"],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
]);
```

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from "eslint-plugin-react-x";
import reactDom from "eslint-plugin-react-dom";

export default defineConfig([
  globalIgnores(["dist"]),
  {
    files: ["**/*.{ts,tsx}"],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs["recommended-typescript"],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ["./tsconfig.node.json", "./tsconfig.app.json"],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
]);
```

# Project Setup

## Project requirements

This project uses configuration scripts, to avoid dealing with long commands constantly, specially for setting up the project this forces the project to require using a Bash teminal.
To start working on the project make sure you have the next requirements

- Access to a bash terminal (this can be done through the WSL on windows, installing bash via brew on macOS or natively on linux).
- pnpm >= 10.30.1 as package manager.
- build-essential tools installed (usually not included in the WSL)

## Initial Setup

### API mock server

This project has for now a mock of the API that will later be used in production made in python's FastAPI framework.

To run the server you don't have to manually install python or the packages needed, but if you still want to take a look at the dependencies check the [pyproject.toml](backend/pyproject.toml) file in the backend directory.

#### Setting the mock API for the first time

#### 1. Install UV

The only dependency needed to set up the server is UV package manager ([see the istallation guide here](https://docs.astral.sh/uv/#installation)).

#### 2. Install the dependecies

```Bash
uv sync --directory backend/
```

This will install the correct package versions and even the correct python version if you don't have it in your system.

#### 3. Running the server

After setting up the server to run it you just need to execute this command each time:

```Bash
make run_api_mock
```

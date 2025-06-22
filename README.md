# Tinib00k: OpenAI Agents SDK Examples

This repository contains the companion code examples for the book _"Building Intelligent Workflows: A Deep Dive into the OpenAI Agents SDK"_. Each chapter's folder corresponds to concepts and patterns discussed in the book.

## Quickstart: Running with GitHub Codespaces (Recommended)

This method runs a fully configured development environment in the cloud, accessible through your browser. It's the fastest way to get started.

**Prerequisites:**
*   A GitHub account.

**Steps:**

1.  Click the **`< > Code`** button.
2.  Go to the **Codespaces** tab.
3.  Click **"Create codespace on main"** (or your current branch). GitHub will prepare the environment based on the `.devcontainer/devcontainer.json` configuration, which may take a few minutes.

4.  **Configure API Keys**:
    *   Once the Codespace loads, a terminal will be open at the bottom. Wait for the `postCreateCommand` to finish.
    *   The file explorer on the left will show a `.env.example` file. Rename it to `.env`.
    *   Open the new `.env` file and add your API keys.
        *   `GEMINI_API_KEY` is required for almost all examples.
        *   `OPENAI_API_KEY` is required for the SDK's tracing features.
        *   The `ANTHROPIC_API_KEY` is optional and only needed for a specific example in Chapter 3.

## Running the Examples

All examples are designed to be run as Python modules from the root directory of the project. This ensures that all imports work correctly.

1.  Open a terminal in your Codespace or Dev Container.
2.  Use the `python -m <package>.<module>` command to execute a script.

**Example: Running the basic agent from Chapter 2**
```bash
python -m chapter2.basic_agent
```

You will be prompted to type input into the terminal to interact with the agent system. To exit, press `Ctrl+C`.

## Alternative: Running Locally with Dev Containers

If you prefer to work on your local machine, you can use the Dev Container feature of VS Code.

**Prerequisites:**
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Visual Studio Code](https://code.visualstudio.com/)
- [VS Code Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

**Steps:**
1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/iamulya/openai-agentsdk-code.git
    cd openai-agentsdk-code
    ```
2.  **Configure API Keys:** Rename `.env.example` to `.env` and add your keys, just as described in the Codespaces setup.
3.  **Open in Dev Container:**
    -   Open the cloned repository folder in VS Code.
    -   A notification will appear at the bottom-right corner asking to "Reopen in Container". Click it.
    -   Alternatively, open the command palette (`Ctrl+Shift+P` or `Cmd+Shift+P`) and run **"Dev Containers: Reopen in Container"**.
4.  VS Code will build the Docker container and install all dependencies. You can then run the examples as described above. Make 

## Project Structure

-   **/src/chapter...**: Each folder contains code demonstrating specific concepts.
-   **/devcontainer**: Contains the `devcontainer.json` and `Dockerfile` for the development environment.
-   **pyproject.toml**: Defines the project, its dependencies, and package structure.
-   **.env.example**: A template for your API key configuration.
-   **/src/utils.py**: A helper script to load and validate the required API keys from the `.env` file.

## Observability and Tracing

Many examples use the SDK's built-in tracing. By default, traces are sent to the OpenAI platform's backend. To view them:

1.  Make sure your `OPENAI_API_KEY` is set in the `.env` file.
2.  Run any example that uses tracing, for instance: `python -m chapter10.tracing_example`.
3.  The console output will include a URL to the trace. Copy and paste this URL into your browser to see a detailed visualization of the agent's execution path, including LLM calls, tool usage, and more.

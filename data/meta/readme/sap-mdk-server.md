<img src="images/MDK_icon.png" width=75px align="right" alt="SAP MDK icon">

# Welcome to @sap/mdk-mcp-server

[![REUSE status](https://api.reuse.software/badge/github.com/sap/mdk-mcp-server)](https://api.reuse.software/info/github.com/sap/mdk-mcp-server)


## What is MCP server for Mobile Development Kit (MDK)?
This open-source server provides AI agents with comprehensive MDK knowledge and tools. By combining best practice guidelines, project-aware context information, templates for creating new projects, and access to the MDK CLI tools, the MDK MCP server transforms AI agents into MDK development experts.

## What is Mobile Development Kit?
The mobile development kit is a powerful framework that enables developers to build cross-platform mobile applications using a metadata-driven approach. It is part of SAP Business Technology Platform and integrates tightly with SAP Mobile Services. 
Some of SAP’s larger and complex mobile apps are built using MDK. An example is [SAP Service and Asset Manager](https://www.sap.com/sea/products/scm/asset-manager.html).

## Table of Contents

- [Setup](#setup)
- [Available Tools](#available-tools)
- [Ingesting GitHub Knowledge (Advanced)](#ingesting-github-knowledge-advanced)
- [Offline OData Querying (Advanced)](#offline-odata-querying-advanced)
- [Support, Feedback, Contributing](#support-feedback-contributing)
- [Telemetry](#telemetry)
- [Security / Disclosure](#security--disclosure)
- [Code of Conduct](#code-of-conduct)
- [Licensing](#licensing)
- [Acknowledgments](#acknowledgments)


## Setup

### Platform Support

The MDK MCP server supports the following platforms:

- **macOS**: Apple Silicon (ARM64) only
  - ⚠️ **Note**: Intel Mac (x64) is **not supported** in v0.4.0+ due to onnxruntime-node ≥1.24 dropping darwin/x64 binaries
- **Linux**: x64, ARM64, and other architectures
- **Windows**: x64, ARM64

If you're on an Intel Mac, you may need to:
- Use Rosetta 2 to run the ARM64 version (performance may vary)
- Or stay on an earlier version that uses onnxruntime-node <1.24

### Installation Steps

1. Install [node.js 24.11.1](https://nodejs.org/dist/v24.11.1/).

2. To install the MDK MCP server, you have two options:

    a. Use npm to install it from the public npmjs registry at [@sap/mdk-mcp-server](https://www.npmjs.com/package/@sap/mdk-mcp-server). 
  
      ```bash
      npm install -g @sap/mdk-mcp-server
      ``` 

    b. Clone the open-source code repository at https://github.com/SAP/mdk-mcp-server, and use `npm` to install.  

      ```bash 
      git clone https://github.com/SAP/mdk-mcp-server.git 
      cd mdk-mcp-server 
      npm i
      npm run build
      npm i -g @sap/mdk-mcp-server@. 
      ```

3. Configure your MCP client (AI agent) to connect to the server. Note that configuration will vary depending on the AI agent used.

    **Cline in VS Code:** Example using the [Cline extension](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev). 
    
    - With Cline open, look below the prompt box and click **Manage MCP Servers**.
    - In the dialog, click **Settings**. The MCP Servers page opens.
    - Click **Configure MCP Servers**. This will open the `cline_mcp_settings.json` file in your editor.
    - In the JSON settings file, add a configuration block for MDK MCP server within the `mcpServers` section, and save the file. The supported schema versions include 26.9 (default), 26.6, 26.3, 25.9, 25.6, 24.11, and 24.7.

    ```json
    {
      "mcpServers": {
        "mdk-mcp": {
          "type": "stdio",
          "command": "mdk-mcp",
          "args": ["--schema-version", "26.9"]
        }
      }
    }
    ```

    > **Note:**  
    > If the MCP server is not listed with its available tools in the Cline extension immediately, restart VS Code.

    <details>
      <summary><b>Expand:</b> Usage in Claude Code (VS Code Extension)</summary>

    Claude Code discovers MCP servers from its configuration.

    1. Open (or create) your Claude Code configuration file:

      ```text
      ~/.claude.json
      ```

    2. Add the following MCP server configuration:

    ```json
    {
      "mcpServers": {
        "mdk-mcp": {
          "type": "stdio",
          "command": "mdk-mcp",
          "args": ["--schema-version", "26.9"]
        }
      }
    }
    ```

   > **Note:** If `~/.claude.json` already exists, merge the `mdk-mcp` entry into the existing `mcpServers` section rather than replacing the entire file.

    3. Reload the VS Code window (or restart VS Code).

    ### Verify the installation

    Open the Claude Code panel in VS Code and run:

    ```text
    /mcp
    ```

    You should see **`mdk-mcp`** listed as an available MCP server.

    </details>

    <details>
      <summary><b>Expand:</b> Usage in OpenCode</summary>

    An example using [OpenCode](https://github.com/sst/opencode):

    ```
    {
      "mcp": {
        "mdk-mcp": {
          "type": "local",
          "command": ["mdk-mcp", "--schema-version", "26.9"],
          "enabled": true
        }
      }
    }
    ```
    </details>


    <details>
      <summary><b>Expand:</b> Usage in Cursor</summary>

    Edit the file `~/.cursor/mcp.json`:

    ```json
    {
      "mcpServers": {
        "mdk-mcp": {
          "type": "stdio",
          "command": "mdk-mcp",
          "args": ["--schema-version", "26.9"]
        }
      }
    }
    ```
    </details>


    <details>
      <summary><b>Expand:</b> Usage in Claude Desktop</summary>    
    Use the absolute path to Node.js in your Claude Desktop configuration file.

    1. Find your Node.js installation path by running the terminal command:
       ```bash
       which node
       ```
       This might output something like `/usr/local/bin/node` or `/opt/homebrew/bin/node`.

    2. Edit `~/Library/Application Support/Claude/claude_desktop_config.json` and update the `command` field to use the absolute path:
       ```json
       {
         "mcpServers": {
           "mdk-mcp": {
             "command": "/usr/local/bin/node",
             "args": ["/usr/local/lib/node_modules/@sap/mdk-mcp-server/build/index.js", "--schema-version", "26.9"]
           }
         }
       }
       ```

    3. Restart Claude Desktop.

    **Note:** Adjust the paths based on your actual Node.js and MDK MCP server installation locations.

 
    </details>

    Once configured, your AI agent will have access to the MDK MCP server. Depending on your IDE settings, you may need to approve initial tool calls.


4. **Create a Rule File**: To ensure your AI coding assistant uses the MCP servers appropriately for your project, define rules and guidelines in a file named [`AGENTS.md`](https://agents.md/). In the Cline extension for VS Code, click the **Manage Cline Rules & Workflows** icon below the prompt box, click **+** to create a new rule file (e.g., `AGENTS.md`) and  add the example rules shown below:

    ```markdown
    - Do not generate `.service.metadata` file.
    - Do not generate `.xml` file in the `Services` folder.
    - Do not change `.project.json` file.
    ```

5. Verify your LLM Provider and AI model.
 
    When you add Cline to VS Code, it serves as the default API provider. You can choose a different LLM provider, such as SAP AI Core.
    To add an SAP AI Core API provider in the Cline extension for VS Code, follow these steps:
      - With Cline open, look below the prompt box and click **Select Model / API Providers**.
      - Choose your API provider (such as SAP AI Core) and enter your details. See the instructions [here](https://docs.cline.bot/provider-config/sap-aicore#sap-ai-core) for a detailed setup.
      - Select your preferred AI model.

6. **Integration with SAP Mobile Services:** To create a new MDK application, the MCP server uses the Cloud Foundry CLI and a `.service.metadata` file containing:
    - The mobile application defined in the SAP Mobile Services instance. 
      - Mobile Services API Endpoint
      - Mobile Services App ID
    - Mobile Destinations including OData service metadata.

    We include a tool to help with creating or updating this file as part of our **VS Code extension: Mobile development kit extension for VS Code**. This is how you can use this tool to create or update the `.service.metadata` file:

      1.	Install the [Mobile development kit extension for VS Code](https://marketplace.visualstudio.com/items?itemName=SAPSE.vsc-extension-mdk) version 1.32.0 or later.
      2.	Install the [Cloud Foundry CLI](https://help.sap.com/docs/btp/sap-business-technology-platform/download-and-install-cloud-foundry-command-line-interface).
      3.	Log in to your SAP BTP Cloud Foundry environment. For more details you can refer to [this help documentation](https://help.sap.com/docs/btp/sap-business-technology-platform/log-on-to-cloud-foundry-environment-using-cloud-foundry-command-line-interface).

      ```bash
      cf login -a <your target endpoint> --sso
      ```

      4. Create an empty folder on your machine and open it in VS Code.
      5. Open the Command Palette in VS Code and select **MDK: Open Mobile App Editor**.
      6. Create a new or select an existing mobile app.
      7. Select a destination.
      8. Click **Add App to Project**.

7. Your environment is now ready for the MDK development with MCP server. You can now enter a prompt to:

    - Generate a new MDK project displaying OData entities information.
    - Enhance an existing project by adding additional UI controls on a given page.
    - Validate your current MDK project schema.
    - Migrate old MDK projects to latest schema.
    - Deploy your MDK project.
    - Generate onboarding QR code.
    - Explain specific properties.
    - Find information about control properties or any aspect of the documentation.

## Available Tools

> [!NOTE]
> Tools are meant to be used by AI models and do not constitute a stable API.

This release of the MDK MCP server includes the following tools, which can be accessed by your AI agent:

| Tools     | Description | Parameters      |
|----------|-----|-----------|
| `mdk-create`    | Creates MDK projects or entity metadata using templates (CRUD, List Detail, Base). Use this for initializing new projects or adding entity metadata to existing projects.  | - `folderRootPath:` The path of the current project root folder. <br> - `scope:` The scope of creation:<br>• `project`: Initialize a new MDK project with full structure<br>• `entity`: Add entity metadata to an existing project<br> - `templateType:` The type of template to use (crud, list detail, base). Note: `base` template is only valid for project scope.<br> - `oDataEntitySets:` The OData entity sets relevant to the user prompt, separated by commas.<br> - `offline:` Whether to generate the project in offline mode (only applicable for project scope). Set to false unless offline is explicitly specified. |
| `mdk-gen`    | Generates MDK artifacts including pages, actions, i18n files, and rule references. Returns prompts for LLM processing (pages, actions, i18n) or searches for rule examples.  | - `artifactType:` The type of artifact to generate:<br>• `page`: Generate MDK page files (`.page`) with databinding or layout<br>• `action`: Generate MDK action files (`.action`)<br>• `i18n`: Generate internationalization files (`.properties`)<br>• `rule`: Search for and return relevant JavaScript rule examples<br> - `folderRootPath:` The path of the current project root folder (not required for rule artifact type).<br><br>**For page artifacts:**<br> - `pageType:` Type of page `page`):<br>• `databinding`: Data-driven pages with controls bound to OData<br>• `layout`: Structure-focused pages with specific layouts<br> - `controlType:` The control type for databinding pages (required when pageType is `databinding`). Available types: ObjectTable, FormCell, KeyValue, ObjectHeader, ContactTable, SimplePropertyCollection, ObjectCard, DataTable, KPIHeader, ProfileHeader, ObjectCollection, Timeline, TimelinePreview,
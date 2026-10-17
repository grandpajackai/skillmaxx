# Pi Security for Grok

Use Pi Security in Grok to investigate findings, review your security posture, and get remediation guidance as you work.

![Pi Security logo](plugins/pi-security/assets/pi-favicon-light.svg)

The official Pi Security plugin connects Grok to your Pi Security workspace through browser-based sign-in. It does not install a local Pi service or include any credentials.

## What you can do

With the plugin, you can ask Grok to:

- Investigate, explain, summarize, and compare Pi Security findings.
- Review threat models and Code Gatekeeper results.
- Get remediation guidance for findings and vulnerable packages.
- Start a security design review.
- Import security reports written in Markdown.
- Find secure development guidance for the repository you're working in.

## Install the plugin

Run these commands in your terminal:

```shell
grok plugin marketplace add pi-sloane/grok-plugin
grok plugin install pi-security --trust
```

The first command adds the Pi Security marketplace. The second installs the plugin; `--trust` skips Grok's installation trust prompt. Browser sign-in connects Grok to Pi Security.

Next, follow the sign-in and verification steps in [SETUP.md](SETUP.md).

## Safety

Before accessing Pi Security data, the plugin shows which account and tenant are connected. It asks for confirmation before actions that upload content, start work in Pi, or record feedback.

## Update the plugin

Run:

```shell
grok plugin update pi-security
```

Use `grok plugin details pi-security` to check the installed version and components. See xAI's [Grok Build CLI reference](https://docs.x.ai/build/cli/reference) for plugin management commands.

## Privacy and support

Only share content that you are authorized to send to Pi Security, and never include credentials or secrets. Do not post customer information, private repository details, or other sensitive material in public issues or pull requests.

- [Privacy Policy](https://www.pi.security/privacy-policy)
- [Terms and Conditions](https://www.pi.security/terms-and-conditions)
- [Data Processing Agreement](https://www.pi.security/data-processing-agreement)
- [Report a security issue](SECURITY.md)
- Support: [contact@pi.security](mailto:contact@pi.security)

This plugin and marketplace are available under the [MIT License](LICENSE).

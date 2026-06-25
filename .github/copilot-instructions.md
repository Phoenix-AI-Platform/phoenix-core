[copilot-instructions.md](https://github.com/user-attachments/files/29357008/copilot-instructions.md)
# Phoenix Copilot Instructions

You are working inside the Phoenix AI Platform.

Always follow the Phoenix Constitution in `phoenix-docs`:

- `00_VISION.md`
- `01_MISSION.md`
- `02_PRINCIPLES.md`
- `03_ARCHITECTURE.md`
- `04_PLUGIN_STANDARD.md`
- `05_CODING_STANDARD.md`
- `06_ROADMAP.md`
- `adr/`

Core rules:

1. AI should complete work, not merely answer questions.
2. Humans remain in control.
3. Phoenix Core owns orchestration and shared services only.
4. Plugins own domain-specific business logic.
5. Keep Core small.
6. Every feature must save measurable time.
7. Every feature must become a reusable capability.
8. Natural language starts workflows; structured data executes them.
9. Professional output is non-negotiable.
10. Do not hardcode personal machine paths, secrets, or one-off assumptions.

Before implementing meaningful changes:

- Identify which repo/module owns the change.
- Keep changes small and reviewable.
- Add or update tests when behavior changes.
- Update docs or ADRs if architecture changes.
- State assumptions clearly in PR descriptions.

Do not put plugin-specific business logic into Phoenix Core.


Repository-specific guidance:

This repository is for shared platform infrastructure only.

Allowed concerns:

- Plugin loading
- Command routing
- Configuration
- Logging
- Events
- Approval workflow abstractions
- Shared result/error types
- Shared interfaces

Not allowed:

- Proposal-specific logic
- Network vendor-specific logic
- Real estate logic
- Trading logic
- Customer-specific workflows

When uncertain, keep functionality out of Core until at least two plugins need it.

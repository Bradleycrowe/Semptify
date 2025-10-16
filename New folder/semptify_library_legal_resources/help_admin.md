# Help – Admin Guide

## What is this?
This section supports Semptify builders, coders, and maintainers. It explains how modules are wired, how flows are checkpointed, and how to onboard new collaborators.

## How to Maintain Semptify
- Each module is self-contained and GUI-wired via register_module()
- Use law_notes_integration.md for scaffolding conventions
- All flows are checkpointed at v0.2-lawnotes and stored in /modules
- To add new buttons, use button_label, action, and category in each module

## What This Enables
- Modular, persistent automation
- Instant onboarding for new devs
- Transparent, repeatable infrastructure for movement builders

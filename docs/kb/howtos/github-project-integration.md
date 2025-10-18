---
doc_type: kb_page
doc_version: 2025-10-18.r1
title: GitHub Project Integration
---

# GitHub Project Integration

## Intent

- Stand up a Projects (v2) board for `pvliesdonk/ai_engineer_contract`.
- Capture repeatable CLI steps to add fields, populate items, and highlight manual follow-ups.

## Prerequisites

- Refresh your GitHub CLI token with project scopes:

```bash
gh auth refresh -h github.com -s project
```

## Create the Project

```bash
gh project create --owner pvliesdonk --title "AI Engineer Contract – Implementation"
```

Record the returned project number (e.g., `3`) and `projectId` (e.g., `PVT_kwHOAVKYys4BF4Sp`).

## Configure Fields

1. Add single-select fields for `Section` and `Priority`:

```bash
gh project field-create 3 --owner pvliesdonk --name "Section" --data-type SINGLE_SELECT \
  --single-select-options "Governance,Decision Logging,Project Ops,Docs & KB,Tooling"

gh project field-create 3 --owner pvliesdonk --name "Priority" --data-type SINGLE_SELECT \
  --single-select-options "P0,P1,P2"
```

2. Update the default `Status` field to include a `Review` stage (GraphQL required; CLI cannot edit options directly):

```bash
gh api graphql -F fieldId=<statusFieldId> \
  -f query='mutation($fieldId:ID!){updateProjectV2Field(input:{fieldId:$fieldId,name:"Status",singleSelectOptions:[
    {name:"Todo",description:"Backlog",color:GRAY},
    {name:"In Progress",description:"Work in progress",color:BLUE},
    {name:"Review",description:"Ready for review",color:YELLOW},
    {name:"Done",description:"Completed",color:GREEN}
  ]}){projectV2Field{__typename}}}'
```

Replace `<statusFieldId>` with the value from `gh project field-list`.

## Add Issues

1. Add each open proposal to the board:

```bash
for n in 42 43 44 45 46 47 49 55 57; do
  gh project item-add 3 --owner pvliesdonk --url \
    https://github.com/pvliesdonk/ai_engineer_contract/issues/$n
done
```

2. Set `Section`, `Priority`, and `Status` (example for Issue #42):

```bash
gh project item-edit --id <itemId> --project-id PVT_kwHOAVKYys4BF4Sp \
  --field-id <sectionFieldId> --single-select-option-id 75aed36a   # Section: Governance

gh project item-edit --id <itemId> --project-id PVT_kwHOAVKYys4BF4Sp \
  --field-id <priorityFieldId> --single-select-option-id d30edd57  # Priority: P1

gh project item-edit --id <itemId> --project-id PVT_kwHOAVKYys4BF4Sp \
  --field-id <statusFieldId> --single-select-option-id 6245e92b    # Status: Todo
```

Use `gh project item-list 3 --owner pvliesdonk --format json` to locate item IDs after adding issues.

## Manual View Setup

- The CLI cannot create views. In the web UI, add:
  - Kanban view grouped by `Status` (columns: Todo, In Progress, Review, Done).
  - Table view grouped by `Section` with `Priority` visible.
- Confirm default `Status` automation moves items between columns.

## Next Steps

- Keep Section/Priority assignments up to date as issues evolve.
- When new contract work is logged, add it to the board using the same commands.
- Revisit field colors/descriptions if the team establishes a different review flow.

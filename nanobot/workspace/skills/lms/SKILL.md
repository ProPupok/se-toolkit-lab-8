---
name: lms
description: Use LMS MCP tools for live course data
always: true
---

# LMS Skill

You have access to the LMS (Learning Management System) via MCP tools. Use them to provide real-time course analytics.

## Available Tools

- `lms_health` — Check if the LMS backend is healthy (no parameters)
- `lms_labs` — List all labs available in the LMS (no parameters)
- `lms_learners` — List all learners registered in the LMS (no parameters)
- `lms_pass_rates` — Get pass rates for a specific lab (requires `lab` parameter, e.g. "lab-01")
- `lms_timeline` — Get submission timeline for a specific lab (requires `lab` parameter)
- `lms_groups` — Get group performance for a specific lab (requires `lab` parameter)
- `lms_top_learners` — Get top learners by average score for a lab (requires `lab` and optional `limit` parameter, default 5)
- `lms_completion_rate` — Get completion rate (passed / total) for a lab (requires `lab` parameter)
- `lms_sync_pipeline` — Trigger the LMS sync pipeline (no parameters)

## Strategy Rules

### When lab parameter is needed but not provided:

**IF** the user asks for scores, pass rates, completion, groups, timeline, or top learners **WITHOUT** naming a specific lab:

1. **First**, call `lms_labs` to get the list of available labs
2. **IF** multiple labs are available, use the shared structured-ui skill to ask the user to choose one
3. **Use** each lab's `title` as the display label and `id` (e.g. "lab-01") as the value to pass back
4. **Pass** the selected lab's `id` to the appropriate tool (`lms_pass_rates`, `lms_timeline`, etc.)

### Example Flow:
User: “Show me the scores”
→ Call lms_labs
→ Present lab choices to user using structured-ui
→ User selects a lab (e.g. “lab-01”)
→ Call lms_pass_rates with lab=“lab-01”
→ Format and present results
### Formatting Results:

- **Percentages**: Show as "XX%" (e.g., "75%" not "0.75")
- **Counts**: Show as plain numbers (e.g., "12 students")
- **Dates**: Keep ISO format or convert to readable (e.g., "2024-01-15" → "Jan 15, 2024")
- **Keep responses concise** — focus on key insights
- **Use bullet points** for multiple data points
- **Highlight trends** (e.g., "Most submissions on Day 3")

## When Asked "What Can You Do?"

Respond with:

> I can help you query the LMS for live course data:
> - Check system health (`lms_health`)
> - List available labs (`lms_labs`) and learners (`lms_learners`)
> - Get pass rates, completion stats, timeline, group performance for any lab
> - Find top learners (top 5 by default)
> - Trigger sync pipeline if data seems outdated
>
> Just ask something like:
> - "What labs are available?"
> - "Show pass rates for lab-01"
> - "Which students are top performers in lab-04?"
> - "When were most submissions made for lab-02?"

## Important Notes

- **Always call `lms_labs` first** when the lab is not specified
- **Let the shared structured-ui skill handle the choice presentation** — don't build your own UI
- **Never guess lab IDs** — always fetch them from `lms_labs`
- **Lab IDs look like** `lab-01`, `lab-02`, etc.
- **If a tool returns an error**, explain it clearly to the user
- **For `lms_top_learners`**, the `limit` parameter defaults to 5 if not specified

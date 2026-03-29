# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

The agentic loop is the fundamental cycle that an AI agent follows to accomplish tasks autonomously. It typically consists of these core    
stages:

 1 Perceive — Gather information from the environment (user input, files, APIs, sensors, etc.)
 2 Reason/Plan — Analyze the information, determine goals, and decide on a course of action
 3 Act — Execute actions using available tools (file operations, web searches, API calls, etc.)
 4 Observe — Receive feedback from the actions taken (outputs, errors, state changes)
 5 Reflect/Iterate — Evaluate results, adjust the plan if needed, and continue the loop until the goal is achieved


 ┌─────────────┐
 │   Perceive  │
 └──────┬──────┘
        ▼
 ┌─────────────┐
 │   Reason    │
 └──────┬──────┘
        ▼
 ┌─────────────┐
 │    Act      │
 └──────┬──────┘
        ▼
 ┌─────────────┐
 │   Observe   │
 └──────┬──────┘
        ▼
 ┌─────────────┐
 │  Reflect    │───(continue or stop)───►
 └─────────────┘


This loop enables agents to:

 • Handle multi-step tasks autonomously
 • Adapt to unexpected outcomes
 • Learn from feedback within a session
 • Decompose complex problems into manageable steps

The quality of an agent depends on how well it executes each stage—especially reasoning (making good decisions) and reflection (knowing whento adjust course vs. when the task is complete).

🐈 nanobot
I'll explore the workspace to find information about available labs in the LMS.
2026-03-28 15:20:41.306 | INFO     | nanobot.agent.loop:_prepare_tools:253 - Tool call: list_dir({"path": "/root/se-toolkit-lab-8/nanobot/workspace"})
2026-03-28 15:20:53.282 | INFO     | nanobot.agent.loop:_prepare_tools:253 - Tool call: list_dir({"path": "/root/se-toolkit-lab-8"})

🐈 nanobot
I see there's a lab directory. Let me explore it to find information about available labs.
2026-03-28 15:20:57.951 | INFO     | nanobot.agent.loop:_prepare_tools:253 - Tool call: list_dir({"path": "/root/se-toolkit-lab-8/lab"})    
2026-03-28 15:20:59.671 | INFO     | nanobot.agent.loop:_prepare_tools:253 - Tool call: list_dir({"path": "/root/se-toolkit-lab-8/lab/tasks"})
2026-03-28 15:21:03.223 | INFO     | nanobot.agent.loop:_prepare_tools:253 - Tool call: list_dir({"path": "/root/se-toolkit-lab-8/lab/tasks/required"})
2026-03-28 15:21:03.223 | INFO     | nanobot.agent.loop:_prepare_tools:253 - Tool call: list_dir({"path": "/root/se-toolkit-lab-8/lab/tasks/optional"})

🐈 nanobot
Let me also check the README and other documentation to get a better overview of the available labs.
2026-03-28 15:21:12.281 | INFO     | nanobot.agent.loop:_prepare_tools:253 - Tool call: read_file({"path": "/root/se-toolkit-lab-8/README.md"})
2026-03-28 15:21:12.282 | INFO     | nanobot.agent.loop:_prepare_tools:253 - Tool call: list_dir({"path": "/root/se-toolkit-lab-8/instructors"})

🐈 nanobot
Based on my exploration, here are the available labs in this LMS:
1 Task 1: Set Up the Agent — install nanobot, configure Qwen API, add MCP tools, write skill prompt
 2 Task 2: Deploy and Connect a Web Client — Dockerize nanobot, add WebSocket channel + Flutter chat UI
 3 Task 3: Give the Agent New Eyes — explore observability data, write log/trace MCP tools
 4 Task 4: Diagnose a Failure and Make the Agent Proactive — investigate a failure, schedule in-chat health checks, fix a planted bug       

Optional Labs

 1 Task 1: Add a Telegram Bot Client — same agent, different interface

Lab Overview

This is Lab 8 — "The Agent is the Interface". The goal is to build an AI agent (nanobot) as a natural-language interface to an LMS system.  
You'll:

 • Set up nanobot from scratch with Qwen API
 • Build MCP tools for querying the LMS and observability data
 • Deploy a web chat client
 • Make the agent proactive with scheduled health checks

The lab is designed to be done on your VM, and the system includes an LMS backend (React + FastAPI + PostgreSQL), observability stack       
(OpenTelemetry + VictoriaLogs/Traces), and the nanobot agent layer.

Would you like me to read the details of any specific task?

## Task 1B — Agent with LMS tools

What labs are available?
Here are the available labs:

 1 Lab 01 – Products, Architecture & Roles
 2 Lab 02 — Run, Fix, and Deploy a Backend Service
 3 Lab 03 — Backend API: Explore, Debug, Implement, Deploy
Here are the available labs:

 1 Lab 01 – Products, Architecture & Roles
 2 Lab 02 — Run, Fix, and Deploy a Backend Service
 3 Lab 03 — Backend API: Explore, Debug, Implement, Deploy
 4 Lab 04 — Testing, Front-end, and AI Agents
 5 Lab 05 — Data Pipeline and Analytics Dashboard
 6 Lab 06 — Build Your Own Agent
 7 Lab 07 — Build a Client with an AI Coding Agent
 8 Lab 08 — lab-08

Would you like more details about any specific lab, such as completion rates, pass rates, or top learners?

Is the LMS backend healthy?
Yes, the LMS backend is healthy! ✅

 • Status: healthy
 • Item count: 56 items
 • Errors: none

Everything is running smoothly.

## Task 1C — Skill prompt

<!-- Paste the agent's response to "Show me the scores" (without specifying a lab) -->

Which lab would you like to see scores for?

I can show you the scores (pass rates) for any lab! Here are the available labs:

 1 lab-01: Lab 01 – Products, Architecture & Roles
 2 lab-02: Lab 02 — Run, Fix, and Deploy a Backend Service
 3 lab-03: Lab 03 — Backend API: Explore, Debug, Implement, Deploy
 4 lab-04: Lab 04 — Testing, Front-end, and AI Agents
 5 lab-05: Lab 05 — Data Pipeline and Analytics Dashboard
 6 lab-06: Lab 06 — Build Your Own Agent
 7 lab-07: Lab 07 — Build a Client with an AI Coding Agent
 8 lab-08: Lab 08

Which lab would you like to see the scores for? Just let me know the lab ID (e.g., "lab-01") or the lab number!

## Task 2A — Deployed agent

<!-- Paste a short nanobot startup log excerpt showing the gateway started inside Docker -->
nanobot-1  | Using config: /tmp/config.resolved.json
nanobot-1  | Workspace: /app/nanobot/workspace
nanobot-1  | Using config: /tmp/config.resolved.json
nanobot-1  | 🐈 Starting nanobot gateway version 0.1.4.post6 on port 18790...
nanobot-1  | /app/.venv/lib/python3.14/site-packages/dingtalk_stream/stream.py:195: SyntaxWarning: 'return' in a 'finally' block
nanobot-1  |   return ip
nanobot-1  | 2026-03-28 16:24:14.231 | DEBUG    | nanobot.channels.registry:discover_all:64 - Skipping built-in channel 'matrix': Matrix dependencies not installed. Run: pip install nanobot-ai[matrix]
nanobot-1  | Warning: No channels enabled
nanobot-1  | ✓ Heartbeat: every 1800s
nanobot-1  | 2026-03-28 16:24:16.144 | INFO     | nanobot.cron.service:start:202 - Cron service started with 0 jobs
nanobot-1  | 2026-03-28 16:24:16.144 | INFO     | nanobot.heartbeat.service:start:124 - Heartbeat started (every 1800s)
nanobot-1  | 2026-03-28 16:24:17.093 | WARNING  | nanobot.channels.manager:start_all:82 - No channels enabled01~
## Task 2B — Web client

<!-- Screenshot of a conversation with the agent in the Flutter web app -->

## Task 3A — Structured logging

<!-- Paste happy-path and error-path log excerpts, VictoriaLogs query screenshot -->

## Task 3B — Traces

<!-- Screenshots: healthy trace span hierarchy, error trace -->

## Task 3C — Observability MCP tools

<!-- Paste agent responses to "any errors in the last hour?" under normal and failure conditions -->

## Task 4A — Multi-step investigation

<!-- Paste the agent's response to "What went wrong?" showing chained log + trace investigation -->

## Task 4B — Proactive health check

<!-- Screenshot or transcript of the proactive health report that appears in the Flutter chat -->

## Task 4C — Bug fix and recovery

<!-- 1. Root cause identified
     2. Code fix (diff or description)
     3. Post-fix response to "What went wrong?" showing the real underlying failure
     4. Healthy follow-up report or transcript after recovery -->

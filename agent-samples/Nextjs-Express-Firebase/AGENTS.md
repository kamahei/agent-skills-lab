# AGENTS.md

## Project Purpose

This project uses `Next.js` for the web application, `Express` for the API layer, and `Firebase` for backend services such as authentication, database, storage, hosting, or serverless integration.

The goal is to help complete tasks safely and consistently without blurring the boundaries between frontend, API, and Firebase responsibilities.

## Default Assumptions

- The frontend uses modern `Next.js`, preferably with the `App Router`.
- The API is implemented in a dedicated `Express` layer.
- `Firebase` may include `Authentication`, `Firestore`, `Storage`, `Hosting`, `Functions`, or the `Local Emulator Suite`.
- The current repository structure and deployment topology take precedence over generic assumptions.

If the repository clearly uses a different setup, follow the repository instead of this file.

## High-Level Architecture Rules

- Treat `Next.js` as the UI and rendering layer.
- Treat `Express` as the main API and business-logic boundary unless the repository explicitly uses a different pattern.
- Treat `Firebase` as infrastructure and managed backend services, not as a place to duplicate application logic unnecessarily.
- Do not duplicate the same business rule in `Next.js` route handlers, `Express` controllers, and Firebase Functions at the same time.
- If a request would change architectural boundaries, call that out explicitly before implementing it.

## Next.js Rules

- Prefer the existing routing model in the repository. If the project uses the `App Router`, keep using it.
- Default to Server Components when possible.
- Add `"use client"` only when browser-only behavior, stateful interactivity, or client-only SDK usage requires it.
- Keep page components thin. Move reusable UI into components and reusable logic into separate modules.
- Do not put privileged Firebase Admin logic in client-side code.
- Be careful with caching, revalidation, and server/client boundaries when changing data-fetching behavior.
- If a task affects rendering strategy, state clearly whether it impacts SSR, SSG, ISR, or client-side rendering.

## Express API Rules

- Keep route handlers focused and small.
- Put validation, business logic, and data access in clear layers if the repository already separates them.
- Reuse existing middleware patterns for auth, validation, logging, and error handling.
- Always return consistent HTTP status codes and response shapes.
- Propagate or handle errors intentionally. Do not swallow errors silently.
- Avoid introducing API behavior in `Next.js` route handlers if the same capability already belongs in the `Express` API.

## Firebase Rules

- Use the Firebase client SDK only for client-safe operations.
- Use the Firebase Admin SDK only in trusted server environments such as `Express`, server-only code, or approved backend runtimes.
- Never expose secrets, service account material, or admin credentials to the browser.
- Treat `NEXT_PUBLIC_*` variables as public. Do not place secrets in them.
- Prefer the Firebase Local Emulator Suite for local development and testing when the task touches Auth, Firestore, Functions, or Hosting behavior.
- Preserve existing Firebase project, region, and emulator configuration unless the task explicitly requires a change.

## Authentication And Authorization

- Keep authentication and authorization logic consistent across `Next.js`, `Express`, and Firebase.
- Do not trust client-provided identity data without server-side verification.
- If Firebase Authentication is used, verify tokens on the trusted server side before privileged operations.
- Keep authorization checks close to protected business actions, not only in the UI.
- When changing auth behavior, document the impact on sign-in flow, session handling, and protected routes or endpoints.

## Data And API Boundaries

- Prefer one clear source of truth for each piece of data.
- Avoid mixing direct client access to Firestore with overlapping `Express` endpoints unless the repository already uses both intentionally.
- If both direct Firebase access and `Express` APIs exist, preserve the current boundary unless the task explicitly asks for refactoring.
- For write operations, favor predictable validation and authorization over convenience.

## Environment Variables

- Keep secrets in server-only environment variables.
- Use `NEXT_PUBLIC_*` only for values that are safe to expose to the browser.
- Do not hardcode Firebase config, API URLs, or project IDs when the repository already uses environment variables.
- If a task requires a new environment variable, update the relevant example or documentation file if one exists.

## File And Change Discipline

- Read the relevant code before editing.
- Follow the existing folder structure and naming conventions.
- Keep changes as small as possible while still solving the task correctly.
- Do not introduce new dependencies unless they are justified by the task.
- Do not refactor unrelated areas opportunistically.

## Testing And Validation

- Run the smallest meaningful validation for the changed area.
- For `Next.js` changes, prefer the repository's existing lint, type-check, and test commands.
- For `Express` changes, validate routing, request handling, and error behavior.
- For Firebase-related changes, use the local emulator workflow when available.
- If you cannot run validation, state exactly what was not verified.

## Deployment Awareness

- Do not assume a single deployment model.
- Confirm whether the project deploys `Next.js`, `Express`, and Firebase resources together or separately before changing deployment-related files.
- If Firebase Hosting, Cloud Functions, or Cloud Run are involved, preserve the current deployment path unless the task explicitly asks to change it.
- Call out any change that affects environment configuration, hosting rewrites, runtime regions, or server startup behavior.

## When To Ask Questions

Ask a short clarifying question before proceeding if the task depends on any of the following and the answer is not already in the repository:

- Whether the project uses the `App Router` or `Pages Router`
- Whether `Express` is a separate service, a custom server, or deployed through Firebase
- Whether Firebase uses direct client SDK access, Admin SDK access, or both
- Which Firebase products are in scope
- The expected deployment target

Otherwise, proceed with the safest repository-consistent assumption.

## Output Rules

- Write created files in English unless explicitly instructed otherwise.
- Use the user's language for chat replies.
- Keep explanations concise and practical.
- State assumptions, validation status, and important tradeoffs when they matter.

## Definition Of Done

- The requested change is implemented consistently with the current repository structure.
- `Next.js`, `Express`, and Firebase responsibilities remain clearly separated.
- Sensitive values are kept server-side.
- Relevant validation has been run, or skipped validation has been stated explicitly.

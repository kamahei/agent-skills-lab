# .env.example Policy

Use this policy when creating `.env.example` files for samples or templates in this repository.

## Goals

- Make sample environment files safe to publish.
- Keep example files easy to copy into a real project.
- Make public and secret values easy to distinguish.

## Rules

- Never put real secrets, tokens, private keys, or service account material in `.env.example`.
- Use placeholder values that clearly show the expected format.
- Group variables by purpose when the list is long.
- Add short comments only when they materially improve clarity.
- Include only variables that are actually needed for the sample.

## Naming Guidance

- Use the naming rules expected by the target framework or platform.
- For browser-exposed values in Next.js samples, use `NEXT_PUBLIC_*` only for values that are safe to expose.
- Keep server-only values separate from browser-safe values.

## Placeholder Guidance

Use placeholders such as:

- `your-project-id`
- `your-api-base-url`
- `your-firebase-api-key`
- `your-service-account-client-email`

Do not use placeholders that look like real credentials.

## When To Add A .env.example File

Add `.env.example` when:

- A sample requires environment variables to be understandable.
- A template is likely to be copied into a real application.
- The distinction between public and private values matters to safe usage.

Skip it when:

- The sample has no runtime configuration.
- The required configuration is better documented inline in the sample file itself.

## Recommended Structure

```dotenv
# Public client-side variables
NEXT_PUBLIC_APP_NAME=your-app-name
NEXT_PUBLIC_API_BASE_URL=http://localhost:3001

# Server-side variables
API_PORT=3001
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_CLIENT_EMAIL=your-service-account-client-email
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nreplace-me\n-----END PRIVATE KEY-----\n"
```

## Maintenance

- Update `.env.example` when adding or removing required environment variables in a sample.
- Keep placeholder values consistent with the rest of the documentation.
- If a sample has a `GUIDE.md`, mention how the `.env.example` file is meant to be used.

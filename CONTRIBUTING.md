\# Contributing Guide



\## Secrets and Environment Variables



\- Never commit API keys, passwords, access tokens, or other secrets to Git.

\- Store local environment variables in a `.env` file.

\- Ensure `.env` is listed in `.gitignore`.

\- Use `.env.example` as a template for the required environment variables.

\- Replace example values with your local configuration.

\- Never put real secrets in `.env.example`.

\- If a secret is accidentally committed or exposed, revoke or rotate it immediately.



\## Development Workflow



\- Create a separate branch for each issue.

\- Write clear commit messages.

\- Test your changes before opening a Pull Request.

\- Follow the project's Definition of Done.




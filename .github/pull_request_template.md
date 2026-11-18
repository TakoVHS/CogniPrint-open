## What and why

<!-- One or two sentences: the problem and the change. Link the issue if there is one. -->

## How it was verified

<!-- Commands run and their result, screenshots for UI, preview URL. -->

## Definition of done

- [ ] Lint, typecheck, tests and build pass locally and in CI
- [ ] New behaviour has a test; every bug fix has a regression test
- [ ] Inputs validated at the boundary (API, forms, webhooks); no silent `catch`
- [ ] No secrets, `.env` values or personal data in the diff
- [ ] Database changes go through a migration
- [ ] UI changes checked on mobile width and with the keyboard
- [ ] Preview deployment checked before production

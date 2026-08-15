# Contributing to NextGenManager

Thank you for your interest in contributing to NextGenManager! This guide will help you get started.

## Getting Started

1. **Fork** the repository on GitHub
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/nextgenmanager.git
   cd nextgenmanager
   ```
3. **Create a branch** for your work:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

See the [Installation](README.md#installation) section in the README for full setup instructions. In short:

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (separate terminal)
cd ../frontend
npm install
npm run dev
```

## How to Contribute

### Reporting Bugs

- Check [existing issues](https://github.com/siddhant2411/nextgenmanager/issues) first to avoid duplicates
- Use the **Bug Report** issue template
- Include steps to reproduce, expected behavior, and actual behavior
- Include your environment details (OS, Python version, browser)

### Suggesting Features

- Use the **Feature Request** issue template
- Explain the use case and why it would be valuable for manufacturers
- Be specific about the expected behavior

### Submitting Code

1. Make sure your code follows the existing patterns in the codebase
2. Each module follows: **Model > Schema > Service > Router > Dependencies**
3. Add Alembic migrations for any database changes (never edit existing migrations)
4. Test your changes locally before submitting
5. Keep commits focused and write clear commit messages

### Pull Request Process

1. Update the PR description with a summary of your changes
2. Link any related issues
3. Make sure the build passes: `pip install -r requirements.txt`
4. Keep PRs focused -- one feature or fix per PR
5. Be responsive to review feedback

## Code Guidelines

### Backend (Python/FastAPI)

- Follow existing package structure and naming conventions
- Use SQLAlchemy models for database entities
- Use Pydantic schemas for request/response validation
- Use Alembic for database migrations
- Soft-delete records using the `is_active` field -- never hard-delete
- Add docstrings to new endpoints for automatic API documentation

### Database

- Alembic migration files go in `backend/alembic/versions/`
- Naming: `{version_number}__description.py`
- **Never modify existing migration files** -- always create a new one
- Use PostgreSQL-compatible SQL

### Frontend (React)

- Components go in `src/components/`
- Pages go in `src/pages/`
- API calls go through service files in `src/services/`
- Use Material-UI components for consistency
- Form validation with Formik + Yup

## Good First Issues

Look for issues labeled [`good first issue`](https://github.com/siddhant2411/nextgenmanager/labels/good%20first%20issue) -- these are great entry points for new contributors.

Some areas that always welcome help:
- Documentation improvements
- UI/UX refinements
- Test coverage
- Bug fixes
- Translations

## Questions?

Open a [Discussion](https://github.com/siddhant2411/nextgenmanager/discussions) or comment on the relevant issue. We're happy to help you get started.

---

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.</arg_value>
</write_to_file></tool_call>
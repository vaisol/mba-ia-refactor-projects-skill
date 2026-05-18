# Architecture Guidelines (Target MVC Strict)

All refactoring must aim for this structure:

## 1. Model Layer
- **Responsibilities**: Data entities, business rules, domain services, validations.
- **Rules**:
  - NO knowledge of HTTP/Web framework.
  - NO raw SQL if using an ORM.
  - Data access abstracted via Repositories.

## 2. View/Route Layer
- **Responsibilities**: Endpoint definition, request parsing, response formatting.
- **Rules**:
  - NO business logic.
  - NO direct database access.
  - Calls Controller/Service layer.

## 3. Controller/Service Layer
- **Responsibilities**: Orchestration, security checks, calling models.
- **Rules**:
  - Lean controllers (delegate to Services).
  - Services contain the "how" of business logic.
  - Controllers handle the "what" of the request.

## 4. Utility Layer
- **Responsibilities**: Shared helpers, logging, configuration.
- **Rules**:
  - Pure functions where possible.
  - Centralized configuration via Environment Variables.

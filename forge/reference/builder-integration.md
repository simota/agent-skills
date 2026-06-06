# Forge Builder Integration

> Purpose: define the minimum artifact set and handoff contract required when a Forge prototype moves to Builder.
>
> Lifecycle (Throwaway vs Evolutionary), L0–L3 quality ladder, handoff pitfalls, and the canonical `.agents/forge-insights.md` template live in `reference/prototype-to-production.md`. This file covers only the artifact-set specifics: directory layout, type/error code templates, the `BUILDER_HANDOFF` block, and the production-conversion checklist.

## Contents

- Required output structure
- `types.ts` template
- `errors.ts` template
- `BUILDER_HANDOFF` block
- Prototype-to-production checklist

## Required Output Structure

```text
components/prototypes/
├── Feature.tsx          # required UI prototype
├── types.ts             # required type definitions
├── Feature.test.tsx     # optional quick tests
└── README.md            # optional usage notes

mocks/
├── handlers.ts          # required MSW handlers
└── errors.ts            # required error cases

.agents/
└── forge-insights.md    # required — see prototype-to-production.md for the canonical template
```

## `types.ts` Template

```typescript
// types.ts - Builder will translate these into production-grade domain types

export interface User {
  id: string;
  email: string;
  name: string;
  role: 'admin' | 'user' | 'guest';
  createdAt: string;
}

export interface Address {
  street: string;
  city: string;
  postalCode: string;
  country: string;
}

export interface CreateUserRequest {
  email: string;
  name: string;
  password: string;
}

export interface CreateUserResponse {
  user: User;
  token: string;
}

export interface ApiError {
  code: string;
  message: string;
  details?: Record<string, string>;
}
```

## `errors.ts` Template

```typescript
// mocks/errors.ts - Builder will map these into production error handling

import { http, HttpResponse } from 'msw';

export const errorHandlers = [
  http.post('/api/users', async ({ request }) => {
    const body = await request.json() as { email?: string; name?: string };

    if (!body.email) {
      return HttpResponse.json(
        { code: 'EMAIL_REQUIRED', message: 'Email is required' },
        { status: 400 }
      );
    }

    if (!body.email.includes('@')) {
      return HttpResponse.json(
        { code: 'INVALID_EMAIL', message: 'Email format is invalid' },
        { status: 400 }
      );
    }

    if (!body.name || body.name.length < 1) {
      return HttpResponse.json(
        { code: 'NAME_REQUIRED', message: 'Name is required' },
        { status: 400 }
      );
    }

    return HttpResponse.json({ id: '1', ...body }, { status: 201 });
  }),

  http.get('/api/protected', ({ request }) => {
    const token = request.headers.get('Authorization');
    if (!token) {
      return HttpResponse.json(
        { code: 'UNAUTHORIZED', message: 'Authentication is required' },
        { status: 401 }
      );
    }
    return HttpResponse.json({ data: 'secret' });
  }),

  http.delete('/api/admin/:id', () => {
    return HttpResponse.json(
      { code: 'FORBIDDEN', message: 'Insufficient permissions' },
      { status: 403 }
    );
  }),
];
```

## `.agents/forge-insights.md`

Canonical template lives in `reference/prototype-to-production.md` under "`.agents/forge-insights.md` Template (canonical)". Builder consumers should read that single source — do not duplicate the structure here.

## Builder Handoff Template

```markdown
## BUILDER_HANDOFF

### Prototype Info
- Location: `components/prototypes/[name].tsx`
- Types: `components/prototypes/types.ts`
- Mocks: `mocks/handlers.ts` + `mocks/errors.ts`
- Insights: `.agents/forge-insights.md`

### Validated Features
- [x] [Validated behavior 1]
- [x] [Validated behavior 2]

### For Builder to Implement
- [ ] Convert `types.ts` into production-grade domain types
- [ ] Replace `handlers.ts` with a real API client
- [ ] Map `errors.ts` into production error handling
- [ ] Implement the rules recorded in `.agents/forge-insights.md`

### Quick Reference
- API Base: `/api/v1`
- Auth: `Bearer` token in header
- Error format: `{ code: string, message: string }`
```

## Prototype-to-Production Checklist

### Code Quality
- [ ] Remove debug logging
- [ ] Replace placeholder styles if the prototype is being adopted
- [ ] Remove `any`
- [ ] Extract magic numbers if the value is reused
- [ ] Convert lingering `#TODO(agent)` items into tickets if the work is adopted

### Error Handling
- [ ] Add loading states
- [ ] Add error states with retry where relevant
- [ ] Handle empty, null, and undefined states
- [ ] Add minimum validation rules

### API Integration
- [ ] Replace mock data with real API calls
- [ ] Keep request and response types explicit
- [ ] Handle API errors gracefully

### Testing
- [ ] Add at least the tests Builder needs for the validated behavior
- [ ] Test one error scenario
- [ ] Test one loading or async scenario

### Accessibility
- [ ] Add the minimum ARIA labels required by the prototype path
- [ ] Ensure basic keyboard navigation
- [ ] Check contrast for key actions and status states

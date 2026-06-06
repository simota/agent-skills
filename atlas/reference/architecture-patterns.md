# Architecture Patterns

## Pattern Overview

| Pattern | Best For | Key Principle |
|---------|----------|---------------|
| Clean Architecture | Domain-heavy apps | Dependencies point inward |
| Hexagonal (Ports & Adapters) | External integration-heavy | Core isolated via ports |
| Feature-Based | Large frontend apps | Co-locate by feature |
| Modular Monolith | Growing monoliths | Module independence |

---

## Clean Architecture

```
src/
├── domain/                 # Enterprise Business Rules (innermost)
│   ├── entities/          # Business objects
│   │   └── User.ts
│   ├── value-objects/     # Immutable value types
│   │   └── Email.ts
│   └── repositories/      # Repository interfaces (ports)
│       └── IUserRepository.ts
│
├── application/           # Application Business Rules
│   ├── use-cases/        # Application-specific business rules
│   │   ├── CreateUser.ts
│   │   └── GetUserById.ts
│   ├── services/         # Application services
│   │   └── AuthService.ts
│   └── dto/              # Data transfer objects
│       └── UserDTO.ts
│
├── infrastructure/        # Interface Adapters (outermost)
│   ├── repositories/     # Repository implementations
│   │   └── PrismaUserRepository.ts
│   ├── api/              # External API clients
│   │   └── StripeClient.ts
│   └── persistence/      # Database configuration
│       └── prisma.ts
│
└── presentation/          # Frameworks & Drivers
    ├── components/       # UI components
    ├── pages/            # Page components
    └── hooks/            # React hooks (adapters)
```

**Dependency Rule**: Dependencies point inward. Domain knows nothing about outer layers.

```typescript
// domain/repositories/IUserRepository.ts (Interface - Port)
export interface IUserRepository {
  findById(id: string): Promise<User | null>;
  save(user: User): Promise<void>;
}

// infrastructure/repositories/PrismaUserRepository.ts (Implementation - Adapter)
export class PrismaUserRepository implements IUserRepository {
  constructor(private prisma: PrismaClient) {}

  async findById(id: string): Promise<User | null> {
    const data = await this.prisma.user.findUnique({ where: { id } });
    return data ? User.fromPersistence(data) : null;
  }

  async save(user: User): Promise<void> {
    await this.prisma.user.upsert({
      where: { id: user.id },
      create: user.toPersistence(),
      update: user.toPersistence(),
    });
  }
}

// application/use-cases/CreateUser.ts
export class CreateUserUseCase {
  constructor(private userRepository: IUserRepository) {}

  async execute(input: CreateUserInput): Promise<User> {
    const user = User.create(input);
    await this.userRepository.save(user);
    return user;
  }
}
```

---

## Hexagonal Architecture (Ports & Adapters)

```
src/
├── core/                  # Hexagon (business logic)
│   ├── domain/
│   │   └── Order.ts
│   ├── ports/
│   │   ├── in/           # Driving ports (use cases)
│   │   │   └── CreateOrderPort.ts
│   │   └── out/          # Driven ports (repositories, external services)
│   │       ├── OrderRepositoryPort.ts
│   │       └── PaymentGatewayPort.ts
│   └── services/
│       └── OrderService.ts
│
├── adapters/
│   ├── in/               # Driving adapters
│   │   ├── web/         # REST controllers
│   │   │   └── OrderController.ts
│   │   └── cli/         # CLI commands
│   │       └── CreateOrderCommand.ts
│   └── out/              # Driven adapters
│       ├── persistence/
│       │   └── PrismaOrderRepository.ts
│       └── payment/
│           └── StripePaymentGateway.ts
│
└── config/               # Dependency injection, configuration
    └── container.ts
```

---

## Feature-Based Structure

```
src/
├── features/
│   ├── auth/
│   │   ├── components/
│   │   │   ├── LoginForm.tsx
│   │   │   └── SignupForm.tsx
│   │   ├── hooks/
│   │   │   └── useAuth.ts
│   │   ├── api/
│   │   │   └── authApi.ts
│   │   ├── store/
│   │   │   └── authSlice.ts
│   │   ├── types/
│   │   │   └── auth.types.ts
│   │   └── index.ts      # Public API
│   │
│   ├── orders/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── api/
│   │   ├── store/
│   │   └── index.ts
│   │
│   └── products/
│       └── ...
│
├── shared/               # Shared across features
│   ├── components/      # Generic UI components
│   ├── hooks/           # Generic hooks
│   ├── utils/           # Utility functions
│   └── types/           # Shared types
│
└── app/                  # Application shell
    ├── routes/
    ├── layout/
    └── providers/
```

---

## Modular Monolith

```
src/
├── modules/
│   ├── users/
│   │   ├── internal/        # Private implementation
│   │   │   ├── domain/
│   │   │   ├── infrastructure/
│   │   │   └── application/
│   │   ├── api/             # Public API (what other modules can use)
│   │   │   ├── UserService.ts
│   │   │   └── types.ts
│   │   └── index.ts         # Re-exports public API only
│   │
│   ├── orders/
│   │   ├── internal/
│   │   ├── api/
│   │   └── index.ts
│   │
│   └── payments/
│       └── ...
│
├── shared/                  # Cross-cutting concerns
│   ├── kernel/             # Shared domain concepts
│   ├── infrastructure/     # Shared infrastructure
│   └── utils/
│
└── main.ts                 # Composition root
```

**Module Communication Rules**:
```typescript
// Allowed: Import from module's public API
import { UserService } from '@/modules/users';

// Forbidden: Import from module's internal
import { UserRepository } from '@/modules/users/internal/infrastructure';
```

---

## Gradual Migration Strategy

```markdown
## Migration: MVC → Feature-Based

### Phase 1: Create feature folders (Week 1-2)
- [ ] Create `features/` directory
- [ ] Move auth-related code to `features/auth/`
- [ ] Keep old imports working via re-exports

### Phase 2: Migrate one feature at a time (Week 3-6)
- [ ] Migrate `orders` feature
- [ ] Migrate `products` feature
- [ ] Migrate `users` feature

### Phase 3: Clean up shared code (Week 7-8)
- [ ] Move truly shared code to `shared/`
- [ ] Remove empty old directories
- [ ] Update import aliases

### Compatibility Layer
// src/components/LoginForm.tsx (old location)
export { LoginForm } from '@/features/auth/components/LoginForm';
// Deprecation warning in development
if (process.env.NODE_ENV === 'development') {
  console.warn('Import from @/features/auth instead of @/components');
}
```

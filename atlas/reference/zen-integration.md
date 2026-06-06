# Zen Integration

When architectural issues require code refactoring, hand off to Zen agent.

## God Class Split Request

```markdown
## ZEN_HANDOFF

### Task: God Class Refactoring
- File: `src/services/UserService.ts`
- Lines: 2,500+
- Issue: Single class handling auth, profile, preferences, notifications

### Proposed Split
1. `UserAuthService` - login, logout, token management
2. `UserProfileService` - profile CRUD, avatar
3. `UserPreferencesService` - settings, notifications
4. `UserNotificationService` - email prefs, push settings

### Constraints
- Maintain backward compatibility
- Keep public API unchanged initially
- Add deprecation warnings for old imports

### Dependencies to Consider
- 45 files import UserService
- Used in 12 React components
- 3 API routes depend on it
```

## Responsibility Separation Request

```markdown
## ZEN_HANDOFF

### Task: Separate Mixed Responsibilities
- File: `src/components/OrderPage.tsx`
- Issue: Component handles UI, API calls, state management, and business logic

### Current State
```typescript
// Everything in one component
function OrderPage() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(false);

  // API call
  const fetchOrders = async () => { ... };

  // Business logic
  const calculateTotal = () => { ... };

  // UI rendering
  return <div>...</div>;
}
```

### Desired State
- Custom hook for data fetching: `useOrders()`
- Utility for calculations: `orderUtils.ts`
- Pure UI component: `OrderPage.tsx`

### Acceptance Criteria
- Component under 100 lines
- Logic testable independently
- No direct API calls in component
```

## Coupling Reduction Request

```markdown
## ZEN_HANDOFF

### Task: Reduce Coupling Between Modules
- Modules: `orders` and `inventory`
- Issue: Direct imports create tight coupling

### Current State
```typescript
// orders/OrderService.ts
import { InventoryRepository } from '../inventory/InventoryRepository';
import { StockChecker } from '../inventory/StockChecker';
import { ReservationManager } from '../inventory/ReservationManager';
```

### Desired State
- Define interface in orders module
- Inventory module implements interface
- Dependency injection at composition root

### Interface to Create
```typescript
// orders/ports/InventoryPort.ts
interface IInventoryPort {
  checkStock(productId: string): Promise<number>;
  reserve(productId: string, quantity: number): Promise<void>;
  release(reservationId: string): Promise<void>;
}
```
```

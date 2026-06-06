# TypeScript/React Refactoring Patterns

Purpose: Use this file when the target is TypeScript, JavaScript, or React and you need language-specific cleanup patterns.

## Contents
- [TypeScript Refactoring](#typescript-refactoring)
- [React Refactoring](#react-refactoring)

Language-specific refactoring patterns for TypeScript and React codebases.

---

## TypeScript Refactoring

### Simplify Complex Types

```typescript
// Before: Inline complex type
function processUser(user: { id: string; name: string; email: string; role: 'admin' | 'user' }) { ... }

// After: Extract type
type UserRole = 'admin' | 'user';
interface User {
  id: string;
  name: string;
  email: string;
  role: UserRole;
}
function processUser(user: User) { ... }
```

### Replace String Unions with Enum (when appropriate)

```typescript
// Before: String literals scattered
function setStatus(status: 'pending' | 'active' | 'completed') { ... }
if (status === 'pending') { ... }

// After: Centralized enum
enum Status {
  Pending = 'pending',
  Active = 'active',
  Completed = 'completed',
}
function setStatus(status: Status) { ... }
if (status === Status.Pending) { ... }
```

### Narrow Types

```typescript
// Before: Overly broad type
function processData(data: any) { ... }

// After: Specific type
interface ProcessableData {
  id: string;
  values: number[];
}
function processData(data: ProcessableData) { ... }
```

### Discriminated Union for State

```typescript
// Before: Multiple booleans
interface RequestState {
  loading: boolean;
  error: Error | null;
  data: Data | null;
}

// After: Discriminated union
type RequestState =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'error'; error: Error }
  | { status: 'success'; data: Data };
```

### Replace Type Assertion with Type Guard

```typescript
// Before: Unsafe assertion
const user = data as User;

// After: Runtime type guard
function isUser(data: unknown): data is User {
  return typeof data === 'object' && data !== null && 'id' in data && 'name' in data;
}
if (isUser(data)) {
  // data is safely narrowed to User
}
```

---

## React Refactoring

### Extract Custom Hook

```typescript
// Before: Logic in component
function UserProfile({ userId }: Props) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    setLoading(true);
    fetchUser(userId)
      .then(setUser)
      .catch(setError)
      .finally(() => setLoading(false));
  }, [userId]);

  if (loading) return <Loading />;
  if (error) return <Error error={error} />;
  return <Profile user={user!} />;
}

// After: Extracted hook
function useUser(userId: string) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    setLoading(true);
    fetchUser(userId)
      .then(setUser)
      .catch(setError)
      .finally(() => setLoading(false));
  }, [userId]);

  return { user, loading, error };
}

function UserProfile({ userId }: Props) {
  const { user, loading, error } = useUser(userId);
  if (loading) return <Loading />;
  if (error) return <Error error={error} />;
  return <Profile user={user!} />;
}
```

### Split Large Components

```typescript
// Before: Monolithic component (200+ lines)
function Dashboard() {
  // ... 50 lines of hooks and state
  return (
    <div>
      {/* 150 lines of JSX */}
    </div>
  );
}

// After: Composed from smaller components
function Dashboard() {
  return (
    <DashboardLayout>
      <DashboardHeader />
      <DashboardMetrics />
      <DashboardCharts />
      <DashboardRecentActivity />
    </DashboardLayout>
  );
}
```

### Memoization for Performance

```typescript
// Before: Recreating objects on every render
function List({ items, onSelect }: Props) {
  return items.map(item => (
    <ListItem
      key={item.id}
      item={item}
      style={{ padding: 10, margin: 5 }}  // New object every render
      onSelect={() => onSelect(item.id)}  // New function every render
    />
  ));
}

// After: Memoized values
const itemStyle = { padding: 10, margin: 5 };  // Stable reference

function List({ items, onSelect }: Props) {
  const handleSelect = useCallback(
    (id: string) => onSelect(id),
    [onSelect]
  );

  return items.map(item => (
    <ListItem
      key={item.id}
      item={item}
      style={itemStyle}
      onSelect={handleSelect}
    />
  ));
}
```

### Prop Drilling to Context

```typescript
// Before: Props passed through 4+ levels
<App user={user}>
  <Layout user={user}>
    <Sidebar user={user}>
      <UserMenu user={user} />
    </Sidebar>
  </Layout>
</App>

// After: Context for shared state
const UserContext = createContext<User | null>(null);

function App() {
  const [user, setUser] = useState<User | null>(null);
  return (
    <UserContext.Provider value={user}>
      <Layout>
        <Sidebar>
          <UserMenu />
        </Sidebar>
      </Layout>
    </UserContext.Provider>
  );
}

function UserMenu() {
  const user = useContext(UserContext);
  // ...
}
```

### Replace Render Props with Hook

```typescript
// Before: Render prop pattern
<DataFetcher url="/api/users">
  {({ data, loading, error }) => (
    loading ? <Spinner /> : <UserList users={data} />
  )}
</DataFetcher>

// After: Custom hook
function UserList() {
  const { data, loading, error } = useFetch<User[]>('/api/users');
  if (loading) return <Spinner />;
  if (error) return <ErrorDisplay error={error} />;
  return <List items={data} />;
}
```

### Extract Compound Component

```typescript
// Before: Monolithic with many props
<Select
  options={options}
  value={value}
  onChange={onChange}
  label="Country"
  placeholder="Select..."
  searchable={true}
  clearable={true}
  renderOption={(opt) => <Flag code={opt.code} />}
/>

// After: Compound component
<Select value={value} onChange={onChange}>
  <Select.Label>Country</Select.Label>
  <Select.Trigger placeholder="Select..." />
  <Select.Search />
  <Select.Options>
    {options.map(opt => (
      <Select.Option key={opt.value} value={opt.value}>
        <Flag code={opt.code} /> {opt.label}
      </Select.Option>
    ))}
  </Select.Options>
  <Select.ClearButton />
</Select>
```

# Frontend Patterns Reference

Builder agent's React frontend implementation patterns.

## React Server Components (RSC)

**Key rules:**
- Server Components are the **DEFAULT** in Next.js App Router
- `'use client'` is the **EXCEPTION** — use only for interactivity/browser APIs
- Push client components down to the leaves of the component tree
- Use Server Actions for form mutations (replaces API routes)

```tsx
// Server Component (default) — direct data access, no 'use client'
async function UsersPage() {
  const users = await db.users.findMany(); // Server-side DB access
  return <UserList users={users} />;
}

// Client Component (exception) — interactivity only
'use client';
export function SearchBar({ onSearch }: Props) {
  const [query, setQuery] = useState('');
  return <input value={query} onChange={e => setQuery(e.target.value)} />;
}
```

```typescript
// Server Action — form processing (replaces API routes for mutations)
// app/actions/users.ts
'use server';
export async function createUser(formData: FormData) {
  const name = formData.get('name') as string;
  await db.users.create({ data: { name } });
  revalidatePath('/users');
}

// Usage in a Server Component form
export default function NewUserPage() {
  return (
    <form action={createUser}>
      <input name="name" />
      <button type="submit">Add User</button>
    </form>
  );
}
```

## State Management Selection Matrix

```
State Type        → Recommended Tool
─────────────────────────────────────
Server State      → TanStack Query v5
Client Global     → Zustand (small-med) / Redux Toolkit (large)
Client Local      → useState / useReducer
Atomic/Derived    → Jotai
Complex Flows     → XState
Form State        → React Hook Form + Zod v4

Anti-pattern: Same data in multiple stores (e.g., both Context API and Redux)
```

### Server State (TanStack Query v5)

```typescript
// TanStack Query v5: no more onSuccess/onError in useQuery
const { data, error, isPending } = useQuery({
  queryKey: ['users', id],
  queryFn: () => fetchUser(id),
});

// Mutations with optimistic updates
const mutation = useMutation({
  mutationFn: updateUser,
  onMutate: async (newUser) => {
    await queryClient.cancelQueries({ queryKey: ['users', newUser.id] });
    const previous = queryClient.getQueryData(['users', newUser.id]);
    queryClient.setQueryData(['users', newUser.id], newUser);
    return { previous };
  },
  onError: (err, newUser, context) => {
    queryClient.setQueryData(['users', newUser.id], context?.previous);
  },
  onSettled: () => {
    queryClient.invalidateQueries({ queryKey: ['users'] });
  },
});
```

### Client State (Zustand)

```typescript
// stores/uiStore.ts
interface UIState {
  sidebarOpen: boolean;
  theme: 'light' | 'dark';
  toggleSidebar: () => void;
  setTheme: (theme: 'light' | 'dark') => void;
}

export const useUIStore = create<UIState>((set) => ({
  sidebarOpen: true,
  theme: 'light',
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  setTheme: (theme) => set({ theme }),
}));
```

## Form Design (React Hook Form + Zod)

```typescript
// schemas/userForm.ts
const userFormSchema = z.object({
  name: z.string().min(1, 'Name is required').max(100),
  email: z.string().email('Please enter a valid email address'),
  age: z.coerce.number().int().min(0).max(150).optional(),
});

type UserFormData = z.infer<typeof userFormSchema>;

// components/UserForm.tsx
export function UserForm({ onSubmit }: { onSubmit: (data: UserFormData) => void }) {
  const form = useForm<UserFormData>({
    resolver: zodResolver(userFormSchema),
    defaultValues: { name: '', email: '' },
  });

  return (
    <form onSubmit={form.handleSubmit(onSubmit)}>
      <input {...form.register('name')} />
      {form.formState.errors.name && (
        <span className="error">{form.formState.errors.name.message}</span>
      )}

      <input {...form.register('email')} />
      {form.formState.errors.email && (
        <span className="error">{form.formState.errors.email.message}</span>
      )}

      <button type="submit" disabled={form.formState.isSubmitting}>
        {form.formState.isSubmitting ? 'Submitting...' : 'Submit'}
      </button>
    </form>
  );
}
```

## Error Boundary + Suspense

```typescript
// components/ErrorBoundary.tsx
'use client';

export function ErrorBoundary({
  children,
  fallback,
}: {
  children: React.ReactNode;
  fallback: React.ReactNode;
}) {
  return (
    <ErrorBoundaryPrimitive
      fallbackRender={({ error, resetErrorBoundary }) => (
        <div className="error-container">
          <h2>An error occurred</h2>
          <p>{error.message}</p>
          <button onClick={resetErrorBoundary}>Retry</button>
        </div>
      )}
    >
      {children}
    </ErrorBoundaryPrimitive>
  );
}

// app/users/page.tsx
export default function UsersPage() {
  return (
    <ErrorBoundary fallback={<ErrorFallback />}>
      <Suspense fallback={<UserListSkeleton />}>
        <UserList />
      </Suspense>
    </ErrorBoundary>
  );
}
```

## Optimistic UI Updates

```typescript
// hooks/useOptimisticLike.ts
export function useOptimisticLike(postId: string) {
  const queryClient = useQueryClient();
  const [optimisticLiked, setOptimisticLiked] = useState<boolean | null>(null);
  const mutation = useMutation({
    mutationFn: () => postApi.toggleLike(postId),
    onMutate: async () => {
      const prev = queryClient.getQueryData<Post>(['posts', postId]);
      setOptimisticLiked(!prev?.liked);
      return { prev };
    },
    onError: () => { setOptimisticLiked(null); toast.error('Failed to like'); },
    onSuccess: () => {
      setOptimisticLiked(null);
      queryClient.invalidateQueries({ queryKey: ['posts', postId] });
    },
  });
  const post = queryClient.getQueryData<Post>(['posts', postId]);
  return { liked: optimisticLiked ?? post?.liked ?? false, toggle: mutation.mutate, isLoading: mutation.isPending };
}
```

---

**Source:** [Vercel: Understanding React Server Components](https://vercel.com/blog/understanding-react-server-components) · [developerway: React State Management 2025](https://www.developerway.com/posts/react-state-management-2025) · [Strapi: React & Next.js 2025 Best Practices](https://strapi.io/blog/react-and-nextjs-in-2025-modern-best-practices)

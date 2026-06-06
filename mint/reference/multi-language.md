# Multi-Language Test Data Support

**Purpose:** Language-specific factory and fixture patterns.
**Read when:** Generating test data for non-JavaScript/TypeScript projects.

---

## Python

### Polyfactory (Pydantic)

```python
from polyfactory.factories.pydantic_factory import ModelFactory
from faker import Faker
from app.models import User, Order

fake = Faker(['ja_JP', 'en_US'])

class UserFactory(ModelFactory):
    __model__ = User

    @classmethod
    def name(cls) -> str:
        return fake.name()

    @classmethod
    def email(cls) -> str:
        return fake.email()

# Usage
user = UserFactory.build()
users = UserFactory.batch(10)
admin = UserFactory.build(role='admin')
```

### factory_boy (Django)

```python
import factory
from factory import fuzzy
from app.models import User, Order

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    name = factory.Faker('name', locale='ja_JP')
    email = factory.LazyAttribute(lambda o: f'{o.name.lower()}@test.example.com')
    role = 'user'

    class Params:
        admin = factory.Trait(role='admin')
        deleted = factory.Trait(deleted_at=factory.Faker('date_time_this_year'))

class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)
    total = fuzzy.FuzzyDecimal(100, 99999, precision=2)
    status = 'pending'
```

### Hypothesis (Property-Based)

```python
from hypothesis import given, strategies as st, settings

user_strategy = st.fixed_dictionaries({
    'name': st.text(min_size=1, max_size=100),
    'email': st.emails(),
    'age': st.integers(min_value=0, max_value=150),
    'role': st.sampled_from(['user', 'admin', 'moderator']),
})

@given(user=user_strategy)
@settings(max_examples=100)
def test_user_validation(user):
    result = validate_user(user)
    assert isinstance(result, ValidationResult)
```

---

## Go

### gofakeit + Custom Builders

```go
package testdata

import "github.com/brianvoss/gofakeit/v7"

type UserBuilder struct {
    user User
}

func NewUserBuilder() *UserBuilder {
    gofakeit.Seed(42)
    return &UserBuilder{
        user: User{
            ID:    gofakeit.UUID(),
            Name:  gofakeit.Name(),
            Email: gofakeit.Email(),
            Role:  "user",
        },
    }
}

func (b *UserBuilder) Admin() *UserBuilder {
    b.user.Role = "admin"
    return b
}

func (b *UserBuilder) Deleted() *UserBuilder {
    t := time.Now().Add(-24 * time.Hour)
    b.user.DeletedAt = &t
    return b
}

func (b *UserBuilder) Build() User {
    return b.user
}

// Usage
user := NewUserBuilder().Admin().Build()
```

### rapid (Property-Based)

```go
import "pgregory.net/rapid"

func TestUserValidation(t *testing.T) {
    rapid.Check(t, func(t *rapid.T) {
        name := rapid.String().Draw(t, "name")
        age := rapid.IntRange(0, 150).Draw(t, "age")
        user := User{Name: name, Age: age}
        err := user.Validate()
        if err != nil {
            t.Logf("validation error: %v", err)
        }
    })
}
```

---

## Rust

### fake-rs

```rust
use fake::{Dummy, Fake, Faker};
use fake::faker::name::en::*;
use fake::faker::internet::en::*;

#[derive(Debug, Dummy)]
struct User {
    #[dummy(faker = "1..1000")]
    id: i32,
    #[dummy(faker = "Name()")]
    name: String,
    #[dummy(faker = "SafeEmail()")]
    email: String,
}

// Usage
let user: User = Faker.fake();
let users: Vec<User> = (0..10).map(|_| Faker.fake()).collect();
```

### proptest

```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn test_user_name_not_empty(
        name in ".{1,100}",
        age in 0u32..150,
    ) {
        let user = User::new(&name, age);
        assert!(!user.name().is_empty());
    }
}
```

---

## Java

### Instancio

```java
import org.instancio.Instancio;
import org.instancio.Select;

// Auto-generate with customization
User user = Instancio.of(User.class)
    .set(Select.field(User::getRole), "admin")
    .set(Select.field(User::getEmail), "admin@test.example.com")
    .create();

// Batch generation
List<User> users = Instancio.ofList(User.class)
    .size(100)
    .create();
```

### jqwik (Property-Based)

```java
@Property
void userValidation(
    @ForAll @StringLength(min = 1, max = 100) String name,
    @ForAll @IntRange(min = 0, max = 150) int age
) {
    User user = new User(name, age);
    assertThat(user.validate()).isNotNull();
}
```

---

## Library Quick Reference

| Language | Factory | Faker | Property-Based |
|----------|---------|-------|----------------|
| JS/TS | Fishery | @faker-js/faker | fast-check |
| Python | Polyfactory / factory_boy | Faker | Hypothesis |
| Go | Custom builders | gofakeit | rapid |
| Rust | Custom + Dummy derive | fake-rs | proptest |
| Java | Instancio | JavaFaker | jqwik |
| Ruby | factory_bot | Faker | Rantly |

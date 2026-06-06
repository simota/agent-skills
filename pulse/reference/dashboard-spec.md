# Dashboard Specification

## Dashboard Template

```markdown
## Dashboard: [Dashboard Name]

**Purpose:** [What questions does this dashboard answer?]
**Audience:** [Who will use this dashboard?]
**Refresh Rate:** [Real-time | Hourly | Daily]

### Sections

#### 1. Executive Summary
- North Star Metric (current + trend)
- Key conversion rates
- Revenue metrics (if applicable)

#### 2. Acquisition
- New users by source
- Signup funnel conversion
- CAC by channel

#### 3. Engagement
- DAU/WAU/MAU
- Feature adoption rates
- Session frequency & duration

#### 4. Retention
- Cohort retention curves
- Churn rate
- Reactivation rate

#### 5. Revenue (if applicable)
- MRR/ARR
- ARPU
- LTV/CAC ratio

### Filters
- Date range
- User segment
- Platform (web/mobile)
- Geography
```

## Chart Specifications

```typescript
interface ChartSpec {
  title: string;
  type: 'line' | 'bar' | 'funnel' | 'table' | 'number';
  metric: string;
  dimensions?: string[];
  timeGranularity?: 'hour' | 'day' | 'week' | 'month';
  comparison?: 'previous_period' | 'year_over_year';
  goal?: number;
}

const dashboardCharts: ChartSpec[] = [
  {
    title: 'Daily Active Users',
    type: 'line',
    metric: 'unique_users',
    timeGranularity: 'day',
    comparison: 'previous_period',
    goal: 10000
  },
  {
    title: 'Signup Funnel',
    type: 'funnel',
    metric: 'conversion_rate',
    dimensions: ['step_name']
  },
  {
    title: 'Revenue by Plan',
    type: 'bar',
    metric: 'mrr',
    dimensions: ['plan_type'],
    timeGranularity: 'month'
  }
];
```

# Production Pipeline Lab

A hands-on data engineering project focused on building reliable, incremental data pipelines using Python, SQL, and dbt.

The project builds on the Stroopwafel shop dataset from *Fundamentals of Analytics Engineering*. Rather than extending the original Google Sheets → Airbyte → BigQuery → dbt Cloud → Tableau pipeline, this project implements custom ingestion components and explores the operational challenges of maintaining data pipelines.

## Project goals

The primary goal is to develop practical experience designing, implementing, and operating data pipelines beyond the analytical transformation layer.

Key learning objectives:

- **Incremental ingestion:** Checkpoints, watermarks, updated records, and late-arriving data.
- **Reliability:** Idempotency, safe reruns, retries, partial failures, and recovery.
- **Data lifecycle:** Backfills, replay, corrections, and deletion handling.
- **Data quality:** Validation, reconciliation, completeness checks, and observability.
- **Orchestration:** Scheduling, dependencies, and pipeline execution.
- **Python engineering:** Project structure, configuration, logging, error handling, typing, and automated testing.

The emphasis is on understanding engineering trade-offs and failure modes, rather than assembling a complex technology stack.

## Architecture

The initial architecture is:

```text
Historical CSV data
       |
       v
SQLite operational database
       ^
       |
Python source simulator
       |
       | New sales, updates, cancellations
       v
SQLite source state
       |
       | Incremental extraction
       v
Python ingestion pipeline
       |
       | Upsert + checkpoint
       v
DuckDB analytical database
       |
       v
dbt Core
       |
       v
Analytical models and data quality tests
```

The historical CSV files initialize a simulated operational database. A Python program will then generate new transactions and modify existing ones.

A separate ingestion pipeline will extract changes from the SQLite source and load them into DuckDB.

The first implementation will run locally. Orchestration and additional infrastructure will be introduced only when the pipeline has meaningful operational requirements.

### Initial technology choices

| Component | Technology | Purpose |
|---|---|---|
| Version control | Git / GitHub | Source control and project history |
| Python environment | uv | Dependency and environment management |
| Operational database | SQLite | Simulated transactional data source |
| Ingestion | Python | Incremental extraction, validation, and loading |
| Analytical database | DuckDB | Persisted destination data and checkpoints |
| Transformations | dbt Core | Analytical models and data quality tests |
| Orchestration | TBD | Future scheduling and dependency management |

Technology choices may evolve as the project develops.

## Dataset

The project uses the Stroopwafel shop dataset provided as part of *Fundamentals of Analytics Engineering*.

The dataset contains:

- Sales — transaction headers, amounts, and payment information.
- Sales_lines — purchased products, quantities, and discounts.
- Products — product catalogue and prices.
- Promotions — product promotions and validity periods.
- Shifts — employee shifts.
- Employees — employee reference data.

The initial implementation focuses on the `sales` table. Related tables will be introduced as the ingestion pipeline evolves.

## Implementation roadmap

### Phase 1 — Establish the operational source

**Goal:** Create a reproducible local source database initialized with historical transactions.

- [ ] Initialize the Git repository and Python project using uv.
- [ ] Create the SQLite operational database.
- [ ] Define the `sales` schema, including primary key and `source_updated_at`.
- [ ] Implement a Python script to import historical sales from CSV.
- [ ] Convert monetary values to integer cents.
- [ ] Make the seed import safe to rerun without overwriting subsequent source changes.
- [ ] Validate row counts, primary-key uniqueness, and required fields.
- [ ] Document how to recreate the source database from the seed files.

**Success criteria:** The database can be recreated from scratch, and rerunning the seed loader does not produce duplicate transactions or overwrite changes to existing records.

### Phase 2 — Build incremental ingestion

**Goal:** Synchronize new and modified sales from SQLite to DuckDB.

- [ ] Create a destination `sales` table in DuckDB.
- [ ] Create persistent ingestion checkpoint metadata.
- [ ] Implement incremental extraction using `source_updated_at`.
- [ ] Define a safe watermark strategy, initially using an inclusive timestamp boundary.
- [ ] Implement destination upserts keyed by `sales_id`.
- [ ] Commit destination changes and checkpoint updates atomically.
- [ ] Verify behavior for an initial full load and subsequent incremental runs.
- [ ] Verify that repeated runs do not duplicate records.
- [ ] Verify that modifications to existing source sales propagate correctly.

**Success criteria:** New and corrected sales appear in the destination, unchanged runs are safe, and checkpoints survive process restarts.

### Phase 3 — Simulate source changes

**Goal:** Generate realistic changing transactional data.

- [ ] Build a simple Python generator for new sales.
- [ ] Generate associated sales lines.
- [ ] Simulate corrections to previously created sales.
- [ ] Introduce delayed or backdated transactions.
- [ ] Simulate cancellations.
- [ ] Ensure source changes maintain appropriate modification metadata.
- [ ] Make test scenarios reproducible using deterministic inputs.

**Success criteria:** The pipeline can ingest a changing source without relying on knowledge of how the simulator generated its data.

### Phase 4 — Reliability and recovery

**Goal:** Make ingestion resilient to failures and repeated execution.

- [ ] Introduce paginated or batched extraction.
- [ ] Test interruptions during ingestion.
- [ ] Ensure failed runs do not incorrectly advance checkpoints.
- [ ] Implement safe reruns and recovery from partial failures.
- [ ] Evaluate retry strategies for transient errors.
- [ ] Test records sharing the same modification timestamp.
- [ ] Investigate the limitations of timestamp-based watermarks.
- [ ] Implement controlled backfills or replay.
- [ ] Add automated tests for failure and recovery scenarios.

**Success criteria:** The pipeline can recover from simulated failures without silently missing records or creating duplicates.

### Phase 5 — Expand the data model and handle deletes

**Goal:** Move from a single-table exercise toward a realistic transactional pipeline.

- [ ] Ingest `sales_lines` and related reference tables.
- [ ] Address consistency between sales headers and line items.
- [ ] Introduce corrections and changes affecting multiple related tables.
- [ ] Investigate soft deletes, hard deletes, and CDC approaches.
- [ ] Decide where historical record versions should be preserved.
- [ ] Implement appropriate deletion and update semantics.

**Success criteria:** The destination remains consistent with supported source changes, including changes to related records and
# Project 11: Concurrent Data Processor

**Level:** Backend Engineering
**Estimated Time:** 20–28 hours

---

## Overview

Implement the same data processing workload using three different concurrency models: sequential, thread-based, and asyncio. Measure and compare their performance characteristics.

---

## Objectives

- Understand the difference between concurrency and parallelism.
- Implement asyncio with `async`/`await`.
- Implement thread-based concurrency.
- Measure and interpret performance differences.

---

## Python Concepts Practised

- `asyncio`
- `async`/`await`
- `asyncio.gather()`
- `threading.Thread`
- `concurrent.futures.ThreadPoolExecutor`
- `concurrent.futures.ProcessPoolExecutor`
- `time.perf_counter` for benchmarking
- Shared state and thread safety

---

## Functional Requirements

Implement all three approaches for the same workload. Suggested workload: fetch data from multiple URLs.

1. **Sequential:** Process each item one at a time.
2. **Thread-based:** Process items using a thread pool.
3. **Asyncio:** Process items using async/await and `asyncio.gather()`.

Measure for each approach:
- Total execution time.
- Throughput (items per second).
- Error count.

Output a comparison table.

---

## Non-Functional Requirements

- Each implementation must be clearly separated.
- Results must be deterministic enough to be comparable.
- Benchmarks must use `time.perf_counter`.

---

## Edge Cases

- Item processing that fails (simulate with a failure rate).
- Zero items.
- Single item.
- Large number of items (100+).

---

## Acceptance Criteria

- [ ] All three approaches produce the same results for the same input.
- [ ] Performance measurements are captured for all three.
- [ ] Comparison table is printed.
- [ ] Errors are counted and reported, not silently swallowed.

---

## Documentation Requirement

Write a `ANALYSIS.md` explaining:
- When to use sequential processing.
- When to use threads.
- When to use asyncio.
- What the GIL means for CPU-bound vs I/O-bound work.

---

## Suggested Implementation Steps

1. Define the work unit.
2. Implement sequential version.
3. Implement thread pool version.
4. Implement asyncio version.
5. Implement the benchmarking harness.
6. Run comparisons and document findings.
7. Write tests.

---

## Testing Requirements

- Test that each implementation processes all items.
- Test that errors are captured, not raised.
- Test the benchmarking result structure.

---

## Constraints

- Use `httpx` for HTTP if fetching URLs.
- Use `asyncio` from the standard library.

---

## Completion Checklist

- [ ] All three implementations work.
- [ ] Benchmark comparison table printed.
- [ ] `ANALYSIS.md` written.
- [ ] Tests written and passing.
- [ ] Linting passes.
- [ ] Progress updated.

---

## Stretch Goals

- ProcessPoolExecutor for CPU-bound workloads.
- Memory usage tracking with `tracemalloc`.
- Visual chart of benchmark results.

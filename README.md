# Memory Fragmentation

In Operating Systems, **fragmentation** refers to the inefficient use of memory that reduces system performance.  
It is mainly categorized into **Internal Fragmentation** and **External Fragmentation**.

---

## 1. Internal Fragmentation
- **Definition:** Wasted memory *inside* an allocated block because the process does not use the entire block.
- **Cause:** Fixed-size memory allocation (e.g., if block = 4 KB but process only needs 3.2 KB → 0.8 KB wasted).
- **Key Point:** Happens *within* partitions.

### Example:
- Memory block allocated: **100 KB**
- Process size: **92 KB**
- **8 KB wasted** inside the block (unused but reserved).

---

## 2. External Fragmentation
- **Definition:** Wasted memory *outside* allocated blocks, i.e., free memory exists but is scattered in small chunks.
- **Cause:** Variable-sized memory allocation where processes finish and leave holes.
- **Key Point:** Free memory exists but not in one contiguous block.

### Example:
- Free memory: 600 KB (100 KB + 200 KB + 300 KB scattered).
- Process requests: **400 KB**.
- Allocation fails (despite total free memory > 400 KB) because no single block is large enough.

---

## Differences

| Aspect                  | Internal Fragmentation | External Fragmentation |
|--------------------------|-------------------------|-------------------------|
| Location of waste        | Inside allocated block | Between allocated blocks |
| Cause                    | Fixed partition size   | Variable partitions      |
| Wasted memory type       | Reserved but unused    | Free but unusable        |
| Solution                 | Dynamic partitioning, paging | Compaction, paging, segmentation |

---

## Solutions
- **For Internal Fragmentation:**  
  - Use **dynamic partitions** or **paging** to allocate exactly what is required.
- **For External Fragmentation:**  
  - Use **compaction** (rearrange memory to create contiguous space).  
  - Use **paging or segmentation**.

---

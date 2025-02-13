## **Task: Rotating Data Science Library Cheat Sheets with Section Deep Dives**

### **🎯 Objective**

Create an **interactive, structured, and rotating task** that runs **three times a day** at **7:00 AM, 11:00 AM, and 4:00 PM**, iterating indefinitely through **Python libraries for Data Science and Machine Learning**, delivering:

1. A **compact cheat sheet** with one-liner usage examples.
2. A **focused section deep dive** that covers:
   - **Concept explanations**
   - **Mid-level examples with variations**
   - **Best practices, common mistakes, optimizations, errors, and fixes**
   - **Occasional external resources (docs, videos, links)**

The task is **interactive**, confirming understanding before proceeding.

---

## **🔄 Task Rotation Logic (Three Times a Day)**

Each day consists of **three scheduled runs:**

1. **7:00 AM** - **[Library Name] Cheat Sheet**
2. **11:00 AM** - **[Library Name] Section Deep Dive (Part 1)**
3. **4:00 PM** - **[Library Name] Section Deep Dive (Part 2, with optimizations and real-world use cases)**

The cycle follows this strict order, covering all relevant libraries:

- **Day 1:** Pandas (Cheat Sheet) → Pandas (Section 1 Deep Dive Part 1) → Pandas (Section 1 Deep Dive Part 2)
- **Day 2:** NumPy (Cheat Sheet) → NumPy (Section 1 Deep Dive Part 1) → NumPy (Section 1 Deep Dive Part 2)
- **Day 3:** Scikit-Learn (Cheat Sheet) → Scikit-Learn (Section 1 Deep Dive Part 1) → Scikit-Learn (Section 1 Deep Dive Part 2)
- **Day 4:** TensorFlow (Cheat Sheet) → TensorFlow (Section 1 Deep Dive Part 1) → TensorFlow (Section 1 Deep Dive Part 2)
- **Day 5:** Keras (Cheat Sheet) → Keras (Section 1 Deep Dive Part 1) → Keras (Section 1 Deep Dive Part 2)
- **Day 6:** PyTorch (Cheat Sheet) → PyTorch (Section 1 Deep Dive Part 1) → PyTorch (Section 1 Deep Dive Part 2)
- **Loop back to Pandas when all libraries and sections are covered, moving to the next section.**

**🔄 This repeats infinitely**, ensuring gradual, structured learning with three deep learning sessions per day.

---

## **1️⃣ Cheat Sheet Format (Compact, One-Liners)**

- **Bullet-based Markdown format**
- **Python code blocks for clarity**
- **Concise, one-liner examples per command**
- **Official documentation links**
- **Occasional video resources**

### **✅ Example: Pandas Cheat Sheet (7:00 AM Run)**

```
## 📈 Pandas Cheat Sheet  
```

### 📈 Importing & Basics

```python
import pandas as pd
df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})  # Create a DataFrame
df.head()  # View first few rows
```

### 🔍 Selecting Data

```python
df['A']  # Select a single column  
df.loc[0, 'A']  # Select a specific value  
df.iloc[0, 1]  # Select by position  
```

### 🔄 Modifying Data

```python
df['C'] = df['A'] + df['B']  # Create a new column  
df.drop('A', axis=1, inplace=True)  # Remove a column  
```

### 🔗 Merging & Joining

```python
df1.merge(df2, on='key', how='left')  # Merge data  
```

### 📚 Resources

- **Docs:** [Pandas Documentation](https://pandas.pydata.org/docs/)
- **Cheat Sheet:** [Pandas Cheat Sheet](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf)
- **Video (Optional):** [Intro to Pandas](https://youtu.be/xyz)

---

## **2️⃣ Section Deep Dive (11:00 AM & 4:00 PM Runs)**

Each deep dive focuses on **one sub-topic** within the library.

- **11:00 AM Run:** Covers **concepts and basic implementations**
- **4:00 PM Run:** Covers **optimizations, best practices, real-world use cases**

### **✅ Example: Pandas Section Deep Dive (11:00 AM Run)**

```
## 🔎 Deep Dive: Pandas - Selecting Data  
```

### ✅ Why Selecting Data Matters

Selecting data efficiently is crucial for performance, especially in large datasets.

### **1️⃣ Method 1: Selecting a Column**

```python
df['A']  # Returns a Series  
df[['A']]  # Returns a DataFrame  
```

**❌ Common Error:**

```python
df['A', 'B']  # ❌ KeyError - Must use double brackets for multiple columns  
df[['A', 'B']]  # ✅ Correct  
```

### **2️⃣ Method 2: Using `.loc[]` for Label-based Indexing**

```python
df.loc[0, 'A']  # Get specific value  
df.loc[:, ['A', 'B']]  # Get multiple columns for all rows  
```

---

### **✅ Example: Pandas Section Deep Dive (4:00 PM Run - Optimizations & Use Cases)**

### **3️⃣ Method 3: Using `.iloc[]` for Position-based Indexing**

```python
df.iloc[0, 1]  # First row, second column  
df.iloc[:3, :2]  # First 3 rows, first 2 columns  
```

**✅ Best Practice:** Use `.iloc[]` when column labels are unknown or dynamic.

### 🌱 Optimization Tips

- **Avoid loops**: Use **vectorized operations** for speed.
- Instead of `df[df['A'] > 10]`, use `df.query("A > 10")` for better performance.
- Convert categorical data to `pd.Categorical` to **reduce memory usage**.

### 📚 Resources

- **Docs:** [Pandas Data Selection Docs](https://pandas.pydata.org/docs/)
- **Video (Optional):** [Efficient Data Selection in Pandas](https://youtu.be/xyz)

---

## **3️⃣ Additional Features & Enhancements**

- **📂 Best Practices & Optimizations** for efficiency.
- **❌ Common Errors & Fixes** to troubleshoot issues.
- **🎨 Performance Considerations** for large datasets.
- **💡 Use Cases** to apply concepts in real-world scenarios.
- **📽️ YouTube Videos (Sometimes)** for extra learning.
- **📚 Official Documentation Links** for deep dives.


schedule every day, 3 times a day, at 7AM, 11AM, and 4PM, based on the above
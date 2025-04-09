
# 📐 ER Diagram – Reverse Engineering Instructions

We used **MySQL Workbench** to reverse engineer the ER diagram from our existing banking database schema. This process helped us visualize the relationships and structure of the system in a clear, interactive model.

---

## 🛠️ Steps for Reverse Engineering

1. **Open MySQL Workbench**
   - Launch the MySQL Workbench application on your system.

2. **Create a New Model**
   - From the top menu, go to `File > New Model`.

3. **Start Reverse Engineering**
   - Click on `Database > Reverse Engineer`.

<img src="https://github.com/user-attachments/assets/98005b16-e121-453d-ae61-6e5552c09035" width="500" />

---
4. **Connect to a Database**
   - Select or configure a MySQL connection that points to your existing banking database.

<img src="https://github.com/user-attachments/assets/721797cf-fe25-442e-8aba-ca6ed1dd3a1a" width="500" />

<img src="https://github.com/user-attachments/assets/c56f0485-abeb-47b4-8246-79e90b65ec65" width="500" />

---

5. **Select the Schema**
   - Choose the target schema (e.g., `banking_system_db`) that contains your tables.

<img src="https://github.com/user-attachments/assets/9a0429db-7d5a-4d4c-8ecf-fa3fb9ca48e9" width="500" />

---

6. **Fetch and Import the Objects**
   - Select all tables, views, and routines you'd like to include, and click **Execute**.

<img src="https://github.com/user-attachments/assets/1bc741bd-1261-4a59-95a3-c7d26db85c16" width="500" />

---

7. **Diagram Generation**
   - Once imported, go to `Model > Create EER Diagram from Catalog Objects`.

<img src="https://github.com/user-attachments/assets/be4ea207-0447-4fa4-9553-a5ef3eb38f13" width="500" />

---

8. **Adjust Layout (Optional)**
   - Rearrange the table boxes for better visibility, and use formatting tools to tidy the layout.

<img src="https://github.com/user-attachments/assets/4b884f36-2b97-4fff-87e5-61f21a09493b" width="500" />

---

9. **Save or Export**
   - Save the model (`.mwb` file), or export the ER diagram as an image (`.png`, `.pdf`) to include in documentation.

> ✅ **Note**: This approach is especially useful when working with legacy databases or when database-first design is preferred.

---

## 🔄 Forward Engineering

MySQL Workbench also supports **forward engineering**, allowing you to generate SQL scripts and create databases directly from your ER diagram.

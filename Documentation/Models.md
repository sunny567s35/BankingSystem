# 🏦 BankingSystem – Models and Admin Overview

This document provides a breakdown of the Django models and admin configurations in the `app/` folder of our **BankingSystem** project. It outlines the relationships between tables and explains how data is managed in the admin panel.

---

## 📁 app/models.py

Below is an overview of all major models and their relationships:

### 1. **Customer**
- Represents a user with personal details.
- Linked with `User` (Django auth user) via a One-to-One relationship.
- Fields include: `first_name`, `last_name`, `gender`, `dob`, `email`, `occupation`, `income`.

### 2. **Account**
- Each `Customer` can have one or more `Accounts`.
- Related to:
  - `Customer` via `customer_id`
  - `Branch` via `branch_id`
  - `AccountType` via `account_type_id`
- Tracks `account_number`, `created_at`, and `last_transaction_date`.

### 3. **AccountType**
- Defines account types like savings or current.
- Fields: `name`, `min_balance`, `interest_rate`.

### 4. **Branch**
- Details about physical branches of the bank.
- Fields: `branch_name`, `location`.

### 5. **Transaction**
- Records transaction activities (withdrawal, deposit, transfer).
- Fields: `account_id`, `transaction_type`, `amount`, `timestamp`.

### 6. **TransferIn** and **TransferOut**
- Track money transferred between accounts.
- `TransferOut`: `from_account_id`, `to_account_id`, `amount`
- `TransferIn`: `to_account_id`, `from_account_id`, `amount`

### 7. **Deposit** and **Withdraw**
- Linked to a `Transaction` for deposits and withdrawals.
- Used to distinguish and log specific transaction types.

### 8. **Balance**
- Tracks the current balance of an account.
- Fields: `account_id`, `balance_amount`, `updated_at`.

### 9. **DeletedAccount**
- Historical log of deleted accounts for auditing.
- Fields: `original_id`, `customer_name`, `reason`, `deleted_by`, `deletion_date`.

### 10. **EditAccount**
- Logs changes made to account settings.
- Fields: `account_id`, `changes`, `note`, `timestamp`.

### 11. **InterestTable**
- Stores calculated interest values for account types.
- Fields: `account_type_id`, `interest_rate`, `calculated_interest`.

### 12. **Login** and **Logout**
- Track customer login/logout events.
- Useful for auditing sessions and activity monitoring.

### 13. **Ticket**
- Customer support ticketing system.
- Linked to `Customer`, contains issue subject, description, status, resolution.

### 14. **Announcement**
- Admin-created messages shown to users.
- Fields: `title`, `message`, `created_at`, `updated_at`.

---

## 🔗 Model Relationships Summary

| Model         | Relationships                                                                 |
|---------------|-------------------------------------------------------------------------------|
| Customer      | One-to-One with `User`, One-to-Many with `Account`, `Address`, `Login`, `Logout`, `Ticket` |
| Account       | Foreign Key to `Customer`, `Branch`, and `AccountType`                        |
| Transaction   | Foreign Key to `Account`                                                      |
| TransferOut   | Foreign Key to `Account` (from & to)                                          |
| TransferIn    | Foreign Key to `Account` (from & to)                                          |
| Balance       | Foreign Key to `Account`                                                      |
| DeletedAccount| Stores soft-deleted Account data                                              |
| EditAccount   | Foreign Key to `Account`                                                      |
| Login/Logout  | Foreign Key to `Customer`                                                     |
| Ticket        | Foreign Key to `Customer`                                                     |
| InterestTable | Foreign Key to `AccountType`                                                  |
| Deposit/Withdraw | Foreign Key to `Transaction`                                               |

---

## ⚙️ app/admin.py

Django admin configurations register models for UI management. Key highlights:

- **Model Registration**:
  - All major models are registered for admin visibility (`Customer`, `Account`, `Transaction`, etc.).
- **Custom Admin Views**:
  - Models may include `list_display`, `search_fields`, and `readonly_fields` for enhanced admin management.
- **Inline Usage**:
  - Some models (e.g., transactions) can be shown inline within parent models like `Account`.

This setup enables easy management of banking records and audit trails through Django’s built-in admin panel.

---

## ✅ Conclusion

This modeling approach balances normalized structure with audit capability. Each action—from transfers and logins to account edits—is traceable via relational models.

> 📌 Note: All models are compatible with Django ORM for queries, and integrity is maintained through `ForeignKey`, `OneToOneField`, and `CASCADE` behaviors.


# 🛡️ Protection Maker

**Cryptographically Secure Password Generation and Local Vault Management**

Welcome to **Protection Maker**, your friendly digital bodyguard for password generation and local management!

This **cross-platform desktop application**, built with **Python** and **Tkinter**, focuses on delivering **strong, unpredictable passwords** and providing a **secure, local vault** for storing and retrieving them when you need them most.

---

## 🌟 Features at a Glance

Why juggle mental gymnastics or rely on sticky notes? Protection Maker does the heavy lifting:

- **🔐 Cryptographically Secure Generation**  
  Uses Python's `secrets` module to generate truly random and unpredictable passwords.

- **💾 Local Persistence**  
  Stores password details (name, password, creation time) in a local **SQLite** database (`passwords.db`).

- **⚙️ Configurable Complexity**  
  Customize password **length (4–64 characters)** and **character sets** (Uppercase, Lowercase, Digits, Symbols).

- **🎯 Guaranteed Diversity**  
  Ensures selected character types are included in the generated password.

- **🖼️ Intuitive Tkinter GUI**  
  Multi-page interface with custom rounded graphics for a clean and user-friendly experience.

---

## 🛠️ Technologies & Dependencies

| Component       | Purpose                   | Notes                                                                 |
|----------------|---------------------------|-----------------------------------------------------------------------|
| **Python 3+**   | Core language              | Foundation of the app                                                 |
| **Tkinter**     | GUI                        | Interface building                                                    |
| **secrets**     | Cryptographic randomness   | Secure password generation                                            |
| **sqlite3**     | Local data storage         | For the `passwords.db`                                                |
| **Pillow (PIL)**| Image and graphics         | Custom icons, rounded buttons, backgrounds                            |
| **datetime**    | Time tracking              | Records password creation time                                        |
| **sys / os**    | Resource management        | Portable application support                                          |
| *(Optional)* **cairo** | Custom drawing     | Not required; Pillow handles graphics robustly                        |

---

## 🧭 Application Breakdown

The app is divided into **three main screens**:

### 1. 🔹 Welcome Page (`main_frame`)

- **Aesthetic Introduction**  
  Large, rounded title box that introduces the app as your "Protection Maker."

- **Main Call to Action**  
  "Click here to start" button (rounded with active-state feedback).

- **Footer Assurance**  
  Displays privacy statement:  
  _"Chooses passwords only for you and does not violate any privacy."_

- **Vault Access**  
  Icon in the top-right for direct access to the saved passwords vault.

---

### 2. 🔸 Password Generator (`options_frame`)

This is where you define how your password should be generated.

#### A. Length Control
- **Spinbox Input**: Set desired password length.
- **Range**: 4–64 characters (defaults to 12).

#### B. Character Set Selection
- **Checkboxes** for:
  - Uppercase (A–Z)
  - Lowercase (a–z)
  - Digits (0–9)
  - Symbols (!@#...) *(Default: Off for compatibility)*

- **Smart Guarantee**: If selected, each type is **guaranteed to appear** in the final password.

#### C. Output and Actions
- **Start**: Generates password via `generate_password`.
- **Validation**: Warns if no character set is selected.
- **Result Display**: Shows generated password in an entry field.
- **Copy Button**: Copies password to clipboard.
- **Save Button**: Allows naming and saving the password to the database.

---

### 3. 🗄️ Saved Passwords Vault (`passwords_frame`)

View all your stored passwords securely in a scrollable vault.

#### Features:
- **Real-Time Retrieval**: Pulls data from `passwords.db`.
- **Informative Display**:
  - **Name** (e.g., "Gmail")
  - **Password**
  - **Creation Time** (`%I:%M %p %d/%m/%Y`)
- **Scrollable View**: Implemented using `tk.Canvas` and `tk.Scrollbar`.
- **Smooth Scrolling**: Mouse wheel binding across OS.
- **Empty State Message**: _"No saved passwords found"_

---

## 🚀 Getting Started

### 🔧 Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/YourUsername/protection-maker.git
   cd protection-maker
   ```

2. **Install Dependencies**:
   ```bash
   pip install Pillow
   ```

   > ⚠️ Note: Cairo is optional and not necessary. Pillow handles all functional graphics.

3. **Run the App**:
   ```bash
   python "Password maker.py"
   ```

---

## 🔒 A Note on Security and Storage

- **Generation**: Uses `secrets` for cryptographically secure passwords.
- **Storage**: Passwords are saved **locally** in an **unencrypted** SQLite database (`passwords.db`).

> ⚠️ **Treat the database file as sensitive**. This is **not** an enterprise-level password manager.

**Disclaimer**:  
Protection Maker excels at **secure generation** but does **not encrypt stored data**. Use professional tools for syncing, device-wide access, or advanced encryption.

---

## 👋 Contributing

We welcome community contributions! To get started:

1. **Fork the repository**
2. Create a feature branch:
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit your changes**:
   ```bash
   git commit -m "Add AmazingFeature"
   ```
4. **Push and open a PR**:
   ```bash
   git push origin feature/AmazingFeature
   ```

---

> 💡 Happy coding, and may your passwords be ever-long and full of entropy!

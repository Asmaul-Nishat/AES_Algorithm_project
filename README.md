## 📌 Problem Statement

**The Blog Publishing and Management System (BPMS)** is designed to provide an **easy-to-use** and **efficient platform** for bloggers, readers, and administrators.  
It enables **content creation**, **management**, and **interaction** through a user-friendly interface while maintaining **secure data handling**.

## 🎯 Objectives

- **Simplify blog creation** for non-technical users  
- Ensure **organized content management** with categories and tags  
- Provide **engagement features** like comments, likes, and sharing  
- Enable **administrators** to monitor content quality and user activity  
- Maintain **data security** and **system reliability**

## 🏗️ System Scope

The BPMS includes the following core modules:

- **User Management** – Registration, login, and profile updates  
- **Post Management** – Create, edit, delete, and search blog posts  
- **Category Management** – Classify and filter blog content  
- **Comment System** – Reader and blogger interactions  
- **Admin Panel** – Manage posts, users, and system settings  
- **Analytics Dashboard** – Track post performance and user engagement  

## 🔍 Key Features

- **Responsive UI** (HTML, CSS, JavaScript)  
- **Backend** using PHP and MySQL  
- **Secure Authentication** with role-based access  
- **Search & Filter** functionality for better content discovery  
- **Like & Share** options to boost audience reach  

---

## 💻 Sample Code Snippet

```php
<?php
// Database connection
$conn = new mysqli("localhost", "root", "", "bpms");

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Insert a new post
$title = "My First Blog Post";
$content = "Welcome to my blog!";
$sql = "INSERT INTO posts (title, content) VALUES ('$title', '$content')";

if ($conn->query($sql) === TRUE) {
    echo "New post created successfully!";
} else {
    echo "Error: " . $sql . "<br>" . $conn->error;
}

$conn->close();
?>

# Clone the repository
git clone https://github.com/yourusername/yourrepo.git

# Navigate into the project directory
cd yourrepo

# Run the script
python aes_project.py
📊 Example Output
sql
Copy
Edit
+---------+----------------------+----------------------+----------------------+-------------------+-------+--------------+
| Test No.| Original String      | Encrypted String     | Decrypted String     | Decryption Success| Score | Running Time |
+---------+----------------------+----------------------+----------------------+-------------------+-------+--------------+
|    1    | Hello, World!        | 2...                 | Hello, World!        | True              | 12.45 | 0.00015      |
...
Average score: 10.82
📦 Example: AES with PyCryptodome
python
Copy
Edit
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# Generate a 16-byte key (128-bit)
key = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_EAX)

data = b"Confidential Message"
ciphertext, tag = cipher.encrypt_and_digest(data)

print("Encrypted:", ciphertext)

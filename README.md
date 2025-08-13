🔐 AES Algorithm – Python Encryption Project
📌 Overview
The Advanced Encryption Standard (AES) is a symmetric encryption algorithm standardized by NIST in 2001.
It is widely used to protect sensitive data due to its high security and efficiency.

Works on fixed-size blocks of 128 bits

Supports key sizes of 128, 192, or 256 bits

This project demonstrates encryption and decryption concepts inspired by AES, implemented in Python.
It also includes a scoring system to evaluate the strength of encryption based on statistical and cryptographic metrics.

⚠️ Note: This is a custom encryption demonstration and not a direct AES implementation.
For production, use libraries like PyCryptodome.

⚙️ How AES Works (Simplified)
1. Key Expansion
The main key is expanded into round keys.

2. Initial Round
The plaintext is XORed with the initial key.

3. Rounds (10 / 12 / 14 depending on key size)
SubBytes – Byte substitution using an S-box

ShiftRows – Shifting rows to increase diffusion

MixColumns – Mixing data within columns

AddRoundKey – XOR with the round key

4. Final Round
Same as above, without MixColumns.

🛠 Features
Custom Encryption Algorithm (AES-inspired)

Decryption Support

Encryption Strength Scoring based on:

Unique character diversity

Sequence variation

Entropy (randomness)

Frequency analysis resistance

Avalanche effect (change propagation)

Reversibility check

Pattern removal efficiency

Execution time efficiency

PrettyTable Output for results display

📂 Project Structure
1️⃣ Cipher Class – Handles Encryption & Decryption
__init__(original_string) – Stores the string

encrypt() – Reverses string, applies ASCII shifts, inserts random characters

decrypt() – Removes inserted characters, reverses ASCII shifts, restores original

2️⃣ Scoring Class – Evaluates Encryption Strength
Calculates entropy, frequency variation, encryption consistency

calculate_score() – Aggregates weighted scores

generate_summary() – Returns metric breakdown

print_results() – Displays results in a table

▶️ Running the Project
bash
Copy
Edit
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

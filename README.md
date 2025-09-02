# English Vocabulary Helper
**`eng`** is a minimal CLI dictionary for memorising English words together with their translations and example contexts.

![1.png](./pictures/1.png)
## 🚀 Installation & Launch
To set up the application, run the `setup.sh` script:
```bash
./setup.sh
```
This script will:
1. Install necessary Python dependencies (`colorama`).
2. Ensure the database directory exists.
3. Initialize the SQLite database (`database/localdb.sqlite`) if it doesn't already exist.

After running the script, you will be prompted to add an alias to your shell configuration (e.g., `~/.bashrc` or `~/.zshrc`) to easily run the `eng` command.

## 📖 Quick Start
```bash
# Add a word without context
eng -n apple яблоко

# Add a word with context
eng -n apple яблоко An apple a day keeps the doctor away.

# List all words
eng -l

# Training: translate a random word
eng -t

# Search with tab-completion
eng -f
> Enter word:
apple - яблоко [An apple a day keeps the doctor away.]

# Delete
eng -d apple
```

![2.png](./pictures/2.png)

## 🎨 Colour Legend
| Output       | Colour      | Purpose                 |
| :----------- | :---------- | :---------------------- |
| English word | **cyan**    | easy visual scanning    |
| Translation  | **yellow**  | quick reading           |
| Context      | **magenta** | visible but unobtrusive |

## 📂 Database Structure
Vocabulary is stored in a SQLite database at `database/localdb.sqlite`. The database contains a table `vocabulary` with the following columns:
- `english` (TEXT, PRIMARY KEY): The English word.
- `otherlg` (TEXT): The translation in another language (e.g., Russian).
- `context` (TEXT): Optional context or example sentence for the word.

## 🛠 Commands
| Flag       | Example                                    | Description                            |
| :--------- | :----------------------------------------- | :------------------------------------- |
| `-n`       | `eng -n run бежать He runs every morning.` | add a word (and optional context)      |
| `-d`       | `eng -d run`                               | delete a word                          |
| `-e`       | `eng -e run бегать`                        | edit entry: word, [new translation], [new context] |
| `-s`       | `eng -s app`                               | show words starting with `app`         |
| `-t`       | `eng -t`                                   | training: translate a random word      |
| `-l`       | `eng -l`                                   | list the entire dictionary             |

## How does training work:

![4.png](./pictures/4.png)

## ❗ Word Already Exists
```
Doctor's recommendation: Get checked for dementia.
```
![3.png](./pictures/3.png)

## 🤝 Dependencies
`pip install colorama`
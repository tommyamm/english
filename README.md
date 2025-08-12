# English Vocabulary Helper
**`eng`** is a minimal CLI dictionary for memorising English words together with their translations and example contexts.

![1.png](./pictures/1.png)

## 🚀 Installation & Launch
```bash
# Clone or copy the repo
git clone https://github.com/yourname/english ~/projects/python/english

# Add an alias to ~/.bashrc or ~/.zshrc
echo 'alias eng="python3 $HOME/projects/python/english/main.py"' >> ~/.bashrc
source ~/.bashrc
```

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
> Enter word: app<Tab>
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

## 📂 Dictionary File Format
The file `english.md` is plain-text:
```
apple   - яблоко [An apple a day keeps the doctor away.]
banana  - банан
cat     - кот [The cat sat on the mat.]
```
Words are automatically grouped by first letter and aligned when the file is formatted.

## 🛠 Commands
| Flag       | Example                                    | Description                            |
| :--------- | :----------------------------------------- | :------------------------------------- |
| `-n`       | `eng -n run бежать He runs every morning.` | add a word (and optional context)      |
| `-d`       | `eng -d run`                               | delete a word                          |
| `-s`       | `eng -s app`                               | show words starting with `app`         |
| `-t`       | `eng -t`                                   | training: translate a random word      |
| `-l`       | `eng -l`                                   | list the entire dictionary             |
| `-f`       | `eng -f`                                   | interactive search with tab-completion |
| `-o`       | `eng -o`                                   | open the dictionary in `less`          |
| `--format` | `eng --format`                             | re-format the file (sort & align)      |


## ❗ Word Already Exists
```
Hey, dumb Down, there's already a word like that:
```
![3.png](./pictures/3.png)

## 🤝 Dependencies
`pip install colorama`

`pip install argparse`
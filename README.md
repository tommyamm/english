# English Vocabulary Helper

**`eng`** — минималистичный CLI-словарь для запоминания английских слов с контекстом и тренировкой.

![1.png](./pictures/1.png)

---

## 🚀 Установка и запуск
```bash
# Склонируйте или скопируйте себе
git clone https://github.com/yourname/english ~/projects/python/english
# Добавьте алиас в ~/.bashrc или ~/.zshrc
echo 'alias eng="python3 $HOME/projects/python/english/main.py"' >> ~/.bashrc
source ~/.bashrc
```

---

## 📖 Быстрый старт
```bash
# Добавить слово без контекста
eng -n apple яблоко

# Добавить слово с контекстом
eng -n apple яблоко An apple a day keeps the doctor away.

# Посмотреть все слова
eng -l

# Тренировка: перевод случайного слова
eng -t

# Найти слово с автодополнением по Tab
eng -f
> Введите слово: app<tab>
apple - яблоко [An apple a day keeps the doctor away.]

# Удалить
eng -d apple
```

![2.png](./pictures/2.png)

---

## 🎨 Цветовая кодировка

| Что выводится    | Цвет        | Назначение           |
| :--------------- | :---------- | :------------------- |
| английское слово | **cyan**    | легко искать глазами |
| перевод          | **yellow**  | быстро читается      |
| контекст         | **magenta** | не мешает, но виден  |

---
## 📂 Формат файла словаря

Файл `english.md` хранится в plain-text:
```
apple   - яблоко [An apple a day keeps the doctor away.]
banana  - банан
cat     - кот [The cat sat on the mat.]
```

Слова автоматически группируются по первой букве и выравниваются при форматировании.

---

## 🛠 Команды

| Ключ       | Пример                                     | Описание                                          |
| :--------- | :----------------------------------------- | :------------------------------------------------ |
| `-n`       | `eng -n run бежать He runs every morning.` | добавить слово и (опц.) контекст                  |
| `-d`       | `eng -d run`                               | удалить слово                                     |
| `-s`       | `eng -s app`                               | показать слова, начинающиеся на `app`             |
| `-t`       | `eng -t`                                   | тренировка: перевод случайного слова              |
| `-l`       | `eng -l`                                   | вывести весь словарь                              |
| `-f`       | `eng -f`                                   | интерактивный поиск с автодополнением             |
| `-o`       | `eng -o`                                   | просмотр словаря через `less`                     |
| `--format` | `eng --format`                             | переформатировать файл (сортировка, выравнивание) |

---

## ❗ Если слово уже есть
```
$ eng -n apple фрукт
Слыш, тупой Даун, такое слово уже есть:
apple - яблоко [An apple a day keeps the doctor away.]
```
![3.png](./pictures/3.png)

---
## 🤝 Зависимости
`pip install colorama`

`pip install argparse`
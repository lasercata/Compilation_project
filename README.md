# 🚀 Compilation Project

A simple tool to **analyze**, **compile**, and **run** NNP programs.

---

## 📁 Project Structure

```
.
├── main.py
├── README.md
│
├── Subject/
│   └── Sujet_Projet_Compilation2024.pdf
│
├── Report/
│   ├── Compilation_project_report.tex
│   ├── data/
│   ├── pics/
│   └── style/
│
├── src/
│   ├── analex.py
│   ├── anasyn.py
│   ├── compiler.py
│   ├── idtable.py
│   ├── interpretor.py
│   ├── parser_ui.py
│   └── utils.py
│
└── nn_programs/
    ├── nna/
    │   ├── correct1.nno
    │   ├── ...
    │   ├── correct4.nno
    │   ├── error1.nno
    │   ├── ...
    │   ├── error7.nno
    │   │
    │   └── expected/
    │       ├── correct1.nno.expected
    │       ├── ...
    │       └── correct4.nno.expected
    │
    └── nnp/
        ├── correct1.nno
        ├── ...
        ├── correct5.nno
        │
        └── expected/
            ├── correct1.nno.expected
            ├── ...
            └── correct4.nno.expected
```

---

## 🛠️ Usage

### 🔧 Setup

Clone the repository:

```bash
git clone --depth=1 https://github.com/lasercata/Compilation_project.git
cd Compilation_project
```

Make the main file executable:

```bash
chmod u+x main.py
```

---

### ▶️ Run

To display help information:

```bash
./main.py -h
```

Help output:

```
usage: main.py [-h] [-v] {analyse,a,compile,c,run,r} ...

Analyse, compile, and run NNP programs

positional arguments:
  {analyse,a,compile,c,run,r}
    analyse (a)         runs the lexical analysis of the NNP program
    compile (c)         compile a NNP program to NNP object code
    run (r)             runs a NNP object code

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
```

---

### 🧪 Examples

```bash
./main.py c -h
./main.py c nn_programs/nna/correct1.nno -o correct1.obj
./main.py r correct1.obj
./main.py r nn_programs/nna/correct1.nno -c
```

---

### Run tests
To run all the tests:
```
python -m pytest
```

To have the details:
```
python -m pytest -vv
```

---

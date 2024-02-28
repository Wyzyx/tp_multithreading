# TP-multithreading

## Objectif du tp :

Le but de ce tp est de comparer les performances de threads en python et en C++.

## Partie Python

1. Lancer le Queue Manager:

```bash
python3 src/queueManager.py
```

2. Dans un nouveau terminal, lancer le  Minion:
```bash
python3 src/minion.py
```

3. Dans un dernier terminal, lancer le Boss:
```bash
python3 src/boss.py
```

## Partie C++

1. Configuration du build :
    
```bash
cmake -B build -S .
```

2. Compilation du projet :

```bash
cmake --build build
```

3. Lancer le proxy python :

```bash
python3 src/proxy.py
```

4. Lancer le client C++ :

```bash
./build/low_level
```



## radare2 documentation generator
***
Python script to extract all the [r2](https://www.radare2.org/n/radare2/html) commands documentation through r2pipe. The script generates a very basic web site. Launch [r2_help.html](https://github.com/mdevillers/r2-docgen/html/r2_help.html) to view the documentation.

### requirements
```pip3 install r2pipe``` (global installation)

or using virtualenv

```python3 -m venv .```

```source venv/bin/activate```

```pip3 install r2pipe```

### execution

```python3 r2-docgen.py```

### TODO

* add hyperlinks on the pages
* create pdf
* add search

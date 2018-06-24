# lilycode

Free javascript obfuscator to help make your websites, web apps and more javascript code more secure and resistant to piracy.

### Features
1. Variables renaming
2. Functions renaming
3. Whitespace/Comments removal
4. Obfuscates strings and numbers

### Limitations
1. So far only tested on "pure" javascript - not tested on javascript frameworks like JQuery, etc...
2. Will only work on javascript files that don't have external dependencies - If your html code references a javascript function/variable, you may get errors.
3. Internal Regex handling not implemented currently.

### Usage
The lilycoder.py file accepts three command-line arguments:

```
-i  --input location of input javascript file
[-o]  --output  location of output javascript file
[-html] --output_html location of output html/javascript file
```
Of these, only the input file is a required argument. By default the output file name will be the same as ``--input`` but suffixed with ``(2).js``. The HTML file option encapsulates the resulting code in a simple HTML document for easy testing of the results.

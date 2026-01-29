### ROLE
You are a senior Python engineer with deep knowledge of Python.

### GOAL
Generate a fully functional Python project with clean architecture and directory structure.

### CONTEXT
- Using Python and suitable web automation/scraping library

### INPUTS
- a web url like https://openclipart.org/detail/4560/dark-plastic-edge-gradient

### REQUIREMENTS
Functional:
1. the input url lands to a HTML which has a title
2. the HTML has an author which can be located after the title preceded by the word 'by'
3. the HTML has a link named "Download SVG"
4. the HTML has a link named "Small" just right to the texts "PNG (Bitmap)"
5. the HTML has a link named "Medium" just right to the link "Small"
6. the HTML has a link named "Large" just right to the link "Medium"

Non-functional:
- CLI argument support
- JSON output support
- async call support
- resilient to HTML structure changes
- support for bulk scraping

### OUTPUT
- the title in the HTML
- the author in the HTML
- the svg url linked with "Download SVG" link
- the image url linked with "Small" link
- the image url linked with "Medium" link
- the image url linked with "Large" link
- a base-file-name combining author and title so that it looks like author-title. Note that spaces in author and title must be replaced by a dash (-). No space in base file name
- the svg to be downloaded with the name base-file-name.svg
- the small to be downloaded with the name base-file-name__small.png
- the medium to be downloaded with the name base-file-name__medium.png
- the large to be downloaded with the name base-file-name__large.png

### ENVIRONMENT
- Python 3.10

### DELIVERY
- Code with reasonable explanation
- Support for specifying configuration in a yaml file
- Support for a list of urls in the configuration yaml in addition to passing url in CLI
- all downloads must go to a directory specified in the configuration yaml file
- a .sh (bash) script and a .bat (Windows command line) script to run the python code with support for passing the arguments necessary for the Python script
- all source must go under a src directory
- all configuration must go to a conf directory


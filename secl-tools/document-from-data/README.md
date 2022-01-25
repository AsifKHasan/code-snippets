# gsheet-to-odt

## Linux usage:
```
BASE_DIR="/home/asif/projects/asif@github/code-snippets/secl-tools/document-from-data"
cd ${DOCULABORATION_BASE}/bin
```

## Windows usage:
```
set BASE_DIR="D:\projects\asif@github\code-snippets\secl-tools\document-from-data"
cd %BASE_DIR%\bin

set sequence="001"
set name="Asif Hasan"

set INPUT_FILE="..\template\salary-enhancement\HR__salary-enhancement-template__2022.odt"
set OUTPUT_FILE="..\out\salary-enhancement\HR__salary-enhancement__2022__%sequence%.odt"
python ooo_fieldreplace -i %INPUT_FILE% -o %OUTPUT_FILE% sequence=%sequence% name=%name%
```

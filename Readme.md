# Installation 

### install flask 
```
pip install flask
```
### install Flask-WeasyPrint
[Befor Installing do this on windows](https://gist.github.com/doobeh/3188318)
```
pip install Flask-WeasyPrint
```
### run project
##### Windows
```
set FLASK_APP=app.py
flask run 
```
##### Linux
```
export FLASK_APP=app.py
flask run
```

### Activate debug mode
##### Windows
```
set FLASK_DEBUG=1
```
##### Linux
```
export FLASK_DEBUG=1
```
# usage 

Navigate to desired inspection report using breadcrumbs and list outputs 
and after reaching the location add `.pdf` at the end of the url to genarate your pdf
# preferd db Structure 
```
rooms> room > date> inspection scan in time > inspection details 

where
inspection details >
    -scan in 
    -scan out
    -name of inspector 
    -checklist 

where
checklist > checklist_item > 
    -value 
    -remark) 
```
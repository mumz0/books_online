(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).content | py -

poetry update 
poetry run python ./main.py
Start-Sleep -Seconds 2
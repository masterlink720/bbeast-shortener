#!/usr/bin/env bash

if ! which pip &> /dev/null; then
    echo '[ERROR] pip command missing, setup python + pip and try again'
    exit 1
fi

key=''

[[ -f ./.key ]] && key=$(cat ./.key)

pip_result=$(pip install -r ./requirements.txt)
if [[ $? -ne 0 ]]; then
    echo -e "[PIP ERROR]: ${pip_result}"
    exit 1
fi

cp ./bbeast.py /usr/local/bin/bbeast

if [[ -z ${key} ]]; then
    echo -e "\t - note, set an api key in .key and run this command again to avoid needing to set the --key flag\n"
else
    sed -ir "s/API_KEY = .*/API_KEY = '${key}'/" /usr/local/bin/bbeast
fi

echo -e "Installed to /usr/local/bin/bbeast"

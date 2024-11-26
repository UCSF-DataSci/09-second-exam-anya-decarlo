#!/bin/bash 

# Make output file for cleaned data
touch ms_data.csv


# Clean raw data and save to ms_data.csv
grep -v '^#' ms_data_dirty.csv | \
sed '/^[[:space:]]*$/d' | \
sed -e 's/,\+/,/g' | \
sed -e 's/^,//g' -e 's/,$//g'
head -n 1
#!/bin/bash 

# Make output file for cleaned data
touch ms_data.csv

# Debug: Print the header line 
echo "Header line:"
sed -n '5p' ms_data.dirty.csv

# Get columns 
echo "Identifying columns.."
COLUMNS=$(sed -n '5p' ms_data_dirty.csv | \
tr ',' '\n' | \
 awk '/^(patient_id|visit_date|age|education_level|walking_speed)$/{print NR}'| \
    paste -sd,)

# Debug: Print the columns found 
echo "Selected columns: $COLUMNS" 
if [-z "$COLUMNS" ]; then 
    echo "Error: Failed to identify required columns"
    exit 1
fi

# Clean raw data and save to ms_data.csv
grep -v '^#' ms_data_dirty.csv | \		
sed '/^[[:space:]]*$/d' | \
sed -e 's/,\+/,/g' | \
sed -e 's/^,//g' -e 's/,$//g' |
sed '1, 5d' | \
cut -d ',' -f"$COLUMNS" |\
awk -F ',' '$5 >= 2.0 && $5 <= 8.0' > ms_data.csv


# Create insurance.lst file 
echo -e "insurance_type\nBronze\nSilver\nGold\bPlatinum" > insurance.lst

# Generate summary of processed data 
echo "Total number of visits: $(($(wc -l < ms_data.csv) -1))"
echo "First few records: 
head -n 5 ms_data.csv 
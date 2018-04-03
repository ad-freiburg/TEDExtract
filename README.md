# TEDExtract

A small test crawler for TED talks. 

## Requirements

As stated within the requirements.txt:

 - pandas
 - bs4

## Usage

```
python3 ./main.py --output=/output/dir --max_pages=76
```

Through this all transcripts of all talks will be saved within the `output` directory with the format:
```$output/<TALK_NAME>.csv```

There is an additional script `combine_csvs.py` which is responsible for creating a single csv file and csv files for each language.

```
python3 ./combine_csvs.py --input_dir=/output/dir --outname=/final/output/dir/name
```

All files will then be saved to the directory `/final/output/dir` with the name `final*`. There will be one file containing all
talks `final.csv` and one file for each language `final.en.csv`, `final.de.vsc`, etc.
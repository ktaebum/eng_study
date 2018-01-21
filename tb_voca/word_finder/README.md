# Word Finder

##### Crawling word's english meaning, korean meaning, example

`Version = 1.1`

## How to use

1. Make target word list file in 'find_targets' folder in csv extension  
    - CSV file should follow sample.csv format in 'find_targets' folder 
    
2. Run finder_main.py

3. Result file should be created in 'find_results' folder
    - Result file name is '${original_filename}_result.csv'

## Behavior
##### Find contents that find_target.csv does not contains

e.g)  

    1. target csv only contains word: Find all (Eng_mean, Kor_mean, Example)  
    2. target csv contains word, Eng_mean, Kor_mean: Find just Example
    and so on ...


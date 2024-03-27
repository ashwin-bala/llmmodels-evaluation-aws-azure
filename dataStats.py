import json
import jsonlines
import pandas as pd
import sys
def read_jsonl_file(jsonl_file):
    data = []
    with jsonlines.open(jsonl_file, 'r') as file:
        for line in file:
            data.append(line)
            #print(line)
    return data

def read_jsonl_file(jsonl_file):
    data = []
    with jsonlines.open(jsonl_file, 'r') as file:
        for line in file:
            score = line['automatedEvaluationResult']['scores'][0]
            metric_name = score['metricName']
            result = score['result']
            data.append({'metricName': metric_name, 'result': result})
    return data


def convert_json_to_dataframe(file,type):
    data = read_jsonl_file(file)
    
    df = pd.DataFrame(data)
    
    # Calculate average
    average = df['result'].mean()

    # Calculate 90th percentile
    percentile_90 = df['result'].quantile(0.9)
    percentile_95 = df['result'].quantile(0.95)
    percentile_99 = df['result'].quantile(0.99)  
    
    print("Metric:",df['metricName'][0])
    print("--------------------------------------")    
    print("Average Score:",average)
    print("90th Percentile",percentile_90)
    print("95th Percentile",percentile_95)
    print("99th Percentile",percentile_99)

    print("\n")
    return df

arguments = sys.argv

type = arguments[1]
filePath = arguments[2]

print("\n\nModel: ",type)      
print("\n")    

df = convert_json_to_dataframe(filePath+"accuracy.jsonl",type)

df = convert_json_to_dataframe(filePath+"robustness.jsonl",type)

df = convert_json_to_dataframe(filePath+"toxicity.jsonl",type)

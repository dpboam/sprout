import pandas as pd
from pendulum import period
import yaml
import sys
import os

def first(data,column):
    return list(data[column])[0]

def last(data,column):
    return list(data[column])[-1]

def difference(data,column):
    return last(data,column) - first(data,column)

def col_max(data,column):
    return max(data[column])

def col_min(data,column):
    return min(data[column])

def col_range(data,column):
    return col_max(data,column) - col_min(data,column)

def total(data,column):
    return sum(data[column])

def count(data,column):
    return len(data[column])

def average(data,column):
    return (sum(data[column]) / len(data[column]))

def average_int(data,column):
    return (int)(sum(data[column]) / len(data[column]))


stats = {
    "first" : first,
    "last" : last,
    "difference" : difference,
    "max" : col_max,
    "min" : col_min,
    "range" : col_range,
    "count" : count,
    "total" : total,
    "average" : average_int
}

def get_metric(data,metric_labels):
    column,stat = metric_labels.rsplit("-",1)
    return stats[stat](data,column)

def get_metrics(data,metric_labels):
    return {m : get_metric(data,m) for m in metric_labels}

def format(metrics):
    return {"metrics" : {m : metrics[m] for m in metrics}}

def add_top_level_meta(tl_meta,summary,label="data-file"):
    tl = tl_meta | { "data-file" : summary}
    tl[label] = tl.pop("data-file")
    return tl

def get_summary_file(config):
    data = pd.read_csv(config["path"])
    metrics = get_metrics(data,config["metrics"])
    return metrics #format(metrics)


def get_summary_dir(config,file_key):
    summary = {}
    for file in os.listdir(config["path"]):
        summary[file_key+"-"+file.replace(".csv","")] = get_summary_file(config | {"path" : config["path"] + file})
 
    return summary

def get_summary_file_group_by_date(config,file_key):
    summary = {}
    data = pd.read_csv(config["path"])
    column,period = config["group-by-date"].split("-")
    data[column] = pd.to_datetime(data[column],format="%Y-%m-%d")
    data["period"] = data[column].dt.to_period(period)
    for p in data["period"].unique():
        filtered_data = data[data[column].dt.to_period(period)]
        metrics = get_metrics(filtered_data,config["metrics"])
        summary(file_key)
    return metrics #format(metrics)

def get_summarys(input):
    summary = {}
    for file_key in input["data-file"].keys():
        config = input["data-file"][file_key]
        if os.path.isfile(config["path"]):
            if "group-by-date" in config.keys():
                summary[file_key] = get_summary_file_group_by_date(config)
            else:
                summary[file_key] =  get_summary_file(config)
        else:
            summary = summary | get_summary_dir(config,file_key)

    return add_top_level_meta(input,summary,input["data-files-label"])


def write_yaml(path,data):
    with open(path, 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False, sort_keys=False)

def read_yaml(path):
    with open(path, 'r') as infile:
        return yaml.safe_load(infile)

def summary_yaml(input_path,output_path):
    write_yaml(output_path,get_summarys(read_yaml(input_path)))

if(__name__ == "__main__"):
    yaml_path_in = sys.argv[1]  #"yaml\\input.yml"
    yaml_path_out = sys.argv[2] #"yaml\\sprout_summary.yml"
    summary_yaml(yaml_path_in,yaml_path_out)
    
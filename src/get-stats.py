from importlib.metadata import files
import pandas as pd
import yaml
import sys

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
    "total" : total,
    "average" : average_int
}

def get_metric(data,metric_labels):
    column,stat = metric_labels.rsplit("-",1)
    return stats[stat](data,column)

def get_metrics(data,metric_labels):
    return {m : get_metric(data,m) for m in metric_labels}

def format(meta,metrics):
    return meta | {"metrics" : {m : {"current" : metrics[m]} for m in metrics}}

def add_top_level_meta(tl_meta,summary,label="data-file"):
    tl = tl_meta | { "data-file" : summary}
    tl[label] = tl.pop("data-file")
    return tl

def add_data_level_meta(dl,summary):
    dl.pop("meta")
    dl.pop("metrics")
    dl.pop("path")
    return dl | summary

def get_summary(input):
    summary = {}
    for file_key in input["data-file"].keys():
        config = input["data-file"][file_key]
        data = pd.read_csv(config["path"])
        meta = get_metrics(data,config["meta"])
        metrics = get_metrics(data,config["metrics"])
        summary[file_key] =  add_data_level_meta(config,format(meta,metrics))
    return add_top_level_meta(input,summary,input["data-files-label"])

def write_yaml(path,data):
    with open(path, 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False, sort_keys=False)

def read_yaml(path):
    with open(path, 'r') as infile:
        return yaml.safe_load(infile)

def summary_yaml(input_path,output_path):
    write_yaml(output_path,get_summary(read_yaml(input_path)))

if(__name__ == "__main__"):
    yaml_path_in = sys.argv[1]  #"yaml\\input.yml"
    yaml_path_out = sys.argv[2] #"yaml\\sprout_summary.yml"
    summary_yaml(yaml_path_in,yaml_path_out)
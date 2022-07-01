import yaml

class Metric:
    def __init__(self,name,current):
        self.name = name
        self.current = current

class Service:
    def __init__(self,name,metrics):
        self.name = name
        self.metrics = metrics

    def addMetrics(self,metrics):
        self.metrics.extend(metrics)

    def getInfo(self):
        return {"metric" : {m.name : {"current" : m.current} for m in self.metrics}}

def summaryInfo(services):
    return {"title" : "Sprout summary statistics" , "service" : {s.name : s.getInfo() for s in services}}


def writeSummaryInfo(path,services):
    with open(path, 'w') as outfile:
        yaml.dump(summaryInfo(services), outfile, default_flow_style=False, sort_keys=False)

services = [Service("twitter",[Metric("followers",15000),Metric("monthly-engagment",100000)]),
            Service("instagram",[Metric("followers",374848),Metric("monthly-engagment",6758)])]

writeSummaryInfo("yaml\\sprout_summary_test.yml",services)



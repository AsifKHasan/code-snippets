import numpy as np
import pandas as pd
from plotnine import *

data_path = "/home/asif/projects/asif@github/code-snippets/helpers/R/agent-banking-data.csv"
data_path = "D:/projects/asif@github/code-snippets/helpers/R/agent-banking-data.csv"

image_dir = "C:/Users/Asif/Downloads"

last_q = '2023-Q2'


theme_set(theme_538())

all_data = pd.read_csv(data_path, sep='\t', thousands=',')

# the latest data is the last quarter data
latest_data = all_data[all_data['quarter'] == last_q] 

# Rural/Urban outlet ratio
data = latest_data[['code', 'outlets-urban', 'outlets-rural']]
data["outlets-ratio"] = data['outlets-rural'] / data['outlets-urban']

# the axes
x = 'code'
y = 'outlets-ratio'

top_values_to_select = 10
bottom_values_to_select = len(data) - top_values_to_select

# top banks
p1 = (ggplot(data.nlargest(top_values_to_select, 'outlets-ratio'), aes(x=x, y=y)) + geom_point() + geom_segment(aes(x=x, xend=x, y=0, yend=y)))
p1 = p1 + theme(axis_text_x=element_text(family="Arial", weight="light", style="normal", size=7, color="black", angle=45, hjust=1)) + xlab("Banks") + ylab("Rural/Urban outlet ratio")

p1_path = f"{image_dir}/outlets-ratio__cumulative__top-{top_values_to_select}-banks.png"
p1.save(filename=p1_path)

# bottom banks
p2 = (ggplot(data.nsmallest(bottom_values_to_select, 'outlets-ratio'), aes(x=x, y=y)) + geom_point() + geom_segment(aes(x=x, xend=x, y=0, yend=y)))
p2 = p2 + theme(axis_text_x=element_text(family="Arial", weight="light", style="normal", size=7, color="black", angle=45, hjust=1)) + xlab("Banks") + ylab("Rural/Urban outlet ratio")

p2_path = f"{image_dir}/outlets-ratio__cumulative__bottom-{bottom_values_to_select}-banks.png"
p2.save(filename=p2_path)
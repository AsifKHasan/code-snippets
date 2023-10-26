import numpy as np
import pandas as pd
from plotnine import *

# theme_set(theme_538())
# theme_set(theme_dark())
# theme_set(theme_bw())
# theme_set(theme_classic())
# theme_set(theme_dark())
# theme_set(theme_gray())
# theme_set(theme_light())
# theme_set(theme_linedraw())
# theme_set(theme_matplotlib())
# theme_set(theme_minimal())
# theme_set(theme_seaborn())
# theme_set(theme_tufte())
# theme_set(theme_void())
# theme_set(theme_xkcd())

theme_set(theme_538())

data = pd.read_csv("/home/asif/projects/asif@github/code-snippets/helpers/R/agent-banking-data.csv", sep='\t')

# Rural/Urban outlet ratio
x = 'code'
y = 'outlets-ratio'
p1 = (ggplot(data, aes(x=x, y=y)) + geom_point() + geom_segment(aes(x=x, xend=x, y=0, yend=y)))
p1 = p1 + theme(axis_text_x=element_text(family="Arial", weight="light", style="normal", size=7, color="black", angle=45, hjust=1)) + xlab("Banks") + ylab("Rural/Urban outlet ratio")

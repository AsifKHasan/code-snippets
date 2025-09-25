# import libraries
library(dplyr)

# read csv
csv_name = '_3v9dP0klkg'
csv_path_template = "/home/asifhasan/projects/asif@github.com/code-snippets/codes/python/audio/out/pitch_data__%s.csv"
df <- read.csv(sprintf(csv_path_template, csv_name), header = TRUE)

# load necessary packages
library(tidyverse)

# time range in seconds
START_S <- 13.0
END_S <- 17.0
# subticks every 20 ms
INTERVAL_S <- 0.02 

# filter the data frame (df_long)
df_filtered <- df_long %>%
  # filter by the desired time range
  filter(seconds >= START_S & seconds <= END_S) %>%
  # filter by the desired MFCC coefficients
  filter(Coefficient %in% SELECTED_COEFFICIENTS)

# sequence of all minor break points (every INTERVAL_S)
minor_breaks_seq <- seq(from = START_S, to = END_S, by = INTERVAL_S)

# ggplot Line Plot using the new 'seconds' column and subticks
ggplot(df_filtered, aes(x = seconds, y = Value, color = Coefficient)) +
  
  # vertical lines for the minor breaks (optional, but very helpful visually)
  geom_vline(xintercept = minor_breaks_seq, color = "gray85", linewidth = 0.2, linetype = "dotted") +
  
  geom_line(alpha = 0.8, linewidth = 0.4) +
  
  labs(
    title = paste0("Selected MFCC Coefficients (", START_S, "s - ", END_S, "s)"),
    subtitle = paste("Coefficients:", paste(SELECTED_COEFFICIENTS, collapse = ", ")),
    x = "Time (Seconds)",
    y = "MFCC Value",
    color = "MFCC Index"
  ) +
  theme_minimal(base_size = 14) +
  scale_color_brewer(palette = "Dark2") +
  
  # define Minor Breaks for MS_INTERVAL subticks ---
  scale_x_continuous(
    # Major breaks (e.g., every 0.5 seconds, can be customized)
    breaks = seq(START_S, END_S, by = 0.1), 
    
    # Minor breaks (subticks) are set to the MS_INTERVAL sequence
    minor_breaks = minor_breaks_seq,
    
    # Ensures the axis labels are displayed with two decimal places
    labels = scales::number_format(accuracy = 0.01)
  ) +
  
  # Ensure the minor grid lines are visible
  theme(panel.grid.minor.x = element_line(color = "gray85", linewidth = 0.2, linetype = "dotted"))



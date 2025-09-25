# import libraries
library(dplyr)

# read csv
csv_name = '_3v9dP0klkg'
csv_path_template = "/home/asifhasan/projects/asif@github.com/code-snippets/codes/python/audio/out/mfcc_data__%s.csv"
df <- read.csv(sprintf(csv_path_template, csv_name), header = TRUE)

# # transpose
# df <- t(df)
# df <- as.data.frame(df)

# # Get the number of rows from the data frame
# num_rows <- nrow(df)

# # Create the sequence of milliseconds, The sequence starts at 0, increases by 10, and runs for 'num_rows' length
# millisecond_values <- seq(from = 0, by = 20, length.out = num_rows)

# # add the new column and move it to the first position
# df <- df %>%
#   mutate(ms = millisecond_values) %>%
#   relocate(ms, .before = 1)

# # rename column names
# df <- df %>% # nolint: commented_code_linter.
#   rename(
#     MFCC_0 = V1,   # Rename current V1 column to MFCC_0
#     MFCC_1 = V2,   # Rename current V2 column to MFCC_1
#     MFCC_2 = V3,   # Rename current V3 column to MFCC_2
#     MFCC_3 = V4,   # Rename current V3 column to MFCC_2
#     MFCC_4 = V5,   # Rename current V3 column to MFCC_2
#     MFCC_5 = V6,   # Rename current V3 column to MFCC_2
#     MFCC_6 = V7,   # Rename current V3 column to MFCC_2
#     MFCC_7 = V8,   # Rename current V3 column to MFCC_2
#     MFCC_8 = V9,   # Rename current V3 column to MFCC_2
#     MFCC_9 = V10,   # Rename current V3 column to MFCC_2
#     MFCC_10 = V11,   # Rename current V3 column to MFCC_2
#     MFCC_11 = V12,   # Rename current V3 column to MFCC_2
#     MFCC_12 = V13 # Rename current V13 column to MFCC_12
#   )


# load necessary packages
library(tidyverse)

# reshape the Data from Wide to Long Format
# gather all MFCC columns into two new columns: 'Coefficient' and 'Value'
df_long <- df %>%
  pivot_longer(
    cols = starts_with("MFCC_"), # Selects all columns starting with MFCC_
    names_to = "Coefficient",    # The new column that holds 'MFCC_0', 'MFCC_1', etc.
    values_to = "Value"          # The new column that holds the actual MFCC values
  )

# time range in seconds
START_S <- 13.0
END_S <- 17.0
# subticks every 20 ms
INTERVAL_S <- 0.02 

# specific MFCC coefficients to plot
SELECTED_COEFFICIENTS <- c("MFCC_00", "MFCC_01", "MFCC_02")

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



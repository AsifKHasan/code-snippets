#!/usr/bin/env Rscript
# Requires: install.packages("dplyr")
# Requires: install.packages("tidyverse")
# Requires: install.packages("ggplot2")
# Requires: install.packages("argparser")
# Requires: install.packages("yaml")

# import libraries
suppressPackageStartupMessages(library(dplyr, quietly = TRUE))
suppressPackageStartupMessages(library(tidyverse, quietly = TRUE))
suppressPackageStartupMessages(library(ggplot2, quietly = TRUE))
suppressPackageStartupMessages(library(argparser, quietly = TRUE))
suppressPackageStartupMessages(library(yaml, quietly = TRUE))

# create the parser object
p <- arg_parser("analyze data from an input CSV file")

# dd arguments (Positional and Optional)
p <- add_argument(p, "csv_name", help = "name of the input CSV file")

# parse the arguments from the command line
argv <- parse_args(p)

# access the arguments
csv_name <- argv$csv_name


# --- Configuration ---
CONFIG_PATH <- file.path("../conf/config.yml")

# read the YAML file
if (!file.exists(CONFIG_PATH)) {
  stop(paste("configuration file not found at:", CONFIG_PATH), call. = FALSE)
}

config <- read_yaml(CONFIG_PATH)

# read csv
csv_path_template = "../out/mfcc_data__%s.csv"
pdf_path_template = "../out/mfcc_plot__%s.pdf"
cat(paste0("[", Sys.time(), "] ", "analysing MFCC for ", csv_name, "\n"))
df <- read.csv(sprintf(csv_path_template, csv_name), header = TRUE)

START_S <- config$start_s
END_S <- config$end_s
INTERVAL_S <- config$interval_s
SELECTED_COEFFICIENTS <- config$mfcc_coefficients

# reshape the Data from Wide to Long Format
# gather all MFCC columns into two new columns: 'Coefficient' and 'Value'
df_long <- df %>%
  pivot_longer(
    cols = starts_with("MFCC_"), # Selects all columns starting with MFCC_
    names_to = "Coefficient",    # The new column that holds 'MFCC_0', 'MFCC_1', etc.
    values_to = "Value"          # The new column that holds the actual MFCC values
  )


# filter the data frame (df_long)
df_filtered <- df_long %>%
  # filter by the desired time range
  filter(seconds >= START_S & seconds <= END_S) %>%
  # filter by the desired MFCC coefficients
  filter(Coefficient %in% SELECTED_COEFFICIENTS)

# all break points (every INTERVAL_S)
times <- seq(from = START_S, to = END_S, by = INTERVAL_S)
is_major <- abs(times - round(times)) < 1e-8
major_df <- data.frame(x = times[is_major], label = times[is_major])
minor_df <- data.frame(x = times[!is_major], label = sub("^[0-9]+", "", format(times[!is_major], trim = TRUE)))
minor_df$label <- as.numeric(minor_df$label)


# Find the overall minimum and maximum from the results
overall_min_y <- min(df_filtered$Value)
overall_max_y <- max(df_filtered$Value)

label_y_position <- (overall_min_y - 40)

# ggplot Line Plot using the new 'seconds' column and subticks
mfcc_plot <- ggplot(df_filtered, aes(x = seconds, y = Value, color = Coefficient)) +
  
  geom_line(alpha = 0.8, linewidth = 0.4) +
  
  labs(
    title = paste0("Selected MFCC Coefficients (", START_S, "s - ", END_S, "s)"),
    subtitle = paste("Coefficients:", paste(SELECTED_COEFFICIENTS, collapse = ", ")),
    x = "Time (Seconds)",
    y = "MFCC Value",
    color = "MFCC Index"
  ) +

  scale_color_brewer(palette = "Dark2") +
  
  scale_x_continuous(
    # all breaks (subticks) are set to the INTERVAL_S sequence
    breaks = times, labels = NULL, expand = c(0,0)
  ) +

  # Set the Y-axis limits to common speech range (e.g., 50 Hz to 500 Hz)
  coord_cartesian(
    ylim = c(overall_min_y, overall_max_y),
    clip = "off"
  ) +
  
  # suppress the default X-axis labels and ticks
  theme(
    panel.grid.major.x = element_blank(),
    panel.grid.minor.x = element_blank(),
    axis.text.x = element_blank(), 
    axis.ticks.x = element_blank(),
    plot.margin = margin(10, 10, 40, 10)
  ) +
    
  # Adjust text size and angle if labels overlap heavily
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1) 
  ) +

  # Add custom grid lines
  geom_vline(xintercept = major_df$x, color = "gray40", linewidth = 0.3) +
  geom_vline(xintercept = minor_df$x, color = "gray85", linewidth = 0.3) +
  
  # --- Add custom labels using geom_text ---  
  # A. Labels for Full Seconds (Bold and Large)
  geom_text(
    data = major_df,
    aes(x = x, y = label_y_position, label = label), # Set Y slightly below the plot area (adjust -10 based on F0 scale)
    label = scales::number(major_df$label, accuracy = 1),
    angle = 45, hjust = 1,
    size = 5, 
    fontface = "bold",
    inherit.aes = FALSE # Do not inherit main plot aesthetics
  ) +
  
  # B. Labels for Intermediate Seconds (Normal size and weight)
  geom_text(
    data = minor_df,
    aes(x = x, y = label_y_position, label = label), # Same Y position
    label = scales::number(minor_df$label, accuracy = 0.01),
    angle = 45, hjust = 1,
    size = 3, 
    fontface = "plain",
    color = "gray40",
    inherit.aes = FALSE
  )

# print the plot
# print(mfcc_plot)

ggsave(
  filename = file.path(sprintf(pdf_path_template, csv_name)),
  plot = mfcc_plot, 
  width = END_S - START_S, 
  height = 12, 
  units = "in"
)
cat(paste0("[", Sys.time(), "] ", "generating output for ", csv_name, "\n"))
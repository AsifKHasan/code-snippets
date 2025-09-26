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
suppressPackageStartupMessages(library(here, quietly = TRUE))

# source plot scripts
# source(here("ggplot2", "mfcc_plot.R"))
script_path <- file.path("ggplot2", "mfcc-plot.R")
source(script_path)

CONFIG_PATH <- file.path("../conf/config.yml")
csv_path_template = "../out/csv/mfcc/mfcc_data__%s.csv"
pdf_path_template = "../out/plot/mfcc/mfcc_plot__%s.pdf"

# create the parser object
p <- arg_parser("analyze data from an input CSV file")
p <- add_argument(p, "--csv_name", default = "", help = "name of the input CSV file")
argv <- parse_args(p)

# read the YAML file
if (!file.exists(CONFIG_PATH)) {
  stop(paste("configuration file not found at:", CONFIG_PATH), call. = FALSE)
}

# --- Configuration ---
config <- read_yaml(CONFIG_PATH)

START_S <- config$start_s
END_S <- config$end_s
INTERVAL_S <- config$interval_s
SELECTED_COEFFICIENTS <- config$mfcc_coefficients

# if a file was passed as argument, work on that, else get files from config
if (argv$csv_name == "") {
  audio_names <- config$audio_names
} else {
  audio_names <- c(argv$csv_name)
}

# iterate over the files
for (csv_name in audio_names) {
  cat(paste0("[", Sys.time(), "] ", "analyzing MFCC for ", csv_name, "\n"))
  df <- read.csv(sprintf(csv_path_template, csv_name), header = TRUE)

  # get the plot
  mfcc_plot <- plot_mfcc(df, START_S = START_S, END_S = END_S, INTERVAL_S = INTERVAL_S, SELECTED_COEFFICIENTS = SELECTED_COEFFICIENTS)

  # save the plot
  ggsave(
    filename = file.path(sprintf(pdf_path_template, csv_name)),
    plot = mfcc_plot, 
    width = max(END_S - START_S, 20), 
    height = 12, 
    units = "in"
  )
  cat(paste0("[", Sys.time(), "] ", "generating output for ", csv_name, "\n"))
}

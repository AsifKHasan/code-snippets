#!/usr/bin/env Rscript
# Requires: install.packages("dplyr")
# Requires: install.packages("tidyverse")
# Requires: install.packages("ggplot2")

# import libraries
suppressPackageStartupMessages(library(dplyr, quietly = TRUE))
suppressPackageStartupMessages(library(tidyverse, quietly = TRUE))
suppressPackageStartupMessages(library(ggplot2, quietly = TRUE))

# Define the Voice Frequency Band for context
MIN_F0_PITCH <- 70    # Lower end of typical male F0
MAX_F0_PITCH <- 350   # Upper end of typical female/child F0

plot_pitch <- function(df, START_S, END_S, INTERVAL_S) {

  # rename columns for clarity in the plot code
  colnames(df) <- c("time", "f0", "voiced", "probability")

  # filter the data frame (df_long)
  df_filtered <- df %>%
    # filter by the desired time range
    filter(time >= START_S & time <= END_S)

  # all break points (every INTERVAL_S)
  times <- seq(from = START_S, to = END_S, by = INTERVAL_S)
  is_major <- abs(times - round(times)) < 1e-8
  major_df <- data.frame(x = times[is_major], label = times[is_major])
  minor_df <- data.frame(x = times[!is_major], label = sub("^[0-9]+", "", format(times[!is_major], trim = TRUE)))
  minor_df$label <- as.numeric(minor_df$label)

  # create the Visualization
  pitch_plot <- ggplot(df_filtered, aes(x = time)) +
      
  # Use annotate with geom="rect" to create the shaded band for frequency range across y axis
    annotate(
      "rect", 
      xmin = -Inf,          # Start shading at the left edge of the plot
      xmax = Inf,           # End shading at the right edge of the plot
      ymin = MIN_F0_PITCH,  # Lower frequency boundary in Hertz (y-axis)
      ymax = MAX_F0_PITCH,  # Upper frequency boundary in Hertz (y-axis)
      fill = "blue",        # Choose a color, e.g., "gray" or "blue"
      alpha = 0.2,          # Set transparency: 0.2 is a good balance for shading
      color = NA            # Set color to NA to remove the rectangle border
    ) +

    # plot the F0 track (Line Plot)
    # Show only F0 values where Voice_Flag is 1 (voiced frames)
    geom_line(
      aes(y = f0),
      data = subset(df_filtered, voiced == 1),
      color = "#0072B2",  # A nice blue color
      alpha = 0.8
    ) +

    # highlight the Voicing Probability (Scatter Plot)
    # This adds points only where F0 is above 0 (i.e., it's a valid pitch estimate)
    geom_point(
      aes(y = f0, size = probability, color = probability),
      data = subset(df_filtered, f0 > 0),
      alpha = 0.6
    ) +

    # set Colors and Scales
    scale_color_gradient(
      low = "yellow",
      high = "darkred",
      name = "Voice Probability"
    ) +

    scale_size_continuous(
      range = c(0.5, 3), # Adjust point size
      name = "Voice Probability"
    ) +

    # labels and theme
    labs(
      title = "Fundamental Frequency ($f0$) Track Over Time",
      x = "Time (seconds)",
      y = "Fundamental Frequency ($f0$) in Hz"
    ) +

    scale_x_continuous(
      # all breaks (subticks) are set to the INTERVAL_S sequence
      breaks = times, labels = NULL, expand = c(0,0)
    ) +

    # set the Y-axis limits to common speech range (e.g., 50 Hz to 500 Hz)
    coord_cartesian(
      ylim = c(50, 700),
      clip = "off"
    ) +

    # use a clean theme
    theme_minimal() +

    # suppress the default X-axis labels and ticks
    theme(
      panel.grid.major.x = element_blank(),
      panel.grid.minor.x = element_blank(),
      axis.text.x = element_blank(), 
      axis.ticks.x = element_blank(),
      plot.margin = margin(10, 10, 40, 10)
    ) +
      
    # adjust text size and angle if labels overlap heavily
    theme(
      axis.text.x = element_text(angle = 45, hjust = 1) 
    ) +

    # add custom grid lines
    geom_vline(xintercept = major_df$x, color = "gray40", linewidth = 0.3) +
    geom_vline(xintercept = minor_df$x, color = "gray85", linewidth = 0.3) +
    
    # --- add custom labels using geom_text ---  
    # labels for Full Seconds (Bold and Large)
    geom_text(
      data = major_df,
      aes(x = x, y = -10, label = label), # Set Y slightly below the plot area (adjust -10 based on F0 scale)
      label = scales::number(major_df$label, accuracy = 1),
      angle = 45, hjust = 1,
      size = 5, 
      fontface = "bold",
      inherit.aes = FALSE # Do not inherit main plot aesthetics
    ) +
    
    # labels for Intermediate Seconds (Normal size and weight)
    geom_text(
      data = minor_df,
      aes(x = x, y = -10, label = label), # Same Y position
      label = scales::number(minor_df$label, accuracy = 0.01),
      angle = 45, hjust = 1,
      size = 3, 
      fontface = "plain",
      color = "gray40",
      inherit.aes = FALSE
    )

  return(pitch_plot)
}

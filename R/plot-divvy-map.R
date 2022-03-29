library(maps)
library(ggplot2)
library(tidyverse)
library(ggmap)
library(googleway)

theme_set(theme_bw(base_size=16))


world_map <- map_data('world')
p <- ggplot() + coord_fixed() +
  xlab("") + ylab("")

base_world_messy <- p + geom_polygon(data=world_map, aes(x=long, y=lat, group=group), 
                                     colour="light green", fill="light green")

base_world_messy

#Strip the map down so it looks super clean (and beautiful!)
cleanup <- 
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(), 
        panel.background = element_rect(fill = 'white', colour = 'white'), 
        axis.line = element_line(colour = "white"), legend.position="none",
        axis.ticks=element_blank(), axis.text.x=element_blank(),
        axis.text.y=element_blank())

base_world <- base_world_messy + cleanup

base_world


usa_map <- map_data('state')
usa <- p + geom_polygon(data=usa_map, aes(x=long, y=lat, group=group) 
                         ,colour="light green"
)
usa <- usa + cleanup
usa

il_map <- map_data('state', region="Illinois")
il <- p + geom_polygon(data=il_map, aes(x=long, y=lat, group=group) 
                       ,colour="light green"
)
il <- il + cleanup
il            
      
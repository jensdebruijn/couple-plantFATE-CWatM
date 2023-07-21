library(tidyverse)

data_with_update <- read.csv("out/test_data_with_update.csv")
data_without_update <- read.csv("out/test_data_without_update.csv")

data_with_update$update = TRUE
data_without_update$update = FALSE

data_all = plyr::rbind.fill(data_with_update, data_without_update)
data_all <- data_all %>% filter(time > 0) %>%
  mutate(date_yr = time / 365)
# data_all= data_with_update
colnames(data_all)

p <- ggplot(data_all, aes(x = date_yr, y = GPP, color = update)) +
  geom_point() + 
  scale_y_continuous("GPP [kgCm-2d-1]") + 
  scale_x_continuous("Time [yr]") + 
  scale_color_discrete("cWATm input")
p

p <- ggplot(data_all, aes(x = date_yr, y = transpiration, color = update)) +
  geom_point()+ 
  scale_y_continuous("Transpiration ") + 
  scale_x_continuous("Time [yr]") + 
  scale_color_discrete("cWATm input")
p

p <- ggplot(data_all, aes(x = date_yr, y = swp_out, color = update)) +
  geom_point()+ 
  scale_y_continuous("Soil Water Potential Input [mPa]") + 
  scale_x_continuous("Time [yr]") + 
  scale_color_discrete("cWATm input")
p

p <- ggplot(data_all, aes(x = date_yr, y = vpd_out, color = update)) +
  geom_point()+ 
  scale_y_continuous("VPD input [Pa]") + 
  scale_x_continuous("Time [yr]") + 
  scale_color_discrete("cWATm input")
p

p <- ggplot(data_all, aes(x = date_yr, y = ppfd_out, color = update)) +
  geom_point() + 
  scale_y_continuous("Photosynthetic Photon Flux Density input [umol m-2 s-1]") + 
  scale_x_continuous("Time [yr]") + 
  scale_color_discrete("cWATm input")
p


p <- ggplot(data_all, aes(x = date_yr, y = gs, color = update)) +
  geom_point()+ 
  scale_y_continuous("Stomatal Conductance [mol m-2 s-1]") + 
  scale_x_continuous("Time [yr]") + 
  scale_color_discrete("cWATm input")
p




library(tidyverse)
data_with_update <- read.csv("data/out_data_test.csv")

data_with_update$update = TRUE
data_all = data_with_update;
# 
# data_all = plyr::rbind.fill(data_with_update, data_without_update)
# data_all <- data_all %>% filter(time > 0) %>%
#  mutate(date_yr = time / 365)
# data_all= data_with_update
colnames(data_all)
data_all$date <- as.Date(data_all$date)

p <- ggplot(data_all, aes(x = date, y = GPP, color = update)) +
  geom_point() + 
  scale_y_continuous("GPP [kgCm-2yr-1]") + 
  scale_x_date("Time [yr]") + 
  scale_color_discrete("cWATm input")
p

p <- ggplot(data_all, aes(x = date, y = transpiration, color = update)) +
  geom_point()+ 
  scale_y_continuous("Transpiration ") + 
  scale_x_date("Time [yr]") + 
  scale_color_discrete("cWATm input")
p

p <- ggplot(data_all, aes(x = date, y = swp_ave_out, color = update)) +
  geom_point()+ 
  scale_y_continuous("Soil Water Potential Input [mPa]") + 
  scale_x_date("Time [yr]") + 
  scale_color_discrete("cWATm input")
p

p <- ggplot(data_all, aes(x = date, y = vpd_ave_out, color = update)) +
  geom_point()+ 
  scale_y_continuous("VPD input [Pa]") + 
  scale_x_date("Time [yr]") + 
  scale_color_discrete("cWATm input")
p


p <- ggplot(data_all, aes(x = date, y = Tavg, color = update)) +
  geom_point()+ 
  scale_y_continuous("Temperature [C]") + 
  scale_x_date("Time [yr]") + 
  scale_color_discrete("cWATm input")
p


p <- ggplot(data_all, aes(x = date_yr, y = ppfd_out, color = update)) +
  geom_point() + 
  scale_y_continuous("Photosynthetic Photon Flux Density input [umol m-2 s-1]") + 
  scale_x_continuous("Time [yr]") + 
  scale_color_discrete("cWATm input")
p


p <- ggplot(data_all, aes(x = date, y = gs, color = update)) +
  geom_point()+ 
  scale_y_continuous("Stomatal Conductance [mol m-2 s-1]") + 
  scale_x_date("Time [yr]") + 
  scale_color_discrete("cWATm input")
p




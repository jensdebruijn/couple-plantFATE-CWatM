def run_plantFATE(soil_water_potential_CWatM):
    # TODO: Implement
    return evapotranspiration

def calculate_soil_water_potential(soil_moisture, soil_thickness):
    # TODO: Implement
    return soil_water_potential
    
def calculate_vapour_pressure_deficit(temperature, relative_humidity):
    # TODO: Implement
    return vapour_pressure_deficit
    
def calculate_photosynthetically_active_radiation(shortwave_radiation, longwave_radiation, xi=0.5):
    # https://doi.org/10.1016/B978-0-12-815826-5.00005-2
    photosynthetically_active_radiation = shortwave_radiation * xi
    return photosynthetically_active_radiation

def couple_plantFATE(
        soil_moisture_layer_1,  # ratio [0-1]
        soil_moisture_layer_2,  # ratio [0-1]
        soil_moisture_layer_3,  # ratio [0-1]
        soil_tickness_layer_1,  # m
        soil_tickness_layer_2,  # m
        soil_tickness_layer_3,  # m
        temperature,  # degrees Kelvin
        relative_humidity,  # ratio [0-1]
        shortwave_radiation,  # W/m2
        longwave_radiation  # W/m2
    ):
        
    soil_water_potential_1 = calculate_soil_water_potential(soil_moisture_layer_1, soil_tickness_layer_1)
    soil_water_potential_2 = calculate_soil_water_potential(soil_moisture_layer_2, soil_tickness_layer_2)
    soil_water_potential_3 = calculate_soil_water_potential(soil_moisture_layer_3, soil_tickness_layer_3)
    
    vapour_pressure_deficit = calculate_vapour_pressure_deficit(temperature, relative_humidity)
    
    photosynthetically_active_radiation = calculate_photosynthetically_active_radiation(shortwave_radiation, longwave_radiation)

    evapotranspiration = run_plantFATE(
        [
            soil_water_potential_1,
            soil_water_potential_2,
            soil_water_potential_3
        ],
        vapour_pressure_deficit,
        photosynthetically_active_radiation,
        temperature
    )
    
    return evapotranspiration


if __name__ == '__main__':
    couple_plantFATE(
        soil_moisture_layer_1=0.7,  # ratio [0-1]
        soil_moisture_layer_2=0.5,  # ratio [0-1]
        soil_moisture_layer_3=0.3,  # ratio [0-1]
        soil_tickness_layer_1=0.05,  # m
        soil_tickness_layer_2=0.5,  # m
        soil_tickness_layer_3=3,  # m
        temperature=293,  # degrees Kelvin
        relative_humidity=0.70,  # ratio [0-1]
        shortwave_radiation,  # W/m2
        longwave_radiation  # W/m2
    )

def run_plantFATE(soil_water_potential_CWatM):
    return psi

def couple_plantFATE(
        soil_moisture_layer_1,
        soil_moisture_layer_2,
        soil_moisture_layer_3,
        soil_tickness_layer_1,
        soil_tickness_layer_2,
        soil_tickness_layer_3,
        precipitation,
        water_pressure_deficit,
        irradiance,
        irrigation=0, # forest never has has irrigation
    ):

    # run plantFATE
    irradiance = 0.5
    water_pressure_deficit = 0.5

    soil_water_potential_CWatM = xxx
    psi = run_plantFATE(soil_water_potential_CWatM)
    

    evapotranspiration = # how do I calculate this?

    return evapotranspiration


if __name__ == '__main__':
    couple_plantFATE(
        soil_moisture_layer_1=0.7, # ratio [0-1]
        soil_moisture_layer_2=0.5, # ratio [0-1]
        soil_moisture_layer_3=0.3, # ratio [0-1]
        soil_tickness_layer_1=0.05, # meter
        soil_tickness_layer_2=0.3, # meter
        soil_tickness_layer_3=0.3, # meter
        precipitation=1, # mm
        water_pressure_deficit=0 # check with Mikhail
        irradiance=0.5, # check with Mikhail
        irrigation=0, # mm, forest never has has irrigation
    )

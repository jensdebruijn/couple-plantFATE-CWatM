import numpy as np
import matplotlib.pyplot as plt

def run_plantFATE(soil_water_potentials, vapour_pressure_deficit, photosynthetically_active_radiation, temperature):
    # TODO: Implement
    return evapotranspiration

def calculate_soil_water_potential(
        soil_moisture,  # [0-1]
        soil_moisture_wilting_point,  # [0-1]
        soil_moisture_field_capacity,  # [0-1]
        wilting_point=-1500,  # kPa
        field_capacity=-33  # kPa
    ):
    # https://doi.org/10.1016/B978-0-12-374460-9.00007-X
    n_potential = - np.log(wilting_point / field_capacity) / np.log(soil_moisture_wilting_point / soil_moisture_field_capacity)
    assert n_potential >= 0
    a_potential = 1.5 * 10 ** 6 * soil_moisture_wilting_point ** n_potential
    assert a_potential >= 0
    soil_water_potential = -a_potential * soil_moisture ** (-n_potential)
    return soil_water_potential / 1000  # Pa to kPa
    
def calculate_vapour_pressure_deficit(temperature, relative_humidity):
    # https://soilwater.github.io/pynotes-agriscience/notebooks/vapor_pressure_deficit.html
    saturated_vapour_pressure = 0.611 * np.exp((17.502 * temperature) / (temperature + 240.97))  # kPa
    actual_vapour_pressure = saturated_vapour_pressure * relative_humidity  # kPa
    vapour_pressure_deficit = saturated_vapour_pressure - actual_vapour_pressure
    return actual_vapour_pressure
    
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
        soil_moisture_wilting_point,  # ratio [0-1]
        soil_moisture_field_capacity,  # ratio [0-1]
        temperature,  # degrees Kelvin
        relative_humidity,  # ratio [0-1]
        shortwave_radiation,  # W/m2
        longwave_radiation  # W/m2
    ):
    
    assert soil_moisture_layer_1 >= 0 and soil_moisture_layer_1 <= 1
    assert soil_moisture_layer_2 >= 0 and soil_moisture_layer_2 <= 1
    assert soil_moisture_layer_3 >= 0 and soil_moisture_layer_3 <= 1
    assert temperature > 150  # temperature is in Kelvin. So on earth should be well above 150.
    assert relative_humidity >= 0 and relative_humidity <= 1
        
    soil_water_potential_1 = calculate_soil_water_potential(soil_moisture_layer_1, soil_moisture_wilting_point, soil_moisture_field_capacity)
    soil_water_potential_2 = calculate_soil_water_potential(soil_moisture_layer_2, soil_moisture_wilting_point, soil_moisture_field_capacity)
    soil_water_potential_3 = calculate_soil_water_potential(soil_moisture_layer_3, soil_moisture_wilting_point, soil_moisture_field_capacity)
    
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


def test_soil_water_potential(soil_moisture_wilting_point, soil_moisture_field_capacity, soil_moisture_saturation):
    soil_moisture_array = np.linspace(soil_moisture_wilting_point, soil_moisture_saturation, 100)
    soil_water_potential_array = [
        calculate_soil_water_potential(
            soil_moisture=soil_moisture,  # [0-1]
            soil_moisture_wilting_point=soil_moisture_wilting_point,  # [0-1]
            soil_moisture_field_capacity=soil_moisture_field_capacity,  # [0-1]
            wilting_point=-1500,  # kPa
            field_capacity=-33  # kPa
        ) for soil_moisture in soil_moisture_array
    ]
    fig, ax = plt.subplots()
    ax.plot(soil_moisture_array, soil_water_potential_array)
    # invert y axis
    ax.invert_yaxis()
    ax.axhline(y=soil_moisture_wilting_point, color='red')
    ax.axhline(y=soil_moisture_field_capacity, color='blue')
    ax.set_xlabel('Soil moisture (ratio)')
    ax.set_ylabel('Soil water potential (kPa)')
    plt.show()


if __name__ == '__main__':
    # test_soil_water_potential(soil_moisture_wilting_point=0.126, soil_moisture_field_capacity=0.268, soil_moisture_saturation=0.461)  # loam
    couple_plantFATE(
        soil_moisture_layer_1=0.25,  # ratio [0-1]
        soil_moisture_layer_2=0.2,  # ratio [0-1]
        soil_moisture_layer_3=0.15,  # ratio [0-1]
        soil_tickness_layer_1=0.05,  # m
        soil_tickness_layer_2=0.5,  # m
        soil_tickness_layer_3=3,  # m
        soil_moisture_wilting_point=0.126,  # ratio [0-1]
        soil_moisture_field_capacity=0.268,  # ratio [0-1]
        temperature=293,  # degrees Kelvin
        relative_humidity=0.70,  # ratio [0-1]
        shortwave_radiation=171.6,  # W/m2
        longwave_radiation=239  # W/m2
    )

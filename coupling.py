import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import cppimport.import_hook
import plantFATE
import plantFATERunner


class PlantFATECoupling:
    # plantFATE_model = None
    # soil_data = None
    def __init__(self, param_file):
        self.plantFATE_model = plantFATERunner.PlantFATERunner("params/p_daily.ini")

    def plantFATE_init(self, tstart, soil_moisture_layer_1,  # ratio [0-1]
                       soil_moisture_layer_2,  # ratio [0-1]
                       soil_moisture_layer_3,  # ratio [0-1]
                       soil_tickness_layer_1,  # m
                       soil_tickness_layer_2,  # m
                       soil_tickness_layer_3,  # m
                       soil_moisture_wilting_point_1,  # ratio [0-1]
                       soil_moisture_wilting_point_2,  # ratio [0-1]
                       soil_moisture_wilting_point_3,  # ratio [0-1]
                       soil_moisture_field_capacity_1,  # ratio [0-1]
                       soil_moisture_field_capacity_2,  # ratio [0-1]
                       soil_moisture_field_capacity_3,  # ratio [0-1]
                       temperature,  # degrees Celcius, mean temperature
                       relative_humidity,  # percentage [0-100]
                       shortwave_radiation,  # W/m2, daily mean
                       longwave_radiation  # W/m2, daily mean
                       ):
        soil_water_potentials0, vapour_pressure_deficit0, photosynthetically_active_radiation0, temperature0 = self.get_plantFATE_input(
            soil_moisture_layer_1,  # ratio [0-1]
            soil_moisture_layer_2,  # ratio [0-1]
            soil_moisture_layer_3,  # ratio [0-1]
            soil_tickness_layer_1,  # m
            soil_tickness_layer_2,  # m
            soil_tickness_layer_3,  # m
            soil_moisture_wilting_point_1,  # ratio [0-1]
            soil_moisture_wilting_point_2,  # ratio [0-1]
            soil_moisture_wilting_point_3,  # ratio [0-1]
            soil_moisture_field_capacity_1,  # ratio [0-1]
            soil_moisture_field_capacity_2,  # ratio [0-1]
            soil_moisture_field_capacity_3,  # ratio [0-1]
            temperature,  # degrees Celcius, mean temperature
            relative_humidity,  # percentage [0-100]
            shortwave_radiation,  # W/m2, daily mean
            longwave_radiation)
        self.plantFATE_model.init(tstart, temperature0, soil_water_potentials0, vapour_pressure_deficit0,
                                  photosynthetically_active_radiation0)

    def close_simulation(self):
        self.plantFATE_model.plantFATE_model.close()

    def run_plantFATE_step(self, soil_water_potentials, vapour_pressure_deficit, photosynthetically_active_radiation,
                           temperature):
        evapotranspiration, soil_specific_depletion_1, \
            soil_specific_depletion_2, soil_specific_depletion_3 = self.plantFATE_model.runstep(soil_water_potentials,
                                                                                                vapour_pressure_deficit,
                                                                                                photosynthetically_active_radiation,
                                                                                                temperature)

        return evapotranspiration, soil_specific_depletion_1, soil_specific_depletion_2, soil_specific_depletion_3

    def calculate_soil_water_potential(
            self,
            soil_moisture,  # [0-1]
            soil_moisture_wilting_point,  # [0-1]
            soil_moisture_field_capacity,  # [0-1]
            wilting_point=-1500,  # kPa
            field_capacity=-33  # kPa
    ):
        # https://doi.org/10.1016/B978-0-12-374460-9.00007-X
        n_potential = - np.log(wilting_point / field_capacity) / np.log(
            soil_moisture_wilting_point / soil_moisture_field_capacity)
        assert n_potential >= 0
        a_potential = 1.5 * 10 ** 6 * soil_moisture_wilting_point ** n_potential
        assert a_potential >= 0
        soil_water_potential = -a_potential * soil_moisture ** (-n_potential)
        return soil_water_potential / 1000000  # Pa to MPa

    def calculate_vapour_pressure_deficit(self, temperature, relative_humidity):
        # https://soilwater.github.io/pynotes-agriscience/notebooks/vapor_pressure_deficit.html
        saturated_vapour_pressure = 0.611 * np.exp((17.502 * temperature) / (temperature + 240.97))  # kPa
        actual_vapour_pressure = saturated_vapour_pressure * relative_humidity / 100  # kPa
        vapour_pressure_deficit = saturated_vapour_pressure - actual_vapour_pressure
        return vapour_pressure_deficit

    def calculate_photosynthetically_active_radiation(self, shortwave_radiation, longwave_radiation, xi=0.5):
        # https://doi.org/10.1016/B978-0-12-815826-5.00005-2
        maximum_shortwave_radiation = shortwave_radiation * 4  # multiply by 2 for night, multiply by 2 for integral of sine wave
        photosynthetically_active_radiation = maximum_shortwave_radiation / xi
        return photosynthetically_active_radiation

    def get_plantFATE_input(self,
                            soil_moisture_layer_1,  # ratio [0-1]
                            soil_moisture_layer_2,  # ratio [0-1]
                            soil_moisture_layer_3,  # ratio [0-1]
                            soil_tickness_layer_1,  # m
                            soil_tickness_layer_2,  # m
                            soil_tickness_layer_3,  # m
                            soil_moisture_wilting_point_1,  # ratio [0-1]
                            soil_moisture_wilting_point_2,  # ratio [0-1]
                            soil_moisture_wilting_point_3,  # ratio [0-1]
                            soil_moisture_field_capacity_1,  # ratio [0-1]
                            soil_moisture_field_capacity_2,  # ratio [0-1]
                            soil_moisture_field_capacity_3,  # ratio [0-1]
                            temperature,  # degrees Celcius, mean temperature
                            relative_humidity,  # percentage [0-100]
                            shortwave_radiation,  # W/m2, daily mean
                            longwave_radiation  # W/m2, daily mean
                            ):
        assert soil_moisture_layer_1 >= 0 and soil_moisture_layer_1 <= 1
        assert soil_moisture_layer_2 >= 0 and soil_moisture_layer_2 <= 1
        assert soil_moisture_layer_3 >= 0 and soil_moisture_layer_3 <= 1
        assert temperature < 100  # temperature is in Celsius. So on earth should be well below 100.
        assert relative_humidity >= 0 and relative_humidity <= 100

        soil_water_potential_1 = self.calculate_soil_water_potential(soil_moisture_layer_1,
                                                                     soil_moisture_wilting_point_1,
                                                                     soil_moisture_field_capacity_1)
        soil_water_potential_2 = self.calculate_soil_water_potential(soil_moisture_layer_2,
                                                                     soil_moisture_wilting_point_2,
                                                                     soil_moisture_field_capacity_2)
        soil_water_potential_3 = self.calculate_soil_water_potential(soil_moisture_layer_3,
                                                                     soil_moisture_wilting_point_3,
                                                                     soil_moisture_field_capacity_3)

        vapour_pressure_deficit = self.calculate_vapour_pressure_deficit(temperature, relative_humidity)

        photosynthetically_active_radiation = self.calculate_photosynthetically_active_radiation(shortwave_radiation,
                                                                                                 longwave_radiation)

        return [soil_water_potential_1, soil_water_potential_2,
                soil_water_potential_3], vapour_pressure_deficit, photosynthetically_active_radiation, temperature

    def step(
            self,
            soil_moisture_layer_1,  # ratio [0-1]
            soil_moisture_layer_2,  # ratio [0-1]
            soil_moisture_layer_3,  # ratio [0-1]
            soil_tickness_layer_1,  # m
            soil_tickness_layer_2,  # m
            soil_tickness_layer_3,  # m
            soil_moisture_wilting_point_1,  # ratio [0-1]
            soil_moisture_wilting_point_2,  # ratio [0-1]
            soil_moisture_wilting_point_3,  # ratio [0-1]
            soil_moisture_field_capacity_1,  # ratio [0-1]
            soil_moisture_field_capacity_2,  # ratio [0-1]
            soil_moisture_field_capacity_3,  # ratio [0-1]
            temperature,  # degrees Celcius, mean temperature
            relative_humidity,  # percentage [0-100]
            shortwave_radiation,  # W/m2, daily mean
            longwave_radiation  # W/m2, daily mean
    ):
        soil_water_potentials, vapour_pressure_deficit, photosynthetically_active_radiation, temperature = self.get_plantFATE_input(
            soil_moisture_layer_1,  # ratio [0-1]
            soil_moisture_layer_2,  # ratio [0-1]
            soil_moisture_layer_3,  # ratio [0-1]
            soil_tickness_layer_1,  # m
            soil_tickness_layer_2,  # m
            soil_tickness_layer_3,  # m
            soil_moisture_wilting_point_1,  # ratio [0-1]
            soil_moisture_wilting_point_2,  # ratio [0-1]
            soil_moisture_wilting_point_3,  # ratio [0-1]
            soil_moisture_field_capacity_1,  # ratio [0-1]
            soil_moisture_field_capacity_2,  # ratio [0-1]
            soil_moisture_field_capacity_3,  # ratio [0-1]
            temperature,  # degrees Celcius, mean temperature
            relative_humidity,  # percentage [0-100]
            shortwave_radiation,  # W/m2, daily mean
            longwave_radiation)

        evapotranspiration, soil_specific_depletion_1, soil_specific_depletion_2, soil_specific_depletion_3 = self.run_plantFATE_step(
            soil_water_potentials,
            vapour_pressure_deficit,
            photosynthetically_active_radiation,
            temperature
        )

        return evapotranspiration, soil_specific_depletion_1, soil_specific_depletion_2, soil_specific_depletion_3


def test_soil_water_potential(soil_moisture_wilting_point, soil_moisture_field_capacity, soil_moisture_saturation):
    plantFATE_coupling = PlantFATECoupling()
    soil_moisture_array = np.linspace(soil_moisture_wilting_point, soil_moisture_saturation, 100)
    soil_water_potential_array = [
        plantFATE_coupling.calculate_soil_water_potential(
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

    plantFATE_df = pd.read_csv('plantFATE.csv', index_col=0)
    plantFATE_df = plantFATE_df.iloc[0:4000, :]

    plantFATE_coupling = PlantFATECoupling('params/p_daily.ini')
    plantFATE_coupling.plantFATE_init(tstart=plantFATE_df.index[0],
                                      soil_moisture_layer_1=plantFATE_df.w1[0],  # ratio [0-1]
                                      soil_moisture_layer_2=plantFATE_df.w2[0],  # ratio [0-1]
                                      soil_moisture_layer_3=plantFATE_df.w3[0],  # ratio [0-1]
                                      soil_tickness_layer_1=plantFATE_df.soildepth_1[0],  # m
                                      soil_tickness_layer_2=plantFATE_df.soildepth_2[0],  # m
                                      soil_tickness_layer_3=plantFATE_df.soildepth_3[0],  # m
                                      soil_moisture_wilting_point_1=plantFATE_df.wwp1[0],  # ratio [0-1]
                                      soil_moisture_wilting_point_2=plantFATE_df.wwp2[0],  # ratio [0-1]
                                      soil_moisture_wilting_point_3=plantFATE_df.wwp3[0],  # ratio [0-1]
                                      soil_moisture_field_capacity_1=plantFATE_df.wfc1[0],  # ratio [0-1]
                                      soil_moisture_field_capacity_2=plantFATE_df.wfc2[0],  # ratio [0-1]
                                      soil_moisture_field_capacity_3=plantFATE_df.wfc3[0],  # ratio [0-1]
                                      temperature=plantFATE_df.Tavg[0],  # degrees Celcius
                                      relative_humidity=plantFATE_df.hurs[0],  # percentage
                                      shortwave_radiation=plantFATE_df.Rsds[0],  # W/m2 - or MJd-1
                                      longwave_radiation=plantFATE_df.Rsdl[0]  # W/m2 - or MJd-1
                                      )

    plantFATE_df = plantFATE_df.iloc[1:10000, :]

    for time, row in plantFATE_df.iterrows():
        evapotranspiration, soil_specific_depletion_1, soil_specific_depletion_2, soil_specific_depletion_3 = plantFATE_coupling.step(
            soil_moisture_layer_1=row['w1'],  # ratio [0-1]
            soil_moisture_layer_2=row['w2'],  # ratio [0-1]
            soil_moisture_layer_3=row['w3'],  # ratio [0-1]
            soil_tickness_layer_1=row['soildepth_1'],  # m
            soil_tickness_layer_2=row['soildepth_2'],  # m
            soil_tickness_layer_3=row['soildepth_3'],  # m
            soil_moisture_wilting_point_1=row['wwp1'],  # ratio [0-1]
            soil_moisture_wilting_point_2=row['wwp2'],  # ratio [0-1]
            soil_moisture_wilting_point_3=row['wwp3'],  # ratio [0-1]
            soil_moisture_field_capacity_1=row['wfc1'],  # ratio [0-1]
            soil_moisture_field_capacity_2=row['wfc2'],  # ratio [0-1]
            soil_moisture_field_capacity_3=row['wfc3'],  # ratio [0-1]
            temperature=row['Tavg'],  # degrees Celcius
            relative_humidity=row['hurs'],  # percentage
            shortwave_radiation=row['Rsds'],  # W/m2 - or MJd-1
            longwave_radiation=row['Rsdl']  # W/m2 - or MJd-1
        )

    plantFATE_coupling.close_simulation()
    plantFATE_coupling.plantFATE_model.exportEnvironment("out/environment_0.csv")
    plantFATE_coupling.plantFATE_model.exportEmergentProps("out/emergentProps_0.csv")
    # plantFATE_coupling.plantFATE_model.exportEnvironment("out/emergentProps.csv")

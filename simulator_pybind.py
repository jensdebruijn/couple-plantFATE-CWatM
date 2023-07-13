import cppimport.import_hook
import plantFATE 

# a = simulator.add(10, 20)
print("TEST the Simulator")

s = plantFATE.Simulator("params/p_daily.ini", "daily")
s.init(0, 700)
s.simulate()
s.close()

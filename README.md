# Rossiter-McPlotlin
A minimal-dependecy package for visualizing orbital geometries for the Rossiter-Mclaughlin effect.
(no starry installation needed!)

## Command Line Useage
```console
user@machine:~/Rossiter-McPlotlin$ python rossiter_mcplotlin -f example.conf
```

## Configuration File Formating

```text
[Stellar and System Parameters]
# planets in the system to be plotted
# quadtratic limb darkening parameter
# quadtratic limb darkening parameter
# stellar inclination
# stellar projected velocity
planets: b,c           
u0: 0.5                
u1: 0.5                
inc: 75
vsini: 2

[Planet Parameters]
# Planet/star radius ratio
# Planet inclination
# Planet impact parameter
# Projected obliquity
# Projected obliquity uncertainties 
rprs_b: 0.017          
inc_b: 87              
imp_b: 0.18            
lam_b = -6             
lam_err_b = 2,3        

rprs_c: 0.03
inc_c: 89
imp_c: 0.45
lam_c = -107
lam_err_c = 5,5

[Plotting Options]
output_name: example
nlat: 9
nlong: 20
plot_err: b,c
color_b: black
color_c: green
dpi: 300
format: png
title_on: True
title: HD 3167
```

<img src="https://github.com/aspolanski/Rossiter-McPlottin/blob/main/toi1759_rm.png" width="400" height="400" />

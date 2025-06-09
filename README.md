# Rossiter-McPlotlin
A minimal-dependecy package for visualizing orbital geometries for the Rossiter-Mclaughlin effect.
(no starry installation needed!)

## Command Line Useage
```console
user@machine:~/Rossiter-McPlotlin$ python rossiter_mcplotlin -f example.conf
```

## Configuration File Formating

```console
[Stellar and System Parameters]
planets: b,c           ; planets in the system to be plotted
u0: 0.5                ; quadtratic limb darkening parameter
u1: 0.5                ; quadtratic limb darkening parameter
inc: 75                ; stellar inclination
vsini: 2               ; stellar projected velocity

[Planet Parameters]
rprs_b: 0.017          ; Planet/star radius ratio
inc_b: 87              ; Planet inclination
imp_b: 0.18            ; Planet impact parameter
lam_b = -6             ; Projected obliquity
lam_err_b = 2,3        ; Projected obliquity uncertainties 

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

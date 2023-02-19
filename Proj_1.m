Ts = 1; % Duracion del simbolo
L = 16; % Numero de muestras por simbolo

a_0 = 0; % Factor de rodamiento
a_0_25 = 0.25; % Factor de rodamiento
a_0_75 = 0.75; % Factor de rodamiento
a_1 = 1 ; % Factor de rodamiento

t = -3:Ts/L: 3; % Vector de tiempo para el eje x

pt_0 = rcosdesign(a_0,6,L,'normal'); %Version muestreada del pulso de coseno alzado
pt_0_25 = rcosdesign(a_0_25,6,L,'normal');
pt_0_75 = rcosdesign(a_0_75,6,L,'normal');
pt_1 = rcosdesign(a_1,6,L,'normal');

figure(1)
plot (t,pt_0,'DisplayName','0')
grid on
hold on

plot (t,pt_0_25,'DisplayName','0.25')
plot (t,pt_0_75,'DisplayName','0.75')
plot (t,pt_1,'DisplayName','1')
hold off




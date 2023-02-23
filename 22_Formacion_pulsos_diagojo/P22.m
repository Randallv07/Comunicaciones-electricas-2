%tx_sig_gen.m
clear all;
close all;
rand(1,1668);     % Cambie los ultimos 3 digitos por los ultimos 3 numeros de su carne.
Ts = 1;           % Duración del símbolo
L  = 16;          % Número de muestras por símbolo
t_step = Ts/L;    % Tamaño del paso para muestreo, es correcto ya que divide el tiempo total del símbolo entre la cantidad de muestras
                  %dando el tiempo entre muestras

%%%%%%%%%<1. Generacion de onda del pulso > %%%%%%%%%%%%%%%%%%%%%%
pt     = rcosdesign(0,6,L,'normal');   % Genera los puntos del coseno alzado con factor de rodamiento de 0.25, 6 tiempos de símbolo y 100 muestras por símbolo
pt_05  = rcosdesign(0.5,6,L,'normal');
pt_075 = rcosdesign(0.75,6,L,'normal');
pt_1   = rcosdesign(1,6,L,'normal');

pt = pt/(max(abs(pt))); %rescaling to match rcosine                                      

%%%%%%%%%<2. Generacion de 100 simbolos binarios >%%%%%%%%%%%%%%%%%%%%
Ns = 1389;                                 % Numero de muestras
data_bit = (rand(1,Ns)>0.5);              % Está correcto ya que se genera un vector de dimensión Ns y convierte a valores booleanos

%%%%%%%%%<3. Unipolar a Bipolar (modulacion de amplitud)>%%%%%%%%%%%%%%
% Descomentar la siguiente linea para trabajar en un sistema 2-ario
%amp_modulated = 2*data_bit-1; % 0=> -1,  1=>1
% Descomentar la siguiente linea para trabajar en un sistema 4-ario
amp_modulated = 2*ceil(rand(1,Ns)*4)-5; 

%%%%%%%%%<4.  Modulacion de pulsos >%%%%%%%%%%%%%%%%%%%%%%%%%%%%
impulse_modulated = [];
for n=1:Ns
    delta_signal = [amp_modulated(n)  zeros(1, L-1)];         % Se genera un vector con el dato seguido de 99 ceros
    impulse_modulated =[impulse_modulated  delta_signal];     % Se concatena el vector anterior de todos los datos
                                                                                                       % dando un vector con los datos de la modulación
end

%%%%%%%%<5.Formacion de pulsos (filtrado de transmision)>%%%%%%%%%%
tx_signal = conv(impulse_modulated, pt);     % Convoluciona la señal modulada con la función de transferencia del filtro (coseno alzado) y da
                                             % como resultado la señal teóricamente sin ISI

% Toma en cuenta el coseno alzado para varios alpha
tx_signal_05  = conv(impulse_modulated, pt_05);
tx_signal_075 = conv(impulse_modulated, pt_075);
tx_signal_1   = conv(impulse_modulated, pt_1);

                                             
                                             
figure(100)
subplot (2,1,1)
stem( t_step: t_step: (Ns*Ts), impulse_modulated, '.');
axis ([0 Ns*Ts -2*max(impulse_modulated) 2*max(impulse_modulated)]);
grid on
title('impulse modulated')
subplot(2,1,2)
plot(t_step:t_step:(t_step*length(tx_signal)), tx_signal);
axis([0 Ns*Ts -2*max(tx_signal) 2*max(tx_signal)]);
grid on
title ('pulse shaped')

% Las figuras a continuación permiten graficar el diagrama de ojo para
% diferentes alpha en el caso de un sistema 4-ario
figure(200)
for k=3 : floor(Ns/2) - 1       % representa la k - esima muestra
    tmp = tx_signal(((k-1)*2*L + 1) : (k*2*L));
    plot(t_step * (0 : (2*L-1)), tmp);
    axis([0 2 min(tx_signal) max(tx_signal)]);
    grid on;
    hold on;
    %pause
end

figure(201)
for k=3 : floor(Ns/2) - 1       % representa la k - esima muestra
    tmp = tx_signal_05(((k-1)*2*L + 1) : (k*2*L));
    plot(t_step * (0 : (2*L-1)), tmp);
    axis([0 2 min(tx_signal_05) max(tx_signal_05)]);
    grid on;
    hold on;
    %pause
end

figure(202)
for k=3 : floor(Ns/2) - 1       % representa la k - esima muestra
    tmp = tx_signal_075(((k-1)*2*L + 1) : (k*2*L));
    plot(t_step * (0 : (2*L-1)), tmp);
    axis([0 2 min(tx_signal_075) max(tx_signal_075)]);
    grid on;
    hold on;
    %pause
end

figure(203)
for k=3 : floor(Ns/2) - 1       % representa la k - esima muestra
    tmp = tx_signal_1(((k-1)*2*L + 1) : (k*2*L));
    plot(t_step * (0 : (2*L-1)), tmp);
    axis([0 2 min(tx_signal_1) max(tx_signal_1)]);
    grid on;
    hold on;
    %pause
end
hold off;

%En la siguiente figura se grafica la PSD para diferentes valores de
%roll-off (0 0.5 0.7 1)

figure(300)
pwelch(tx_signal, L*8, [], 2048, 16);
axis([0 1 -10 15])
legend('\alpha = 0', '\alpha = 0.5', '\alpha = 0.7', '\alpha = 1');
hold on


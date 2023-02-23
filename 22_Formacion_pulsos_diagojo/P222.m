%tx_sig_gen.m
clear all;
close all;
rand(1,1668);     % Cambie los ultimos 3 digitos por los ultimos 3 numeros de su carne.
Ts = 1;           % Duración del símbolo
L  = 16;          % Número de muestras por símbolo
t_step = Ts/L;    % Tamaño del paso para muestreo, es correcto ya que divide el tiempo total del símbolo entre la cantidad de muestras
                  %dando el tiempo entre muestras

%%%%%%%%%<1. Generacion de onda del pulso > %%%%%%%%%%%%%%%%%%%%%%
pt = rcosdesign(0.25,6,L,'normal');   % Genera los puntos del coseno alzado con factor de rodamiento de 0.25, 6 tiempos de símbolo
                                      % y 100 muestras por símbolo

%%%%%%%%%<2. Generacion de 100 simbolos binarios >%%%%%%%%%%%%%%%%%%%%
Ns = 100;                                 % Numero de muestras
data_bit = (rand(1,Ns)>0.5);              % Está correcto ya que se genera un vector de dimensión Ns y convierte a valores booleanos

%%%%%%%%%<3. Unipolar a Bipolar (modulacion de amplitud)>%%%%%%%%%%%%%%
amp_modulated = 2*data_bit-1; % 0=> -1,  1=>1

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
function vec = toUAVFrame(pan, tilt, distance)
clc;
syms ct st cp sp d

disp('Frame 0 - Measurement');
vec_init = [0; 0; distance; 1]

disp('Frame 1 - Offsets to servo');
T_0TO1 = [1, 0, 0, 0.5; 0, 1, 0, 0; 0, 0, 1, 2.1;0 ,0 ,0, 1];
vec = T_0TO1 * vec_init;

disp('Frame 2 - Change orientation');
T_1TO2 = [1 0 0 0; 0 0 1 0; 0 -1 0 0; 0 0 0 1];
vec = T_1TO2 * vec;

disp('Frame 3 - Reverse tilt');
T_2TO3 = [cosd(tilt) sind(tilt) 0 0; -sind(tilt) cosd(tilt) 0 0 ; 0 0 1 0;0 0 0 1];
vec = T_2TO3 * vec;

disp('Frame 4 - Offsets to servo');
T_3TO4 = [1 0 0 3.5; 0 1 0 2.5; 0 0 1 0;0 0 0 1];
vec = T_3TO4 * vec;

disp('Frame 5 - To NED coordinates');
T_4TO5 = [0 1 0 0; 0 0 1 0; -1 0 0 0 ;0 0 0 1];
vec = T_4TO5 * vec;

disp('Frame 6 - Reverse pan');
T_5TO6 = [cosd(pan) -sind(pan) 0 0; sind(pan) cosd(pan) 0 0; 0 0 1 0; 0 0 0 1];
vec = T_5TO6 * vec

disp('Testing total rotation');
vec_init = [0;0;d;1]
T1 = T_1TO2 * T_0TO1
Ttilt = [ct st 0 0; -st ct 0 0 ; 0 0 1 0;0 0 0 1]
T2 = T_4TO5 * T_3TO4
Tpan = [cp -sp 0 0; sp cp 0 0; 0 0 1 0; 0 0 0 1]
vec = Tpan * T2 * Ttilt * T1 * vec_init
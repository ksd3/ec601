

#include <string>
#include <map>
#include <iostream>
#include <cmath>
#include <array>
#include <fstream>
#include "integrator.h"


enum StringValue { notdefined, String1, String2, String3};

static std::map<std::string, StringValue> s_mapStringValues;

void Initialize(){
  s_mapStringValues["euler"] = String1;
  s_mapStringValues["rk4"] = String2;
  s_mapStringValues["leapfrog"] = String3;
}

static constexpr int K_CONST = 5000;
static constexpr double L0 = 10; 
static constexpr int DIM = 4;
static constexpr double G = 10;
static constexpr int N_BODIES = 3;
static constexpr int N_STEPS = 5000; //CHANGE TO MODIFY RK4 STEPS!



double distance(std::array<double, 3> r1, std::array<double, 3> r2){
    return sqrt(pow(r1[0]-r2[0],2)+pow(r1[1]-r2[1],2)+pow(r1[2]-r2[2],2));
}


class Star{
public:

    double m;
    double r;
    std::array <double, 3> x;
    std::array <double, 3> v;
    std::array <double, 3> a;
    double energy;
    double omega;
    
    Star (double mass, double x_position, double y_position, double z_position, double x_velocity, double y_velocity, double z_velocity, double radius) {
        m = mass;
        r = radius;
		x[0] = x_position;
		x[1] = y_position;
        x[2] = z_position;
		v[0] = x_velocity;
        v[1] = y_velocity;
        v[2] = z_velocity;
    };
    void computeKineticEnergy(){
        energy = 0.5 * m * (pow(v[0],2)+pow(v[1],2)+pow(v[2],2));
    }
    
    void computeOmega(){
        omega = sqrt(K_CONST / m);
    }
};

std::array<double, 3> differenceOfArrays(std::array<double, 3>  v1, std::array<double, 3> v2){
    std::array<double, 3> difference;
    for(int j=0;j<3;j++){
        difference[j] = v1[j]-v2[j];
    }
    return difference;
}

double computePotentialEnergy(Star star1, Star star2, Star star3){
    return -1 * G * ( star3.m * star1.m / distance(star3.x, star1.x) +  star3.m * star2.m / distance(star3.x, star2.x) + star1.m * star2.m / distance(star1.x, star2.x));
        
}
std::array<double, 3> computeCM(Star star1, Star star2, Star star3){
    std::array<double, 3> cm;
    for(int j=0;j<DIM-1;j++){
        cm[j] = (star1.m * star1.x[j] + star2.m * star2.x[j] + star3.m * star3.x[j]) / (star1.m + star2.m + star3.m);
    }
    return cm;
}

std::array<double, 3> AngularMomentum(std::array<double, 3> cm, Star star){
    std::array<double, 3> L;
    std::array<double, 3> difference;
    difference = differenceOfArrays(cm, star.x);
    L[0] = star.m * (difference[1] * star.v[2] - difference[2] * star.v[1]);
    L[1] = star.m * (difference[2] * star.v[0] - difference[0] * star.v[2]);
    L[2] = star.m * (difference[0] * star.v[1] - difference[1] * star.v[0]);
    return L;
}



double C_spring(double x, double v, double t, Star A, Star B, Star C, int axe){
    return (-1 * (G * (A.m * (C.x[axe]-A.x[axe]) / pow(distance(A.x, C.x), 3) + B.m * (C.x[axe]-B.x[axe]) / pow(distance(B.x, C.x), 3))) - (K_CONST / C.m) * (std::abs(distance(B.x, C.x))-L0) * (C.x[axe]-B.x[axe]) / (distance(B.x, C.x)));
}

double B_Spring(double x, double v, double t, Star A, Star B, Star C, int axe){
    return (-1 * (G * (A.m * (C.x[axe]-A.x[axe]) / pow(distance(A.x, C.x), 3) + B.m * (C.x[axe]-B.x[axe]) / pow(distance(B.x, C.x), 3))) - (K_CONST / C.m) * (std::abs(distance(A.x, C.x))-L0) * (C.x[axe]-A.x[axe]) / (distance(A.x, C.x)));
}

double acceleration(double x, double v, double t, Star A, Star B, Star C, int axe){
    return (-1 * G * (A.m * (C.x[axe]-A.x[axe]) / pow(distance(A.x, C.x), 3) + B.m * (C.x[axe]-B.x[axe]) / pow(distance(B.x, C.x), 3)));
}

int main(int argc, char** argv){
    
    double h = 0.002;

//Star Starname(Mass,xposition,yposition,zposition,xvel,yvel,zvel,radius)
    //CONFIG SET YOUR STUFF HERE!!!
     Star A(1000, -100, 0, 0, 0, 0, 0,0);
     Star B(6.12, 0, 0, 31.24, 65, 0, 0,1.8);
     Star C(5.34,1,2,3,-65,2,0, 1.1);

    double x_A[DIM][3];
    double x_B[DIM][3];
    double x_C[DIM][3];

    double mass_A = A.m;
    double mass_B = B.m;
    double mass_C = C.m;

    double radius_A=A.r;
    double radius_B=B.r;
    double radius_C=C.r;

    x_A[0][0] = A.x[0];
    x_B[0][0] = B.x[0];
    x_C[0][0] = C.x[0];

    x_A[1][0] = A.x[1];
    x_B[1][0] = B.x[1];
    x_C[1][0] = C.x[1];

    x_A[2][0] = A.x[2];
    x_B[2][0] = B.x[2];
    x_C[2][0] = C.x[2];

    Initialize();
   
    std::ofstream file_energy("totalenergy_" + std::string(argv[1]) + ".csv");
    std::ofstream output_file_A("apositions" + std::string(argv[1]) + ".csv");
    std::ofstream output_file_B("bpositions" + std::string(argv[1]) + ".csv");
    std::ofstream output_file_C("cpositions" + std::string(argv[1]) + ".csv");
    std::ofstream file_angmom("angularmomentum" + std::string(argv[1]) + ".csv");

    output_file_A<<"x;y;z;r"<<std::endl;
    output_file_B<<"x;y;z;r"<<std::endl;
    output_file_C<<"x;y;z;r"<<std::endl;
    file_energy<<"k;p"<<std::endl;
    file_angmom<<"Lx;Ly;Lz"<<std::endl;

    double m1[4][4];
    double k1[4][4];
    double m2[4][4];
    double k2[4][4];
    double m3[4][4];
    double k3[4][4];
    double m4[4][4];
    double k4[4][4];

    //initial velocity conditions
    
    std::array<double,3> vA = A.v; 
    std::array<double,3> xA = A.x;
    std::array<double,3> vB = B.v;
    std::array<double,3> xB = B.x;
    std::array<double,3> vC = C.v; 
    std::array<double,3> xC = C.x;
    double t;
    std::array<double,3> cm = computeCM(A, B, C);

    if (argc>=2){
        switch (s_mapStringValues[argv[1]]){
            case String1: 
                //euler method
                for (int i=0; i<N_STEPS-1; i++){
                    output_file_A << A.x[0] << ";" << A.x[1] << ";" << A.x[2]<< std::endl;
                    output_file_B << B.x[0] << ";" << B.x[1] << ";" << B.x[2]<< std::endl;
                    output_file_C << C.x[0] << ";" << C.x[1] << ";" << C.x[2]<< std::endl;
                    for(int j=0; j<DIM-1; j++){

                        A.a[j] = acceleration(0, 0, 0, B, C, A, j);
                        B.a[j] = acceleration(0, 0, 0, A, C, B, j);
                        C.a[j] = acceleration(0, 0, 0, B, A, C, j);
                    }
                    for(int j=0; j<DIM-1; j++){
                        
                        A.v[j] += A.a[j] * h;
                        B.v[j] += B.a[j] * h;
                        C.v[j] += C.a[j] * h;
                        
                        A.x[j] += A.v[j] * h;
                        B.x[j] += B.v[j] * h;
                        C.x[j] += C.v[j] * h;
                        
                    } 
                    
                    A.computeKineticEnergy();
                    B.computeKineticEnergy();
                    C.computeKineticEnergy();
                    cm = computeCM(A,B,C);
                    file_energy<<A.energy + B.energy + C.energy<<";"<< computePotentialEnergy(A, B, C)<<std::endl;
                    file_angmom<<AngularMomentum(cm, A)[0]+ AngularMomentum(cm, B)[0]+AngularMomentum(cm, C)[0]<<";"<< AngularMomentum(cm, A)[1]+ AngularMomentum(cm, B)[1]+AngularMomentum(cm, C)[1]<<";"<<AngularMomentum(cm, A)[2]+ AngularMomentum(cm, B)[2]+AngularMomentum(cm, C)[2]<<std::endl;
                }
                
                break;
            case String2:{
                //rk4 method
                h *= 4;
                
                for(int i=0; i<N_STEPS/4-1; i++){
                    vA = A.v;
                    xA = A.x;
                    vB = B.v;
                    xB = B.x;
                    vC = C.v;
                    xC = C.x;
                    for(int j=0; j<DIM-1; j++){
                        m1[0][j] = h * vA[j];
                        k1[0][j] = h * acceleration(xA[j], vA[j], t, C, B, A, j);
                        m1[1][j] = h * vB[j];
                        k1[1][j] = h * B_Spring(xB[j], vB[j], t, C, A, B, j); 
                        m1[2][j] = h * vC[j];
                        k1[2][j] = h * C_spring(xC[j], vC[j], t, A, B, C, j); 
                    }
                    for(int j=0; j<DIM-1;j++){
                        A.v[j] = vA[j] + 0.5 * k1[0][j];
                        B.v[j] = vB[j] + 0.5 * k1[1][j];
                        C.v[j] = vC[j] + 0.5 * k1[2][j];          
                        A.x[j] = xA[j] + 0.5 * m1[0][j];
                        B.x[j] = xB[j] + 0.5 * m1[1][j];
                        C.x[j] = xC[j] + 0.5 * m1[2][j];
                    }
                    for(int j=0; j<DIM-1; j++){
                        m2[0][j] = h * A.v[j];
                        k2[0][j] = h * acceleration(A.x[j], A.v[j], t+0.5*h, C, B, A, j);
                        m2[1][j] = h * B.v[j];
                        k2[1][j] = h * B_Spring(B.x[j], B.v[j], t+0.5*h, C, A, B, j);
                        m2[2][j] = h * C.v[j];
                        k2[2][j] = h * C_spring(C.x[j], C.v[j], t+0.5*h, A, B, C, j);
                    }
                     for(int j=0; j<DIM-1;j++){
                        A.v[j] = vA[j] + 0.5 * k2[0][j];
                        B.v[j] = vB[j] + 0.5 * k2[1][j];
                        C.v[j] = vC[j] + 0.5 * k2[2][j];          
                        A.x[j] = xA[j] + 0.5 * m2[0][j];
                        B.x[j] = xB[j] + 0.5 * m2[1][j];
                        C.x[j] = xC[j] + 0.5 * m2[2][j];
                    }
                    for(int j=0; j<DIM-1; j++){
                        m3[0][j] = h * A.v[j];
                        k3[0][j] = h * acceleration(A.x[j], A.v[j], t+0.5*h, C, B, A, j);
                       
                        m3[1][j] = h * B.v[j];
                        k3[1][j] = h * B_Spring(B.x[j], B.v[j], t+0.5*h, C, A, B, j);
                        m3[2][j] = h * C.v[j];
                        k3[2][j] = h * C_spring(C.x[j], C.v[j], t+0.5*h, A, B, C, j);
                    }
                     for(int j=0; j<DIM-1;j++){
                        A.v[j] = vA[j] + k3[0][j];
                        B.v[j] = vB[j] + k3[1][j];
                        C.v[j] = vC[j] + k3[2][j];          
                        A.x[j] = xA[j] + m3[0][j];
                        B.x[j] = xB[j] + m3[1][j];
                        C.x[j] = xC[j] + m3[2][j];
                    }
                    for(int j=0; j<DIM-1; j++){
                        m4[0][j] = h * A.v[j];
                        k4[0][j] = h * acceleration(A.x[j], A.v[j], t + h, C, B, A, j);
                        m4[1][j] = h * B.v[j];
                        k4[1][j] = h * B_Spring(B.x[j], B.v[j], t + h, C, A, B, j);
                        m4[2][j] = h * C.v[j];
                        k4[2][j] = h * C_spring(C.x[j], C.v[j], t + h, A, B, C, j);
                    }

                    for(int j=0; j<DIM-1;j++){
                        A.v[j] = vA[j] + (k1[0][j] + 2*k2[0][j] + 2*k3[0][j] + k4[0][j])/6;
                        B.v[j] = vB[j] + (k1[1][j] + 2*k2[1][j] + 2*k3[1][j] + k4[1][j])/6;
                        C.v[j] = vC[j] + (k1[2][j] + 2*k2[2][j] + 2*k3[2][j] + k4[2][j])/6;          
                        A.x[j] = xA[j] + (m1[0][j] + 2*m2[0][j] + 2*m3[0][j] + m4[0][j])/6;
                        B.x[j] = xB[j] + (m1[1][j] + 2*m2[1][j] + 2*m3[1][j] + m4[1][j])/6;
                        C.x[j] = xC[j] + (m1[2][j] + 2*m2[2][j] + 2*m3[2][j] + m4[2][j])/6;
                    }

                    output_file_A << A.x[0] << ";" << A.x[1] << ";" << A.x[2]<<";" <<radius_A<< std::endl;
                    output_file_B << B.x[0] << ";" << B.x[1] << ";" << B.x[2]<<";"<< radius_B<< std::endl;
                    output_file_C << C.x[0] << ";" << C.x[1] << ";" << C.x[2]<< ";"<<radius_C<<std::endl;
                    A.computeKineticEnergy();
                    B.computeKineticEnergy();
                    C.computeKineticEnergy();
                    file_energy<<A.energy + B.energy + C.energy <<";"<< computePotentialEnergy(A, B, C)<<std::endl;
                    cm=computeCM(A, B, C);
                    file_angmom<<AngularMomentum(cm, A)[0]+ AngularMomentum(cm, B)[0]+AngularMomentum(cm, C)[0]<<";"<< AngularMomentum(cm, A)[1]+ AngularMomentum(cm, B)[1]+AngularMomentum(cm, C)[1]<<";"<<AngularMomentum(cm, A)[2]+ AngularMomentum(cm, B)[2]+AngularMomentum(cm, C)[2]<<std::endl;
                }
                }
                break;
            case String3:
                //leapfrog
            
                for (int i=0; i<N_STEPS-1; i++){
                    output_file_A << A.x[0] << ";" << A.x[1] << ";" << A.x[2]<< std::endl;
                    output_file_B << B.x[0] << ";" << B.x[1] << ";" << B.x[2]<< std::endl;
                    output_file_C << C.x[0] << ";" << C.x[1] << ";" << C.x[2]<< std::endl;

                    for(int j=0; j<DIM-1; j++){
                        A.x[j] += A.v[j] * h / 2;
                        B.x[j] += B.v[j] * h / 2;
                        C.x[j] += C.v[j] * h / 2;
                    }
                    
                    for(int j=0; j<DIM-1; j++){
                        A.a[j] = acceleration(0, 0, 0, B, C, A, j);
                        B.a[j] = acceleration(0, 0, 0, A, C, B, j);
                        C.a[j] = acceleration(0, 0, 0, B, A, C, j);

                        A.v[j] += A.a[j] * h;
                        B.v[j] += B.a[j] * h;
                        C.v[j] += C.a[j] * h;

                    } 
                    for(int j=0; j<DIM-1; j++){

                        A.x[j] += A.v[j] * h / 2;
                        B.x[j] += B.v[j] * h / 2;
                        C.x[j] += C.v[j] * h / 2;
                    }
        
                    A.computeKineticEnergy();
                    B.computeKineticEnergy();
                    C.computeKineticEnergy();
                    cm = computeCM(A,B,C);
                    file_energy<<A.energy + B.energy + C.energy<<";"<< computePotentialEnergy(A, B, C)<<std::endl;
                    file_angmom<<AngularMomentum(cm, A)[0]+ AngularMomentum(cm, B)[0]+AngularMomentum(cm, C)[0]<<";"<< AngularMomentum(cm, A)[1]+ AngularMomentum(cm, B)[1]+AngularMomentum(cm, C)[1]<<";"<<AngularMomentum(cm, A)[2]+ AngularMomentum(cm, B)[2]+AngularMomentum(cm, C)[2]<<std::endl;
                }

            break;
            default:
                std::cout<<"euler, rk4, or leapfrog?"<<std::endl;
                return 0;
        }
    }else{
        std::cout<<"euler, rk4, or leapfrog?"<<std::endl;
        return 0;
    }
    
//----------------------------------------------------------------  

    output_file_A.close();
    output_file_B.close(); 
    output_file_C.close();
    file_energy.close();

    #ifdef _WIN32
        std::string command ="python3.9 plotting.py " + std::string(argv[1]);
    #elif __APPLE__
        std::string command ="python3.11 plotting.py " + std::string(argv[1]);
    #endif
    FILE* pipe = popen(command.c_str(), "w");
    pclose(pipe);
   return 0;
}

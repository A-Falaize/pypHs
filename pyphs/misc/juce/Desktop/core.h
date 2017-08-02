/*
    Copyright or (c) or Copr. Project-Team S3 (Sound Signals and Systems) and
    Analysis/Synthesis team, Laboratory of Sciences and Technologies of Music and
    Sound (UMR 9912), IRCAM-CNRS-UPMC, 1 place Igor Stravinsky, F-75004 Paris
    * contributors : Antoine Falaize, Thomas Helie,
    * corresponding contributor: antoine.falaize@ircam.fr
    * date: 2016/12/31 12:47:34

    This has been geerated by Py which purpose is to generate C++
    code for the simulation of multiphysics system described by graph structures.

    This software is governed by the CeCILL-B license under French law and
    abiding by the rules of distribution of free software.  You can  use,
    modify and/ or redistribute the software under the terms of the CeCILL-B
    license as circulated by CEA, CNRS and INRIA at the following URL
    "http://www.cecill.info".

    As a counterpart to the access to the source code and  rights to copy,
    modify and redistribute granted by the license, users are provided only
    with a limited warranty  and the software's author,  the holder of the
    economic rights, and the successive licensors  have only  limited liability.

    In this respect, the user's attention is drawn to the risks associated
    with loading,  using,  modifying and/or developing or reproducing the
    software by the user in light of its specific status of free software,
    that may mean  that it is complicated to manipulate,  and  that  also
    therefore means  that it is reserved for developers  and  experienced
    professionals having in-depth computer knowledge. Users are therefore
    encouraged to load and test the software's suitability as regards their
    requirements in conditions enabling the security of their systems and/or
    data to be ensured and,  more generally, to use and operate it in the
    same conditions as regards security.

    The fact that you are presently reading this means that you have had
    knowledge of the CeCILL-B license and that you accept its terms.

    Created on 2016/12/31 12:47:34

    author: Antoine Falaize


===========================================================================

    This file was automatically generated by Py, date 2017/08/02 19:52:27.

    It contains the code for the simulation of system 'PHSCORE'.

===========================================================================
*/


#ifndef PHSCORE_H
#define PHSCORE_H

#include "iostream"
#include "vector"
#include "math.h"

# include "parameters.h"

#include </Users/afalaize/Developement/libs/eigen/Eigen/Dense>

using namespace std;
using namespace Eigen;

class PHSCORE {
//==========================================================================
// PUBLIC    
    public:
    //==========================================================================
    // Sample Rate
    void set_sampleRate(double &);
    //==========================================================================
    // Core update
    void update();
    //==========================================================================
    // Acessors to Arguments, return vector<double>
    vector<double> x_vector() const;
    vector<double> dx_vector() const;
    vector<double> w_vector() const;
    vector<double> u_vector() const;
    vector<double> p_vector() const;
    vector<double> vl_vector() const;
    vector<double> o_vector() const;
    //==========================================================================
    // Acessors to Arguments, return Matrix<double, n, m>
    Matrix<double, 2, 1> x() const;
    Matrix<double, 2, 1> dx() const;
    Matrix<double, 1, 1> w() const;
    Matrix<double, 1, 1> u() const;
    Matrix<double, 0, 0> p() const;
    Matrix<double, 3, 1> vl() const;
    Matrix<double, 0, 0> o() const;
    //==========================================================================
    // Mutators for Arguments, type = vector<double>
    void set_x(vector<double> &);
    void set_dx(vector<double> &);
    void set_w(vector<double> &);
    void set_u(vector<double> &);
    void set_p(vector<double> &);
    void set_vl(vector<double> &);
    void set_o(vector<double> &);
    //==========================================================================
    // Mutators for Arguments, type = Matrix<double, n, m>
    void set_x(Matrix<double, 2, 1> &);
    void set_dx(Matrix<double, 2, 1> &);
    void set_w(Matrix<double, 1, 1> &);
    void set_u(Matrix<double, 1, 1> &);
    void set_p(Matrix<double, 0, 0> &);
    void set_vl(Matrix<double, 3, 1> &);
    void set_o(Matrix<double, 0, 0> &);
    //==========================================================================
    // Mutators for Arguments, type is double with int index
    void set_x(double &, unsigned int &);
    void set_dx(double &, unsigned int &);
    void set_w(double &, unsigned int &);
    void set_u(double &, unsigned int &);
    void set_p(double &, unsigned int &);
    void set_vl(double &, unsigned int &);
    void set_o(double &, unsigned int &);
    //==========================================================================
    // Functions Results Accessors (matrix)
    Matrix<double, 0, 0> ud_o() const;
    Matrix<double, 3, 3> jactempFll() const;
    Matrix<double, 3, 1> Gl() const;
    Matrix<double, 2, 1> dxH() const;
    Matrix<double, 1, 1> z() const;
    Matrix<double, 1, 1> y() const;
    //==========================================================================
    // Functions Results Accessors (vector)
    vector<double> ud_o_vector() const;
    vector<double> jactempFll_vector() const;
    vector<double> Gl_vector() const;
    vector<double> dxH_vector() const;
    vector<double> z_vector() const;
    vector<double> y_vector() const;
    //==========================================================================
    // Functions Results Accessors (element)
    double ud_o(unsigned int &) const;
    double jactempFll(unsigned int &) const;
    double Gl(unsigned int &) const;
    double dxH(unsigned int &) const;
    double z(unsigned int &) const;
    double y(unsigned int &) const;
    //==========================================================================
    // Oprations Results Accessors
    Matrix<double, 2, 1> ud_x() const;
    Matrix<double, 3, 3> ijactempFll() const;
    Matrix<double, 3, 1> ud_vl() const;
    //==========================================================================
    // Oprations Results Accessors
    vector<double> ud_x_vector() const;
    vector<double> ud_vl_vector() const;
    //==========================================================================
    // Default Constructor
    PHSCORE();
    //==========================================================================
    // Default Destructor
    ~PHSCORE();

//==========================================================================
// PRIVATE    
    private:
    //==========================================================================
    // Sample Rate
    double sampleRate = 48000.0;
    const double * F_S = & sampleRate;
    //==========================================================================
    // Parameters
    const unsigned int indexParameters = 0;  // See file "parameters.cpp".
    const double * R = & subs[indexParameters][0];
    const double * L = & subs[indexParameters][1];
    const double * C = & subs[indexParameters][2];
    //==========================================================================
    // Arguments
    Matrix<double, 6, 1> args;
    double * xL = & args(0, 0);
    double * xC = & args(1, 0);
    double * dxL = & args(2, 0);
    double * dxC = & args(3, 0);
    double * wR = & args(4, 0);
    double * uin = & args(5, 0);
    //==========================================================================
    // Functions Results Definitions
    Matrix<double, 0, 0> _ud_o;
    Matrix<double, 3, 3> _jactempFll;
    Matrix<double, 3, 1> _Gl;
    Matrix<double, 2, 1> _dxH;
    Matrix<double, 1, 1> _z;
    Matrix<double, 1, 1> _y;
    //==========================================================================
    // Functions Results Updates
    void ud_o_update();
    void jactempFll_update();
    void Gl_update();
    void dxH_update();
    void z_update();
    void y_update();
    //==========================================================================
    // Operations Results Definition
    Matrix<double, 2, 1> _ud_x;
    Matrix<double, 3, 3> _ijactempFll;
    Matrix<double, 3, 1> _ud_vl;
    //==========================================================================
    // Oprations Results Updates
    void ud_x_update();
    void ijactempFll_update();
    void ud_vl_update();
    //==========================================================================
    // Initialization
    void init();
};

#endif /* PHSCORE_H */

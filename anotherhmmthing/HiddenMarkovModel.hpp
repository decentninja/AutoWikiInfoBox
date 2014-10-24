#ifndef HMM_H
#define HMM_H

#include "Matrix.hpp"
using namespace std;


class HMM {

public:

	typedef vector<double> Emission;
	typedef vector<int> Sequence;

	Matrix<> A;
	Matrix<> B;
	Matrix<> q;

	HMM() {}

	HMM(Matrix<> A, Matrix<> B, Matrix<> q) {
		this->A = A;
		this->B = B;
		this->q = q;
	}

	string str() {
		stringstream ss;
		ss << "A =\n" << A.str();
		ss << "\nB = \n" << B.str();
		ss << "\nq = \n" << q.str() << "\n";
		return ss.str();
	}

	Matrix<> nextemission() {
		return q * A * B;
	}

	int K() {
		return q.m();
	}

	static HMM readfromstdin() {
		Matrix<> A = Matrix<>::readfromstdin();
		Matrix<> B = Matrix<>::readfromstdin();
		Matrix<> q = Matrix<>::readfromstdin();
		return HMM(A, B, q);
	}

	static Emission stdinemission() {
		Emission v;
		int n;
		cin >> n;
		for(int j = 0; j < n; j++) {
			int cell;
			cin >> cell;
			v.push_back(cell);
		}
		return v;
	}

	string kattis() {
		stringstream ss;
		ss << A.kattis() << "\n";
		ss << B.kattis() << "\n";
		return ss.str();
	}

	double test(Sequence emission) {
		vector<double> last(K());
		for(int i = 0; i < K(); i++) {
			last[i] = q[0][i] * B[i][emission[0]];
		}
		for(int i = 1; i < emission.size(); i++) {
			vector<double> next(K());
			for(int k = 0; k < K(); k++) {
				double sum = 0;
				for(int j = 0; j < K(); j++) {
					sum += last[j] * A[j][k];
				}
				next[k] = sum * B[k][emission[i]];
			}
			last = next;
		}
		double chance = 0;
		for(int i = 0; i < last.size(); i++) {
			chance += last[i];
		}
		return chance;
	}

	Sequence viterbi(Emission emission) {
		// https://en.wikipedia.org/wiki/Viterbi_algorithm
		int T = emission.size();
		Matrix<> T_1(K(), T);
		Matrix<int> T_2(K(), T);
		for(int i = 0; i < K(); i++) {
			T_1[i][0] = q[0][i] * B[i][emission[0]];
			T_2[i][0] = 0;
		}
		for(int i = 1; i < T; i++) {
			for(int j = 0; j < K(); j++) {
				double max = -1;
				int argmax = -1;
				for(int k = 0; k < K(); k++) {
					double tmp = T_1[k][i - 1] * A[k][j] * B[j][emission[i]];
					if(tmp > max) {
						max = tmp;
						argmax = k;
					}
				}
				T_1[j][i] = max;
				T_2[j][i] = argmax;
			}
		}
		vector<int> Z(T);
		vector<int> X(T);
		double max = -1;
		for(int k = 0; k < K(); k++) {
			double tmp = T_1[k][T - 1];
			if(tmp > max) {
				max = tmp;
				Z[T - 1] = k;
			}
		}
		X[T - 1] = Z[T - 1];
		for(int i = T - 1; i > 0; i--) {
			Z[i - 1] = T_2[Z[i]][i];
			X[i - 1] = Z[i - 1];
		}
		return X;
	}

};

#endif
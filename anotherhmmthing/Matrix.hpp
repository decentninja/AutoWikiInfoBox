#ifndef Matrix_H
#define Matrix_H

#include <vector>
#include <sstream>
#include <iostream>
#include <assert.h>
using namespace std;


template <typename T = double>
class Matrix {
	vector<vector<T>> data;

public:

	Matrix() {}

	Matrix(int n, int m, T initial = 0) {
		for(int i = 0; i < n; i++) {
			vector<T> row;
			for(int j = 0; j < m; j++) {
				row.push_back(initial);
			}
			data.push_back(row);
		}
	}

	void scramble() {
		for(int i = 0; i < n(); i++) {
			double sum = 0;
			for(int j = 0; j < m(); j++) {
				data[i][j] = rand();
				sum += data[i][j];
			}
			for(int j = 0; j < m(); j++) {
				data[i][j] /= sum;
			}
		}
	}

	int n() {
		return data.size();
	}

	int m() {
		return data.at(0).size();
	}

	string str() {
		stringstream ss;
		for(int i = 0; i < n(); i++) {
			for(int j = 0; j < m(); j++) {
				ss << data[i][j] << " ";
			}
			ss << "\n";
		}
		return ss.str();
	}

	string kattis() {
		stringstream ss;
		ss << n() << " " << m() << " ";
		for(int i = 0; i < n(); i++) {
			for(int j = 0; j < m(); j++) {
				ss << data[i][j];
				if(!(i == n()-1 && j == m()-1)) {
					ss << " ";
				}
			}
		}
		return ss.str();
	}

	vector<T> &operator[](int i)
    {
        return data.at(i);
    }

    Matrix<T> operator*(Matrix other) {
    	assert(m() == other.n());
    	Matrix product(n(), other.m());
    	for(int i = 0; i < product.n(); i++) {
    		for(int j = 0; j < product.m(); j++) {
    			product[i][j] = 0;
    			for(int k = 0; k < other.n(); k++) {
    				product[i][j] += data[i][k] * other[k][j];
    			}
    		}
    	}
    	return product;
    }

	static Matrix<T> readfromstdin() {
		Matrix matrix;
		int n;
		int m;
		cin >> n;
		cin >> m;
		matrix.data = vector<vector<double>>();
		for(int i = 0; i < n; i++) {
			vector<double> row = vector<double>();
			for(int j = 0; j < m; j++) {
				double cell;
				cin >> cell;
				row.push_back(cell);
			}
			matrix.data.push_back(row);
		}
		return matrix;
	}
};

#endif
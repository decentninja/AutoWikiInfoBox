#include "HiddenMarkovModel.hpp"
using namespace std;

int main() {
	HMM model = HMM::readfromstdin();
	while(true) {
		HMM::Emission emission = HMM::stdinemission();
		HMM::Sequence r = model.viterbi(emission);
		cout << r[0];
		for(int i = 1; i < r.size(); i++) {
			cout << " " << r[i];
		}
		cout << endl;
	}
}
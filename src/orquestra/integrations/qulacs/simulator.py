import os

# It seems that qulacs has some conflict with pyquil, therefore it needs to be imported before zquantum.core.
import qulacs
import numpy as np
from qulacs.observable import create_observable_from_openfermion_text
from pyquil.wavefunction import Wavefunction
from zquantum.core.interfaces.backend import QuantumSimulator
from zquantum.core.circuit import save_circuit
from zquantum.core.measurement import (
    load_wavefunction,
    load_expectation_values,
    sample_from_wavefunction,
    ExpectationValues,
    Measurements,
    expectation_values_to_real,
)
from zquantum.core.measurement import (
    sample_from_wavefunction,
    expectation_values_to_real,
    ExpectationValues,
)
import openfermion
from .utils import convert_circuit_to_qulacs, qubitop_to_qulacspauli


class QulacsSimulator(QuantumSimulator):
    def __init__(self, n_samples=None):
        super().__init__(n_samples)

    def run_circuit_and_measure(self, circuit, **kwargs):
        """
        Run a circuit and measure a certain number of bitstrings

        Args:
            circuit (zquantum.core.circuit.Circuit): the circuit to prepare the state
            n_samples (int): the number of bitstrings to sample
        Returns:
            a list of bitstrings (a list of tuples)
        """
        wavefunction = self.get_wavefunction(circuit)
        bitstrings = sample_from_wavefunction(wavefunction, self.n_samples)
        return Measurements(bitstrings)

    def get_wavefunction(self, circuit):
        super().get_wavefunction(circuit)
        qulacs_state = self.get_qulacs_state_from_circuit(circuit)
        amplitudes = qulacs_state.get_vector()
        return Wavefunction(amplitudes)

    def get_qulacs_state_from_circuit(self, circuit):
        qulacs_circuit = convert_circuit_to_qulacs(circuit)
        num_qubits = len(circuit.qubits)
        qulacs_state = qulacs.QuantumState(num_qubits)
        qulacs_circuit.update_quantum_state(qulacs_state)
        return qulacs_state

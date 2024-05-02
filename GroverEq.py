
"""
15 变元的布尔方程
eq_per_group = [[0,1,2,3,4], [5,6,7,8], [9,10,11], [12,13], [14]]

"""
from qiskit import *
import numpy as np
from math import pi
from qiskit.visualization import plot_state_city, plot_state_hinton,plot_state_qsphere, plot_bloch_multivector

class GroverEq:

    def __init__(self, num_variable, eq_set, eq_value, eq_per_group):
        self.eq_set = eq_set
        self.eq_value = eq_value
        self.num_variable = num_variable
        self.num_equation = len(self.eq_set)
        self.eq_per_group = eq_per_group
        self.total_bit = num_variable + len(eq_per_group[0]) + 1
        self.circuit = None
        self.var_reg = None
        self.output_reg = None
        self.cbits = None
        self.num_qubits = num_variable
        self.num_ancillas = len(self.eq_per_group[0]) + 1
    
    def construct(self, cycles):
        """
        构建电路
        """
        num_ancillas = self.num_ancillas
        num_qubits = self.num_qubits
        self.var_reg = QuantumRegister(num_qubits, name='variable')
        self.anc_reg = AncillaRegister(num_ancillas, name='ancilla')
        self.output_reg = QuantumRegister(1, name='output')
        self.cbits = ClassicalRegister(num_qubits, name='cbits')
        self.circuit = QuantumCircuit(self.var_reg,self.anc_reg,self.cbits)

        # Initialise 'out0' in state |->
        # self.circuit.initialize([1, -1]/np.sqrt(2), self.output_reg)

        # Initialise qubits in state |s>
        self.circuit.h(self.var_reg)
        self.circuit.barrier() # for visual separation

        # Apply our oracle
        # cycles = int(((2**self.num_variable)**0.5)*pi/4)
        # cycles = 1
        for _ in range(cycles):
            # self.circuit.x(self.var_reg)
            self.black_box()
            self.inversion_about_average()
        self.circuit.barrier()
        self.circuit.measure(self.var_reg, self.cbits)


    def run(self, shots=100000):
        """
        运行电路
        """
        # backend = Aer.get_backend('qasm_simulator')
        # results = execute(self.circuit, backend=backend, shots=shots).result()
        # answer = results.get_counts()
        # return answer

        backend = Aer.get_backend('statevector_simulator')
        results = execute(self.circuit, backend=backend).result()
        fig_city = plot_state_city(results.get_statevector(self.circuit),figsize=(100,70))
        fig_qs = plot_state_qsphere(results.get_statevector(self.circuit))
        fig_bm = plot_bloch_multivector(results.get_statevector(self.circuit))
        fig_city.savefig('city.png')
        # backend = Aer.get_backend('statevector_simulator')
        # result = execute(self.circuit, backend).result()

        fig_qs.savefig('qsphere.png')
        fig_bm.savefig('bv.png')
    def draw_oracle(self, i):
        """
            功能：画电路的关键部分
        """
        anc_size = self.anc_reg.size
        groups = len(self.eq_per_group)
        groups_t = len(self.eq_per_group[groups-1])
        num = anc_size-i-1
        t1 = 0
        for eq_num in self.eq_per_group[i]:
            for term in self.eq_set[eq_num]:
                if type(term) == int:
                    self.circuit.cx(self.var_reg[term], self.anc_reg[t1])
                    
                elif type(term) == tuple:
                    self.circuit.ccx(self.var_reg[term[0]], self.var_reg[term[1]], self.anc_reg[t1])
            
            if self.eq_value[eq_num] == 0:
                self.circuit.x(self.anc_reg[t1])
            t1 += 1
        if i == groups-1:
            self.circuit.mcx(self.anc_reg[:groups_t], self.anc_reg[num])
        else:
            self.circuit.mcx(self.anc_reg[:num], self.anc_reg[num])

        t1 = 0
        for eq_num in self.eq_per_group[i]:
            for term in self.eq_set[eq_num]:
                if type(term) == int:
                    self.circuit.cx(self.var_reg[term], self.anc_reg[t1])
                elif type(term) == tuple:
                    self.circuit.ccx(self.var_reg[term[0]], self.var_reg[term[1]], self.anc_reg[t1])
            
            if self.eq_value[eq_num] == 0:
                self.circuit.x(self.anc_reg[t1])
            t1 += 1
        

    def black_box(self):
        """
            功能：oracle映射(黑盒)
        """
        groups = len(self.eq_per_group)
        anc_size = self.anc_reg.size

        for i in range(len(self.eq_per_group)):
            self.draw_oracle(i)
            self.circuit.barrier()
        self.circuit.mcp(pi, self.anc_reg[anc_size-groups:anc_size-1], self.anc_reg[anc_size-1])
        #self.circuit.mcx(self.anc_reg[anc_size-groups:anc_size], self.output_reg)

        for i in range(len(self.eq_per_group)-1,-1,-1): 
            self.draw_oracle(i)
            self.circuit.barrier()
        
    def inversion_about_average(self):
        """
            功能：振幅平均取反
        """
        register = self.var_reg
        # 变量寄存器的大小
        size = register.size
        self.circuit.h(register)
        self.circuit.barrier()
        self.circuit.x(register)
        self.circuit.h(register[size-1])
        
        self.circuit.mcx(register[:size-1], register[size-1])

        self.circuit.h(register[size-1])
        self.circuit.x(register)
        self.circuit.barrier()
        self.circuit.h(register)


    def draw(self, output=None):
        """
        画grover电路图
        """
        return self.circuit.draw(output)
        
#GROVER算法的实现
class Grover:

    def __init__(self, num_variable, eq_set, eq_value, eq_per_group):
        self.eq_set = eq_set
        self.eq_value = eq_value
        self.num_variable = num_variable
        self.eq_per_group = eq_per_group
        self.total_bit = num_variable + len(eq_per_group[0]) + 2
    

    def draw_circuit(self, circuit, qreg_q, i):
        """
            功能：画电路的关键部分
        """
        t1 = 0
        for j in self.eq_per_group[i]:
            for k in self.eq_set[j]:
                if type(k) == int:
                    circuit.cx(qreg_q[k], qreg_q[t1+self.num_variable])
                elif type(k) == tuple:
                    circuit.ccx(qreg_q[k[0]], qreg_q[k[1]], qreg_q[t1+self.num_variable])
            
            if self.eq_value[j] == 0:
                circuit.x(qreg_q[t1+self.num_variable])
            t1 += 1

        circuit.mcx(qreg_q[self.num_variable:self.num_variable+len(self.eq_per_group[i])],qreg_q[self.total_bit-i-2])

        t1 = 0
        for j in self.eq_per_group[i]:
            for k in self.eq_set[j]:
                if type(k) == int:
                    circuit.cx(qreg_q[k], qreg_q[t1+self.num_variable])
                elif type(k) == tuple:
                    circuit.ccx(qreg_q[k[0]], qreg_q[k[1]], qreg_q[t1+self.num_variable])
            
            if self.eq_value[j] == 0:
                circuit.x(qreg_q[t1+self.num_variable])
            t1 += 1
        circuit.barrier()

    def black_box(self, circuit, qreg_q):
        """
            功能：oracle映射(黑盒)
        """
        circuit.x(qreg_q[self.total_bit-1])
        circuit.h(qreg_q[self.total_bit-1])

        try:
            for i in range(len(self.eq_per_group)):
                self.draw_circuit(circuit, qreg_q, i)
        except:
            pass
                
        circuit.mcx(qreg_q[self.total_bit-len(self.eq_per_group)-1:self.total_bit-1] ,qreg_q[self.total_bit-1])

        circuit.h(qreg_q[self.total_bit-1])
        circuit.x(qreg_q[self.total_bit-1])

        try:
            for i in range(len(self.eq_per_group)-1,-1,-1): 
                self.draw_circuit(circuit, qreg_q, i)
        except:
            pass
        
        
    def inversion_about_average(self, circuit, qreg_q):
        """
            功能：振幅平均取反
        """
        circuit.h(qreg_q[:self.num_variable])
        circuit.barrier()
        circuit.x(qreg_q[:self.num_variable])
        circuit.h(qreg_q[self.num_variable-1])
        
        circuit.mct(qreg_q[:self.num_variable-1], qreg_q[self.num_variable-1])

        circuit.h(qreg_q[self.num_variable-1])
        circuit.x(qreg_q[:self.num_variable])
        circuit.barrier()
        circuit.h(qreg_q[:self.num_variable])
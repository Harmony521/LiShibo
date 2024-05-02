import time
# from math import pi
from Grover import Grover
from BoolEquations import BoolEquations
from qiskit import Aer, execute, QuantumRegister, ClassicalRegister, QuantumCircuit


def main():
    num_variable = int(input("请输入变元数量："))
    print("运行规模: {:d}变元".format(num_variable))
    equations = BoolEquations(num_variable)
    print("正在生成方程组中...")
    eq_set, eq_value = equations.run()

    equations.print_equations()
    print("正在经典算法求解中...")
    print("经典算法：")
    print(equations.result_set)

    eq_per_group = equations.split_integer()

    print("正在量子算法求解中...")
    time_start = time.time()
    grover = Grover(num_variable, eq_set, eq_value, eq_per_group)
    qreg_q = QuantumRegister(grover.total_bit, 'q')
    creg_c = ClassicalRegister(num_variable, 'c')
    circuit = QuantumCircuit(qreg_q, creg_c)

    # cycles = int(((2**num_variable)**0.5)/4*pi)
    cycles = 1
    circuit.h(qreg_q[:num_variable])
    for i in range(cycles):
        grover.black_box(circuit, qreg_q)
        grover.inversion_about_average(circuit, qreg_q)
    circuit.barrier()
    circuit.measure(qreg_q[:num_variable], creg_c[:num_variable])
    
    backend = Aer.get_backend('qasm_simulator')
    job = execute(circuit, backend, shots=5000000)
    
    
    result = job.result()
    counts = result.get_counts(circuit)
    print("量子算法：")
    print(sorted(counts.items(),key=lambda x:x[1],reverse=True)[0])
    print("量子电路深度为：%d" % circuit.depth())
    time_end = time.time()
    print('量子电路运行时间:%fs' % (time_end - time_start))
    # 需画图取消下行代码注释
    # circuit.draw("mpl")

if __name__ == '__main__':
    main()
    
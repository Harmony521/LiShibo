import random
from time import time
from multiprocessing import Process, Manager

class BoolEquations:
    """
        用法：布尔方程组生成和求解
    """

    def __init__(self, num_variable):
        self.num_variable = num_variable
        # 方程组
        self.eq_set = []
        # 方程式右边的值
        self.eq_value = [random.randint(0,1) for _ in range(num_variable)]
        self.result_set = Manager().list()

    def run(self):
        """
            功能：运行，得出最终方程组
        """
        self.random_equations()
        self.optimize()
        self.exhaustion()

        while len(self.result_set) != 1:
            while len(self.result_set) == 0:
                self.no_solution()
                self.exhaustion()
            while len(self.result_set) > 1:
                self.multiple_solutions()
                self.exhaustion()

        return self.eq_set, self.eq_value
    
    def run_other(self):
        """
            功能：运行非本程序生成的方程组
        """
        self.optimize()
        self.exhaustion()

        while len(self.result_set) != 1:
            while len(self.result_set) == 0:
                self.no_solution()
                self.exhaustion()
            while len(self.result_set) > 1:
                self.multiple_solutions()
                self.exhaustion()

        return self.eq_set, self.eq_value

    # ==============================
    # 生成方程组模块
    # random_equations()
    # ==============================
    def random_equations(self):
        '''
            功能：随机生成布尔方程组
            布尔方程组格式如下：
            x1 + x2 = 0
            x1 * x2 = 1
            eq_set = [[1, 2], [(1, 2)]]    内部列表[1, 2]表示x1 + x2, 元组(1, 2)表示x1 * x2
            eq_value = [0, 1]
        '''
        # 一个方程式最多有most_items项
        # most_items = int(self.num_variable*(self.num_variable+1)*0.5)
        # 生成一变元集合
        list_one = [i for i in range(self.num_variable)]
        # 生成二变元集合
        list_two = [(i, j) for i in range(self.num_variable) for j in range(i, self.num_variable)]
        # 所有元素列表
        list_all_elem = list_one + list_two

        #随机生成方程组
        for _ in range(self.num_variable):
            random.shuffle(list_all_elem)
            # 设置随机数种子
            random.seed(time())
            # m = random.randint(1,most_items)
            m = random.randint(1,self.num_variable)
            self.eq_set.append(list_all_elem[:m])


    # ==============================
    # 优化模块
    # optimize()
    #   --delete_none()
    #   --xx_to_x()
    #   --delete_same()
    #   --insertionSort()
    # ==============================
    def delete_none(self):
        '''
            功能：删除方程组中为空的方程
        '''
        for eq in self.eq_set:
            if len(eq) == 0:
                removed_index = self.eq_set.index(eq)
                self.eq_set.pop(removed_index)
                self.eq_value.pop(removed_index)

    def xx_to_x(self):
        """
            功能：优化x^2 -> x
        """
        for eq in self.eq_set:
            for j in range(len(eq)):
                if type(eq[j]) == tuple and eq[j][0] == eq[j][1]:
                    eq[j] = eq[j][0]

    def delete_same(self):
        """
            功能；删除重复项
            由于一个方程只能出现重复个数为2的项，所以仅需将重复项全删 1+1=0
        """

        delete_temp = [[] for _ in range(len(self.eq_set))]
        for i in range(len(self.eq_set)):
            for j in range(len(self.eq_set[i])):
                # 记录每个方程的重复元素，并保存到delete_temp
                if self.eq_set[i].count(self.eq_set[i][j]) > 1:
                    delete_temp[i].append(self.eq_set[i][j])
            # set集合 可以删除重复元素，保留一个 
            delete_temp[i] = list(set(delete_temp[i]))

            for term in delete_temp[i]:
                for _ in range(2):
                    self.eq_set[i].remove(term)
        
        # 删除方程组中为空的方程
        self.delete_none()

    def insertionSort(self):
        '''
        功能：利用直接插入排序按照方程长度排序方程组
        '''
        for i in range(len(self.eq_set)):
            preIndex = i-1
            current = self.eq_set[i]
            current_value = self.eq_value[i]
            while preIndex >= 0 and len(self.eq_set[preIndex]) > len(current):
                self.eq_set[preIndex+1] = self.eq_set[preIndex]
                self.eq_value[preIndex+1] = self.eq_value[preIndex]
                preIndex-=1
            self.eq_set[preIndex+1] = current
            self.eq_value[preIndex+1] = current_value

    def delete_included(self):
        '''
            功能：删除包含被包含方程的方程中被包含方程
        '''
        # 被包含方程
        for i in range(len(self.eq_set)):
            # 包含方程
            for j in range(len(self.eq_set)):
                in_bool = 0
                # 被包含方程与包含方程是同一个
                if i == j:
                    continue
                # 被包含方程是否被包含
                for term in self.eq_set[i]:
                    if term in self.eq_set[j]:
                        in_bool += 1
                
                # 如果被包含
                if in_bool == len(self.eq_set[i]):
                    if self.eq_value[i] == 0:
                        for term in self.eq_set[i]:
                            self.eq_set[j].remove(term)
                    elif self.eq_value[i] == 1:
                        if self.eq_value[j] == 0:
                            for term in self.eq_set[i]:
                                self.eq_set[j].remove(term)
                            self.eq_value[j] = 1
                        elif self.eq_value[j] == 1:
                            for term in self.eq_set[i]:
                                self.eq_set[j].remove(term)
                            self.eq_value[j] = 0
        self.delete_none()
        self.insertionSort()

    def optimize(self):
        '''
            功能：优化布尔方程组
        '''
        # 删除方程组中为空的方程
        self.delete_none()
        # 优化x^2 -> x
        self.xx_to_x()
        # 删除重复项
        self.delete_same()
        # 利用直接插入排序按照方程长度排序
        self.insertionSort()
        # 删除包含被包含方程的方程中被包含方程
        self.delete_included()


    # ==============================    
    # 暴力求解模块
    # exhaustion()
    # base_exhaustion()
    # ==============================
    def exhaustion(self):
        """
            功能：暴力破解布尔方程组
        """
        self.result_set = []
        test_answer = '0'*self.num_variable
        while test_answer != '1'+'0'*(self.num_variable):
            count = 0
            for j in range(len(self.eq_set)):
                temp = 0
                for term in self.eq_set[j]:
                    if type(term) == int:
                        temp += int(test_answer[term])
                    elif type(term) == tuple:
                        temp += int(test_answer[term[0]]) * int(test_answer[term[1]])
                if temp%2 == self.eq_value[j]:
                    count += 1
            if count == len(self.eq_set):
                self.result_set.append(test_answer[::-1])
            
            temp = int(test_answer, 2) + 1
            test_answer = str('{:0{}b}'.format(temp, self.num_variable))

    """
    def exhaustion(self):
        ""
            #功能：多进程暴力破解布尔方程组
        ""
        if self.num_variable < 10:
            test_answer = '0'*self.num_variable
            end = '1'+'0'*(self.num_variable)
            self.base_exhaustion(test_answer, end)
        else:
            num_list = []
            num = int((2**self.num_variable)/4)
            for i in range(4+1):
                num_list.append(str('{:0{}b}'.format(num*i, self.num_variable)))

            process = []
            for i in range(4):
                p = Process(target=self.base_exhaustion, args=(num_list[i],num_list[i+1],))
                process.append(p)
            [p.start() for p in process]
            [p.join()  for p in process]
    """

    # ==============================    
    # 无解/多解模块
    # no_solution()
    # multiple_solutions()
    #   get_one_eq()
    # ==============================
    def no_solution(self):
        '''
        功能: 处理无解情况
        '''
        eq_delete = [i for i in range(len(self.eq_set))]
        
        test_answer = '0'*self.num_variable
        while test_answer != '1'+'0'*self.num_variable:
            result_temp = []
            for j in range(len(self.eq_set)):
                temp1 = 0
                for term in self.eq_set[j]:
                    if type(term) == int:
                        temp1 += int(test_answer[term])
                    elif type(term) == tuple:
                        temp1 += int(test_answer[term[0]]) * int(test_answer[term[1]])
                if temp1%2 != self.eq_value[j]:
                    result_temp.append(j)
            if len(result_temp) < len(eq_delete):
                eq_delete = result_temp[:]
            
            temp2 = int(test_answer, 2) + 1
            test_answer = str('{:0{}b}'.format(temp2, self.num_variable))

        for i in eq_delete:
            self.eq_set.pop(i)
            self.eq_value.pop(i)

        self.optimize()

    def get_one_eq(self):
        one = [i for i in range(self.num_variable)]
        # 生成二变元集合
        two = [(i, j) for i in range(self.num_variable) for j in range(i+1, self.num_variable)]
        # 所有元素列表
        all_elem = one + two
        result_set = set(self.result_set)
        result_current = []
        while True:
            # most_items = int(self.num_variable*(self.num_variable+1)*0.5)
            n = random.randint(1, self.num_variable)
            random.shuffle(all_elem)
            eq_set_add = all_elem[:n]
            eq_value_add = random.randint(0,1)
            test_answer = '0'*self.num_variable
            while test_answer != '1'+'0'*self.num_variable:
                temp1 = 0
                for term in eq_set_add:
                    if type(term) == int:
                        temp1 += int(test_answer[term])
                    elif type(term) == tuple:
                        temp1 += int(test_answer[term[0]]) * int(test_answer[term[1]])
                if temp1%2 == eq_value_add:
                    result_current.append(test_answer[::-1])
                
                temp2 = int(test_answer, 2) + 1
                test_answer = str('{:0{}b}'.format(temp2, self.num_variable))

            result_temp = list(set(result_current).intersection(result_set))

            if len(result_temp) != 1:
                break
            
        return eq_set_add, eq_value_add

    def multiple_solutions(self):
        '''
        功能：处理方程组多解情况
        '''
        if len(self.eq_set) == self.num_variable:
            # 删除项最多的方程，即最后一个，因为方程组按照方程长度由小到大排列
            index_delete = len(self.eq_set)-1
            self.eq_set.pop(index_delete)
            self.eq_value.pop(index_delete)
            # 寻找具有唯一解的一个方程
            eq_set_add, eq_value_add = self.get_one_eq()
            self.eq_set.append(eq_set_add)
            self.eq_value.append(eq_value_add)

        elif len(self.eq_set) < self.num_variable:
            # 寻找具有相同解的一个方程
            eq_set_add, eq_value_add = self.get_one_eq()
            self.eq_set.append(eq_set_add)
            self.eq_value.append(eq_value_add)

        self.optimize()


    # ==============================
    # 其他功能模块
    # split_intege()
    # print_equations()
    # ==============================
    
    def split_integer(self):
        """
            功能：
        """
        max_num_group = 1
        num_per_group = []

        while max_num_group*(max_num_group+1) < 2*len(self.eq_set):
            max_num_group += 1

        while max_num_group > 0:
            num_per_group.append(max_num_group)
            max_num_group -= 1
            if sum(num_per_group) >= len(self.eq_set):
                break
        num_per_group[-1] -= sum(num_per_group) - len(self.eq_set)

        eq_per_group = []
        temp1, temp2 = 0, 0
        for i in range(len(num_per_group)):
            temp1 += num_per_group[i]
            eq_per_group.append(list(range(temp2,temp1)))
            temp2 = temp1
        return eq_per_group

    def print_equations(self):
        '''
            功能：打印方程组
        '''
        self.insertionSort()
        print("============方程组============")
        for i in range(len(self.eq_set)):
            print(self.eq_set[i], end='\n')
        print("============方程的值==========")
        print(self.eq_value)
        print("==============================")

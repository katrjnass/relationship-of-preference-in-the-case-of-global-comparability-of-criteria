import copy

with open('lab3tpr.txt') as f:  #зчитування матриці та інформацію про порівнюваність критеріїв з файлу lab3tpr.txt
    data = f.readlines()
    matrix = [list(map(int, row.split())) for row in data[:-2]]
    array_class = data.pop()
    array_k = data.pop()

array_k = list(map(int, array_k.replace('k', '').split('>')))
array_class = list(map(int, array_class.replace(' < ', ' ').replace('{', '').replace('}', '').replace(',', ' ').replace('k', '').split(' ')))

array_class_one = array_class[:4]
array_class_two = array_class[4:8]
array_class_three = array_class[8:]

len1 = len(matrix)
len2 = len(matrix[0])


def calculate_vector_figma(): #знаходимо вектори сігма
    matrix_vector_figm = []

    for i in range(len1):
        matrix_vector_figm.append([0] * len1)
        for j in range(len1):
            matrix_vector_figm[i][j] = [0] * len2

    for i in range(len1 - 1):
        for j in range(i + 1, len1):
            for k in range(len2):
                subtraction = matrix[i][k] - matrix[j][k]
                if subtraction > 0:
                    matrix_vector_figm[i][j][k] = 1
                    matrix_vector_figm[j][i][k] = -1
                elif subtraction == 0:
                    matrix_vector_figm[i][j][k] = matrix_vector_figm[j][i][k] = 0
                else:
                    matrix_vector_figm[i][j][k] = -1
                    matrix_vector_figm[j][i][k] = 1
    return matrix_vector_figm


def search_vidnoshenia_pareto(matrix_vector_figm):   #знаходимо відношення Парето
    vidnoshenia_pareto = [[0] * len(matrix_vector_figm) for _ in range(len(matrix_vector_figm))]
    for i in range(len(matrix_vector_figm)):
        for j in range(len(matrix_vector_figm[i])):
            counter = 0
            for k in matrix_vector_figm[i][j]:
                if k >= 0:
                    counter += 1
                if counter == len2:
                    vidnoshenia_pareto[i][j] = 1
                else:
                    vidnoshenia_pareto[i][j] = 0
    return vidnoshenia_pareto


def check_simetrichnist(array):   #перевіряємо матрицю на симетричність
    simetrichnist = False

    for i in range(len(array)):
        for j in range(len(array[0])):
            if array[i][j] == 1:
                if array[j][i] == 1:
                    simetrichnist = True
    return simetrichnist


def optimization_dominuvania(array):   #виконуємо оптимізацію за домінуванням
    simetrichnist = check_simetrichnist(array)

    len_row_array = len(array)
    len_cols_array = len(array[0])

    if not simetrichnist:
        mnoshyna_xp = []
        for p in range(len_row_array):
            counter = 0
            for l in range(len_cols_array):
                if array[p][l] == 1 and p != l:
                    counter += 1
            if counter == len_cols_array - 1:
                mnoshyna_xp.append(p + 1)
        if mnoshyna_xp:
            print("Елементи найбільші по P: ", mnoshyna_xp)
            return mnoshyna_xp
    else:
        mnoshyna_xr = []
        mnoshyna_xrr = []
        for p in range(len_row_array):
            counter = 0
            for l in range(len_cols_array):
                if array[p][l] == 1:
                    counter += 1
            if counter == len_cols_array:
                mnoshyna_xr.append(p + 1)
                counter = 0
                for n in range(len_row_array):
                    if array[n][p] == 0 and n != p:
                        counter += 1
                if counter == len_row_array - 1:
                    mnoshyna_xrr.append(p + 1)
        if mnoshyna_xr and mnoshyna_xrr:
            print("Елементи найбільші по R: ", mnoshyna_xr)
            print("Елементи строго найбільші по R: ", mnoshyna_xrr)
            return mnoshyna_xr, mnoshyna_xrr
        if mnoshyna_xr:
            print("Елементи найбільші по R: ", mnoshyna_xr)
            return mnoshyna_xr


def optimization_blokuvannya(array):   #виконуємо оптимізацію за блокуванням
    simetrichnist = check_simetrichnist(array)

    len_row_array = len(array)
    len_cols_array = len(array[0])

    if not simetrichnist:
        mnoshyna_x0p = []
        for i in range(len_cols_array):
            counter = 0
            for j in range(len_row_array):
                if array[j][i] == 0:
                    counter += 1
            if counter == len_row_array:
                mnoshyna_x0p.append(i + 1)
        if mnoshyna_x0p:
            print("Елементи максимальні по P:", mnoshyna_x0p)
            return mnoshyna_x0p
    else:
        mnoshyna_x0r = []
        mnoshyna_x00r = []
        for i in range(len_cols_array):
            counter = 0
            for j in range(len_row_array):
                if array[j][i] == 1:
                    if array[i][j] != 1:
                        counter = 0
                        break
                counter += 1
            if counter == len_row_array:
                mnoshyna_x0r.append(i + 1)
        counter = 0
        for i in range(len_cols_array):
            if counter == len_row_array:
                mnoshyna_x00r.append(i + 1)
            for j in range(len_row_array):
                if array[j][i] == 1 and j != i:
                    break
                counter += 1
        if mnoshyna_x00r and mnoshyna_x0r:
            print("Елементи максимальні по R: ", mnoshyna_x0r)
            print("Елементи строго максимальні по R: ", mnoshyna_x00r)
            return mnoshyna_x0r, mnoshyna_x00r
        if mnoshyna_x0r:
            print("Елементи максимальні по R:", mnoshyna_x0r)
            return mnoshyna_x0r


def search_mazhorytarne_vidnoshenia(matrix_vector_figm):    #знаходимо мажоритарне відношення
    mazhorytarne_vidnoshenia = [[0] * len(matrix_vector_figm) for _ in range(len(matrix_vector_figm))]
    for i in range(len(matrix_vector_figm)):
        for j in range(len(matrix_vector_figm[i])):
            counter = 0
            for k in matrix_vector_figm[i][j]:
                counter += k
            if counter > 0:
                mazhorytarne_vidnoshenia[i][j] = 1
            else:
                mazhorytarne_vidnoshenia[i][j] = 0
    return mazhorytarne_vidnoshenia


def print_matrix(array):  #вивід матриці на екран
    for i in range(len(array)):
        for j in range(len(array[0])):
            print(array[i][j], end=' ')
        print()


def define_optim_alternative(func, name_vidnoshenia):   #визначаємо оптимальну альтернативу
    print(f'{name_vidnoshenia}: ')
    print_matrix(func)
    if optimization_dominuvania(func) is not None:
        return
    else:
        optimization_blokuvannya(func)


def search_leksykographichne_vidnoshenia(matrix_vector_figm):   #знаходимо лексикографічне відношення
    leksykographichne_vidnoshenia = [[0] * len(matrix_vector_figm) for _ in range(len(matrix_vector_figm))]
    for i in range(len(matrix_vector_figm)):
        for j in range(len(matrix_vector_figm[i])):
            for l in array_k:
                if matrix_vector_figm[i][j][l - 1] == 1:
                    leksykographichne_vidnoshenia[i][j] = 1
                    break
                if matrix_vector_figm[i][j][l - 1] == -1:
                    break
    return leksykographichne_vidnoshenia


def build_system_vidnpareto(matrix_vector_figm, array_numclass):   #будуємо систему відношень Парето
    P0j = [[0] * len(matrix_vector_figm) for _ in range(len(matrix_vector_figm))]
    I0j = [[0] * len(matrix_vector_figm) for _ in range(len(matrix_vector_figm))]
    N0j = [[0] * len(matrix_vector_figm) for _ in range(len(matrix_vector_figm))]

    array_numclass = [i - 1 for i in array_numclass]

    for i in range(len(matrix_vector_figm)):
        for j in range(len(matrix_vector_figm)):
            exist_one = False
            exist_minus_one = False
            zero_counter = 0
            for l in range(len(matrix_vector_figm[j][i])):
                if l in array_numclass:
                    if matrix_vector_figm[j][i][l] == -1:
                        exist_minus_one = True
                    if matrix_vector_figm[j][i][l] == 1:
                        exist_one = True
                    if matrix_vector_figm[j][i][l] == 0:
                        zero_counter += 1
            if exist_one and not exist_minus_one:
                P0j[j][i] = 1
            if exist_minus_one and exist_one and zero_counter == 0:
                N0j[j][i] = 1
            if zero_counter == len(array_numclass):
                I0j[j][i] = 1
    return P0j, I0j, N0j


def build_vidnoshenia_berezovskogo(P0j, I0j, PBj_1, IBj_1, NBj_1):   #будуємо відношення Березовського
    PBj = [[0] * len(P0j) for _ in range(len(P0j))]
    IBj = [[0] * len(P0j) for _ in range(len(P0j))]
    NBj = [[0] * len(P0j) for _ in range(len(P0j))]

    for i in range(len(P0j)):
        for j in range(len(P0j[0])):
            if (P0j[i][j] and PBj_1[i][j]) or (P0j[i][j] and NBj_1[i][j]) or (P0j[i][j] and IBj_1[i][j]) or (I0j[i][j] and PBj_1[i][j]):
                PBj[i][j] = 1
            if I0j[i][j] and IBj_1[i][j]:
                IBj[i][j] = 1

    for i in range(len(P0j)):
        for j in range(len(P0j[0])):
            if not (PBj[i][j] or PBj[j][i] or IBj[i][j]):
                NBj[i][j] = 1
    return PBj, IBj, NBj


def search_vidnoshenia_podynovskogo():    #знаходимо відношення Подиновського
    matrix_vector_func = [[0] * len(matrix[0]) for _ in range(len(matrix))]
    arr_vidnoshenia_pareto = [[0] * len(matrix) for _ in range(len(matrix))]

    for i in range(len(matrix)):
        arr_row = []
        for j in range(len(matrix[0])):
            arr_row.append(matrix[i][j])
        arr_row.sort(reverse=True)
        for k in range(len(arr_row)):
            matrix_vector_func[i][k] = arr_row[k]

    for i in range(len(matrix_vector_func)):
        for l in range(len(matrix_vector_func)):
            counter = 0
            for j in range(len(matrix_vector_func[0])):
                if matrix_vector_func[i][j] >= matrix_vector_func[l][j]:
                    counter += 1
            if counter == len(matrix_vector_func[0]):
                arr_vidnoshenia_pareto[i][l] = 1
    arr_vidnoshenia_podynovskogo = copy.copy(arr_vidnoshenia_pareto)
    return arr_vidnoshenia_podynovskogo


arr_P01 = []
arr_I01 = []
arr_N01 = []
arr_P02 = []
arr_I02 = []
arr_N02 = []
arr_P03 = []
arr_I03 = []
arr_N03 = []
arr_PB2 = []
arr_IB2 = []
arr_NB2 = []
arr_PB3 = []
arr_IB3 = []
arr_NB3 = []

define_optim_alternative(search_vidnoshenia_pareto(calculate_vector_figma()), "Відношення Парето")
define_optim_alternative(search_mazhorytarne_vidnoshenia(calculate_vector_figma()), "Мажоритарне відношення")
define_optim_alternative(search_leksykographichne_vidnoshenia(calculate_vector_figma()), "Лексикографічне відношення")

arr_P01, arr_I01, arr_N01 = build_system_vidnpareto(calculate_vector_figma(), array_class_one)
arr_P02, arr_I02, arr_N02 = build_system_vidnpareto(calculate_vector_figma(), array_class_two)
arr_P03, arr_I03, arr_N03 = build_system_vidnpareto(calculate_vector_figma(), array_class_three)

arr_PB2, arr_IB2, arr_NB2 = build_vidnoshenia_berezovskogo(arr_P02, arr_I02, arr_P01, arr_I01, arr_N01)
arr_PB3, arr_IB3, arr_NB3 = build_vidnoshenia_berezovskogo(arr_P03, arr_I03, arr_PB2, arr_IB2, arr_NB2)

define_optim_alternative(arr_PB3, "Відношення Березовського PB")
define_optim_alternative(search_vidnoshenia_podynovskogo(), "Відношення Подиновського")

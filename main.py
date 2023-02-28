from numpy.polynomial import Polynomial
import numpy as np
import random

n = 256
k = 2
q = 3329
eta1 = 3
eta2 = 2


def gen_s():
    s = []
    for _ in range(2):
        s_coefs = [random.randint(-eta1,eta1) % 17 for _ in range(4)]
        s_coefs.insert(0,0)
        s.append(Polynomial(s_coefs))
    return s

def gen_e():
    e = []
    for _ in range(2):
        e_coefs = [random.randint(-eta1,eta1) for _ in range(4)]
        e_coefs.insert(0,0)
        e.append(Polynomial(e_coefs))
    return e

def gen_matrix_A():
    A = [[],[]]
    for i in range(2):
        for _ in range(2):
            coefs = [random.randint(0,16) for _ in range(4)]
            coefs.insert(0,0)
            poly = Polynomial(coefs)
            A[i].append(poly)
    return A

def gen_t(matrix_A, matrix_s, matrix_e):
    product_As = []
    matrix_t = []
    for i in range(2):
        poly_a = matrix_A[i][0]
        poly_a1 = matrix_A[i][0]
        poly_s = matrix_s[0]
        poly_s1 = matrix_s[1]

        first_product = np.polymul(poly_a, poly_s)
        second_product = np.polymul(poly_a1, poly_s1)

        added_products = np.polyadd(first_product, second_product)
        product_As.append(added_products)

        As_add_e = np.polyadd(product_As[i], matrix_e[i])
        matrix_t.append(As_add_e[0])
    return matrix_t


def gen_m_bar(in_str):
    bitstr = ''.join(format(ord(i), '08b') for i in in_str) 
    scaled_coefs = [int(i)*8 for i in bitstr]
    m_bar = Polynomial(scaled_coefs)
    return m_bar


def encrypt(pk, m_bar):
    e1 = []
    e2 = []
    for _ in range(2):
        e1_coefs = [random.randint(-eta1,eta1) % 17 for _ in range(4)]
        e2_coefs = [random.randint(-eta2,eta2) % 17 for _ in range(4)]
        e1_coefs.insert(0,0)
        e2_coefs.insert(0,0)
        e1.append(Polynomial(e1_coefs))
        e2.append(Polynomial(e2_coefs))

    e3 = [random.randint(-eta2,eta2) % 17 for _ in range(4)]
    e3 = Polynomial(e3)


    def gen_u():
        matrix_u = []
        product_Ae1 = []
        matrix_A = pk[0]
        for i in range(2):
            poly_a = matrix_A[i][0]
            poly_a1 = matrix_A[i][0]
            poly_e1_0 = e1[0]
            poly_e1_1 = e1[1]

            first_product = np.polymul(poly_a, poly_e1_0)
            second_product = np.polymul(poly_a1, poly_e1_1)

            added_products = np.polyadd(first_product, second_product)
            product_Ae1.append(added_products)

            Ae1_add_e2 = np.polyadd(product_Ae1[i], e2[i])
            matrix_u.append(Ae1_add_e2[0])
        return matrix_u

    def gen_v():
        matrix_v = []
        product_te1 = []
        matrix_t = pk[1]
        for i in range(2):
            poly_t = matrix_t[i]
            poly_t1 = matrix_t[i]
            poly_e1_0 = e1[0]
            poly_e1_1 = e1[1]

            first_product = np.polymul(poly_t, poly_e1_0)
            second_product = np.polymul(poly_t1, poly_e1_1)

            added_products = np.polyadd(first_product, second_product)
            product_te1.append(added_products)

        #    matrix_v.append(te1_add_e2_m[0])
        #x = np.polyadd(product_te1[i], e3)
        #v = np.polyadd(product_te1[i], e3)
        return matrix_v

    u = gen_u()
    v = gen_v()
    cyphertext = {'u':u, 'v':v}
    return cyphertext


A = gen_matrix_A()
s = gen_s()
e = gen_e()
t = gen_t(A,s, e)
m_bar = gen_m_bar('hi there im mattyb')
pk = (A, t)

ctext = encrypt(pk, m_bar)
print(ctext)



import gmpy2
from itertools import product
import binascii

from Crypto.Util.number import *

"""

alpha = p' * q' - l

beta = l^2 * [(e * d - 1) / s] + q' * l + p' * l - p' * q' - alpha - l^2
i.e.:
beta = l^2 * {[(e * d - 1) / s] - 1} + l * (q' + p') - alpha - p' * q'

if l,s are correct:
    alpha = k * t
    beta = k * (p' - l) + t * (q' - l)

i.e:


"""


def alpha_from_pprime_qprime_l(pprime, qprime, l):
    return pprime*qprime - l

def beta_from_pprime_qprime_e_d_l_s_alpha(pprime, qprime, e, d, l, s, alpha):
    temp1 = e*d - 1
    assert temp1 % s == 0
    temp2 = ((temp1 // s) - 1) * l * l
    temp3 = temp2 + l * (pprime + qprime)
    return temp3 - alpha - (pprime*qprime)

def k_t_from_pprime_qprime_l_alpha_beta(pprime, qprime, l, alpha, beta):
    a = pprime - l
    b = -beta
    c = alpha * (qprime - l)
    disc = b * b - 4 * a * c
    assert gmpy2.is_square(disc)
    temp = -b + gmpy2.isqrt(disc)
    assert temp % (2*a) == 0
    k = temp // (2*a) 
    assert alpha % k == 0
    return k, alpha // k

def brute_k_t_l(pprime, qprime, e, d):
    
   # l, s = 2, 2

    ss = [s for s in range(e - 100000, e + 1000000) if (e*d - 1) % s == 0]

    for l, s in product(range(1, 5000), ss):
        #print(f'l = {l}, s = {s}')
        try:
            alpha = alpha_from_pprime_qprime_l(pprime, qprime, l)
            beta = beta_from_pprime_qprime_e_d_l_s_alpha(pprime, qprime, e, d, l, s, alpha)
            k, t = k_t_from_pprime_qprime_l_alpha_beta(pprime, qprime, l, alpha, beta)
            return k, t, l

        except AssertionError:
            continue

if __name__ == "__main__":
    e = 1048583
    d = 20899585599499852848600179189763086698516108548228367107221738096450499101070075492197700491683249172909869748620431162381087017866603003080844372390109407618883775889949113518883655204495367156356586733638609604914325927159037673858380872827051492954190012228501796895529660404878822550757780926433386946425164501187561418082866346427628551763297010068329425460680225523270632454412376673863754258135691783420342075219153761633410012733450586771838248239221434791288928709490210661095249658730871114233033907339401132548352479119599592161475582267434069666373923164546185334225821332964035123667137917080001159691927
    pprime = 138356012157150927033117814862941924437637775040379746970778376921933744927520585574595823734209547857047013402623714044512594300691782086053475259157899010363944831564630625623351267412232071416191142966170634950729938561841853176635423819365023039470901382901261884795304947251115006930995163847675576699331
    qprime = 22886390627173202444468626406642274959028635116543626995297684671305848436910064602418012808595951325519844918478912090039470530649857775854959462500919029371215000179065185673136642143061689849338228110909931445119687113803523924040922470616407096745128917352037282612768345609735657018628096338779732460743
    k, t, l = brute_k_t_l(pprime, qprime, e, d)

    lp, lq = qprime + k, pprime + t
    assert lp % l == 0, lq % l == 0
    p, q = lp // l, lq // l
    
    assert gmpy2.invert(p, q) == pprime, gmpy2.invert(q, p) == qprime
    assert gmpy2.is_prime(p), gmpy2.is_prime(q)
    N = p*q

    flag = b'32074de818f2feeb788e36d7d3ee09f0000381584a72b2fba0dcc9a2ebe5fd79cf2d6fd40c4dbfea27d3489704f2c1a30b17a783baa67229d02043c5bc9bdb995ae984d80a96bd79370ea2c356f39f85a12d16983598c1fb772f9183441fea5dfeb5b26455df75de18ce70a6a9e9dbc0a4ca434ba94cf4d1e5347395cf7aafa756c8a5bd6fd166bc30245a4bded28f5baac38d024042a166369f7515e8b0c479a1965b5988b350064648738f6585c0a0d1463bd536d11a105bb926b44236593b5c6c71ef5b132cd9c211e8ad9131aa53ffde88f5b0df18e7c45bcdb6244edcaa8d386196d25297c259fca3be37f0f2015f40cb5423a918c51383390dfd5a8703'
    flag_num = bytes_to_long(binascii.unhexlify(flag))
    flag_decoded = pow(flag_num, d, N)
    print(long_to_bytes(flag_decoded))

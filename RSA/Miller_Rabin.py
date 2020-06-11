from random import randint


def bin_pow(base, step, mod):
    if step == 0:
        return 1
    if step % 2 != 0:
        return (bin_pow(base, step - 1, mod) * base) % mod
    else:
        temp = bin_pow(base, int(step/2), mod)
        return (temp * temp) % mod

    
def MR(n, c=1):
    k = n - 1
    s = 0
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    m = (n-1)
    s = 0

    while m % 2 == 1:
        m = m // 2
        s = s+1

    for j in range(c):
        a = randint(2, n - 2)
        b = bin_pow(a, m, n)
        if (b != 1) and (b != (n - 1)):
            i = 1
            while (i < s) and (b != (n - 1)):
                b = b*b % n
                if b == 1:
                    return False
                i += 1
            if b != (n - 1):
                return False
    return True


